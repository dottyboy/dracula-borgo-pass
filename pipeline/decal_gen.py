#!/usr/bin/env python3
"""Procedural decal textures for set dressing -> assets/decals/*.png (RGBA). numpy + PIL."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "assets" / "decals"
OUT.mkdir(parents=True, exist_ok=True)


def save(img, name):
    img.save(OUT / f"{name}.png")
    print("decal", name)


def cobweb():
    n = 256
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rng = np.random.default_rng(3)
    ox, oy = 0, 0   # corner at top-left
    for a in np.linspace(0.05, np.pi / 2 - 0.05, 7):
        d.line([(ox, oy), (ox + np.cos(a) * n * 1.35, oy + np.sin(a) * n * 1.35)], fill=(235, 235, 235, 150), width=1)
    for r in np.linspace(24, 230, 9):
        pts = []
        for a in np.linspace(0.0, np.pi / 2, 24):
            rr = r * (1 + rng.uniform(-0.04, 0.04))
            pts.append((ox + np.cos(a) * rr, oy + np.sin(a) * rr * (0.92 + 0.08 * np.sin(a * 5))))
        d.line(pts, fill=(235, 235, 235, 110), width=1)
    save(img.filter(ImageFilter.GaussianBlur(0.4)), "cobweb")


def banner(name, base, trim):
    w, h = 128, 320
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(4, 0), (w - 4, 0), (w - 4, h - 52), (w / 2, h - 12), (4, h - 52)]
    d.polygon(pts, fill=base + (255,))
    d.line(pts + [pts[0]], fill=trim + (255,), width=5)
    d.rectangle([0, 0, w, 14], fill=trim + (255,))
    # emblem: dragon-ish ring + cross
    d.ellipse([w / 2 - 34, 90, w / 2 + 34, 158], outline=trim + (255,), width=5)
    d.line([(w / 2, 100), (w / 2, 150)], fill=trim + (255,), width=5)
    d.line([(w / 2 - 20, 118), (w / 2 + 20, 118)], fill=trim + (255,), width=5)
    arr = np.array(img).astype(float)
    noise = np.random.default_rng(1).normal(0, 6, arr.shape[:2])
    arr[..., :3] += noise[..., None]
    save(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), name)


def painting(name, bg, fig, seed):
    w, h = 192, 256
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], fill=(150, 112, 40, 255))
    d.rectangle([10, 10, w - 11, h - 11], fill=(90, 66, 24, 255))
    d.rectangle([18, 18, w - 19, h - 19], fill=bg + (255,))
    rng = np.random.default_rng(seed)
    arr = np.array(img).astype(float)
    yy, xx = np.mgrid[0:h, 0:w]
    glow = np.exp(-(((xx - w / 2) / 70) ** 2 + ((yy - h * 0.38) / 90) ** 2))
    inner = (xx > 18) & (xx < w - 19) & (yy > 18) & (yy < h - 19)
    for c in range(3):
        arr[..., c] = np.where(inner, arr[..., c] * (0.6 + 0.6 * glow) + glow * fig[c] * 0.25, arr[..., c])
    # bust silhouette
    img2 = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d2 = ImageDraw.Draw(img2)
    d2.ellipse([w / 2 - 26, 70, w / 2 + 26, 134], fill=fig + (255,))
    d2.polygon([(w / 2 - 62, h - 19), (w / 2 - 40, 140), (w / 2 + 40, 140), (w / 2 + 62, h - 19)], fill=tuple(int(c * 0.55) for c in fig) + (255,))
    save(img2.filter(ImageFilter.GaussianBlur(0.8)), name)


def stain(name, seed):
    n = 256
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:n, 0:n] / n
    a = np.zeros((n, n))
    for _ in range(7):
        cx, cy, r = rng.uniform(0.3, 0.7), rng.uniform(0.3, 0.7), rng.uniform(0.08, 0.24)
        a += np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r)) ** 1.2)
    a = np.clip(a, 0, 1)
    from scipy.ndimage import gaussian_filter
    a = gaussian_filter(a, 3) * (0.6 + 0.4 * gaussian_filter(rng.random((n, n)), 6) * 4)
    a = np.clip(a, 0, 1) ** 1.3
    rgba = np.zeros((n, n, 4), np.uint8)
    rgba[..., 0:3] = (28, 22, 16)
    rgba[..., 3] = (a * 150).astype(np.uint8)
    save(Image.fromarray(rgba), name)


def light_shaft():
    w, h = 64, 256
    yy, xx = np.mgrid[0:h, 0:w]
    a = np.clip(1 - np.abs(xx / w - 0.5) * 2, 0, 1) ** 1.5 * np.clip(1 - yy / h, 0, 1) ** 0.8
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., 0:3] = 255
    rgba[..., 3] = (a * 90).astype(np.uint8)
    save(Image.fromarray(rgba), "shaft")


def main():
    cobweb()
    banner("banner_red", (110, 20, 28), (205, 165, 70))
    banner("banner_black", (24, 22, 30), (190, 150, 60))
    painting("painting_1", (46, 36, 28), (170, 130, 100), 1)
    painting("painting_2", (30, 38, 44), (140, 150, 160), 2)
    painting("painting_3", (50, 24, 24), (190, 150, 120), 3)
    stain("stain_1", 5)
    stain("stain_2", 6)
    light_shaft()


if __name__ == "__main__":
    main()
