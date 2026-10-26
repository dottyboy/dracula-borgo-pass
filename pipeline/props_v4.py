"""Nature / village / harbour props (v4). Loaded by blender_gen after props_v3 (math and Asset are injected globals).
Front = -Y in Blender (= +z in game); origin at base centre; 1 unit = 1 m. Deterministic jitter via a local LCG."""

_G = Asset.limb.__globals__
bmesh = _G["bmesh"]
Vector = _G["Vector"]


class _R:
    def __init__(self, seed):
        self.s = (seed * 2654435761 + 12345) % 4294967296

    def f(self):
        self.s = (self.s * 1664525 + 1013904223) % 4294967296
        return self.s / 4294967296.0

    def r(self, lo, hi):
        return lo + (hi - lo) * self.f()

    def j(self, amp=1.0):
        return (self.f() * 2 - 1) * amp


def _rock(a, c, rad, mat, R, sc=(1, 1, 1), seg=8, jit=0.2, zmin=None, smooth=False, rz=None):
    """Jittered (faceted) sphere; rad = base radius, sc = axis scale, zmin clips the underside."""
    bm = a.parts[a.cur][0]
    rot = (0, 0, R.r(0, 6.28) if rz is None else rz)
    res = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(4, seg // 2), radius=rad,
                                    matrix=a._m(c, rot, sc))
    cv = Vector(c)
    for v in res["verts"]:
        v.co += (v.co - cv) * R.j(jit)
        if zmin is not None and v.co.z < zmin:
            v.co.z = zmin
    a._finish(res["verts"], mat, smooth)


def _chunk(a, c, size, mat, R, jit=0.1, rot=(0, 0, 0)):
    """Box with each corner jittered: irregular stone slab (12 tris)."""
    bm = a.parts[a.cur][0]
    res = bmesh.ops.create_cube(bm, size=1.0, matrix=a._m(c, rot, size))
    for v in res["verts"]:
        v.co += Vector((R.j(jit * size[0]), R.j(jit * size[1]), R.j(jit * size[2])))
    a._finish(res["verts"], mat, False)


def _leaf(a, p0, p1, w, t, mat, up=(0, 0, 1)):
    """Flat double-sided blade (8-tri bipyramid) from p0 to p1, width w, thickness t."""
    bm = a.parts[a.cur][0]
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    side = d.cross(Vector(up))
    if side.length < 1e-5:
        side = Vector((1, 0, 0))
    side.normalize()
    n = side.cross(d).normalized()
    m = p0 + d * 0.4
    L, Rr, T, B = m + side * (w / 2), m - side * (w / 2), m + n * t, m - n * t
    vs = [bm.verts.new(p) for p in (p0, p1, L, Rr, T, B)]
    p0v, p1v, Lv, Rv, Tv, Bv = vs
    for tri in ((p0v, Lv, Tv), (p0v, Tv, Rv), (p0v, Rv, Bv), (p0v, Bv, Lv),
                (p1v, Tv, Lv), (p1v, Rv, Tv), (p1v, Bv, Rv), (p1v, Lv, Bv)):
        bm.faces.new(tri)
    a._finish(vs, mat, False)


def _chain(a, pts, r0, r1, mat, seg=5):
    """Polyline of tapered limbs through pts, radius r0 -> r1."""
    n = len(pts) - 1
    for i in range(n):
        ra = r0 + (r1 - r0) * i / n
        rb = r0 + (r1 - r0) * (i + 1) / n
        a.limb(pts[i], pts[i + 1], ra, rb, mat, seg=seg, cap=(i == n - 1 or i == 0))


def _slab(a, p0, p1, width, thick, mat):
    """Thin flat plank spanning p0 -> p1 in the YZ plane direction (x width fixed)."""
    dy, dz = p1[1] - p0[1], p1[2] - p0[2]
    L = math.hypot(dy, dz)
    th = math.atan2(dz, dy) - math.pi / 2 + math.pi / 2
    a.box((width, L, thick), ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2), mat, rot=(th, 0, 0))


def _ring(a, c, r, n, thick, mat, plane="xz", sq=1.0):
    """Ring of n beams in a plane through centre c."""
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        u, v = math.cos(t) * r, math.sin(t) * r * sq
        pts.append((c[0] + u, c[1], c[2] + v) if plane == "xz" else
                   (c[0], c[1] + u, c[2] + v) if plane == "yz" else (c[0] + u, c[1] + v, c[2]))
    for i in range(n):
        a.beam(pts[i], pts[i + 1], thick, mat)


# --------------------------------------------------------------------------- vegetation
def b_bush(a, r=0.9):
    a.part("bush")
    R = _R(11 + int(r * 10))
    for k in range(3):                       # trunk stubs
        ang = k * 2.1 + R.j(0.4)
        a.limb((math.cos(ang) * 0.05, math.sin(ang) * 0.05, 0), (math.cos(ang) * r * 0.25, math.sin(ang) * r * 0.25, r * 0.5),
               r * 0.07, r * 0.04, "bark", seg=5)
    n = 7
    for i in range(n):
        ang = i * 2 * math.pi / n + R.j(0.3)
        d = r * R.r(0.3, 0.5)
        rad = r * R.r(0.5, 0.65)
        _rock(a, (math.cos(ang) * d, math.sin(ang) * d, rad * 0.62 + r * 0.05), rad, "foliage", R,
              sc=(1, 1, 0.78), seg=9, jit=0.12, smooth=True)
    _rock(a, (R.j(0.1), R.j(0.1), r * 0.78), r * 0.5, "foliage", R, sc=(1, 1, 0.75), seg=9, jit=0.1, smooth=True)
    for i in range(6):                       # protruding twigs
        ang = R.r(0, 6.28)
        z = r * R.r(0.3, 0.9)
        d0, d1 = r * 0.5, r * R.r(0.95, 1.2)
        a.limb((math.cos(ang) * d0, math.sin(ang) * d0, z), (math.cos(ang) * d1, math.sin(ang) * d1, z + r * R.r(0.05, 0.25)),
               r * 0.025, r * 0.008, "bark", seg=4)


def b_fern(a):
    a.part("fern")
    R = _R(21)
    n = 9
    for i in range(n):
        phi = i * 2 * math.pi / n + R.j(0.2)
        L = R.r(0.7, 1.0)
        steps = 6
        ds = L / steps
        x = 0.04
        z = 0.04
        al = math.radians(R.r(55, 70))
        pts = [(x, z)]
        for s in range(steps):
            al -= math.radians(R.r(17, 22))
            x += math.cos(al) * ds
            z += math.sin(al) * ds
            pts.append((x, max(z, 0.02)))
        cp, sp = math.cos(phi), math.sin(phi)
        P = [(px * cp, px * sp, pz) for px, pz in pts]
        for k in range(steps):
            a.limb(P[k], P[k + 1], 0.016 * (1 - k / steps) + 0.004, 0.016 * (1 - (k + 1) / steps) + 0.004, "foliage", seg=3, cap=False)
        for k in range(1, steps):
            ll = 0.2 * (1 - k / (steps + 1)) + 0.05
            for sd in (-1, 1):
                px, py, pz = P[k]
                ox = -sp * sd * ll + cp * ll * 0.5
                oy = cp * sd * ll + sp * ll * 0.5
                _leaf(a, P[k], (px + ox, py + oy, pz - ll * 0.18), ll * 0.6, 0.008, "foliage")
        _leaf(a, P[-1], (P[-1][0] + cp * 0.14, P[-1][1] + sp * 0.14, P[-1][2] - 0.08), 0.06, 0.008, "foliage")


def b_flower_patch(a):
    a.part("flowers")
    R = _R(31)
    for i in range(16):                      # grass/leaf blades
        ang = R.r(0, 6.28)
        d = R.r(0.03, 0.28)
        bx, by = math.cos(ang) * d, math.sin(ang) * d
        tx, ty = bx * 1.5 + R.j(0.06), by * 1.5 + R.j(0.06)
        _leaf(a, (bx, by, 0), (tx, ty, R.r(0.12, 0.28)), 0.045, 0.006, "plant")
    for i in range(11):
        ang = i * 2 * math.pi / 11 + R.j(0.4)
        d = R.r(0.05, 0.3)
        bx, by = math.cos(ang) * d, math.sin(ang) * d
        h = R.r(0.18, 0.4)
        tx, ty = bx + R.j(0.04), by + R.j(0.04)
        a.limb((bx, by, 0), (tx, ty, h), 0.011, 0.008, "plant", seg=3)
        a.cyl(0.055, 0.02, (tx, ty, h + 0.01), "petal", r2=0.045, seg=7, rot=(R.j(0.3), R.j(0.3), 0))
        a.sphere(0.03, (tx, ty, h + 0.03), "petal", seg=6)


def b_reeds(a):
    a.part("reeds")
    R = _R(41)
    n = 18
    for i in range(n):
        ang = R.r(0, 6.28)
        d = R.r(0.0, 0.34)
        bx, by = math.cos(ang) * d, math.sin(ang) * d * 0.7
        h = R.r(0.8, 1.5)
        la = R.r(0, 6.28)
        lean = R.r(0.05, 0.28)
        pts = []
        for k in range(4):
            t = k / 3
            pts.append((bx + math.cos(la) * lean * t * t * h, by + math.sin(la) * lean * t * t * h, h * t))
        if i % 3 == 2:                       # broad leaf blade
            _leaf(a, pts[0], pts[3], 0.07, 0.006, "plant")
            continue
        _chain(a, pts, 0.014, 0.006, "plant", seg=3)
        if i % 4 == 0:                       # seed head
            top = pts[3]
            a.cyl(0.032, 0.2, (top[0], top[1], top[2] + 0.04), "plant", r2=0.022, seg=6)
    for i in range(3):
        _leaf(a, (0, 0, 0), (R.j(0.3), R.j(0.3), R.r(0.6, 0.9)), 0.05, 0.006, "plant")


def b_log(a):
    a.part("log")
    R = _R(51)
    xs = [-1.0, -0.35, 0.3, 0.85]
    rs = [0.30, 0.32, 0.29, 0.27]
    for i in range(3):
        a.limb((xs[i], R.j(0.02), rs[i]), (xs[i + 1], R.j(0.03), rs[i + 1] - 0.01), rs[i], rs[i + 1], "bark", seg=10, cap=(i != 1))
    # cut end rings at -X
    for k, rr in enumerate((0.3, 0.23, 0.16, 0.09, 0.03)):
        a.cyl(rr, 0.02, (-1.0 - 0.012 - k * 0.004, 0, 0.3), "bark", seg=10, rot=(0, math.pi / 2, 0))
    # broken jagged end at +X
    for i in range(7):
        ang = i * 2 * math.pi / 7 + R.j(0.3)
        rr = R.r(0.05, 0.2)
        yy, zz = math.cos(ang) * rr, 0.27 + math.sin(ang) * rr
        a.limb((0.8, yy * 0.9, zz), (0.8 + R.r(0.1, 0.35), yy, zz + R.j(0.05)), 0.045, 0.006, "bark", seg=4)
    for p in ((-0.5, 0.0, 0.31), (0.2, 0.04, 0.3)):
        a.sphere(0.08, (p[0], p[1] - 0.2, p[2] + 0.1), "bark", scale=(1, 0.5, 1) if False else (1, 0.6, 1), seg=7)
    # branch stubs
    for x, sy, lift in ((-0.45, -1, 0.55), (0.35, 1, 0.5), (0.0, -1, 0.35)):
        a.limb((x, sy * 0.2, 0.42), (x + 0.12, sy * (0.2 + 0.28), 0.42 + lift * 0.5), 0.055, 0.035, "bark", seg=6)
        a.cyl(0.032, 0.02, (x + 0.12, sy * 0.48, 0.42 + lift * 0.5), "bark", seg=6)
    a.sphere(0.07, (0.55, -0.25, 0.22), "bark", seg=6)


def b_stump(a):
    a.part("stump")
    R = _R(61)
    a.limb((0, 0, 0.0), (0.02, 0, 0.3), 0.42, 0.36, "bark", seg=11, cap=False)
    a.limb((0.02, 0, 0.3), (0.0, 0.0, 0.62), 0.36, 0.33, "bark", seg=11, cap=False)
    for i in range(6):                       # roots
        ang = i * 2 * math.pi / 6 + R.j(0.25)
        c, s = math.cos(ang), math.sin(ang)
        a.limb((c * 0.25, s * 0.25, 0.32), (c * R.r(0.65, 0.85), s * R.r(0.65, 0.85), 0.01), 0.15, 0.04, "bark", seg=6)
    for k, rr in enumerate((0.33, 0.26, 0.19, 0.12, 0.05)):   # rings on top
        a.cyl(rr, 0.02, (0, 0, 0.62 + 0.006 * k), "bark", seg=11)
    for i in range(3):                       # splintered edge
        ang = i * 2.1 + 0.4
        a.limb((math.cos(ang) * 0.27, math.sin(ang) * 0.27, 0.6), (math.cos(ang) * 0.3, math.sin(ang) * 0.3, 0.6 + R.r(0.1, 0.25)),
               0.045, 0.005, "bark", seg=4)
    a.sphere(0.08, (0.3, -0.12, 0.33), "bark", seg=6)


def b_hedge(a, w=3.0):
    a.part("hedge")
    R = _R(71)
    a.box((w - 0.4, 0.5, 0.2), (0, 0, 0.1), "bark")
    for x in (-w / 2 + 0.3, 0, w / 2 - 0.3):
        a.cyl(0.07, 0.3, (x, R.j(0.05), 0.15), "bark", seg=5)
    n = 6
    cw = w / n
    for i in range(n):
        x = -w / 2 + cw * (i + 0.5)
        hh = R.r(0.85, 1.05)
        a.box((cw + 0.04, R.r(0.7, 0.85), hh - 0.15), (x, R.j(0.03), 0.15 + (hh - 0.15) / 2), "foliage")
    for i in range(10):                      # lumpy top and sides
        x = -w / 2 + 0.2 + (w - 0.4) * i / 9 + R.j(0.08)
        _rock(a, (x, R.j(0.12), R.r(0.9, 1.0)), 0.3, "foliage", R, sc=(1.1, 1.3, 0.55), seg=8, jit=0.1, smooth=True, rz=0)
    for i in range(12):
        sy = -1 if i % 2 == 0 else 1
        _rock(a, (-w / 2 + 0.25 + (i // 2) * 0.5 + R.j(0.05), sy * 0.33, R.r(0.45, 0.8)), 0.34, "foliage", R, sc=(1.5, 0.7, 1.1), seg=8, jit=0.12, smooth=True, rz=0)


def b_low_wall(a, w=3.0):
    a.part("wall")
    R = _R(81)
    h0 = 0.0
    a.box((w - 0.9, 0.3, 0.75), (-0.45, 0, 0.375), "stone")
    a.box((0.9, 0.3, 0.3), (w / 2 - 0.45, 0, 0.15), "stone")
    courses = [0.15, 0.14, 0.15, 0.14, 0.15]
    z = 0.0
    for ci, ch in enumerate(courses):
        x = -w / 2
        off = 0.0 if ci % 2 == 0 else -0.2
        x += off
        while x < w / 2 - 0.05:
            sw = R.r(0.3, 0.6)
            x0 = max(x, -w / 2)
            x1 = min(x + sw, w / 2)
            x += sw
            if x1 - x0 < 0.12:
                continue
            xc = (x0 + x1) / 2
            # collapsed corner at +X: higher courses missing
            if xc > w / 2 - 0.75 and z > 0.28 + (w / 2 - xc) * 0.0 and (ci >= 2 and (xc > w / 2 - 0.35 or ci >= 4)):
                continue
            hh = ch * R.r(0.9, 1.05)
            _chunk(a, (xc, R.j(0.015), z + hh / 2), (x1 - x0 - 0.02, R.r(0.38, 0.42), hh), "stone", R, jit=0.04, rot=(0, 0, R.j(0.03)))
        z += ch
    x = -w / 2 + 0.1
    while x < w / 2 - 0.9:                   # coping stones
        sw = R.r(0.45, 0.65)
        sw = min(sw, w / 2 - 0.85 - x)
        if sw < 0.2:
            break
        _chunk(a, (x + sw / 2, R.j(0.01), 0.78), (sw - 0.02, 0.46, 0.14), "stone", R, jit=0.06, rot=(0, R.j(0.04), R.j(0.04)))
        x += sw
    for i in range(6):                       # fallen rubble
        _chunk(a, (w / 2 - 0.5 + R.j(0.5), -0.35 - R.r(0, 0.4), 0.08), (R.r(0.2, 0.4), R.r(0.18, 0.3), R.r(0.12, 0.18)),
               "stone", R, jit=0.12, rot=(0, R.j(0.2), R.r(0, 6)))
    _chunk(a, (w / 2 - 0.55, 0.0, 0.38), (0.55, 0.4, 0.14), "stone", R, jit=0.08, rot=(R.j(0.2), R.j(0.2), 0.2))


def b_well(a):
    a.part("well")
    R = _R(91)
    n = 14
    for course in range(2):
        for i in range(n):
            ang = (i + 0.5 * course) * 2 * math.pi / n
            c, s = math.cos(ang), math.sin(ang)
            _chunk(a, (c * 0.72, s * 0.72, 0.2 + course * 0.4), (0.3, 0.38, 0.4 * R.r(0.95, 1.0)), "stone", R, jit=0.015,
                   rot=(0, 0, ang + math.pi / 2))
    for i in range(n):                       # coping
        ang = i * 2 * math.pi / n + R.j(0.05)
        c, s = math.cos(ang), math.sin(ang)
        _chunk(a, (c * 0.72, s * 0.72, 0.86), (0.4, 0.46, 0.1), "stone", R, jit=0.05, rot=(0, 0, ang + math.pi / 2))
    a.cyl(0.55, 0.05, (0, 0, 0.55), "iron", seg=12)          # dark water
    for sx in (-1, 1):
        a.box((0.12, 0.14, 1.45), (sx * 0.66, 0, 0.85 + 0.725), "wood")
    a.beam((-0.78, 0, 2.2), (0.78, 0, 2.2), 0.14, "wood")
    a.cyl(0.11, 1.25, (0, 0, 1.6), "wood", seg=8, rot=(0, math.pi / 2, 0))
    a.cyl(0.04, 0.35, (0.85, 0, 1.6), "iron", seg=5, rot=(0, math.pi / 2, 0))
    a.beam((0.98, 0, 1.6), (0.98, 0.0, 1.25), 0.05, "iron")
    a.prism(1.7, 1.5, 0.6, (0, 0, 2.27), "roof")
    a.box((1.75, 0.08, 0.06), (0, 0, 2.27), "wood")
    a.limb((0, 0.0, 1.6), (0, 0, 1.15), 0.015, 0.015, "wood", seg=4)
    a.cyl(0.14, 0.2, (0, 0, 1.0), "wood", r2=0.11, seg=9)
    a.cyl(0.145, 0.03, (0, 0, 1.06), "iron", seg=9)
    a.cyl(0.115, 0.03, (0, 0, 0.94), "iron", seg=9)
    a.limb((-0.12, 0, 1.12), (0.12, 0, 1.12), 0.012, 0.012, "iron", seg=4)


def b_market_stall(a):
    a.part("stall")
    R = _R(101)
    a.box((2.1, 0.8, 0.08), (0, -0.2, 0.9), "wood")
    a.box((2.1, 0.06, 0.7), (0, -0.58, 0.55), "wood")
    a.box((2.1, 0.06, 0.12), (0, 0.18, 0.42), "wood")
    a.box((2.1, 0.5, 0.05), (0, 0.4, 0.2), "wood")
    for sx in (-1, 1):
        a.box((0.1, 0.1, 2.35), (sx * 1.05, -0.65, 1.175), "wood")
        a.box((0.1, 0.1, 2.65), (sx * 1.05, 0.55, 1.325), "wood")
        a.beam((sx * 1.05, -0.65, 0.2), (sx * 1.05, 0.55, 0.2), 0.07, "wood")
    a.beam((-1.05, 0.55, 2.0), (1.05, 0.55, 2.0), 0.06, "wood")
    a.box((2.0, 0.06, 0.04), (0, 0.55, 1.4), "wood")
    # awning: sagging stripes
    ns = 10
    sw = 2.5 / ns
    for i in range(ns):
        x = -1.25 + sw * (i + 0.5)
        up = 0.02 if i % 2 else 0.0
        sag = 0.06 + 0.08 * math.sin(math.pi * (i + 0.5) / ns)
        pa = (x, 0.7, 2.62 + up)
        pm = (x, -0.1, 2.5 - sag + up)
        pb = (x, -0.85, 2.28 + up)
        _slab(a, pa, pm, sw - 0.005, 0.03, "cloth")
        _slab(a, pm, pb, sw - 0.005, 0.03, "cloth")
        if i % 2 == 0:                       # scalloped valance
            a.box((sw - 0.01, 0.03, 0.16 + 0.02 * (i % 4)), (x, -0.86, 2.2 - 0.04), "cloth")
    for sx in (-1, 1):
        a.beam((sx * 1.05, -0.65, 2.3), (sx * 1.05, -0.85, 2.3), 0.05, "wood")
    # goods
    a.box((0.5, 0.4, 0.28), (-0.7, -0.15, 1.08), "wood", rot=(0, 0, 0.1))
    a.box((0.4, 0.35, 0.22), (-0.55, -0.1, 1.33), "wood", rot=(0, 0, -0.2))
    a.box((0.45, 0.35, 0.2), (0.75, -0.3, 1.04), "wood", rot=(0, 0, 0.25))
    for x, y in ((0.1, -0.3), (0.35, -0.05)):
        a.cyl(0.17, 0.16, (x, y, 1.02), "wood", r2=0.2, seg=9)
        a.cyl(0.18, 0.025, (x, y, 1.11), "wood", seg=9)
    a.cyl(0.14, 0.12, (-0.1, 0.1, 0.98), "wood", r2=0.17, seg=8)
    a.sphere(0.2, (0.1, -0.3, 1.1), "cloth", scale=(1, 1, 0.5), seg=8)


def b_hay_bale(a):
    a.part("bale")
    R = _R(111)
    a.box((1.0, 0.5, 0.45), (0, 0, 0.225), "straw")
    a.box((0.96, 0.52, 0.4), (0.02, 0.0, 0.24), "straw", rot=(0, 0, 0.05))
    a.box((0.94, 0.46, 0.08), (0, 0, 0.45), "straw", rot=(0.04, 0, -0.03))
    for x in (-0.25, 0.25):
        a.box((0.035, 0.53, 0.47), (x, 0, 0.225), "leather")
        a.box((0.06, 0.54, 0.05), (x, 0, 0.45), "leather")
    for i in range(30):
        px = R.r(-0.5, 0.5)
        face = i % 3
        if face == 0:
            p0 = (px, R.r(-0.25, 0.25), R.r(0.05, 0.45))
            p1 = (px + R.j(0.05), p0[1] + (0.12 if p0[1] > 0 else -0.12) * R.r(0.5, 1), p0[2] + R.r(-0.04, 0.1))
        elif face == 1:
            p0 = (px, R.r(-0.2, 0.2), 0.44)
            p1 = (px + R.j(0.12), p0[1] + R.j(0.1), 0.44 + R.r(0.05, 0.14))
        else:
            sx = 1 if R.f() > 0.5 else -1
            p0 = (sx * 0.48, R.r(-0.22, 0.22), R.r(0.05, 0.42))
            p1 = (sx * (0.48 + R.r(0.05, 0.14)), p0[1] + R.j(0.06), p0[2] + R.j(0.05))
        a.limb(p0, p1, 0.012, 0.004, "straw", seg=3, cap=False)


def _wheel(a, cx, cy, cz, r, R):
    n = 10
    for i in range(n):
        t0, t1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        a.beam((cx + math.cos(t0) * r, cy, cz + math.sin(t0) * r), (cx + math.cos(t1) * r, cy, cz + math.sin(t1) * r), 0.07, "wood")
    for i in range(8):
        t = 2 * math.pi * i / 8 + 0.2
        a.beam((cx + math.cos(t) * 0.07, cy, cz + math.sin(t) * 0.07), (cx + math.cos(t) * r, cy, cz + math.sin(t) * r), 0.045, "wood")
    a.cyl(0.1, 0.16, (cx, cy, cz), "iron", seg=8, rot=(math.pi / 2, 0, 0))
    for i in range(n):
        t = 2 * math.pi * (i + 0.5) / n
        a.box((0.03, 0.075, 0.06), (cx + math.cos(t) * (r + 0.03), cy, cz + math.sin(t) * (r + 0.03)), "iron", rot=(0, -t, 0))


def b_cart(a):
    a.part("cart")
    R = _R(121)
    for sy in (-1, 1):
        _wheel(a, 0.1, sy * 0.72, 0.5, 0.5, R)
    a.beam((0.1, -0.78, 0.5), (0.1, 0.78, 0.5), 0.07, "iron")
    for i in range(4):
        y = -0.5 + i * 0.33
        a.box((1.6, 0.31, 0.05), (0.1, y, 0.7), "wood", rot=(0, 0, R.j(0.01)))
    for sy in (-1, 1):
        a.box((1.6, 0.05, 0.28), (0.1, sy * 0.52, 0.86), "wood")
        a.beam((-0.7, sy * 0.5, 0.64), (-2.1, sy * 0.3, 0.3), 0.07, "wood")
        a.beam((0.8, sy * 0.5, 0.64), (-0.7, sy * 0.5, 0.64), 0.07, "wood")
    a.box((0.05, 1.1, 0.28), (0.9, 0, 0.86), "wood")
    a.beam((-2.1, -0.3, 0.3), (-2.1, 0.3, 0.3), 0.05, "wood")
    a.box((0.05, 1.1, 0.2), (-0.72, 0, 0.82), "wood")
    for x, y, rz in ((0.35, -0.2, 0.3), (0.45, 0.25, -0.2), (-0.1, 0.1, 0.5)):
        a.sphere(0.3, (x, y, 0.95), "cloth", scale=(0.85, 1.0, 0.9), seg=9, rot=(0, 0, rz))
        a.cyl(0.07, 0.1, (x, y, 1.2), "cloth", r2=0.03, seg=6)
    a.sphere(0.22, (-0.4, -0.25, 0.9), "cloth", scale=(1.2, 0.8, 0.7), seg=8)


def b_anchor(a):
    a.part("anchor")
    R = _R(131)
    a.limb((-0.75, 0, 0.12), (0.7, 0, 0.1), 0.045, 0.05, "iron", seg=6)
    a.sphere(0.07, (0.75, 0, 0.1), "iron", seg=6)
    a.beam((-0.55, -0.42, 0.2), (-0.55, 0.45, 0.14), 0.06, "iron")      # stock
    a.sphere(0.07, (-0.55, -0.44, 0.2), "iron", seg=6)
    a.sphere(0.07, (-0.55, 0.47, 0.14), "iron", seg=6)
    _ring(a, (-0.88, 0, 0.2), 0.14, 8, 0.045, "iron", plane="xz")
    for sy in (-1, 1):                       # arms
        pts = [(0.7, sy * 0.05, 0.09), (0.72, sy * 0.25, 0.1), (0.62, sy * 0.42, 0.15), (0.45, sy * 0.52, 0.2)]
        _chain(a, pts, 0.05, 0.04, "iron", seg=6)
        _leaf(a, (0.55, sy * 0.46, 0.17), (0.3, sy * 0.58, 0.24), 0.2, 0.025, "iron")
    # chain snaking away
    cx, cy = -0.88, 0.14
    for i in range(10):
        ang = 1.9 + 0.35 * math.sin(i * 0.7)
        cx += math.cos(ang) * 0.13
        cy += math.sin(ang) * 0.13
        if i % 2 == 0:
            _ring(a, (cx, cy, 0.04), 0.075, 6, 0.032, "iron", plane="xy", sq=0.55)
        else:
            _ring(a, (cx, cy, 0.05), 0.075, 6, 0.032, "iron", plane="xz", sq=0.55)


def b_net_rack(a):
    a.part("rack")
    R = _R(141)
    for sx in (-1, 1):
        a.beam((sx * 1.1, -0.4, 0.0), (sx * 1.1, -0.05, 1.85), 0.09, "wood")
        a.beam((sx * 1.1, 0.4, 0.0), (sx * 1.1, 0.05, 1.85), 0.09, "wood")
        a.beam((sx * 1.1, -0.25, 0.4), (sx * 1.1, 0.25, 0.4), 0.05, "wood")
    a.beam((-1.2, 0, 1.8), (1.2, 0, 1.8), 0.09, "wood")
    a.beam((-1.15, 0, 1.05), (1.15, 0.0, 1.0), 0.05, "wood")
    a.limb((-1.05, -0.12, 1.7), (1.05, -0.12, 1.7), 0.02, 0.02, "leather", seg=4)
    for i in range(9):                       # floats along rope
        x = -0.95 + i * 0.24
        a.sphere(0.065, (x, -0.14, 1.64), "wood", scale=(1, 1, 1.15), seg=7)
    # net: vertical strings with ragged hem, horizontal strings sagging
    nv = 18
    for i in range(nv):
        x = -1.0 + 2.0 * i / (nv - 1)
        ln = 1.35 - 0.25 * math.sin(i * 0.9) ** 2 - R.r(0, 0.25) - (0.15 if i in (6, 7) else 0)
        a.limb((x, -0.12, 1.7), (x + R.j(0.02), -0.12 - 0.04 * (ln / 1.3), 1.7 - ln), 0.012, 0.012, "leather", seg=3, cap=False)
    for k in range(6):
        z = 1.55 - k * 0.22
        pts = []
        for i in range(7):
            x = -1.0 + 2.0 * i / 6
            pts.append((x, -0.14 - 0.03 * math.sin(math.pi * i / 6), z - 0.03 * math.sin(math.pi * i / 6)))
        _chain(a, pts, 0.012, 0.012, "leather", seg=3)
    a.sphere(0.4, (0.85, -0.55, 0.1), "leather", scale=(1.2, 1.0, 0.35), seg=8)       # heap of net on ground
    a.sphere(0.25, (0.45, -0.7, 0.07), "leather", scale=(1.2, 1.0, 0.35), seg=7)


# --------------------------------------------------------------------------- terrain / stone
def b_cliff_face(a, w=8.0, h=9.0):
    """Weathered sea cliff: stacked layers of rounded, overlapping boulders with ledges, a grassy crest and scree at the foot."""
    a.part("cliff")
    R = _R(151)
    nl = 7
    lh = h / nl
    for i in range(nl):
        wi = w * (1.0 - 0.05 * i)
        fy = -1.35 + 0.2 * i
        zc = i * lh + lh * 0.5
        _chunk(a, (R.j(0.1), fy + 2.3, zc), (wi * 0.8, 3.0, lh * 1.15), "rock", R, jit=0.08)           # solid core
    n_blobs = int(w * h * 1.5)
    for k in range(n_blobs):                                                                           # lumpy rock mass, scattered over the face
        z = R.r(0.3, h - 0.2)
        lvl = z / lh
        wi = w * (1.0 - 0.05 * lvl)
        x = R.r(-wi / 2 + 0.3, wi / 2 - 0.3)
        y = -1.35 + 0.2 * lvl + R.r(-0.35, 0.55)
        rad = R.r(0.55, 1.05) * (1.15 - 0.04 * lvl)
        _rock(a, (x, y, z), rad, "rock", R, sc=(R.r(0.95, 1.3), R.r(0.85, 1.15), R.r(0.8, 1.15)), seg=9, jit=0.34)
    for i in range(8):                                                                                 # scree and boulders at the foot
        x = -w / 2 + 0.3 + i * (w - 0.6) / 7 + R.j(0.35)
        rad = R.r(0.45, 0.95)
        _rock(a, (x, -1.75 + R.j(0.25), rad * 0.4), rad, "rock", R, sc=(1.2, 1.0, 0.7), seg=8, jit=0.28, zmin=0.0)
    for i in range(5):                                                                                 # grass tufts on ledges
        lv = 1 + i % (nl - 1)
        x = R.r(-w / 2 + 1.2, w / 2 - 1.2) * (1 - 0.05 * lv)
        y = -1.35 + 0.2 * lv - 0.15
        _rock(a, (x, y, lv * lh + 0.05), R.r(0.28, 0.45), "foliage", R, sc=(1.4, 1.0, 0.55), seg=7, jit=0.15, smooth=True, rz=0)
        for bl in range(3):
            bx, by = x + R.j(0.25), y + R.j(0.12)
            _leaf(a, (bx, by, lv * lh), (bx + R.j(0.12), by - R.r(0, 0.15), lv * lh + R.r(0.25, 0.45)), 0.07, 0.01, "foliage")
    top = nl * lh
    for i in range(7):                                                                                 # grassy crest
        x = -w * 0.3 + i * w * 0.1 + R.j(0.15)
        _rock(a, (x, R.r(-0.6, 0.9), top + 0.0), R.r(0.6, 1.0), "foliage", R, sc=(1.3, 1.1, 0.45), seg=8, jit=0.15, smooth=True, rz=0)
    for i in range(9):
        bx, by = R.r(-w * 0.35, w * 0.35), R.r(-0.9, 0.4)
        _leaf(a, (bx, by, top), (bx + R.j(0.2), by - R.r(0, 0.2), top + R.r(0.4, 0.7)), 0.09, 0.012, "foliage")
    _rock(a, (w * 0.28, -0.3, top + 0.25), 0.75, "rock", R, sc=(1.1, 1, 0.8), seg=8, jit=0.25)


def b_cliff_stairs(a, steps=20):
    a.part("stairs")
    R = _R(161)
    x0, x1, H = -3.5, 2.8, 4.0
    run = (x1 - x0) / steps
    rise = H / steps
    for i in range(steps):
        top = rise * (i + 1)
        _chunk(a, (x0 + run * (i + 0.5), 0.0, top / 2), (run * 1.04, 1.4 + R.j(0.04), top), "stone", R, jit=0.03)
    _chunk(a, ((x1 + 3.5) / 2, 0.0, H / 2 - 0.05), (0.72, 1.6, H - 0.1), "stone", R, jit=0.02)
    _chunk(a, ((x1 + 3.5) / 2, 0.0, H - 0.07), (0.78, 1.64, 0.14), "stone", R, jit=0.03)
    for i in range(steps):                   # protruding facing blocks on the outer wall
        if i % 2 == 0:
            top = rise * (i + 1)
            _chunk(a, (x0 + run * (i + 0.5), -0.78, top * 0.5), (run * 0.9, 0.12, top * R.r(0.5, 0.9)), "stone", R, jit=0.1)
    ry = -0.66
    nposts = 6
    prev = None
    for k in range(nposts + 1):
        xi = k * (steps - 1) / nposts
        x = x0 + run * (xi + 0.5)
        zt = rise * (xi + 1)
        p = (x, ry, zt + 0.95)
        a.limb((x, ry, zt), p, 0.03, 0.025, "iron", seg=5)
        a.sphere(0.04, p, "iron", seg=5)
        if prev:
            a.limb(prev, p, 0.022, 0.022, "iron", seg=4)
            mid = ((prev[0] + p[0]) / 2, ry, (prev[2] + p[2]) / 2 - 0.45)
            a.limb((prev[0], ry, prev[2] - 0.3), p if False else (p[0], ry, p[2] - 0.3), 0.012, 0.012, "iron", seg=3)
        prev = p
    for k in range(3):                       # landing rail
        x = 2.9 + k * 0.3
        a.limb((x, ry, H), (x, ry, H + 0.95), 0.03, 0.025, "iron", seg=5)
    a.limb((2.9, ry, H + 0.95), (3.5, ry, H + 0.95), 0.022, 0.022, "iron", seg=4)
    a.limb((3.5, ry, H), (3.5, ry, H + 0.95), 0.03, 0.025, "iron", seg=5)
    if prev:
        a.limb(prev, (2.9, ry, H + 0.95), 0.022, 0.022, "iron", seg=4)


def b_quay_edge(a, w=4.0):
    a.part("quay")
    R = _R(171)
    n = 4
    bw = w / n
    for i in range(n):
        x = -w / 2 + bw * (i + 0.5)
        hh = 0.28 + R.j(0.01)
        _chunk(a, (x, R.j(0.01), hh / 2), (bw - 0.03, 0.5, hh), "stone", R, jit=0.015)
        a.box((bw - 0.04, 0.44, 0.075), (x, 0.03, 0.28 + 0.03), "stone")
        a.cyl(0.07, bw - 0.05, (x, -0.18, 0.28), "stone", seg=7, rot=(0, math.pi / 2, 0))
    a.box((0.14, 0.12, 0.03), (0.7, -0.1, 0.36), "iron")
    _ring(a, (0.7, -0.15, 0.46), 0.1, 8, 0.03, "iron", plane="xz")
    a.beam((0.7, -0.15, 0.36), (0.7, -0.15, 0.4), 0.05, "iron")
    for x in (-1.5, 1.5):
        a.box((0.5, 0.03, 0.05), (x, 0.0, 0.37), "stone")


def b_boulders(a):
    a.part("boulders")
    R = _R(181)
    spec = [((0.0, 0.0), 0.85, (1.2, 1.0, 0.8)), ((0.95, 0.35), 0.55, (1.1, 1.0, 0.85)), ((-0.8, 0.5), 0.5, (1.0, 1.2, 0.8)),
            ((0.35, -0.75), 0.4, (1.2, 1.0, 0.75)), ((-0.5, -0.65), 0.28, (1.0, 1.0, 0.8))]
    for (x, y), rad, sc in spec:
        _rock(a, (x, y, rad * sc[2] * 0.6), rad, "rock", R, sc=sc, seg=8, jit=0.22, zmin=0.0)
    for i in range(3):
        _rock(a, (R.j(0.3), R.j(0.3), 0.8), 0.2, "rock", R, sc=(1.2, 1.0, 0.5), seg=6, jit=0.2)


def b_picket_fence(a, w=3.0):
    a.part("fence")
    R = _R(191)
    lean = 0.04
    posts = [-w / 2 + 0.05, 0.0, w / 2 - 0.05]
    for x in posts:
        a.box((0.09, 0.09, 1.0), (x, 0.0, 0.5), "wood", rot=(0, lean + R.j(0.015), 0))
    for z in (0.3, 0.72):
        a.beam((-w / 2, 0.05, z), (w / 2, 0.05, z + R.j(0.02) + 0.01), 0.06, "wood")
    n = 14
    for i in range(n):
        x = -w / 2 + 0.1 + (w - 0.2) * i / (n - 1)
        hh = 0.82 + R.j(0.04)
        tilt = lean + R.j(0.03)
        rz = R.j(0.02)
        zc = 0.08 + hh / 2
        a.box((0.09, 0.02, hh), (x, -0.02, zc), "wood", rot=(0, tilt, rz))
        a.cyl(0.0636, 0.1, (x + math.sin(tilt) * (hh / 2 + 0.04), -0.02, zc + hh / 2 + 0.04), "wood", r2=0.0, seg=4,
              rot=(0, tilt, math.pi / 4 + rz), smooth=False)


# --------------------------------------------------------------------------- trees
def b_oak(a, h=6.0):
    a.part("oak")
    R = _R(201)
    tp = [(0, 0, 0.0), (0.12, 0.05, 1.3), (-0.05, -0.05, 2.4), (0.05, 0.0, 3.0)]
    rs = [0.62, 0.48, 0.4, 0.32]
    for i in range(3):
        a.limb(tp[i], tp[i + 1], rs[i], rs[i + 1], "bark", seg=9, cap=(i == 2))
    for i in range(6):                       # root flare
        ang = i * 2 * math.pi / 6 + R.j(0.3)
        c, s = math.cos(ang), math.sin(ang)
        a.limb((c * 0.3, s * 0.3, 0.7), (c * R.r(0.8, 0.95), s * R.r(0.8, 0.95), 0.0), 0.3, 0.1, "bark", seg=6)
    nb = 5
    cz = h * 0.72
    for i in range(nb):
        ang = i * 2 * math.pi / nb + R.j(0.3)
        c, s = math.cos(ang), math.sin(ang)
        mid = (c * 0.5, s * 0.5, 3.4 + R.j(0.1))
        end = (c * R.r(1.2, 1.7), s * R.r(1.2, 1.7), R.r(cz - 0.5, cz + 0.2))
        a.limb((0.05, 0, 2.8), mid, 0.2, 0.15, "bark", seg=6)
        a.limb(mid, end, 0.15, 0.06, "bark", seg=6)
    n = 9
    for i in range(n):
        ang = i * 2 * math.pi / n + R.j(0.3)
        d = R.r(0.9, 1.5) if i < n - 1 else 0.2
        z = h * 0.62 + R.r(-0.2, 0.6) if i < n - 1 else h - 1.0
        rad = R.r(1.05, 1.3)
        _rock(a, (math.cos(ang) * d, math.sin(ang) * d, z), rad, "foliage", R, sc=(1, 1, 0.72), seg=10, jit=0.14, smooth=True)
    for i in range(3):
        ang = R.r(0, 6.28)
        _rock(a, (math.cos(ang) * 2.0, math.sin(ang) * 2.0, h * 0.55), 0.6, "foliage", R, sc=(1, 1, 0.7), seg=8, jit=0.15, smooth=True)


def b_yew(a, h=5.0):
    a.part("yew")
    R = _R(211)
    for k in range(2):                       # twisted trunk pair
        o = 0.1 * (1 if k == 0 else -1)
        pts = [(o, 0, 0), (-o * 1.2, 0.08, 0.5), (o * 0.7, -0.08, 1.0), (0.0, 0.05, 1.7)]
        _chain(a, pts, 0.24 if k == 0 else 0.17, 0.17 if k == 0 else 0.11, "bark", seg=7)
    for i in range(4):
        ang = i * 1.6 + 0.5
        a.limb((math.cos(ang) * 0.1, math.sin(ang) * 0.1, 0.4), (math.cos(ang) * 0.5, math.sin(ang) * 0.5, 0.0), 0.1, 0.04, "bark", seg=5)
    tiers = 7
    for i in range(tiers):
        f = i / tiers
        z = 0.7 + i * (h - 1.6) / tiers
        r1 = 1.3 * (1 - f) + 0.2
        ox, oy = R.j(0.08), R.j(0.08)
        a.cyl(r1, 1.1, (ox, oy, z + 0.55), "foliage", r2=r1 * 0.45, seg=9, rot=(R.j(0.04), R.j(0.04), R.r(0, 3)))
        if i < 5:
            for k in range(3):
                ang = R.r(0, 6.28)
                _rock(a, (ox + math.cos(ang) * r1 * 0.85, oy + math.sin(ang) * r1 * 0.85, z + 0.35), r1 * 0.38, "foliage", R,
                      sc=(1, 1, 0.65), seg=6, jit=0.15, smooth=True)
    a.cyl(0.25, h * 0.2, (0, 0, h - 0.4), "foliage", r2=0.0, seg=7)
