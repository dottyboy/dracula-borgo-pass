"""New outdoor/town assets: buildings, lighthouse, ship masts, pier, boat, lamp post, crates, bollards.
Loaded by blender_gen (like props_v2). Front = -Y in Blender (= +z in game). Roles: stone (walls), roof, wood, glass, iron, flame."""


def _windows(a, w, d, h, floors, per_floor, y_front):
    for f in range(floors):
        zc = 1.5 + f * 2.2 if floors > 1 else 1.5
        n = per_floor
        for i in range(n):
            x = (i - (n - 1) / 2.0) * (w / n)
            if f == 0 and abs(x) < 0.7 and n % 2 == 1:
                continue
            a.box((0.95, 0.07, 1.25), (x, y_front - 0.02, zc + 0.3), "wood")
            a.box((0.8, 0.09, 1.1), (x, y_front - 0.045, zc + 0.3), "glass")
            a.box((0.05, 0.1, 1.1), (x, y_front - 0.05, zc + 0.3), "wood")
            a.box((1.1, 0.12, 0.08), (x, y_front - 0.06, zc - 0.32), "stone")                      # sill


def _side_windows(a, w, d, h, floors):
    """Windows on the back and both gable walls so a house reads as a whole building from any side."""
    for f in range(floors):
        zc = 1.5 + f * 2.2 if floors > 1 else 1.5
        n = max(2, int(w // 2.4))
        for i in range(n):                                                 # back wall (+Y)
            x = (i - (n - 1) / 2.0) * (w / n)
            a.box((0.95, 0.07, 1.25), (x, d / 2 + 0.02, zc + 0.3), "wood")
            a.box((0.8, 0.09, 1.1), (x, d / 2 + 0.045, zc + 0.3), "glass")
        m = max(1, int(d // 2.6))
        for sx in (-1, 1):                                                 # gable walls
            for i in range(m):
                y = (i - (m - 1) / 2.0) * (d / m)
                a.box((0.07, 0.95, 1.25), (sx * (w / 2 + 0.02), y, zc + 0.3), "wood")
                a.box((0.09, 0.8, 1.1), (sx * (w / 2 + 0.045), y, zc + 0.3), "glass")
    a.box((1.1, 0.12, 2.1), (0, d / 2 + 0.03, 1.05), "wood")                    # back door


def b_house_row(a, w=6.0, d=5.0, h=4.6, rise=2.3, chimney=True, floors=2, door=True):
    a.part("house")
    a.box((w, d, h), (0, 0, h / 2), "stone")
    a.box((w + 0.12, d + 0.12, 0.35), (0, 0, 0.175), "stone")                                       # plinth
    a.box((w + 0.1, d + 0.1, 0.18), (0, 0, h - 0.09), "stone")                                      # eaves course
    a.prism(w + 0.6, d + 0.9, rise, (0, 0, h), "roof", ridge_offset=0.0)
    _windows(a, w, d, h, floors, max(2, int(w // 2)), -d / 2)
    _side_windows(a, w, d, h, floors)
    if door:
        a.box((1.1, 0.12, 2.1), (0, -d / 2 - 0.03, 1.05), "wood")
        a.box((1.35, 0.1, 0.18), (0, -d / 2 - 0.06, 2.2), "stone")                                   # lintel
    if chimney:
        a.box((0.7, 0.7, rise * 0.9), (w * 0.28, d * 0.15, h + rise * 0.55), "stone")
        a.box((0.85, 0.85, 0.15), (w * 0.28, d * 0.15, h + rise * 1.02), "stone")
    # dormer
    a.box((1.1, 0.9, 1.0), (-w * 0.2, -d / 2 + 0.5, h + rise * 0.28), "stone")
    a.prism(1.3, 1.2, 0.6, (-w * 0.2, -d / 2 + 0.5, h + rise * 0.28 + 0.5), "roof")
    a.box((0.55, 0.06, 0.6), (-w * 0.2, -d / 2 + 0.03, h + rise * 0.28 + 0.1), "glass")


def b_cottage(a, w=4.4, d=4.0):
    b_house_row(a, w=w, d=d, h=2.7, rise=1.7, chimney=True, floors=1)


def b_cottage_nd(a, w=4.4, d=4.0):
    b_house_row(a, w=w, d=d, h=2.7, rise=1.7, chimney=True, floors=1, door=False)


def b_lighthouse(a, h=15.0):
    a.part("lighthouse")
    a.cyl(2.4, 0.8, (0, 0, 0.4), "stone", seg=16)
    segs = 5
    for i in range(segs):
        z0 = 0.8 + i * (h - 4.0) / segs
        z1 = 0.8 + (i + 1) * (h - 4.0) / segs
        r0 = 2.0 - i * 0.22
        r1 = 2.0 - (i + 1) * 0.22
        a.limb((0, 0, z0), (0, 0, z1), r0, r1, "stone" if i % 2 == 0 else "roof", seg=16)
    top = h - 3.2
    a.cyl(1.55, 0.18, (0, 0, top), "iron", seg=16)                                                    # gallery
    a.cyl(1.4, 0.9, (0, 0, top + 0.55), "glass", seg=12)                                              # lamp room
    a.sphere(0.4, (0, 0, top + 0.55), "flame", seg=8)
    a.limb((0, 0, top + 1.0), (0, 0, top + 2.1), 1.5, 0.05, "roof", seg=12)
    for k in range(8):
        import math as _m
        ang = k * _m.pi / 4
        a.beam((_m.cos(ang) * 1.4, _m.sin(ang) * 1.4, top + 0.1), (_m.cos(ang) * 1.4, _m.sin(ang) * 1.4, top + 1.0), 0.06, "iron")
    a.box((0.9, 0.12, 1.7), (0, -1.95, 1.8), "wood")


def b_mast_cluster(a):
    a.part("masts")
    a.box((7.0, 1.4, 0.7), (0, 0, 0.35), "wood")                                                      # hull silhouette
    for x, hgt in ((-2.3, 9.0), (0.2, 11.0), (2.6, 8.0)):
        a.cyl(0.12, hgt, (x, 0, hgt / 2), "wood", r2=0.07, seg=6)
        for k, z in enumerate((hgt * 0.45, hgt * 0.72)):
            a.beam((x - 1.3 + k * 0.2, 0, z), (x + 1.3 - k * 0.2, 0, z), 0.07, "wood")
            a.box((2.4 - k * 0.5, 0.05, hgt * 0.22), (x, -0.05, z - hgt * 0.1), "cloth")


def b_pier(a, length=8.0, width=2.4):
    a.part("pier")
    n = int(length / 0.28)
    for i in range(n):
        x = -length / 2 + (i + 0.5) * length / n
        a.box((length / n - 0.02, width, 0.1), (x, 0, 0.0), "wood")
    for i in range(int(length // 2) + 1):
        x = -length / 2 + i * 2.0
        for sy in (-1, 1):
            a.cyl(0.11, 1.6, (x, sy * (width / 2 - 0.05), -0.55), "wood", seg=7)
            a.cyl(0.13, 0.12, (x, sy * (width / 2 - 0.05), 0.2), "iron", seg=7)
    for sy in (-1, 1):
        a.beam((-length / 2, sy * (width / 2 - 0.05), 0.55), (length / 2, sy * (width / 2 - 0.05), 0.55), 0.07, "wood")
    a.box((0.18, width, 0.12), (-length / 2 - 0.0, 0, 0.0), "wood")


def b_boat(a, length=3.4):
    a.part("boat")
    a.sphere(0.5, (0, 0, 0.3), "wood", scale=(length, 1.35, 0.85), seg=14)                                 # hull
    a.sphere(0.5, (0, 0, 0.42), "earth", scale=(length * 0.9, 1.1, 0.55), seg=14)                         # inside
    a.limb((length * 0.45, 0, 0.3), (length * 0.6, 0, 0.62), 0.12, 0.03, "wood", seg=6)                   # bow
    a.limb((-length * 0.45, 0, 0.3), (-length * 0.52, 0, 0.5), 0.1, 0.04, "wood", seg=6)                  # stern
    for x in (-0.7, 0.1, 0.9):
        a.box((0.14, 1.0, 0.05), (x, 0, 0.38), "wood")
    a.beam((-0.6, -0.5, 0.5), (0.6, -1.4, 0.2), 0.04, "wood")                                              # oar
    a.beam((0.4, 0.5, 0.5), (-0.4, 1.4, 0.2), 0.04, "wood")


def b_lamp_post(a, h=3.4):
    a.part("lamp_post")
    a.cyl(0.22, 0.3, (0, 0, 0.15), "iron", r2=0.15, seg=8)
    a.cyl(0.07, h - 0.6, (0, 0, h / 2), "iron", seg=8)
    a.cyl(0.14, 0.12, (0, 0, h - 0.65), "iron", seg=8)
    a.limb((0, 0, h - 0.5), (0, 0, h - 0.1), 0.2, 0.28, "glass", seg=6)
    a.sphere(0.07, (0, 0, h - 0.3), "flame", seg=6)
    a.limb((0, 0, h - 0.1), (0, 0, h + 0.2), 0.32, 0.03, "iron", seg=6)
    for k in range(6):
        import math as _m
        ang = k * _m.pi / 3
        a.beam((_m.cos(ang) * 0.22, _m.sin(ang) * 0.22, h - 0.5), (_m.cos(ang) * 0.3, _m.sin(ang) * 0.3, h - 0.1), 0.02, "iron")


def b_crate_stack(a, n=3):
    a.part("crates")
    a.box((0.8, 0.8, 0.7), (0, 0, 0.35), "wood")
    a.box((0.85, 0.05, 0.1), (0, -0.4, 0.5), "wood")
    a.box((0.7, 0.7, 0.6), (0.6, 0.35, 0.3), "wood", rot=(0, 0, 0.3))
    if n > 2:
        a.box((0.65, 0.65, 0.6), (0.1, 0.05, 1.0), "wood", rot=(0, 0, -0.25))


def b_bollard(a):
    a.part("bollard")
    a.cyl(0.15, 0.6, (0, 0, 0.3), "iron", r2=0.12, seg=8)
    a.sphere(0.17, (0, 0, 0.62), "iron", seg=8)
    a.limb((0, 0, 0.3), (0.0, -0.6, 0.05), 0.04, 0.04, "leather", seg=5)


def b_rope_coil(a):
    import math as _m
    a.part("rope_coil")
    for k in range(3):
        for i in range(14):
            t0 = i * 2 * _m.pi / 14
            t1 = (i + 1) * 2 * _m.pi / 14
            r = 0.26 - k * 0.04
            a.limb((_m.cos(t0) * r, _m.sin(t0) * r, 0.04 + k * 0.05), (_m.cos(t1) * r, _m.sin(t1) * r, 0.04 + k * 0.05), 0.04, 0.04, "leather", seg=5)
