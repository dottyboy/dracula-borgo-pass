"""Whole buildings (v5): parish church with west tower. Loaded by blender_gen after props_v4. Front = -Y (= +z in game); origin at base centre."""


def b_church(a, w=8.5, d=4.6, h=4.2, tower_h=9.5):
    a.part("church")
    a.box((w + 0.2, d + 0.2, 0.4), (0, 0, 0.2), "stone")                                    # plinth
    a.box((w, d, h), (0, 0, h / 2 + 0.1), "stone")                                           # nave
    a.prism(w + 0.7, d + 1.1, 2.6, (0, 0, h + 0.1), "roof")
    a.box((2.6, d - 0.6, h - 0.8), (w / 2 + 1.0, 0, (h - 0.8) / 2 + 0.1), "stone")           # chancel
    a.prism(2.9, d + 0.2, 1.9, (w / 2 + 1.0, 0, h - 0.7), "roof")
    # west tower
    tx = -w / 2 - 1.3
    a.box((3.0, 3.0, tower_h), (tx, 0, tower_h / 2 + 0.1), "stone")
    a.box((3.3, 3.3, 0.3), (tx, 0, tower_h + 0.2), "stone")
    a.cyl(2.5, 4.2, (tx, 0, tower_h + 0.35 + 2.1), "roof", r2=0.06, seg=4)                   # spire
    for k in range(4):                                                                       # belfry openings
        import math as _m
        ang = k * _m.pi / 2
        a.box((0.1 if k % 2 == 0 else 0.7, 0.7 if k % 2 == 0 else 0.1, 1.4),
              (tx + _m.cos(ang) * 1.5, _m.sin(ang) * 1.5, tower_h - 1.2), "glass")
    a.box((1.3, 0.14, 2.3), (tx, -1.55, 1.25), "wood")                                      # tower door
    a.box((1.6, 0.12, 0.22), (tx, -1.58, 2.5), "stone")
    # tall windows, buttresses
    nw = 3
    for i in range(nw):
        x = -w / 2 + 1.4 + i * (w - 2.8) / (nw - 1)
        for sy in (-1, 1):
            y = sy * (d / 2 + 0.02)
            a.box((0.9, 0.08, 2.0), (x, y, 2.4), "wood")
            a.box((0.7, 0.1, 1.8), (x, y + sy * 0.02, 2.4), "glass")
            a.box((0.4, 0.5, h * 0.85), (x + (w - 2.8) / (nw - 1) / 2, sy * (d / 2 + 0.1), h * 0.42 + 0.1), "stone")
    a.box((0.1, 1.2, 1.6), (w / 2 + 2.32, 0, 2.2), "glass")                                  # east window
    a.box((1.2, 0.14, 2.1), (1.2, -d / 2 - 0.04, 1.15), "wood")                              # porch door
    a.box((1.5, 0.12, 0.2), (1.2, -d / 2 - 0.05, 2.3), "stone")
