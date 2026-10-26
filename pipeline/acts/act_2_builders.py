"""Act II extra 3D models: the Russian schooner Demeter and her helm. Model front is -Y (bow) in Blender."""
import math


def b_a2_schooner(a, length=8.0, beam=2.4, depth=1.1):
    a.part("a2_schooner")
    n = 9
    seg = length / n
    for i in range(n):
        t = i / (n - 1)                       # 0 = bow, 1 = stern
        w = beam * (0.22 + 0.78 * math.sin(min(1.0, t * 1.6 + 0.12) * math.pi / 2))
        y = -length / 2 + seg * (i + 0.5)
        rise = 0.35 * (1 - t) ** 2            # bow sweeps up
        a.box((w, seg + 0.02, depth), (0, y, depth / 2 + 0.25 + rise * 0.5), "wood")
        a.box((w + 0.06, seg + 0.02, 0.07), (0, y, depth + 0.28 + rise), "wood")          # deck planking / gunwale cap
        for sx in (-1, 1):
            a.box((0.07, seg + 0.02, 0.5), (sx * (w / 2 - 0.02), y, depth + 0.55 + rise), "wood")   # bulwark
    a.box((beam * 0.5, 0.15, 0.2), (0, length / 2 - 0.05, 0.3), "iron")               # rudder post
    a.box((0.15, length * 0.8, 0.35), (0, 0, 0.12), "wood")                            # keel
    # deck house at the stern and forward hatch
    a.box((1.3, 1.5, 0.7), (0, length / 2 - 1.5, depth + 0.65), "wood")
    a.box((1.4, 1.6, 0.06), (0, length / 2 - 1.5, depth + 1.02), "wood")
    a.box((0.8, 0.9, 0.12), (0, -length / 2 + 2.2, depth + 0.4), "wood")
    # masts, booms and torn sails
    for my, mh in ((-1.0, 6.4), (1.0, 5.6)):
        a.cyl(0.1, mh, (0, my, depth + 0.3 + mh / 2), "wood", seg=8)
        a.beam((0, my, depth + 1.4), (0, my + 2.6, depth + 1.2), 0.07, "wood")
        a.box((0.04, 2.3, mh * 0.55), (0.03, my + 1.3, depth + 1.7 + mh * 0.28), "cloth", rot=(0.05, 0, 0))
    a.beam((0, -length / 2, depth + 0.7), (0, -1.0, depth + 5.5), 0.04, "iron")      # forestay
    a.box((0.08, 0.5, 0.08), (0, -length / 2 + 0.1, depth + 0.95), "iron")
    a.cyl(0.18, 0.18, (0.7, -2.6, depth + 0.4), "iron", seg=8)                          # windlass


def b_a2_wheel(a, r=0.55):
    a.part("a2_wheel")
    a.box((0.22, 0.22, 0.9), (0, 0, 0.45), "wood")
    zc = 1.15
    n = 10
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = 2 * math.pi * (i + 1) / n
        a.beam((r * math.cos(a0), 0, zc + r * math.sin(a0)), (r * math.cos(a1), 0, zc + r * math.sin(a1)), 0.07, "wood")
        a.beam((0, 0, zc), (1.25 * r * math.cos(a0), 0, zc + 1.25 * r * math.sin(a0)), 0.05, "wood")
    a.cyl(0.1, 0.16, (0, 0, zc), "iron", seg=8, rot=(math.pi / 2, 0, 0))
