#!/usr/bin/env python3
"""Procedural equirectangular sky panoramas -> assets/sky/<name>.png (1024x512). numpy + PIL only."""
from pathlib import Path

import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "assets" / "sky"
W, H = 1024, 512


def fbm(seed, n=(H, W), octaves=5):
    rng = np.random.default_rng(seed)
    out = np.zeros(n)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        res = (4 * 2 ** o, 8 * 2 ** o)
        g = rng.random(res)
        up = np.kron(g, np.ones((n[0] // res[0] + 1, n[1] // res[1] + 1)))[:n[0], :n[1]]
        # cheap smoothing for tileable-ish low freq noise
        from scipy.ndimage import gaussian_filter
        up = gaussian_filter(up, sigma=max(1, n[0] // res[0] // 2), mode="wrap")
        out += up * amp
        tot += amp
        amp *= 0.5
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-9)


def grad(top, hor, bot):
    y = np.linspace(0, 1, H)[:, None]            # 0 = zenith, 1 = nadir
    t = np.clip(y / 0.5, 0, 1)
    upper = np.array(top)[None, None, :] * (1 - t[..., None]) + np.array(hor)[None, None, :] * t[..., None]
    b = np.clip((y - 0.5) / 0.5, 0, 1)
    lower = np.array(hor)[None, None, :] * (1 - b[..., None]) + np.array(bot)[None, None, :] * b[..., None]
    return np.where((y < 0.5)[..., None], upper, lower) * np.ones((H, W, 1))


def hexc(s):
    s = s.lstrip("#")
    return [int(s[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def night():
    img = grad(hexc("#050814"), hexc("#16223c"), hexc("#0a0e18"))
    rng = np.random.default_rng(3)
    for _ in range(900):
        x, y = rng.integers(0, W), rng.integers(0, int(H * 0.5))
        b = rng.random() ** 3 * 0.9 + 0.1
        img[y, x] += b
        if b > 0.7 and x + 1 < W:
            img[y, x + 1] += b * 0.4
    # milky glow band
    yy, xx = np.mgrid[0:H, 0:W]
    band = np.exp(-((yy - (0.25 * H + 0.1 * H * np.sin(xx / W * 6.28))) / 40.0) ** 2) * fbm(5)
    img += band[..., None] * np.array([0.05, 0.07, 0.12])
    # moon + halo
    mx, my = int(W * 0.72), int(H * 0.22)
    d = np.hypot(xx - mx, yy - my)
    img += np.exp(-(d / 70.0) ** 2)[..., None] * np.array([0.10, 0.12, 0.18])
    img += (d < 16)[..., None] * np.array([0.9, 0.92, 0.85])
    # thin clouds
    c = np.clip(fbm(7) - 0.55, 0, 1) * 2.0
    img = img * (1 - c[..., None] * 0.5) + c[..., None] * np.array([0.05, 0.07, 0.1]) * 0.6
    return img


def dusk():
    img = grad(hexc("#1c1a3a"), hexc("#e08a5a"), hexc("#2a1a22"))
    c = np.clip(fbm(11) - 0.5, 0, 1) * 2.2
    img = img * (1 - c[..., None] * 0.6) + c[..., None] * np.array([0.9, 0.5, 0.4]) * 0.5
    return img


def day():
    img = grad(hexc("#5f86b8"), hexc("#cfdcec"), hexc("#8a97a8"))
    c = np.clip(fbm(13) - 0.48, 0, 1) * 2.4
    img = img * (1 - c[..., None] * 0.8) + c[..., None] * np.array([0.97, 0.97, 0.98]) * 0.8
    return img


def storm():
    img = grad(hexc("#14181d"), hexc("#3b434b"), hexc("#1a1e22"))
    c = fbm(17)
    img = img * (0.6 + 0.6 * c[..., None])
    return img


def snow():
    img = grad(hexc("#3a4258"), hexc("#b8a0a8"), hexc("#7a7a88"))
    c = np.clip(fbm(19) - 0.5, 0, 1) * 2.0
    img = img * (1 - c[..., None] * 0.5) + c[..., None] * np.array([0.8, 0.75, 0.8]) * 0.5
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("night", night), ("dusk", dusk), ("day", day), ("storm", storm), ("snow", snow)):
        img = np.clip(fn(), 0, 1)
        Image.fromarray((img * 255).astype(np.uint8)).save(OUT / f"{name}.png")
        print("sky", name)


if __name__ == "__main__":
    main()
