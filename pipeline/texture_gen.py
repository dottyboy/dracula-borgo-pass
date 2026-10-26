#!/usr/bin/env python3
"""Step 2: procedural, seamlessly tiling textures (albedo + normal).

Textures are *base patterns*. Neutral patterns (skin, cloth, wool, hair ...) are
meant to be multiplied by a tint in the variant, so one file serves many looks.
Output: assets/textures/<id>_albedo.png, <id>_normal.png (512 px, tile 1 m).
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "textures"
N = 512


# ---------------------------------------------------------------- noise -----
def fbm(seed, beta=2.0, n=None):
    """Tileable 1/f^beta noise in 0..1 (FFT filtered white noise)."""
    n = n or N
    rng = np.random.default_rng(seed)
    f = np.fft.fftfreq(n)
    fy, fx = np.meshgrid(f, f, indexing="ij")
    r = np.sqrt(fx ** 2 + fy ** 2)
    r[0, 0] = 1.0
    spec = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / r ** (beta / 2 * 2)
    spec[0, 0] = 0
    out = np.fft.ifft2(spec).real
    out -= out.min()
    return out / max(out.max(), 1e-9)


def stretch(seed, sx, sy, n=None):
    """Anisotropic noise. Larger s = smoother along that axis (features elongate along it)."""
    n = n or N
    rng = np.random.default_rng(seed)
    w = rng.normal(size=(n, n))
    kx = np.exp(-0.5 * (np.fft.fftfreq(n) * sx * n) ** 2)
    ky = np.exp(-0.5 * (np.fft.fftfreq(n) * sy * n) ** 2)
    out = np.fft.ifft2(np.fft.fft2(w) * ky[:, None] * kx[None, :]).real
    out -= out.min()
    return out / max(out.max(), 1e-9)


def grid_xy(n=None):
    n = n or N
    y, x = np.mgrid[0:n, 0:n] / n
    return x, y


def rgb(h, lo, hi):
    lo, hi = np.array(lo, float), np.array(hi, float)
    return lo + (hi - lo) * h[..., None]


def hexc(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) / 255 for i in (0, 2, 4))


def normal_from_height(h, strength=2.0):
    dx = np.roll(h, -1, 1) - np.roll(h, 1, 1)
    dy = np.roll(h, -1, 0) - np.roll(h, 1, 0)
    nz = np.ones_like(h) / strength
    v = np.stack([-dx, dy, nz], -1)
    v /= np.linalg.norm(v, axis=-1, keepdims=True)
    return v * 0.5 + 0.5


# -------------------------------------------------------------- patterns ----
def blocks(rows, seed, mortar=0.035, offset=True):
    x, y = grid_xy()
    row = np.floor(y * rows).astype(int)
    cols = np.where(row % 2 == 0, 3, 3)
    xs = (x * 3 + (row % 2) * 0.5 * offset) % 1.0
    cell_x = np.floor(x * 3 + (row % 2) * 0.5 * offset).astype(int) % 3
    rng = np.random.default_rng(seed)
    tone = rng.uniform(0.75, 1.1, size=(rows, 3))[row % rows, cell_x]
    fy = (y * rows) % 1.0
    edge = np.minimum.reduce([xs, 1 - xs, fy * 0.5, (1 - fy) * 0.5]) * 1.0
    m = np.clip((edge - mortar) / 0.02, 0, 1)  # 0 in mortar
    return m, tone


def tex_stone_blocks(seed=1):
    """Ashlar masonry: rows with random block widths, per-block tone, chips, thin recessed mortar. One tile = 2 m."""
    n = N
    x, y = grid_xy()
    rng = np.random.default_rng(seed)
    rows = 5
    row = np.floor(y * rows).astype(int)
    fy = (y * rows) % 1.0
    tone = np.zeros((n, n))
    mortar_x = np.ones((n, n))
    for r in range(rows):
        off = rng.uniform(0, 1)
        xr = (x - off) % 1.0
        k = int(rng.integers(3, 5))
        cuts = (np.arange(1, k) + rng.uniform(-0.28, 0.28, k - 1)) / k
        edges = np.concatenate([[0.0], cuts, [1.0]])
        for i in range(len(edges) - 1):
            a0, a1 = edges[i], edges[i + 1]
            inside = (row == r) & (xr >= a0) & (xr < a1)
            tone[inside] = rng.uniform(0.78, 1.1)
            e = np.minimum(xr - a0, a1 - xr)
            mortar_x[inside] = np.clip((e - 0.003) / 0.006, 0, 1)[inside]
    my = np.clip((np.minimum(fy, 1 - fy) / rows - 0.0022) / 0.0045, 0, 1)
    m = np.minimum(mortar_x, my)
    nz = fbm(seed, 2.6)
    nz2 = fbm(seed + 9, 1.4)
    fine = fbm(seed + 3, 0.6)
    base = rgb(nz * 0.5 + nz2 * 0.3 + fine * 0.2, hexc("#716e68"), hexc("#aaa49a"))
    col = base * tone[..., None] * (0.5 + 0.5 * m[..., None])
    chips = (fbm(seed + 21, 0.3) > 0.86) * 1.0
    col *= (1 - 0.2 * chips)[..., None]
    crack = 1 - np.abs(fbm(seed + 5, 2.2) * 2 - 1)
    col *= (1 - 0.18 * (crack > 0.992))[..., None]
    h = m * (0.55 + 0.3 * nz2 + 0.15 * fine)
    return np.clip(col, 0, 1), h, dict(roughness=0.92, world=2.0)


def tex_stone_moss(seed=2):
    col, h, meta = tex_stone_blocks(seed)
    moss = fbm(seed + 20, 3.0)
    mask = np.clip((moss - 0.6) * 3.2, 0, 0.85)[..., None]
    green = rgb(fbm(seed + 21, 1.8) * 0.6 + fbm(seed + 22, 0.7) * 0.4, hexc("#2b4520"), hexc("#648a38"))
    lower = np.clip((np.arange(N)[:, None] / N - 0.55) * 1.4, 0, 1)[..., None]   # more moss low on the blocks
    mask = np.clip(mask + 0.15 * lower * (moss[..., None] > 0.45), 0, 0.9)
    return col * (1 - mask) + green * mask, h, meta


def tex_stone_rough(seed=3):
    n = fbm(seed, 2.2)
    n2 = fbm(seed + 1, 1.2)
    ridge = 1 - np.abs(fbm(seed + 2, 2.4) * 2 - 1)
    h = n * 0.7 + (ridge > 0.96) * -0.3 + n2 * 0.3
    col = rgb(np.clip(h, 0, 1), hexc("#5b5852"), hexc("#a8a398"))
    return col, np.clip(h, 0, 1), dict(roughness=0.95)


def tex_cobble(seed=4):
    """Rounded stones with varied tone, mud between, 2 m tile."""
    n = N
    k = 11
    rng = np.random.default_rng(seed)
    cell = (np.stack(np.meshgrid(np.arange(k), np.arange(k), indexing="ij"), -1) + rng.uniform(0.15, 0.85, (k, k, 2))) / k
    pts = cell.reshape(-1, 2)
    x, y = grid_xy()
    d1 = np.full((n, n), 9.0)
    d2 = np.full((n, n), 9.0)
    ids = np.zeros((n, n), int)
    for i, (py, px) in enumerate(pts):
        dxs = np.minimum.reduce([np.abs(x - px + o) for o in (-1, 0, 1)])
        dys = np.minimum.reduce([np.abs(y - py + o) for o in (-1, 0, 1)])
        d = np.hypot(dxs, dys * 1.0)
        upd1 = d < d1
        d2 = np.where(upd1, d1, np.minimum(d2, d))
        ids = np.where(upd1, i, ids)
        d1 = np.where(upd1, d, d1)
    edge = d2 - d1
    m = np.clip((edge - 0.004) * 55, 0, 1)
    dome = np.clip(edge * 22, 0, 1)
    tone = rng.uniform(0.62, 1.12, len(pts))[ids]
    hue = rng.uniform(0, 1, len(pts))[ids][..., None]
    nz = fbm(seed, 2.4)
    nz2 = fbm(seed + 4, 0.9)
    base = rgb(nz * 0.6 + nz2 * 0.4, hexc("#55524c"), hexc("#948f84"))
    warm = np.array([1.05, 0.98, 0.88])
    cool = np.array([0.92, 0.96, 1.04])
    col = base * tone[..., None] * (warm * hue + cool * (1 - hue)) * (0.22 + 0.78 * m[..., None]) * (0.85 + 0.15 * dome[..., None])
    mud = rgb(fbm(seed + 8, 1.2), hexc("#2a241c"), hexc("#4a4033"))
    col = col * m[..., None] + mud * (1 - m[..., None]) * 0.9 * (1 - m[..., None]) + col * 0
    col = np.where((m < 0.3)[..., None], mud * 0.8, col)
    return np.clip(col, 0, 1), dome * (0.6 + 0.4 * nz2), dict(roughness=0.9, world=2.0)


def tex_wood_planks(seed=5):
    """Vertical planks (8 per tile): per-plank tone, grain running along the plank, knots, butt joints, bevelled gaps."""
    n = N
    x, y = grid_xy()
    planks = 8
    pid = np.floor(x * planks).astype(int)
    px = (x * planks) % 1.0
    rng = np.random.default_rng(seed)
    tone = rng.uniform(0.72, 1.06, planks)[pid]
    shift = (rng.uniform(0, 1, planks) * n).astype(int)
    grain_a = stretch(seed, 2.5, 90)
    grain_b = stretch(seed + 1, 6, 28)
    grain_c = stretch(seed + 2, 1.5, 150)
    idx_y = (np.arange(n)[:, None] + shift[pid]) % n
    ga = grain_a[idx_y, np.arange(n)[None, :]]
    gb = grain_b[idx_y, np.arange(n)[None, :]]
    gc = grain_c[idx_y, np.arange(n)[None, :]]
    g = ga * 0.45 + gb * 0.35 + gc * 0.2
    # knots
    for _ in range(5):
        kx, ky = rng.uniform(0, 1), rng.uniform(0, 1)
        d = np.hypot(((x - kx + 0.5) % 1.0 - 0.5) * 1.0, ((y - ky + 0.5) % 1.0 - 0.5) * 0.45)
        g = g - np.exp(-(d / 0.018) ** 2) * 0.5 + np.exp(-((d - 0.03) / 0.012) ** 2) * 0.12
    base = rgb(np.clip(g, 0, 1), hexc("#5e4128"), hexc("#a98050"))
    # butt joints
    joint = np.zeros((n, n))
    for i in range(planks):
        yy = rng.uniform(0.1, 0.9)
        joint[:, :] += ((pid == i) & (np.abs(y - yy) < 0.004)) * 1.0
    gap = np.clip(np.minimum(px, 1 - px) / 0.022, 0, 1)
    bevel = np.clip((np.minimum(px, 1 - px) - 0.022) / 0.03, 0, 1)
    col = base * tone[..., None] * (0.18 + 0.82 * gap[..., None]) * (0.92 + 0.08 * bevel[..., None]) * (1 - 0.6 * joint[..., None])
    h = g * 0.25 * gap + bevel * 0.4 - joint * 0.6
    return np.clip(col, 0, 1), h, dict(roughness=0.8, world=2.0)


def tex_plaster(seed=6):
    n = fbm(seed, 2.4)
    s = fbm(seed + 1, 0.8)
    col = rgb(n * 0.7 + s * 0.3, hexc("#c9c0ac"), hexc("#ece5d4"))
    return col, n * 0.5 + s * 0.2, dict(roughness=0.95)


def weave(freq, seed, soft=0.2):
    x, y = grid_xy()
    w = 0.5 + 0.25 * np.sin(x * freq * np.pi * 2) + 0.25 * np.sin(y * freq * np.pi * 2)
    w = w * (1 - soft) + fbm(seed, 1.0) * soft
    return w


def tex_cloth(seed=7):
    w = weave(24, seed)
    n = fbm(seed, 2.0)
    col = rgb(w * 0.2 + n * 0.8, (0.78,) * 3, (1.0,) * 3)
    return col, w * 0.4, dict(roughness=0.95)


def tex_wool(seed=8):
    w = weave(12, seed, 0.35)
    n = fbm(seed + 1, 1.2)
    col = rgb(w * 0.2 + n * 0.8, (0.7,) * 3, (1.0,) * 3)
    return col, w * 0.5 + n * 0.3, dict(roughness=1.0)


def tex_velvet(seed=9):
    n = fbm(seed, 0.9)
    d = fbm(seed + 1, 3.0)
    col = rgb(n * 0.5 + d * 0.5, (0.7,) * 3, (1.0,) * 3)
    return col, n * 0.1, dict(roughness=0.7)


def tex_leather(seed=10):
    n = fbm(seed, 1.1)
    c = fbm(seed + 1, 2.4)
    col = rgb(n * 0.6 + c * 0.4, (0.6,) * 3, (1.0,) * 3)
    return col, n * 0.6, dict(roughness=0.6)


def tex_iron(seed=11):
    n = fbm(seed, 1.6)
    sc = stretch(seed + 1, 80, 2) * 0.4
    col = rgb(n * 0.6 + sc, hexc("#2e2f34"), hexc("#6b6e77"))
    return col, n * 0.3 + sc * 0.5, dict(roughness=0.5, metallic=0.9)


def tex_gold(seed=12):
    n = fbm(seed, 1.8)
    col = rgb(n, hexc("#a47a1c"), hexc("#f0c850"))
    return col, n * 0.2, dict(roughness=0.35, metallic=1.0)


def tex_glass(seed=13):
    n = fbm(seed, 2.6)
    col = rgb(n, (0.82,) * 3, (1.0,) * 3)
    return col, n * 0.05, dict(roughness=0.1, alpha=0.55)


def tex_wax(seed=14):
    n = fbm(seed, 2.4)
    col = rgb(n, (0.85,) * 3, (1.0,) * 3)
    return col, n * 0.1, dict(roughness=0.4)


def tex_flame(seed=15):
    n = fbm(seed, 2.2)
    col = rgb(n, hexc("#ffb040"), hexc("#fff0b0"))
    return col, n * 0.0, dict(roughness=1.0, emission=1.6)


def tex_parchment(seed=16):
    n = fbm(seed, 2.0)
    col = rgb(n, hexc("#cdb88a"), hexc("#efe2bd"))
    return col, n * 0.1, dict(roughness=0.9)


def tex_dirt(seed=17):
    n = fbm(seed, 1.8)
    g = fbm(seed + 1, 0.8)
    col = rgb(n * 0.6 + g * 0.4, hexc("#3a2b1e"), hexc("#7d6549"))
    rng = np.random.default_rng(seed)
    x, y = grid_xy()
    peb = np.zeros((N, N))
    for _ in range(90):
        cx, cy, r = rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0.004, 0.012)
        d = np.hypot((x - cx + 0.5) % 1.0 - 0.5, (y - cy + 0.5) % 1.0 - 0.5)
        peb += np.clip(1 - d / r, 0, 1) * rng.uniform(0.3, 0.8)
    col = col * (1 - np.clip(peb, 0, 1)[..., None] * 0.0) + np.clip(peb, 0, 1)[..., None] * np.array([0.35, 0.33, 0.3])
    return np.clip(col, 0, 1), n * 0.5 + g * 0.2 + np.clip(peb, 0, 1) * 0.5, dict(roughness=1.0, world=3.0)


def tex_bark(seed=18):
    n = stretch(seed, 80, 4) * 0.7 + fbm(seed + 1, 1.6) * 0.3
    col = rgb(n, hexc("#2c2118"), hexc("#5a4630"))
    return col, n, dict(roughness=1.0)


def tex_foliage(seed=19):
    n = fbm(seed, 1.4)
    g = fbm(seed + 1, 0.7)
    col = rgb(n * 0.6 + g * 0.4, (0.55,) * 3, (1.0,) * 3) * np.array([0.6, 0.85, 0.5])
    return np.clip(col * 1.1, 0, 1), n * 0.5 + g * 0.3, dict(roughness=1.0)


def tex_grass(seed=20):
    n = fbm(seed, 1.3)
    b = stretch(seed + 1, 7, 100)
    b2 = stretch(seed + 2, 3, 40)
    patch = fbm(seed + 3, 3.2)
    col = rgb(n * 0.3 + b * 0.35 + b2 * 0.35, hexc("#24401a"), hexc("#64883a"))
    col = col * (0.88 + 0.24 * patch[..., None])
    dry = np.clip((patch - 0.7) * 3, 0, 0.35)[..., None]
    col = col * (1 - dry) + rgb(n, hexc("#6a6a30"), hexc("#9a8a48")) * dry
    rng = np.random.default_rng(seed)
    x, y = grid_xy()
    for _ in range(14):
        cx, cy = rng.uniform(0, 1), rng.uniform(0, 1)
        d = np.hypot((x - cx + 0.5) % 1.0 - 0.5, (y - cy + 0.5) % 1.0 - 0.5)
        col = np.where((d < 0.0025)[..., None], np.array([0.9, 0.88, 0.7]) if rng.random() < 0.5 else np.array([0.9, 0.75, 0.2]), col)
    return np.clip(col, 0, 1), b * 0.4 + n * 0.2, dict(roughness=1.0, world=4.0)


def tex_snow(seed=21):
    n = fbm(seed, 2.4)
    col = rgb(n, hexc("#d8e0ea"), hexc("#ffffff"))
    return col, n * 0.2, dict(roughness=0.85)


def tex_fur(seed=22):
    a = stretch(seed, 90, 4)
    b = fbm(seed + 1, 1.0)
    col = rgb(a * 0.6 + b * 0.4, (0.55,) * 3, (1.0,) * 3)
    return col, a * 0.4, dict(roughness=1.0)


def tex_hair(seed=23):
    a = stretch(seed, 4, 70)
    col = rgb(a, (0.5,) * 3, (1.0,) * 3)
    return col, a * 0.3, dict(roughness=0.6)


def tex_skin(seed=24):
    n = fbm(seed, 2.4)
    col = rgb(n, (0.9,) * 3, (1.0,) * 3)
    return col, n * 0.05, dict(roughness=0.7)


def tex_flat(seed=25):
    n = fbm(seed, 2.4)
    return rgb(n, (0.94,) * 3, (1.0,) * 3), n * 0.0, dict(roughness=0.8)


TEXTURES = {k[4:]: v for k, v in globals().items() if k.startswith("tex_")}


def build(force=False):
    OUT.mkdir(parents=True, exist_ok=True)
    meta_all = {}
    big = {"wood_planks", "stone_blocks", "stone_moss", "cobble", "grass", "dirt", "stone_rough", "plaster"}
    global N
    for tid, fn in TEXTURES.items():
        N = 1024 if tid in big else 512
        a, h, meta = fn()
        meta_all[tid] = {"albedo": f"textures/{tid}_albedo.png", "normal": f"textures/{tid}_normal.png", **meta}
        pa = OUT / f"{tid}_albedo.png"
        if pa.exists() and not force:
            continue
        Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(pa)
        strength = 1.5 if tid not in ("skin", "flat", "glass", "flame", "wax") else 6.0
        Image.fromarray((normal_from_height(h, strength) * 255).astype(np.uint8)).save(OUT / f"{tid}_normal.png")
        print("texture", tid)
    (OUT / "_textures.json").write_text(json.dumps(meta_all, indent=1))


if __name__ == "__main__":
    import sys
    build(force="--force" in sys.argv)
