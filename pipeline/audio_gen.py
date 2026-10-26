#!/usr/bin/env python3
"""Procedural audio: ambience loops, music, sound effects. numpy/scipy synthesis -> wav -> ogg (ffmpeg).

    python3 pipeline/audio_gen.py [--force] [name ...]

Output: assets/audio/<name>.ogg  (+ data/audio.json index: kind/loop/volume). Deterministic (seeded).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "audio"
SR = 32000


# ------------------------------------------------------------------ helpers
def rng(seed):
    return np.random.default_rng(seed)


def white(n, seed):
    return rng(seed).normal(0, 1, n)


def lp(x, fc, order=4):
    return signal.sosfilt(signal.butter(order, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, order=4):
    return signal.sosfilt(signal.butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=3):
    return signal.sosfilt(signal.butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def t_(n):
    return np.arange(n) / SR


def norm(x, peak=0.8):
    m = np.max(np.abs(x)) or 1.0
    return x / m * peak


def fade(x, a=0.01, b=0.05):
    n = len(x)
    ia, ib = int(a * SR), int(b * SR)
    e = np.ones(n)
    if ia:
        e[:ia] = np.linspace(0, 1, ia)
    if ib:
        e[-ib:] = np.linspace(1, 0, ib)
    return x * e


def loopify(x, fade_s=1.5):
    """Make x loop seamlessly: overlap tail onto head with an equal-power crossfade."""
    f = int(fade_s * SR)
    head, tail = x[:f].copy(), x[-f:].copy()
    w = np.linspace(0, np.pi / 2, f)
    mixed = head * np.sin(w) + tail * np.cos(w)
    return np.concatenate([mixed, x[f:-f]])


def reverb(x, wet=0.3, size=1.0):
    out = np.zeros(len(x) + int(1.5 * SR))
    out[:len(x)] += x
    for d, g in ((0.029, 0.55), (0.037, 0.5), (0.043, 0.45), (0.051, 0.4), (0.067, 0.33), (0.089, 0.27)):
        k = int(d * SR * size)
        out[k:k + len(x)] += x * g * wet
    ap = out
    for d, g in ((0.005, 0.7), (0.0017, 0.7)):
        k = int(d * SR)
        y = np.zeros_like(ap)
        for i in range(len(ap)):
            pass
        break
    return out[:len(x) + int(0.6 * SR)]


def mixp(*arrs):
    n = max(len(a) for a in arrs)
    out = np.zeros(n)
    for a in arrs:
        out[:len(a)] += a
    return out


def place(buf, x, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(x))
    buf[i:j] += x[:j - i]


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def pluck(freq, dur, seed=0, decay=0.996):
    n = int(dur * SR)
    N = max(2, int(SR / freq))
    buf = rng(seed).uniform(-1, 1, N)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % N]
        buf[i % N] = decay * 0.5 * (buf[i % N] + buf[(i + 1) % N])
    return out


def pluck_fast(freq, dur, seed=0, decay=0.996):
    """Vectorised Karplus-Strong via a recursive filter (much faster than the loop)."""
    n = int(dur * SR)
    N = max(2, int(round(SR / freq)))
    exc = np.zeros(n)
    exc[:N] = rng(seed).uniform(-1, 1, N)
    b = [1.0]
    a = np.zeros(N + 2)
    a[0] = 1.0
    a[N] = -decay * 0.5
    a[N + 1] = -decay * 0.5
    return signal.lfilter(b, a, exc)


def pad(freqs, dur, bright=0.5, seed=0):
    n = int(dur * SR)
    t = t_(n)
    out = np.zeros(n)
    for k, f in enumerate(freqs):
        for det in (-0.004, 0.0, 0.004):
            ff = f * (1 + det)
            out += np.sin(2 * np.pi * ff * t + k) + 0.35 * np.sin(4 * np.pi * ff * t) * bright + 0.15 * np.sin(6 * np.pi * ff * t) * bright
    out = lp(out, 900 + 2500 * bright)
    e = np.minimum(1, np.minimum(t / (dur * 0.35), (dur - t) / (dur * 0.4)))
    return out * e / max(1, len(freqs))


def bell(freq, dur=3.0, seed=0):
    n = int(dur * SR)
    t = t_(n)
    out = np.zeros(n)
    for ratio, amp, dec in ((1, 1.0, 1.2), (2.0, 0.6, 1.6), (2.76, 0.5, 2.2), (5.4, 0.3, 3.3), (8.93, 0.15, 4.2)):
        out += amp * np.sin(2 * np.pi * freq * ratio * t) * np.exp(-t * dec)
    return out


def thump(freq=60, dur=0.5, drop=40):
    n = int(dur * SR)
    t = t_(n)
    f = freq + drop * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)


def noise_burst(dur, fc=2000, hi=False, decay=10, seed=0):
    n = int(dur * SR)
    x = white(n, seed)
    x = hp(x, fc) if hi else lp(x, fc)
    return x * np.exp(-t_(n) * decay)


# ------------------------------------------------------------------ ambience (loops)
def amb_wind(dur=24, cold=False, seed=1):
    n = int(dur * SR)
    w = white(n, seed)
    low = lp(w, 400 if not cold else 900)
    mod = 0.55 + 0.45 * np.sin(2 * np.pi * t_(n) / 9.0 + 1) * np.sin(2 * np.pi * t_(n) / 5.3)
    x = low * mod
    gust = bp(white(n, seed + 1), 300, 1100) * (0.3 + 0.7 * np.clip(np.sin(2 * np.pi * t_(n) / 11 + 2), 0, 1) ** 2)
    out = x + 0.6 * gust
    if cold:
        out = hp(out, 150)
    return loopify(norm(out, 0.55))


def amb_day(dur=24, seed=2):
    n = int(dur * SR)
    out = lp(white(n, seed), 500) * 0.25 * (0.6 + 0.4 * np.sin(2 * np.pi * t_(n) / 7))
    r = rng(seed + 5)
    for _ in range(9):
        f0 = r.uniform(2500, 4200)
        at = r.uniform(0, dur - 1)
        chirp = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.3 * np.sin(2 * np.pi * 14 * t_(int(0.12 * SR))))) / SR) * np.exp(-t_(int(0.12 * SR)) * 25)
        for k in range(r.integers(2, 4)):
            place(out, chirp * 0.08, at + k * 0.16)
    return loopify(norm(out, 0.45))


def amb_sea(dur=28, seed=3):
    n = int(dur * SR)
    w = white(n, seed)
    t = t_(n)
    env = 0.25 + 0.75 * np.clip(np.sin(2 * np.pi * t / 8.5 - 1.2), 0, 1) ** 1.5
    out = lp(w, 900) * env + 0.4 * hp(lp(w, 4000), 1500) * env ** 2
    return loopify(norm(out, 0.6), 2.0)


def amb_fire(dur=24, seed=4):
    n = int(dur * SR)
    out = lp(white(n, seed), 220) * 0.35
    out += 0.06 * np.sin(2 * np.pi * 55 * t_(n))
    r = rng(seed + 9)
    for _ in range(int(dur * 14)):
        a = r.uniform(0.0, dur - 0.1)
        c = noise_burst(r.uniform(0.01, 0.05), fc=r.uniform(1500, 5000), hi=True, decay=r.uniform(60, 160), seed=int(r.integers(1e9)))
        place(out, c * r.uniform(0.1, 0.5), a)
    return loopify(norm(out, 0.5))


def amb_crypt(dur=28, seed=5):
    n = int(dur * SR)
    t = t_(n)
    out = 0.5 * np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 13)) + 0.35 * np.sin(2 * np.pi * 82.4 * t + 1) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 9))
    out += 0.12 * np.sin(2 * np.pi * 58.3 * t) + lp(white(n, seed), 160) * 0.3
    r = rng(seed)
    for _ in range(7):
        a = r.uniform(0.5, dur - 1.5)
        d = np.sin(2 * np.pi * r.uniform(900, 1500) * t_(int(0.25 * SR))) * np.exp(-t_(int(0.25 * SR)) * 20)
        place(out, d * 0.10, a)
        place(out, d * 0.04, a + 0.22)
    return loopify(norm(out, 0.5), 2.0)


def amb_storm(dur=28, seed=6):
    n = int(dur * SR)
    w = white(n, seed)
    out = hp(lp(w, 7000), 400) * 0.5 + lp(w, 300) * 0.8
    out *= 0.7 + 0.3 * np.sin(2 * np.pi * t_(n) / 6.3)
    r = rng(seed)
    for at in (6.0, 17.0):
        rum = lp(white(int(3.5 * SR), seed + int(at)), 90) * np.exp(-t_(int(3.5 * SR)) * 1.1) * 2.5
        place(out, rum, at)
    return loopify(norm(out, 0.7), 2.0)


def amb_asylum(dur=24, seed=7):
    n = int(dur * SR)
    t = t_(n)
    out = 0.35 * np.sin(2 * np.pi * 50 * t) + 0.25 * np.sin(2 * np.pi * 100.5 * t) + lp(white(n, seed), 250) * 0.25
    tick = noise_burst(0.02, fc=2500, hi=True, decay=140, seed=3) * 0.5
    for k in range(int(dur)):
        place(out, tick if k % 2 == 0 else tick * 0.7, k * 1.0)
    return loopify(norm(out, 0.45))


def amb_city(dur=24, seed=8):
    n = int(dur * SR)
    w = white(n, seed)
    out = bp(w, 150, 900) * 0.4 * (0.6 + 0.4 * np.sin(2 * np.pi * t_(n) / 6.7))
    r = rng(seed)
    for _ in range(5):
        a = r.uniform(0, dur - 1)
        hoof = thump(r.uniform(90, 130), 0.12, 20) * 0.25
        for k in range(8):
            place(out, hoof, a + k * 0.32)
    return loopify(norm(out, 0.45))


def amb_interior(dur=24, seed=9):
    n = int(dur * SR)
    out = lp(white(n, seed), 180) * 0.4 + 0.15 * np.sin(2 * np.pi * 60 * t_(n))
    return loopify(norm(out, 0.35))


# ------------------------------------------------------------------ music
A_MINOR = [57, 59, 60, 62, 64, 65, 68, 69]   # A harmonic minor


def mus_title(dur=64, seed=11):
    out = np.zeros(int(dur * SR) + 4 * SR)
    chords = [[45, 57, 64, 69], [41, 53, 60, 65], [38, 50, 57, 62], [40, 52, 59, 68]]
    bar = dur / 8
    for i in range(8):
        ch = chords[i % 4]
        place(out, pad([midi(n) for n in ch], bar * 1.4, 0.4, seed + i) * 0.35, i * bar)
    r = rng(seed)
    for i in range(10):
        n = r.choice([69, 72, 76, 71, 64, 68])
        place(out, bell(midi(int(n)), 4.0, seed) * 0.12, 3 + i * 6.0)
    place(out, thump(48, 1.2, 10) * 0.25, 0)
    return loopify(norm(out[:int(dur * SR)], 0.6), 3.0)


def mus_explore(dur=64, seed=12):
    out = np.zeros(int(dur * SR) + 4 * SR)
    chords = [[57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 56, 59]]
    bar = dur / 16
    for i in range(16):
        ch = chords[(i // 4) % 4]
        for k, n in enumerate(ch + [ch[1] + 12]):
            place(out, pluck_fast(midi(n), 2.4, seed + i * 7 + k, 0.9965) * 0.30, i * bar + k * bar / 4)
    for i in range(4):
        place(out, pad([midi(n - 12) for n in chords[i]], dur / 3.2, 0.2, seed) * 0.35, i * dur / 4)
    return loopify(norm(out[:int(dur * SR)], 0.55), 3.0)


def mus_dread(dur=48, seed=13):
    n = int(dur * SR)
    t = t_(n)
    out = 0.4 * np.sin(2 * np.pi * 43.65 * t) + 0.3 * np.sin(2 * np.pi * 61.7 * t + 0.5) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 7))
    out += 0.12 * np.sin(2 * np.pi * 311 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 11)) * np.clip(np.sin(2 * np.pi * t / 17), 0, 1)
    beat = thump(52, 0.6, 14) * 0.5
    for k in range(int(dur / 1.6)):
        place(out, beat, k * 1.6)
        place(out, beat * 0.5, k * 1.6 + 0.28)
    out = np.concatenate([out, np.zeros(2 * SR)])
    for i in range(6):
        place(out, bell(midi(81 + (i % 3)), 5.0) * 0.05, 4 + i * 7.3)
    return loopify(norm(out[:n], 0.55), 3.0)


def mus_combat(dur=32, seed=14):
    out = np.zeros(int(dur * SR) + 2 * SR)
    beat = 60 / 112
    kick = thump(62, 0.35, 50) * 0.9
    snare = noise_burst(0.18, fc=2200, hi=True, decay=22, seed=1) * 0.5
    roots = [45, 45, 41, 43]
    for bar in range(int(dur / (beat * 4))):
        base = bar * beat * 4
        for b in range(4):
            if b in (0, 2):
                place(out, kick, base + b * beat)
            if b in (1, 3):
                place(out, snare, base + b * beat)
        for e in range(8):
            place(out, noise_burst(0.05, 6000, True, 70, seed=e) * 0.12, base + e * beat / 2)
        r = roots[bar % 4]
        for q in range(8):
            f = midi(r - 12 + (7 if q % 4 == 3 else 0))
            seg = lp(signal.sawtooth(2 * np.pi * f * t_(int(beat * 0.5 * SR))), 700) * np.exp(-t_(int(beat * 0.5 * SR)) * 6)
            place(out, seg * 0.35, base + q * beat / 2)
        if bar % 2 == 0:
            place(out, pad([midi(r), midi(r + 7), midi(r + 12)], beat * 8, 0.8, seed) * 0.3, base)
    return loopify(norm(out[:int(dur * SR)], 0.7), 1.0)


def mus_sad(dur=48, seed=15):
    out = np.zeros(int(dur * SR) + 4 * SR)
    melody = [74, 72, 69, 65, 67, 69, 72, 69, 62, 65, 69, 74, 72, 69, 67, 64]
    step = dur / 16
    for i, n in enumerate(melody):
        place(out, pluck_fast(midi(n), 3.5, seed + i, 0.9985) * 0.35, i * step)
    bass = [38, 34, 31, 33]
    for i, n in enumerate(bass):
        place(out, pad([midi(n), midi(n + 7), midi(n + 12)], dur / 3.5, 0.15, seed) * 0.35, i * dur / 4)
    return loopify(norm(out[:int(dur * SR)], 0.5), 3.0)


# ------------------------------------------------------------------ sfx
def sfx_click():
    return fade(np.sin(2 * np.pi * 880 * t_(int(0.05 * SR))) * np.exp(-t_(int(0.05 * SR)) * 60), 0.001, 0.01) * 0.5


def sfx_pickup():
    a = bell(988, 0.5) * 0.4
    b = bell(1318, 0.5) * 0.4
    out = np.zeros(int(0.7 * SR))
    place(out, a, 0)
    place(out, b, 0.09)
    return out


def sfx_door():
    n = int(0.9 * SR)
    t = t_(n)
    creak = np.sin(2 * np.pi * np.cumsum(180 + 120 * np.sin(2 * np.pi * 3 * t) + 60 * t) / SR) * 0.3 * np.minimum(1, t * 8) * np.exp(-t * 2.2)
    return mixp(creak, noise_burst(0.15, 800, False, 20, 2) * 0.4)


def sfx_door_locked():
    out = np.zeros(int(0.5 * SR))
    place(out, thump(110, 0.12, 20) * 0.7, 0)
    place(out, thump(95, 0.12, 20) * 0.6, 0.14)
    place(out, noise_burst(0.05, 3000, True, 80, 4) * 0.3, 0.02)
    return out


def sfx_step():
    return fade(noise_burst(0.09, 600, False, 28, int(rng(0).integers(1e6))) * 0.5, 0.002, 0.03)


def sfx_hit():
    out = thump(90, 0.4, 70) * 0.9
    n = noise_burst(0.12, 1800, False, 30, 6) * 0.7
    return fade(out + np.pad(n, (0, len(out) - len(n))), 0.001, 0.05)


def sfx_miss():
    n = int(0.3 * SR)
    t = t_(n)
    x = bp(white(n, 7), 600, 3500) * np.sin(np.pi * t / 0.3) ** 2
    return x * 0.5


def sfx_hurt():
    n = int(0.45 * SR)
    t = t_(n)
    f = 260 - 100 * t
    return mixp(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * 0.5, noise_burst(0.2, 900, False, 12, 8) * 0.4)


def sfx_bite():
    return mixp(sfx_hurt() * 0.6, noise_burst(0.5, 1200, True, 10, 9) * 0.25)


def sfx_howl():
    n = int(2.4 * SR)
    t = t_(n)
    f = 330 + 220 * np.sin(np.pi * t / 2.4) ** 1.4
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    x *= np.sin(np.pi * t / 2.4) ** 0.7
    return lp(x, 2500) * 0.3


def sfx_bat():
    n = int(0.8 * SR)
    t = t_(n)
    x = bp(white(n, 12), 1500, 6000) * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * t)) * np.sin(np.pi * t / 0.8)
    return x * 0.4


def sfx_bell():
    return bell(196, 5.0) * 0.6


def sfx_heartbeat():
    out = np.zeros(int(1.2 * SR))
    place(out, thump(55, 0.25, 15) * 0.9, 0)
    place(out, thump(50, 0.25, 15) * 0.6, 0.28)
    return out


def sfx_page():
    n = int(0.35 * SR)
    return bp(white(n, 13), 2000, 7000) * np.sin(np.pi * t_(n) / 0.35) * 0.4


def sfx_flame():
    n = int(0.7 * SR)
    t = t_(n)
    return lp(white(n, 14), 1800) * np.sin(np.pi * t / 0.7) ** 0.6 * 0.5


def sfx_holy():
    out = np.zeros(int(2.0 * SR))
    for i, f in enumerate((660, 880, 1320, 1760)):
        place(out, bell(f, 1.8) * 0.25, i * 0.07)
    return out


def sfx_repel():
    n = int(1.0 * SR)
    t = t_(n)
    f = 400 + 800 * t
    return mixp(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3) * 0.35, bell(1500, 1.0)[:n] * 0.2)


def sfx_victory():
    out = np.zeros(int(2.5 * SR))
    for i, n in enumerate((57, 64, 69, 72)):
        place(out, bell(midi(n + 12), 2.2) * 0.35, i * 0.12)
    return out


def sfx_defeat():
    n = int(2.0 * SR)
    t = t_(n)
    return np.sin(2 * np.pi * np.cumsum(120 - 50 * t) / SR) * np.exp(-t * 2.2) * 0.6


def sfx_craft():
    out = np.zeros(int(0.8 * SR))
    for k in range(3):
        place(out, mixp(thump(300, 0.12, 120) * 0.6, noise_burst(0.03, 3500, True, 90, k) * 0.3), k * 0.22)
    return out


def sfx_card():
    out = np.zeros(int(3.5 * SR))
    place(out, bell(147, 3.5) * 0.5, 0)
    place(out, pad([midi(38), midi(45), midi(50)], 3.4, 0.2) * 0.4, 0)
    return out


def sfx_levelup():
    out = np.zeros(int(2.0 * SR))
    for i, n in enumerate((60, 64, 67, 72, 76)):
        place(out, bell(midi(n + 12), 1.6) * 0.3, i * 0.1)
    return out


SOUNDS = {
    # name: (generator, kind, loop, volume_db)
    "amb_wind": (lambda: amb_wind(), "ambience", True, -6),
    "amb_snow": (lambda: amb_wind(cold=True, seed=21), "ambience", True, -6),
    "amb_day": (lambda: amb_day(), "ambience", True, -8),
    "amb_sea": (lambda: amb_sea(), "ambience", True, -6),
    "amb_fire": (lambda: amb_fire(), "ambience", True, -6),
    "amb_crypt": (lambda: amb_crypt(), "ambience", True, -6),
    "amb_storm": (lambda: amb_storm(), "ambience", True, -5),
    "amb_asylum": (lambda: amb_asylum(), "ambience", True, -8),
    "amb_city": (lambda: amb_city(), "ambience", True, -8),
    "amb_interior": (lambda: amb_interior(), "ambience", True, -9),
    "mus_title": (lambda: mus_title(), "music", True, -8),
    "mus_explore": (lambda: mus_explore(), "music", True, -10),
    "mus_dread": (lambda: mus_dread(), "music", True, -10),
    "mus_combat": (lambda: mus_combat(), "music", True, -9),
    "mus_sad": (lambda: mus_sad(), "music", True, -9),
    "sfx_click": (sfx_click, "sfx", False, -10), "sfx_pickup": (sfx_pickup, "sfx", False, -6),
    "sfx_door": (sfx_door, "sfx", False, -6), "sfx_door_locked": (sfx_door_locked, "sfx", False, -6),
    "sfx_step": (sfx_step, "sfx", False, -16), "sfx_hit": (sfx_hit, "sfx", False, -4), "sfx_miss": (sfx_miss, "sfx", False, -8),
    "sfx_hurt": (sfx_hurt, "sfx", False, -5), "sfx_bite": (sfx_bite, "sfx", False, -5), "sfx_howl": (sfx_howl, "sfx", False, -6),
    "sfx_bat": (sfx_bat, "sfx", False, -8), "sfx_bell": (sfx_bell, "sfx", False, -6), "sfx_heartbeat": (sfx_heartbeat, "sfx", False, -8),
    "sfx_page": (sfx_page, "sfx", False, -8), "sfx_flame": (sfx_flame, "sfx", False, -8), "sfx_holy": (sfx_holy, "sfx", False, -6),
    "sfx_repel": (sfx_repel, "sfx", False, -6), "sfx_victory": (sfx_victory, "sfx", False, -5), "sfx_defeat": (sfx_defeat, "sfx", False, -5),
    "sfx_craft": (sfx_craft, "sfx", False, -6), "sfx_card": (sfx_card, "sfx", False, -6), "sfx_levelup": (sfx_levelup, "sfx", False, -5),
}


def main():
    args = sys.argv[1:]
    force = "--force" in args
    names = [a for a in args if not a.startswith("--")] or list(SOUNDS)
    OUT.mkdir(parents=True, exist_ok=True)
    index = {}
    for name, (gen, kind, loop, db) in SOUNDS.items():
        index[name] = {"file": f"assets/audio/{name}.ogg", "kind": kind, "loop": loop, "db": db}
        if name not in names:
            continue
        dest = OUT / f"{name}.ogg"
        if dest.exists() and not force:
            continue
        x = np.asarray(gen(), float)
        x = np.clip(x, -1, 1)
        wav = OUT / f"{name}.wav"
        wavfile.write(wav, SR, (x * 32000).astype(np.int16))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-c:a", "libvorbis", "-q:a", "3", str(dest)], check=True)
        wav.unlink()
        print(f"{name:<16} {len(x) / SR:5.1f}s  {dest.stat().st_size // 1024} KB")
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "audio.json").write_text(json.dumps(index, indent=1))


if __name__ == "__main__":
    main()
