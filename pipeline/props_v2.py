"""Improved prop / architecture builders (override the originals in blender_gen.py).
`math` and `Asset` are injected as module globals by blender_gen._load_overrides (no bpy import here)."""


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _rng(seed):
    s = [(int(seed) * 9301 + 49297) & 0x7FFFFFFF]

    def r():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7FFFFFFF
        return (s[0] >> 8) / float(1 << 23)
    return r


def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def _add(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])


def _mul(p, k):
    return (p[0] * k, p[1] * k, p[2] * k)


def _cross(p, q):
    return (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])


def _norm(p):
    l = math.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2) or 1.0
    return (p[0] / l, p[1] / l, p[2] / l)


def loft(a, rings, mat, smooth=False, caps=True, closed=True, wrap=False):
    """Skin a list of equal-length vertex rings (tuples). Caps get their own flat verts."""
    bm = a.parts[a.cur][0]
    vr = [[bm.verts.new(p) for p in ring] for ring in rings]
    n = len(vr[0])
    allv = [v for r in vr for v in r]
    pairs = range(len(vr)) if wrap else range(len(vr) - 1)
    for i in pairs:
        r0, r1 = vr[i], vr[(i + 1) % len(vr)]
        for j in range(n if closed else n - 1):
            jn = (j + 1) % n
            try:
                bm.faces.new((r0[j], r0[jn], r1[jn], r1[j]))
            except ValueError:
                pass
    capfaces = []
    if caps and not wrap and closed:
        for ring, rev in ((rings[0], True), (rings[-1], False)):
            vs = [bm.verts.new(p) for p in ring]
            allv += vs
            try:
                capfaces.append(bm.faces.new(vs[::-1] if rev else vs))
            except ValueError:
                pass
    a._finish(allv, mat, smooth)
    for f in capfaces:
        f.smooth = False


def lathe(a, prof, mat, seg=12, c=(0, 0, 0), smooth=True, caps=True, sx=1.0, sy=1.0, rot0=0.0):
    rings = []
    for (r, z) in prof:
        r = max(r, 0.002)
        rings.append([(c[0] + r * sx * math.cos(rot0 + 2 * math.pi * k / seg),
                       c[1] + r * sy * math.sin(rot0 + 2 * math.pi * k / seg), c[2] + z) for k in range(seg)])
    loft(a, rings, mat, smooth=smooth, caps=caps)


def prism_xz(a, outline, y0, y1, mat, caps=True):
    """Extrude an (x, z) outline along Y from y0 to y1."""
    loft(a, [[(x, y0, z) for (x, z) in outline], [(x, y1, z) for (x, z) in outline]], mat, caps=caps)


def prism_xy(a, outline, z0, z1, mat, caps=True, s1=1.0):
    """Extrude an (x, y) outline along Z; top ring scaled by s1 about the origin."""
    loft(a, [[(x, y, z0) for (x, y) in outline], [(x * s1, y * s1, z1) for (x, y) in outline]], mat, caps=caps)


def tube(a, pts, radius, mat, seg=6, smooth=False, caps=True):
    """Sweep a round section along a path. radius: float, list per point, or f(t)."""
    n = len(pts)
    rings = []
    for i, p in enumerate(pts):
        t = _norm(_sub(pts[min(i + 1, n - 1)], pts[max(i - 1, 0)]))
        ref = (0, 0, 1) if abs(t[2]) < 0.95 else (1, 0, 0)
        n1 = _norm(_cross(t, ref))
        n2 = _cross(t, n1)
        if callable(radius):
            r = radius(i / max(1, n - 1))
        elif isinstance(radius, (list, tuple)):
            r = radius[i]
        else:
            r = radius
        r = max(r, 0.002)
        ring = []
        for k in range(seg):
            ang = 2 * math.pi * k / seg
            ring.append(_add(p, _add(_mul(n1, r * math.cos(ang)), _mul(n2, r * math.sin(ang)))))
        rings.append(ring)
    loft(a, rings, mat, smooth=smooth, caps=caps)


def torus(a, R, r, c, mat, axis="x", seg=16, rseg=6, smooth=True):
    rings = []
    for i in range(seg):
        th = 2 * math.pi * i / seg
        ring = []
        for j in range(rseg):
            ph = 2 * math.pi * j / rseg
            u = r * math.sin(ph)
            rad = R + r * math.cos(ph)
            p, q = rad * math.cos(th), rad * math.sin(th)
            if axis == "x":
                ring.append((c[0] + u, c[1] + p, c[2] + q))
            elif axis == "y":
                ring.append((c[0] + p, c[1] + u, c[2] + q))
            else:
                ring.append((c[0] + p, c[1] + q, c[2] + u))
        rings.append(ring)
    loft(a, rings, mat, smooth=smooth, wrap=True)


def arc(c, r, t0, t1, n, z=None):
    return [(c[0] + r * math.cos(t0 + (t1 - t0) * i / n), c[1] + r * math.sin(t0 + (t1 - t0) * i / n)) for i in range(n + 1)]


def flame(a, x, y, z, s=1.0):
    a.sphere(0.018 * s, (x, y, z), "flame", scale=(0.8, 0.8, 2.0), seg=6)


# --------------------------------------------------------------------------- #
# architecture
# --------------------------------------------------------------------------- #
def b_floor(a, w=4, d=4, t=0.2, mat="stone"):
    a.part("floor")
    a.box((w, d, t - 0.02), (0, 0, -t / 2 - 0.01), mat)
    nx, ny = max(1, round(w / 0.9)), max(1, round(d / 0.9))
    r = _rng(int(w * 10 + d))
    sw, sd = w / nx, d / ny
    for i in range(nx):
        for j in range(ny):
            dz = (r() - 0.5) * 0.012
            top = -0.004 + dz
            a.box((sw - 0.025, sd - 0.025, 0.05), ((i + 0.5) * sw - w / 2, (j + 0.5) * sd - d / 2, top - 0.025), mat)


def _bands(a, w, t, z0, z1, proud, mat, gaps=(), xext=0.0):
    segs, cur, end = [], -w / 2 - xext, w / 2 + xext
    for g0, g1 in sorted(gaps):
        if g0 > cur:
            segs.append((cur, g0))
        cur = max(cur, g1)
    if cur < end:
        segs.append((cur, end))
    for sgn in (-1, 1):
        for x0, x1 in segs:
            a.box((x1 - x0, proud + 0.01, z1 - z0), ((x0 + x1) / 2, sgn * (t / 2 + proud / 2 - 0.005), (z0 + z1) / 2), mat)


def b_wall(a, w=4, h=3, t=0.4, mat="stone", door=0.0, window=0.0):
    """Wall along X, centred on origin, base at z=0. door/window = opening width."""
    a.part("wall")
    gaps_low, gaps_hi = [], []
    dh = min(h - 0.5, 2.3)
    wy0, wy1 = 1.2, 2.4
    if door > 0:
        sw = (w - door) / 2
        a.box((sw, t, h), (-(w - sw) / 2, 0, h / 2), mat)
        a.box((sw, t, h), ((w - sw) / 2, 0, h / 2), mat)
        a.box((door, t, h - dh), (0, 0, dh + (h - dh) / 2), mat)
        gaps_low = [(-door / 2 - 0.14, door / 2 + 0.14)]
        # architrave: jambs, lintel and a small hood moulding on both faces
        for sgn in (-1, 1):
            yc = sgn * (t / 2 + 0.02)
            for sx in (-1, 1):
                a.box((0.14, 0.05, dh + 0.02), (sx * (door / 2 + 0.07), yc, (dh + 0.02) / 2), mat)
            a.box((door + 0.28, 0.06, 0.16), (0, sgn * (t / 2 + 0.025), dh + 0.1), mat)
            a.box((door + 0.40, 0.09, 0.07), (0, sgn * (t / 2 + 0.04), dh + 0.215), mat)
            a.box((0.22, 0.08, 0.12), (0, sgn * (t / 2 + 0.04), dh + 0.1), mat)   # keystone
    elif window > 0:
        sw = (w - window) / 2
        a.box((sw, t, h), (-(w - sw) / 2, 0, h / 2), mat)
        a.box((sw, t, h), ((w - sw) / 2, 0, h / 2), mat)
        a.box((window, t, wy0), (0, 0, wy0 / 2), mat)
        a.box((window, t, h - wy1), (0, 0, wy1 + (h - wy1) / 2), mat)
        zc, wh = (wy0 + wy1) / 2, wy1 - wy0
        # timber frame inside the reveal
        for sx in (-1, 1):
            a.box((0.06, 0.12, wh), (sx * (window / 2 - 0.03), 0, zc), "wood")
        a.box((window, 0.12, 0.06), (0, 0, wy0 + 0.03), "wood")
        a.box((window, 0.12, 0.06), (0, 0, wy1 - 0.03), "wood")
        a.box((window, 0.02, wh), (0, 0, zc), "glass")
        # mullion + transom, leading
        a.box((0.06, 0.1, wh), (0, 0, zc), "wood")
        a.box((window, 0.08, 0.05), (0, 0, wy0 + wh * 0.62), "wood")
        for i in (1, 2):
            a.box((0.012, 0.035, wh), (-window / 2 + window * i / 3, 0, zc), "iron")
        for i in (1, 2, 3):
            a.box((window, 0.035, 0.012), (0, 0, wy0 + wh * i / 4), "iron")
        for sgn in (-1, 1):
            yc = sgn * (t / 2 + 0.03)
            # stone sill and head hood
            a.box((window + 0.3, 0.14, 0.07), (0, sgn * (t / 2 + 0.05), wy0 - 0.035), mat)
            a.box((window + 0.2, 0.08, 0.05), (0, sgn * (t / 2 + 0.02), wy0 - 0.095), mat)
            for sx in (-1, 1):
                a.box((0.1, 0.05, wh + 0.08), (sx * (window / 2 + 0.05), yc - sgn * 0.005, zc), mat)
            a.box((window + 0.3, 0.07, 0.1), (0, sgn * (t / 2 + 0.03), wy1 + 0.05), mat)
            a.box((window + 0.4, 0.1, 0.06), (0, sgn * (t / 2 + 0.045), wy1 + 0.13), mat)
        gaps_low = []
    else:
        a.box((w, t, h), (0, 0, h / 2), mat)
    gaps_hi = []
    # skirting (stepped plinth), dado rail, picture rail
    _bands(a, w, t, 0.0, 0.22, 0.06, mat, gaps_low)
    _bands(a, w, t, 0.22, 0.30, 0.04, mat, gaps_low)
    _bands(a, w, t, 0.98, 1.04, 0.035, mat, gaps_low)
    if h > 2.4:
        pz = h - 0.52
        if door > 0 and pz < dh + 0.3:
            gaps_hi = [(-door / 2 - 0.2, door / 2 + 0.2)]
        _bands(a, w, t, pz, pz + 0.05, 0.03, mat, gaps_hi)
    # cornice: stepped crown moulding + corbels
    _bands(a, w, t, h - 0.2, h - 0.12, 0.03, mat, xext=0.0)
    _bands(a, w, t, h - 0.12, h - 0.05, 0.05, mat, xext=0.0)
    a.box((w + 0.05, t + 0.14, 0.05), (0, 0, h - 0.025), mat)
    n = max(2, round(w / 1.0))
    skip = []
    if door > 0:
        skip = [(-door / 2 - 0.1, door / 2 + 0.1)]
    for i in range(n):
        x = -w / 2 + (i + 0.5) * w / n
        if any(s0 < x < s1 for s0, s1 in skip):
            continue
        for sgn in (-1, 1):
            a.box((0.13, 0.05, 0.16), (x, sgn * (t / 2 + 0.025), h - 0.28), mat)
            a.box((0.09, 0.04, 0.06), (x, sgn * (t / 2 + 0.02), h - 0.39), mat)


def _wedge(a, cx, cz, r0, r1, t0, t1, y0, y1, mat, m=1):
    p = []
    for (r, t) in ((r0, t0), (r1, t0), (r1, t1), (r0, t1)):
        p.append((m * (cx + r * math.cos(t)), cz + r * math.sin(t)))
    loft(a, [[(x, y0, z) for (x, z) in p], [(x, y1, z) for (x, z) in p]], mat)


def b_arch(a, w=2.0, h=3.2, depth=0.6):
    a.part("arch")
    pw = 0.45
    ph = h - w / 2
    hw = w / 2
    e = 0.12
    ri = hw + e
    ro = ri + pw
    # piers with plinth, impost and chamfered edges
    for sx in (-1, 1):
        xc = sx * (hw + pw / 2)
        a.box((pw, depth, ph - 0.2), (xc, 0, 0.2 + (ph - 0.2) / 2), "stone")
        a.box((pw + 0.1, depth + 0.1, 0.2), (xc, 0, 0.1), "stone")
        a.box((pw + 0.04, depth + 0.04, 0.08), (xc, 0, 0.22), "stone")
        a.box((pw + 0.12, depth + 0.08, 0.14), (xc, 0, ph - 0.07), "stone")
        a.box((pw + 0.06, depth + 0.04, 0.06), (xc, 0, ph - 0.17), "stone")
        for sy in (-1, 1):                       # engaged shaft on each face
            a.cyl(0.08, ph - 0.5, (xc - sx * 0.08, sy * (depth / 2 + 0.03), 0.3 + (ph - 0.5) / 2), "stone", seg=8)
    n = 6
    ta = math.acos(e / ri)
    for m in (-1, 1):
        for i in range(n):
            t0, t1 = ta * i / n, ta * (i + 1) / n
            d = depth * (1.0 if i % 2 == 0 else 0.9)
            _wedge(a, -e, ph, ri, ro, t0, t1 + 0.002, -d / 2, d / 2, "stone", m)
            # hood moulding on both faces
            for sy in (-1, 1):
                y0, y1 = sy * depth / 2, sy * (depth / 2 + 0.05)
                _wedge(a, -e, ph, ro - 0.04, ro + 0.07, t0, t1 + 0.002, min(y0, y1), max(y0, y1), "stone", m)
    za = ph + math.sqrt(ri ** 2 - e ** 2)
    zb = ph + math.sqrt(ro ** 2 - e ** 2)
    a.box((0.2, depth + 0.1, zb - za + 0.1), (0, 0, (za + zb) / 2 + 0.04), "stone")
    a.box((0.3, depth + 0.06, 0.1), (0, 0, zb + 0.14), "stone")


def b_column(a, h=3.0, r=0.3):
    a.part("column")
    ph = 0.14
    cap = 0.42
    a.box((r * 3.0, r * 3.0, ph), (0, 0, ph / 2), "stone")
    lathe(a, [(r * 1.55, ph), (r * 1.5, ph + 0.05), (r * 1.3, ph + 0.1), (r * 1.34, ph + 0.15), (r * 1.1, ph + 0.2),
              (r * 1.02, ph + 0.24)], "stone", seg=16)
    zs0, zs1 = ph + 0.24, h - cap
    fl = 12
    rings = []
    for k, tt in enumerate((0.0, 0.25, 0.6, 1.0)):
        rr = r * (1.0 - 0.12 * tt) * (1.0 + 0.03 * math.sin(math.pi * tt))
        z = zs0 + (zs1 - zs0) * tt
        rings.append([(rr * (1.0 if j % 2 == 0 else 0.9) * math.cos(math.pi * j / fl),
                       rr * (1.0 if j % 2 == 0 else 0.9) * math.sin(math.pi * j / fl), z) for j in range(2 * fl)])
    loft(a, rings, "stone", caps=False)
    rt = r * 0.88
    lathe(a, [(rt * 1.02, zs1 - 0.01), (rt * 1.18, zs1 + 0.04), (rt * 1.18, zs1 + 0.08), (rt * 1.0, zs1 + 0.1),
              (rt * 1.3, h - 0.3), (r * 1.55, h - 0.16), (r * 1.6, h - 0.12)], "stone", seg=16)
    a.box((r * 3.3, r * 3.3, 0.12), (0, 0, h - 0.06), "stone")
    a.box((r * 3.0, r * 3.0, 0.04), (0, 0, h - 0.14), "stone")


def b_stairs(a, steps=6, w=1.6, rise=0.2, run=0.35):
    a.part("stairs")
    for i in range(steps):
        yf = i * run - run / 2
        top = rise * (i + 1)
        a.box((w - 0.16, run, top - 0.04), (0, i * run, (top - 0.04) / 2), "stone")
        a.box((w - 0.12, run + 0.05, 0.05), (0, i * run - 0.025, top - 0.025), "stone")       # nosing
        a.box((w - 0.14, 0.02, 0.03), (0, yf - 0.03, top - 0.065), "stone")                      # shadow line under nosing
    y0, y1 = -run / 2, steps * run - run / 2
    zt = rise * steps
    for sx in (-1, 1):
        xc = sx * (w / 2 - 0.06)
        loft(a, [[(xc - 0.06, y0 - 0.05, 0.0), (xc - 0.06, y1, 0.0), (xc - 0.06, y1, zt + 0.12), (xc - 0.06, y0 - 0.05, 0.14)],
                 [(xc + 0.06, y0 - 0.05, 0.0), (xc + 0.06, y1, 0.0), (xc + 0.06, y1, zt + 0.12), (xc + 0.06, y0 - 0.05, 0.14)]], "stone")
        a.box((0.16, 0.16, 0.14), (xc, y1 - 0.06, zt + 0.12), "stone")
        a.box((0.2, 0.2, 0.06), (xc, y0 + 0.05, 0.1), "stone")


# --------------------------------------------------------------------------- #
# furniture
# --------------------------------------------------------------------------- #
def _turned_leg(a, x, y, lh, r, mat="wood", seg=8, block=0.1):
    p = [(0.8, 0), (1.0, 0.03), (0.68, 0.08), (0.74, 0.2), (1.18, 0.29), (0.8, 0.39), (0.78, 0.6), (1.0, 0.69),
         (0.74, 0.76), (0.95, 0.84)]
    zt = lh - block
    lathe(a, [(r * k, zt * z) for k, z in p] + [(r * 0.95, zt)], mat, seg=seg, c=(x, y, 0))
    a.box((r * 2.1, r * 2.1, block), (x, y, lh - block / 2), mat)


def b_door(a, w=1.1, h=2.2, t=0.1, style="plank"):
    a.part("door", pivot=(-w / 2, 0, 0))
    st, rl = 0.1, 0.13
    inner = w - 2 * st
    # frame
    for sx in (-1, 1):
        a.box((st, t, h), (sx * (w / 2 - st / 2), 0, h / 2), "wood")
    for z in (rl / 2, h - rl / 2):
        a.box((inner, t, rl), (0, 0, z), "wood")
    a.box((inner, t, 0.1), (0, 0, h * 0.5), "wood")
    # vertical planks
    n = max(3, round(inner / 0.2))
    pw = inner / n
    for zc, zh in ((rl + (h * 0.5 - 0.05 - rl) / 2, h * 0.5 - 0.05 - rl), (h * 0.5 + 0.05 + (h - rl - h * 0.5 - 0.05) / 2, h - rl - h * 0.5 - 0.05)):
        for i in range(n):
            a.box((pw - 0.012, t - 0.03, zh - 0.01), (-inner / 2 + pw * (i + 0.5), 0, zc), "wood")
    for sgn in (-1, 1):
        yo = sgn * (t / 2 + 0.01)
        for z in (0.36, h - 0.36):
            a.box((w * 0.72, 0.02, 0.085), (-w / 2 + w * 0.36, yo, z), "iron")
            a.box((0.12, 0.02, 0.15), (-w / 2 + w * 0.72 + 0.05, yo, z), "iron", rot=(0, 0, 0))
            a.cyl(0.03, 0.14, (-w / 2 + 0.03, sgn * (t / 2 + 0.02), z), "iron", seg=6)
            for k in range(5):
                a.cyl(0.014, 0.016, (-w / 2 + 0.1 + k * (w * 0.13), sgn * (t / 2 + 0.025), z), "iron", seg=6, rot=(math.pi / 2, 0, 0))
        hx, hz = w / 2 - 0.17, h * 0.47
        a.cyl(0.05, 0.012, (hx, sgn * (t / 2 + 0.012), hz), "iron", seg=10, rot=(math.pi / 2, 0, 0))
        torus(a, 0.045, 0.01, (hx, sgn * (t / 2 + 0.04), hz - 0.035), "iron", axis="y", seg=12, rseg=4)
        a.sphere(0.02, (hx, sgn * (t / 2 + 0.03), hz + 0.02), "iron", seg=6)
        a.box((0.03, 0.012, 0.07), (hx, sgn * (t / 2 + 0.012), hz - 0.12), "iron")


def b_table(a, w=1.8, d=0.9, h=0.8):
    a.part("table")
    a.box((w, d, 0.05), (0, 0, h - 0.025), "wood")
    a.box((w - 0.04, d - 0.04, 0.03), (0, 0, h - 0.065), "wood")
    lx, ly = w / 2 - 0.12, d / 2 - 0.12
    ah = 0.11
    for sy in (-1, 1):
        a.box((2 * lx, 0.03, ah), (0, sy * ly, h - 0.08 - ah / 2 + 0.02), "wood")
    for sx in (-1, 1):
        a.box((0.03, 2 * ly, ah), (sx * lx, 0, h - 0.08 - ah / 2 + 0.02), "wood")
    xs = [-lx, lx] + ([0.0] if w > 3.0 else [])
    for x in xs:
        for sy in (-1, 1):
            _turned_leg(a, x, sy * ly, h - 0.08, 0.04 if w < 3 else 0.055)
    zst = 0.2
    for sy in (-1, 1):
        a.cyl(0.018, 2 * lx, (0, sy * ly, zst), "wood", seg=6, rot=(0, math.pi / 2, 0))
    for x in xs:
        a.cyl(0.018, 2 * ly, (x, 0, zst), "wood", seg=6, rot=(math.pi / 2, 0, 0))
    if w > 3.0:
        a.cyl(0.02, 2 * lx, (0, 0, zst + 0.01), "wood", seg=6, rot=(0, math.pi / 2, 0))


def b_chair(a, h=0.9, seat=0.48, hist="wood"):
    a.part("chair")
    # seat frame + cushion
    a.box((0.46, 0.44, 0.045), (0, 0, seat - 0.02), "wood")
    a.box((0.4, 0.38, 0.03), (0, -0.005, seat + 0.015), "cloth")
    a.sphere(0.21, (0, -0.005, seat + 0.03), "cloth", scale=(0.95, 0.9, 0.22), seg=10)
    for sx in (-1, 1):
        _turned_leg(a, sx * 0.2, -0.19, seat - 0.04, 0.026, block=0.05)
        a.beam((sx * 0.2, 0.19, 0.0), (sx * 0.2, 0.235, h), 0.04, "wood")
        for z, y in ((0.16, 0), ):
            a.cyl(0.012, 0.4, (sx * 0.2, 0, z), "wood", seg=5, rot=(math.pi / 2, 0, 0))
        a.sphere(0.03, (sx * 0.2, 0.236, h + 0.02), "wood", seg=6)
    a.cyl(0.012, 0.4, (0, -0.19, 0.16), "wood", seg=5, rot=(0, math.pi / 2, 0))
    a.cyl(0.012, 0.4, (0, 0.19, 0.16), "wood", seg=5, rot=(0, math.pi / 2, 0))
    # curved top rail
    pts = []
    for i in range(7):
        x = -0.2 + 0.4 * i / 6
        pts.append((x, 0.236 + 0.02 * (1 - (x / 0.2) ** 2) * 0 , h - 0.04 + 0.03 * (1 - (x / 0.2) ** 2)))
    tube(a, pts, 0.028, "wood", seg=6)
    # splats + padded panel
    a.box((0.34, 0.025, 0.2), (0, 0.228, seat + 0.22), "cloth")
    a.sphere(0.17, (0, 0.215, seat + 0.22), "cloth", scale=(1.0, 0.16, 0.65), seg=10)
    for x in (-0.1, 0, 0.1):
        a.box((0.025, 0.02, h - seat - 0.4), (x, 0.232, seat + 0.35 + (h - seat - 0.4) / 2 - 0.02), "wood")


def b_bed(a, w=1.4, l=2.1, posts=True):
    a.part("bed")
    hw, hl = w / 2, l / 2
    # base frame, side rails with moulding
    a.box((w, l, 0.3), (0, 0, 0.3), "wood")
    a.box((w + 0.06, l - 0.04, 0.05), (0, 0, 0.465), "wood")
    for sx in (-1, 1):
        for y in (-hl + 0.15, hl - 0.15):
            a.box((0.1, 0.1, 0.16), (sx * (hw - 0.05), y, 0.08), "wood")
    # mattress, rolled edges, sheet, blanket, pillows
    a.box((w - 0.1, l - 0.16, 0.18), (0, 0.0, 0.58), "linen")
    for sx in (-1, 1):
        a.cyl(0.05, l - 0.2, (sx * (hw - 0.07), 0, 0.66), "linen", seg=8, rot=(math.pi / 2, 0, 0))
    a.box((w - 0.14, 0.62 * l, 0.05), (0, -0.2, 0.69), "cloth")
    for sx in (-1, 1):
        a.box((0.03, 0.62 * l - 0.04, 0.2), (sx * (hw - 0.05), -0.2, 0.6), "cloth")
    a.box((w - 0.14, 0.03, 0.2), (0, -0.2 - 0.31 * l, 0.6), "cloth")
    a.cyl(0.05, w - 0.16, (0, -0.2 + 0.31 * l, 0.72), "linen", seg=8, rot=(0, math.pi / 2, 0))     # folded-back sheet
    rg = _rng(5)
    for k in range(3):
        a.box((w - 0.16, 0.05, 0.015), (0, -0.2 - 0.2 * k + 0.05, 0.725), "cloth")                # fold ridges
    for sx in ((-1, 1) if w > 1.0 else (0,)):
        a.sphere(0.23, (sx * (hw * 0.45), hl - 0.35, 0.78), "linen", scale=(0.9 if w > 1 else 1.0, 1.0, 0.38), seg=10)
    # headboard (high, shaped) and footboard
    def board(zlo, zhi, bump):
        out = [(-hw, zlo), (hw, zlo), (hw, zhi)]
        for i in range(1, 8):
            x = hw - w * i / 8
            out.append((x, zhi + bump * (1 - (x / hw) ** 2) ** 0.7))
        out.append((-hw, zhi))
        return out
    prism_xz(a, board(0.12, 1.1, 0.28), hl - 0.1, hl, "wood")
    prism_xz(a, board(0.12, 0.72, 0.1), -hl, -hl + 0.08, "wood")
    a.box((w - 0.3, 0.02, 0.5), (0, hl - 0.11, 0.78), "wood")        # raised panel on headboard
    if posts:
        for sx in (-1, 1):
            for sy, top in ((1, 2.1), (-1, 2.1)):
                lathe(a, [(0.065, 0.0), (0.075, 0.05), (0.05, 0.12), (0.05, 0.6), (0.075, 0.7), (0.055, 0.8), (0.04, 0.85),
                          (0.04, 1.45), (0.06, 1.55), (0.04, 1.65), (0.04, top - 0.18), (0.065, top - 0.1), (0.04, top - 0.02), (0.02, top)],
                      "wood", seg=8, c=(sx * hw, sy * hl, 0))
        # canopy: frame, cloth top, valance, drapes
        for sy in (-1, 1):
            a.box((w + 0.1, 0.06, 0.06), (0, sy * hl, 2.06), "wood")
        for sx in (-1, 1):
            a.box((0.06, l + 0.1, 0.06), (sx * hw, 0, 2.06), "wood")
        a.box((w + 0.06, l + 0.06, 0.03), (0, 0, 2.11), "cloth")
        for sy in (-1, 1):
            n = 7
            for i in range(n):
                a.box((w / n - 0.005, 0.02, 0.2 + 0.04 * (i % 2)), (-hw + (i + 0.5) * w / n, sy * (hl + 0.04), 1.95 - 0.02 * (i % 2)), "cloth")
        for sx in (-1, 1):
            n = 8
            for i in range(n):
                a.box((0.02, l / n - 0.005, 0.2 + 0.04 * (i % 2)), (sx * (hw + 0.04), -hl + (i + 0.5) * l / n, 1.95 - 0.02 * (i % 2)), "cloth")
        for sx in (-1, 1):                                             # tied-back curtains at the head
            for k in range(3):
                y = hl - 0.1 - k * 0.07
                a.box((0.025, 0.06, 1.0 - 0.1 * k), (sx * (hw + 0.035), y, 1.55 - 0.05 * k + 0.0), "cloth")
            a.box((0.04, 0.3, 0.05), (sx * (hw + 0.04), hl - 0.17, 1.1), "cloth")


def b_chest(a, w=1.0, d=0.55, h=0.5):
    a.part("chest")
    bh = h * 0.6
    a.box((w + 0.04, d + 0.04, 0.05), (0, 0, 0.025), "wood")
    a.box((w, d, bh - 0.05), (0, 0, 0.05 + (bh - 0.05) / 2), "wood")
    for sx in (-1, 1):
        x = sx * (w / 2 - 0.09)
        a.box((0.06, d + 0.03, bh), (x, 0, bh / 2), "iron")
        a.box((0.075, 0.03, 0.05), (x, -d / 2 - 0.01, bh - 0.02), "iron")
    a.box((w + 0.02, d + 0.02, 0.04), (0, 0, bh - 0.02), "wood")
    for z in (0.12,):
        a.box((w + 0.02, 0.012, 0.03), (0, -d / 2 - 0.004, z), "iron")
    a.box((0.12, 0.03, 0.14), (0, -d / 2 - 0.01, bh - 0.08), "gold")
    a.box((0.04, 0.032, 0.05), (0, -d / 2 - 0.012, bh - 0.09), "iron")
    # lid: half-round with iron straps, hinged at the back edge
    a.part("lid", pivot=(0, d / 2, bh))
    R = d / 2 + 0.01
    rr = lambda r_: [(r_ * math.cos(math.pi * i / 10), r_ * math.sin(math.pi * i / 10) * 0.8) for i in range(11)]
    arcp = rr(R)
    prism_yz = lambda pts, x0, x1, m: loft(a, [[(x0, y, bh + z) for (y, z) in pts], [(x1, y, bh + z) for (y, z) in pts]], m)
    prism_yz(arcp, -w / 2, w / 2, "wood")
    for sx in (-1, 1):
        x = sx * (w / 2 - 0.09)
        prism_yz(rr(R + 0.012), x - 0.03, x + 0.03, "iron")
        prism_yz(rr(R + 0.012), sx * (w / 2) - 0.012, sx * (w / 2) + 0.012, "wood") if False else None
    prism_yz(rr(R + 0.008), -0.001, 0.001, "iron") if False else None
    a.box((0.1, 0.04, 0.04), (0, -R - 0.005, bh + 0.045), "gold")


def b_barrel(a, r=0.35, h=0.9):
    a.part("barrel")
    n = 12
    zs = [0.0, 0.12, 0.3, 0.5, 0.7, 0.88, 1.0]
    rad = lambda t: r * (0.84 + 0.16 * math.sin(math.pi * t))
    rings = []
    for t in zs:
        rr = rad(t)
        rings.append([(rr * math.cos(2 * math.pi * k / n + 0.13), rr * math.sin(2 * math.pi * k / n + 0.13), t * h) for k in range(n)])
    loft(a, rings, "wood", smooth=False)
    a.cyl(r * 0.8, 0.03, (0, 0, h - 0.015 - 0.01), "wood", seg=n)
    lathe(a, [(r * 0.84, 0.0), (r * 0.84, 0.02), (r * 0.78, 0.03)], "wood", seg=n)
    for t in (0.07, 0.24, 0.76, 0.93):
        rr = rad(t) * 1.012 + 0.006
        a.cyl(rr, 0.045, (0, 0, t * h), "iron", seg=n + 4, smooth=False)
    a.cyl(r * 0.86, 0.025, (0, 0, h), "wood", seg=n)
    a.cyl(0.03, 0.04, (r * 0.45, 0.1, h + 0.02), "wood", seg=6)          # bung


def b_bookshelf(a, w=1.6, h=2.2, d=0.4):
    a.part("bookshelf")
    for sx in (-1, 1):
        a.box((0.05, d, h - 0.06), (sx * (w / 2 - 0.025), 0, (h - 0.06) / 2 + 0.0), "wood")
    a.box((w, 0.03, h - 0.06), (0, d / 2 - 0.015, (h - 0.06) / 2), "wood")
    a.box((w + 0.04, d + 0.02, 0.1), (0, 0, 0.05), "wood")             # plinth
    a.box((w + 0.02, 0.025, 0.06), (0, -d / 2 - 0.02, 0.1), "wood")
    n = 5
    top = h - 0.08
    pitch = (top - 0.1) / n
    shelves = [0.1 + i * pitch for i in range(n)]
    for z in shelves[1:]:
        a.box((w - 0.1, d - 0.03, 0.035), (0, -0.01, z), "wood")
    # crown moulding
    a.box((w + 0.08, d + 0.08, 0.04), (0, 0, h - 0.02), "wood")
    a.box((w + 0.03, d + 0.03, 0.05), (0, 0, h - 0.065), "wood")
    a.box((w + 0.0, 0.04, 0.03), (0, -d / 2 - 0.02, h - 0.1), "wood")
    a.box((w - 0.1, d - 0.03, 0.035), (0, -0.01, top - 0.01), "wood") if False else None
    r = _rng(11)
    for i in range(n):
        z0 = shelves[i] + 0.02 if i else 0.12
        room = (shelves[i + 1] - 0.02 if i < n - 1 else h - 0.1) - z0 - 0.02
        x = -w / 2 + 0.08
        k = 0
        lim = w / 2 - 0.09
        while x < lim:
            if r() < 0.1 and k > 2:
                x += 0.08 + r() * 0.08                      # gap
                continue
            bw = 0.03 + r() * 0.035
            bh = min(room - 0.02, 0.2 + r() * 0.17)
            bd = d - 0.1 - r() * 0.05
            if x + bw > lim:
                break
            lean = 0.0
            if r() < 0.12 and k > 1:
                lean = 0.18 + r() * 0.15
            mat = "leather" if r() < 0.55 else "cloth"
            if lean > 0 and x + bw + bh * 0.25 < lim:
                a.box((bw, bd, bh), (x + bw / 2 + bh * 0.09, 0.0, z0 + bh / 2), mat, rot=(0, lean, 0))
                x += bw + bh * 0.22
            else:
                a.box((bw, bd, bh), (x + bw / 2, 0.0, z0 + bh / 2), mat)
                if r() < 0.6:
                    for bz in (0.2, 0.78):
                        a.box((bw + 0.004, 0.012, 0.012), (x + bw / 2, -bd / 2 - 0.002, z0 + bh * bz), "wood" if mat == "cloth" else "cloth")
                x += bw + 0.003
            k += 1
        if i in (1, 3):                                      # flat-stacked books at the end
            for s in range(2):
                a.box((0.2 + r() * 0.04, 0.26, 0.04), (w / 2 - 0.2, 0.0, z0 + 0.02 + 0.045 * s), "leather" if s else "cloth", rot=(0, 0, (r() - 0.5) * 0.3))


# --------------------------------------------------------------------------- #
# funerary
# --------------------------------------------------------------------------- #
def _scale_xy(pts, sx, sy):
    return [(x * sx, y * sy) for x, y in pts]


def b_coffin(a, open_lid=False):
    a.part("coffin")
    L, W, H = 2.1, 0.8, 0.6
    hl = L / 2
    outer = [(-0.25, -hl), (0.25, -hl), (0.4, -hl + 0.55), (0.2, hl), (-0.2, hl), (-0.4, -hl + 0.55)]
    # hexagon is walked so the head end is -Y; build the open box from outer/inner rings
    inner = [(x * 0.86, y * 0.97 + (0.02 if y < 0 else -0.02)) for x, y in outer]
    prism_xy(a, outer, 0.0, 0.06, "wood")
    loft(a, [[(x, y, 0.06) for x, y in outer], [(x * 1.03, y * 1.0, H * 0.5) for x, y in outer],
             [(x * 1.0, y, H) for x, y in outer]], "wood", caps=False)
    loft(a, [[(x, y, H) for x, y in inner], [(x * 1.0, y, 0.12) for x, y in inner]], "wood", caps=False)
    loft(a, [[(x, y, H) for x, y in outer], [(x, y, H) for x, y in inner]], "wood", caps=False)
    prism_xy(a, _scale_xy(inner, 0.97, 0.99), 0.1, 0.14, "earth")
    a.part("lid", pivot=(0, -L / 2, H))
    ol = [(x * 1.06, y * 1.015) for x, y in outer]
    loft(a, [[(x, y, H) for x, y in ol], [(x, y, H + 0.035) for x, y in ol],
             [(x * 0.9, y * 0.97, H + 0.075) for x, y in ol], [(x * 0.62, y * 0.9, H + 0.115) for x, y in ol]], "wood")
    zt = H + 0.115
    a.box((0.045, 0.62, 0.012), (0, -0.2 + 0.12, zt + 0.006), "gold")                       # cross emblem
    a.box((0.28, 0.045, 0.012), (0, -0.5 + 0.12 + 0.1, zt + 0.006), "gold")
    for s in (-1, 1):
        for y in (-0.5, 0.0, 0.55):
            xe = 0.4 - 0.2 * (y + hl - 0.55) / (L - 0.55) * (1 if y > -hl + 0.55 else 0) if y > -hl + 0.55 else 0.4
            a.box((0.03, 0.12, 0.03), (s * (xe + 0.05) * 1.0, y, H - 0.1), "gold")             # side handles
    for p in ol:
        a.sphere(0.022, (p[0] * 0.99, p[1] * 0.99, H + 0.035), "gold", seg=6)


def b_tomb(a):
    a.part("tomb")
    a.box((1.7, 2.9, 0.12), (0, 0, 0.06), "stone")
    a.box((1.5, 2.7, 0.1), (0, 0, 0.17), "stone")
    a.box((1.4, 2.6, 0.5), (0, 0, 0.47), "stone")
    # arched panels on the long sides
    for sx in (-1, 1):
        for i in range(3):
            y = -0.85 + i * 0.85
            a.box((0.04, 0.55, 0.26), (sx * 0.71, y, 0.4), "stone")
            a.box((0.04, 0.4, 0.08), (sx * 0.71, y, 0.57), "stone")
    for sy in (-1, 1):
        a.box((0.7, 0.04, 0.3), (0, sy * 1.31, 0.45), "stone")
    # cornice + lid with chamfer
    a.box((1.62, 2.82, 0.07), (0, 0, 0.745), "stone")
    loft(a, [[(-0.8 * x, 1.4 * y, 0.78) for x, y in ((1, 1), (1, -1), (-1, -1), (-1, 1))],
             [(-0.8 * x * 0.92, 1.4 * y * 0.96, 0.9) for x, y in ((1, 1), (1, -1), (-1, -1), (-1, 1))]], "stone")
    # recumbent effigy
    a.sphere(0.2, (0, -0.25 + 0.55, 0.96), "stone", scale=(1.0, 2.6, 0.45), seg=10)
    a.sphere(0.12, (0, -0.95, 0.99), "stone", scale=(1.0, 1.1, 0.8), seg=8)
    a.box((0.34, 0.12, 0.05), (0, -0.62, 0.95), "stone")
    for sx in (-1, 1):
        a.cyl(0.04, 0.4, (sx * 0.12, -0.3, 0.97), "stone", seg=6, rot=(math.pi / 2, 0, 0))
    a.sphere(0.07, (0, -0.35, 0.98), "stone", scale=(1.3, 1, 0.5), seg=6)
    # head-end plinth and cross
    a.box((0.9, 0.3, 0.14), (0, -1.28, 0.93), "stone") if False else None
    a.box((0.8, 0.22, 0.34), (0, -1.12, 0.96), "stone") if False else None
    a.box((0.7, 0.24, 0.12), (0, -1.15, 0.9), "stone")
    a.box((0.5, 0.2, 0.14), (0, -1.15, 1.03), "stone")
    a.box((0.13, 0.15, 0.85), (0, -1.15, 1.55), "stone")
    a.box((0.52, 0.15, 0.12), (0, -1.15, 1.75), "stone")
    for (x, z, sx, sz) in ((0, 1.99, 0.17, 0.12), (-0.28, 1.75, 0.12, 0.16), (0.28, 1.75, 0.12, 0.16)):
        a.box((sx, 0.15, sz), (x, -1.15, z), "stone")


def _stone_outline(w, hs, style, r, seg=8, jit=0.0):
    """Outline (x, z) of a gravestone slab of half-width w/2 with top shape."""
    hw = w / 2
    pts = [(-hw, 0.0), (hw, 0.0)]
    if style == "round":
        zs = hs - hw * 0.9
        pts += [(hw, zs)]
        for i in range(1, seg):
            t = math.pi * i / seg
            pts.append((hw * math.cos(t), zs + hw * 0.9 * math.sin(t) + (r() - 0.5) * jit))
        pts += [(-hw, zs)]
    else:
        zs = hs - hw * 1.25
        pts += [(hw, zs), (hw * 0.78, zs + hw * 0.55), (hw * 0.38, zs + hw * 1.0), (0.0, hs),
                (-hw * 0.38, zs + hw * 1.0), (-hw * 0.78, zs + hw * 0.55), (-hw, zs)]
    return pts


def b_gravestone(a, h=1.1, w=0.6, style="round", lean=0.0):
    a.part("gravestone")
    r = _rng(int(h * 100 + w * 10) + (3 if style == "round" else 8))
    # base plinth, stepped
    a.box((w * 1.45, 0.42, 0.1), (0, 0, 0.05), "stone")
    a.box((w * 1.2, 0.32, 0.1), (0, 0, 0.15), "stone")
    tz = 0.2
    out = _stone_outline(w, h - tz, style, r, jit=0.02)
    out = [(x, z + tz) for x, z in out]
    prism_xz(a, out, -0.075, 0.075, "stone")
    # raised front panel
    inn = [(x * 0.84, tz + 0.05 + (z - tz) * 0.9 - (0.0)) for x, z in out]
    prism_xz(a, inn, -0.088, -0.07, "stone")
    # cross emblem
    zc = h - 0.3 - (0.05 if style != "round" else 0.0)
    a.box((0.035, 0.016, 0.22), (0, -0.092, zc), "stone")
    a.box((0.14, 0.016, 0.035), (0, -0.092, zc + 0.04), "stone")
    # rubble/chip at the foot
    a.sphere(0.07, (w * 0.4, -0.12, 0.2), "stone", scale=(1.2, 1, 0.5), seg=6)
    a.box((w * 0.5, 0.012, 0.012), (0, -0.09, tz + 0.2), "stone")
    a.box((w * 0.4, 0.012, 0.012), (0, -0.09, tz + 0.26), "stone")


def b_grave_cross(a, h=1.5):
    a.part("grave_cross")
    a.box((0.46, 0.44, 0.1), (0, 0, 0.05), "stone")
    a.box((0.34, 0.32, 0.1), (0, 0, 0.15), "stone")
    a.box((0.24, 0.22, 0.12), (0, 0, 0.26), "stone")
    z0 = 0.32
    loft(a, [[(-0.1, -0.1, z0), (0.1, -0.1, z0), (0.1, 0.1, z0), (-0.1, 0.1, z0)],
             [(-0.07, -0.07, z0 + h * 0.4), (0.07, -0.07, z0 + h * 0.4), (0.07, 0.07, z0 + h * 0.4), (-0.07, 0.07, z0 + h * 0.4)],
             [(-0.065, -0.065, z0 + h), (0.065, -0.065, z0 + h), (0.065, 0.065, z0 + h), (-0.065, 0.065, z0 + h)]], "stone")
    za = z0 + h * 0.7
    aw = h * 0.5
    a.box((aw, 0.13, 0.12), (0, 0, za), "stone")
    for sx in (-1, 1):
        a.box((0.12, 0.15, 0.2), (sx * (aw / 2 - 0.02), 0, za), "stone")
    a.box((0.2, 0.15, 0.2), (0, 0, z0 + h + 0.04), "stone")
    a.box((0.13, 0.15, 0.12), (0, 0, z0 + h + 0.15), "stone")
    a.box((0.2, 0.15, 0.04), (0, 0, za), "stone")
    a.cyl(0.11, 0.05, (0, -0.07, za), "stone", seg=10, rot=(math.pi / 2, 0, 0))


def b_crucifix(a, h=0.5):
    a.part("crucifix")
    s = h / 0.5
    t = 0.03
    a.box((0.055 * s ** 0.6, t, h), (0, 0, h / 2), "wood")
    a.box((h * 0.55, t, 0.05 * s ** 0.6), (0, 0, h * 0.7), "wood")
    for sx in (-1, 1):
        a.box((0.075 * s ** 0.5, t, 0.075 * s ** 0.5), (sx * h * 0.275, 0, h * 0.7), "wood")
    a.box((0.075 * s ** 0.5, t, 0.075 * s ** 0.5), (0, 0, h), "wood")
    a.box((0.07 * s ** 0.5, t, 0.07 * s ** 0.5), (0, 0, 0.02), "wood")
    a.box((0.12 * s, 0.01, 0.025 * s), (0, -t / 2 - 0.004, h * 0.9), "gold")     # INRI plate
    # gold corpus
    y = -t / 2 - 0.015 * s
    a.sphere(0.022 * s, (0, y, h * 0.76), "gold", seg=8)
    a.box((0.04 * s, 0.018 * s, 0.17 * s), (0, y, h * 0.62), "gold")
    a.box((h * 0.48, 0.012 * s, 0.015 * s), (0, y, h * 0.69), "gold")
    a.box((0.03 * s, 0.014 * s, 0.1 * s), (-0.006 * s, y, h * 0.4), "gold", rot=(0, 0.07, 0))
    a.box((0.03 * s, 0.014 * s, 0.1 * s), (0.012 * s, y, h * 0.4), "gold", rot=(0, -0.07, 0))


# --------------------------------------------------------------------------- #
# light, small items
# --------------------------------------------------------------------------- #
def b_candle(a, h=0.18):
    a.part("candle")
    lathe(a, [(0.03, 0.0), (0.03, h * 0.9), (0.026, h * 0.97), (0.012, h)], "wax", seg=8)
    a.cyl(0.04, 0.012, (0, 0, 0.006), "wax", seg=8)                       # pooled wax
    a.cyl(0.006, 0.07, (0.027, 0.0, h * 0.78), "wax", seg=5, r2=0.012)     # drip
    a.sphere(0.011, (0.03, 0.0, h * 0.62), "wax", seg=5)
    a.cyl(0.003, 0.025, (0, 0, h + 0.012), "flame", seg=4)
    a.sphere(0.017, (0, 0, h + 0.04), "flame", scale=(0.8, 0.8, 1.8), seg=6)


def b_candelabra(a, arms=3, h=1.4):
    a.part("candelabra")
    lathe(a, [(0.24, 0.0), (0.25, 0.03), (0.19, 0.06), (0.1, 0.12), (0.06, 0.2), (0.04, 0.24)], "gold", seg=12)
    lathe(a, [(0.04, 0.24), (0.04, 0.4), (0.07, 0.46), (0.04, 0.52), (0.035, 0.7), (0.065, 0.76), (0.04, 0.82),
              (0.035, 1.0), (0.06, 1.05), (0.04, 1.1), (0.035, h - 0.2), (0.07, h - 0.12), (0.09, h - 0.08), (0.05, h - 0.05)],
          "gold", seg=8)
    for i in range(arms):
        ang = i * 2 * math.pi / arms + math.pi / 2
        ca, sa = math.cos(ang), math.sin(ang)
        pts = []
        reach = 0.32
        for k in range(9):
            t = k / 8
            rr = reach * (math.sin(t * math.pi / 2)) ** 1.0
            z = (h - 0.36) + 0.34 * t ** 2.2 - 0.0 * t + 0.08 * math.sin(t * math.pi) * 0
            pts.append((ca * rr, sa * rr, z))
        tube(a, pts, [0.016] * 9, "gold", seg=6)
        x, y, z = pts[-1]
        lathe(a, [(0.012, z - 0.0), (0.05, z + 0.0), (0.05, z + 0.015), (0.03, z + 0.03), (0.03, z + 0.05)], "gold", seg=8, c=(x, y, 0))
        a.cyl(0.024, 0.16, (x, y, z + 0.13), "wax", seg=8)
        flame(a, x, y, z + 0.235, 1.1)
    a.cyl(0.026, 0.16, (0, 0, h + 0.05), "wax", seg=8)
    flame(a, 0, 0, h + 0.155, 1.1)


def b_lantern(a):
    a.part("lantern")
    n = 6
    lathe(a, [(0.13, 0.0), (0.13, 0.03), (0.11, 0.05)], "iron", seg=n)
    lathe(a, [(0.11, 0.05), (0.1, 0.33)], "glass", seg=n, caps=False)
    for k in range(n):
        ang = 2 * math.pi * k / n
        a.box((0.022, 0.022, 0.3), (0.108 * math.cos(ang), 0.108 * math.sin(ang), 0.19), "iron", rot=(0, 0, ang))
    for z in (0.12, 0.26):
        lathe(a, [(0.108, z), (0.108, z + 0.012)], "iron", seg=n, caps=False)
    lathe(a, [(0.13, 0.33), (0.12, 0.36), (0.11, 0.38), (0.06, 0.44), (0.045, 0.47)], "iron", seg=n)
    a.cyl(0.04, 0.035, (0, 0, 0.485), "iron", seg=6)
    torus(a, 0.045, 0.008, (0, 0, 0.545), "iron", axis="y", seg=10, rseg=4)
    pts = [(math.cos(t) * 0.12, 0, 0.36 + 0.13 * math.sin(t)) for t in [math.pi * i / 8 for i in range(9)]]
    tube(a, pts, 0.006, "iron", seg=4)
    a.cyl(0.025, 0.05, (0, 0, 0.09), "iron", seg=6)
    a.sphere(0.04, (0, 0, 0.19), "flame", scale=(1, 1, 1.4), seg=8)


def b_sconce(a):
    a.part("sconce")
    # ornate back plate (leaf/shield shape), arm curling out, drip dish, candle
    plate = [(0.0, -0.17), (0.07, -0.1), (0.075, 0.04), (0.04, 0.13), (0.0, 0.17), (-0.04, 0.13), (-0.075, 0.04), (-0.07, -0.1)]
    prism_xz(a, plate, -0.01, 0.03, "iron")
    a.sphere(0.03, (0, -0.02, 0.0), "iron", seg=6)
    pts = []
    for k in range(9):
        t = k / 8
        pts.append((0.0, -0.02 - 0.2 * math.sin(t * math.pi / 2), -0.08 + 0.1 * t ** 2 * 0.8 - 0.04 * math.sin(t * math.pi)))
    tube(a, pts, 0.012, "iron", seg=6)
    x, y, z = pts[-1]
    lathe(a, [(0.01, z - 0.005), (0.055, z - 0.0), (0.055, z + 0.01), (0.03, z + 0.025)], "iron", seg=10, c=(x, y, 0))
    a.cyl(0.025, 0.17, (x, y, z + 0.1), "wax", seg=8)
    flame(a, x, y, z + 0.215, 1.0)


def b_mirror(a, w=0.7, h=1.4):
    a.part("mirror")
    hw = w / 2

    def outline(g, seg=10):
        zs = h + 0.06 - hw
        pts = [(-hw - g, 0.06 - g), (hw + g, 0.06 - g)]
        for i in range(seg + 1):
            t = math.pi * i / seg
            pts.append(((hw + g) * math.cos(t), zs + (hw + g) * 0.95 * math.sin(t)))
        return pts
    prism_xz(a, outline(0.0), -0.045, 0.0, "glass")
    prism_xz(a, outline(0.04), -0.02, 0.04, "gold")
    prism_xz(a, outline(0.065), -0.0, 0.05, "gold")
    # inner bead moulding standing proud
    prism_xz(a, outline(0.02), -0.056, -0.03, "gold", caps=True)
    prism_xz(a, outline(0.0), -0.048, -0.02, "glass")
    zs = h + 0.06 - hw
    # crest: scrolled finial
    a.sphere(0.05, (0, -0.0, h + 0.06 + 0.1), "gold", scale=(1, 0.7, 1.3), seg=8)
    for sx in (-1, 1):
        a.sphere(0.035, (sx * 0.1, 0.0, h + 0.06 + 0.06), "gold", scale=(1, 0.7, 1), seg=6)
        a.sphere(0.04, (sx * (hw + 0.03), -0.02, 0.1), "gold", seg=6)
    # corner rosettes and base feet
    a.sphere(0.045, (-hw - 0.03, -0.02, 0.1), "gold", seg=6)
    for sx in (-1, 1):
        a.sphere(0.04, (sx * (hw + 0.045), -0.02, zs), "gold", seg=6)
    a.box((w + 0.2, 0.1, 0.05), (0, 0.0, 0.025), "gold")


def b_goblet(a):
    a.part("goblet")
    lathe(a, [(0.055, 0.0), (0.057, 0.008), (0.045, 0.02), (0.02, 0.03), (0.011, 0.045), (0.011, 0.06), (0.02, 0.07), (0.011, 0.082),
              (0.012, 0.095), (0.03, 0.115), (0.048, 0.15), (0.056, 0.19), (0.053, 0.215), (0.05, 0.22)],
          "gold", seg=12)
    a.cyl(0.049, 0.004, (0, 0, 0.212), "wine", seg=12)


def b_bottle(a):
    a.part("bottle")
    lathe(a, [(0.0, 0.0), (0.04, 0.0), (0.052, 0.012), (0.054, 0.12), (0.05, 0.19), (0.036, 0.24), (0.022, 0.275), (0.02, 0.34),
              (0.025, 0.35), (0.025, 0.37), (0.02, 0.375)], "glass", seg=12)
    a.cyl(0.018, 0.05, (0, 0, 0.385), "wood", r2=0.021, seg=8)
    a.cyl(0.026, 0.01, (0, 0, 0.36), "glass", seg=10)


# --------------------------------------------------------------------------- #
# nature
# --------------------------------------------------------------------------- #
def b_pine(a, h=7.0):
    a.part("pine")
    r = _rng(int(h * 13))
    k = 0.6 + 0.4 * min(1.0, h / 7.0)
    # trunk with root flare
    lathe(a, [(0.52, -0.05), (0.34, 0.2), (0.25, 0.5), (0.21, h * 0.3), (0.15, h * 0.6), (0.07, h * 0.9)], "bark", seg=8, smooth=False, c=(0, 0, 0))
    for i in range(5):                                          # roots
        ang = i * 1.26 + r() * 0.5
        tube(a, [(0.15 * math.cos(ang), 0.15 * math.sin(ang), 0.25), (0.45 * math.cos(ang), 0.45 * math.sin(ang), 0.08),
                 (0.75 * math.cos(ang), 0.75 * math.sin(ang), 0.0)], [0.1, 0.07, 0.03], "bark", seg=4)
    tiers = 6
    for i in range(tiers):
        t = i / (tiers - 1)
        z0 = h * (0.2 + 0.7 * t) - 0.05
        rad = k * (1.9 - 1.5 * t) * (0.92 + 0.16 * r())
        ht = h * 0.2 * (1.0 - 0.3 * t) + 0.5
        ox, oy = (r() - 0.5) * 0.15, (r() - 0.5) * 0.15
        n = 11
        rot = r() * 6.28
        rim, mid, tip = [], [], []
        for j in range(n):
            ang = rot + 2 * math.pi * j / n
            rr = rad * (1.0 if j % 2 else 0.72) * (0.88 + 0.24 * r())
            zz = z0 - 0.1 * (1 if j % 2 else 0.2) - 0.18 * r()
            rim.append((ox + rr * math.cos(ang), oy + rr * math.sin(ang), zz))
            rm = rr * 0.62
            mid.append((ox + rm * math.cos(ang + 0.1), oy + rm * math.sin(ang + 0.1), z0 + ht * 0.42 + 0.08 * r()))
            tip.append((ox + 0.05 * math.cos(ang), oy + 0.05 * math.sin(ang), z0 + ht))
        loft(a, [rim, mid, tip], "foliage", caps=False)
        # underside skirt
        loft(a, [rim, [(ox + 0.1 * math.cos(rot + 2 * math.pi * j / n), oy + 0.1 * math.sin(rot + 2 * math.pi * j / n), z0 - 0.05) for j in range(n)]], "foliage", caps=False)
    a.cyl(0.03, 0.25, (0, 0, h * 0.9 + 0.5 * 1 + 0.35), "foliage", r2=0.005, seg=5, smooth=False)


def b_deadtree(a, h=4.0):
    a.part("deadtree")
    r = _rng(int(h * 7))

    def bough(p0, d, length, rad, depth):
        pts = [p0]
        dd = list(d)
        p = p0
        n = 4
        for i in range(n):
            dd = _norm((dd[0] + (r() - 0.5) * 0.7, dd[1] + (r() - 0.5) * 0.7, dd[2] + (r() - 0.35) * 0.3))
            p = _add(p, _mul(dd, length / n))
            pts.append(p)
        tube(a, pts, [rad, rad * 0.85, rad * 0.65, rad * 0.45, rad * 0.2], "bark", seg=5)
        if depth > 0:
            for q in (1, 2, 3):
                if r() < 0.8:
                    ang = r() * 6.28
                    nd = _norm((math.cos(ang) * 0.8, math.sin(ang) * 0.8, 0.45 + r() * 0.4))
                    bough(pts[q], nd, length * (0.55 - 0.05 * q), rad * (0.55 - 0.06 * q), depth - 1)
    # trunk, leaning and twisting, with root flare
    trunk = [(0, 0, -0.05), (0.04, 0.02, h * 0.15), (-0.05, 0.05, h * 0.35), (0.08, -0.02, h * 0.55), (0.03, 0.06, h * 0.72)]
    tube(a, trunk, [0.5, 0.3, 0.25, 0.19, 0.12], "bark", seg=7)
    for i in range(5):
        ang = i * 1.26 + 0.4
        tube(a, [(0.1 * math.cos(ang), 0.1 * math.sin(ang), 0.4), (0.4 * math.cos(ang), 0.4 * math.sin(ang), 0.1),
                 (0.7 * math.cos(ang), 0.7 * math.sin(ang), 0.0)], [0.12, 0.08, 0.03], "bark", seg=4)
    for z, ang, ln in ((0.45, 0.2, 1.3), (0.58, 2.6, 1.2), (0.7, 4.4, 1.0), (0.85, 1.4, 0.8)):
        d = _norm((math.cos(ang) * 0.9, math.sin(ang) * 0.9, 0.5))
        bough(trunk[3 if z > 0.6 else 2], d, ln * h / 4, 0.1, 1)
    bough(trunk[4], (0.1, 0.1, 1.0), 0.9 * h / 4, 0.09, 1)


def b_rock(a, s=1.0):
    a.part("rock")
    r = _rng(int(s * 10) + 3)

    def blob(cx, cy, cz, rx, ry, rz, nlat=4, nlon=8, jit=0.28):
        rings = []
        for i in range(nlat + 1):
            ph = math.pi * i / nlat
            ring = []
            for j in range(nlon):
                th = 2 * math.pi * j / nlon + (i % 2) * 0.3
                k = 1 + (r() - 0.5) * 2 * jit
                z = cz + rz * math.cos(ph) * k
                if z < 0.0:
                    z = -0.02 * s
                ring.append((cx + rx * math.sin(ph) * math.cos(th) * k, cy + ry * math.sin(ph) * math.sin(th) * k, z))
            rings.append(ring)
        # collapse poles to a single point per ring
        for idx in (0, -1):
            p = (sum(v[0] for v in rings[idx]) / nlon, sum(v[1] for v in rings[idx]) / nlon, rings[idx][0][2])
            rings[idx] = [(p[0] + 0.002 * math.cos(j), p[1] + 0.002 * math.sin(j), p[2]) for j in range(nlon)]
        loft(a, rings, "rock", caps=False)
    blob(0, 0, 0.18 * s, 0.7 * s, 0.58 * s, 0.34 * s, 4, 9)
    blob(0.5 * s, 0.22 * s, 0.1 * s, 0.34 * s, 0.3 * s, 0.22 * s, 3, 7)
    blob(-0.42 * s, -0.28 * s, 0.1 * s, 0.28 * s, 0.26 * s, 0.2 * s, 3, 7)
    if s > 1.5:
        blob(-0.2 * s, 0.35 * s, 0.35 * s, 0.4 * s, 0.35 * s, 0.35 * s, 4, 8)


def b_fence(a, w=3.0):
    a.part("fence")
    n = int(w / 0.5)
    for i in range(n + 1):
        x = -w / 2 + i * w / n
        post = i in (0, n) or i == n // 2
        if post:
            a.box((0.09, 0.09, 1.75), (x, 0, 0.875), "iron")
            a.box((0.12, 0.12, 0.06), (x, 0, 1.0), "iron") if False else None
            a.sphere(0.065, (x, 0, 1.85), "iron", seg=8)
            a.box((0.12, 0.12, 0.05), (x, 0, 1.76), "iron")
        else:
            a.box((0.03, 0.03, 1.62), (x, 0, 0.81), "iron")
            lathe(a, [(0.02, 1.58), (0.04, 1.62), (0.02, 1.65), (0.052, 1.68), (0.052, 1.7), (0.03, 1.8), (0.003, 1.92)], "iron", seg=4, smooth=False, c=(x, 0, 0), rot0=0.78)
    for z in (0.28, 1.4, 1.6):
        a.box((w, 0.035, 0.04), (0, 0, z), "iron")
    for i in range(n):
        x = -w / 2 + (i + 0.5) * w / n
        a.cyl(0.07, 0.015, (x, 0, 0.84), "iron", seg=8, rot=(math.pi / 2, 0, 0)) if False else torus(a, 0.06, 0.012, (x, 0, 0.84), "iron", axis="y", seg=8, rseg=4)


def b_signpost(a):
    a.part("signpost")
    r = _rng(4)
    lathe(a, [(0.14, 0.0), (0.09, 0.1), (0.065, 0.3), (0.06, 2.1), (0.08, 2.15), (0.03, 2.28)], "wood", seg=6, smooth=False)
    a.box((0.2, 0.2, 0.06), (0, 0, 0.03), "wood") if False else None
    for ang, z in ((0.0, 1.9), (0.0, 1.55)):
        pass

    def arrow(x0, x1, z, hh, sign, yo):
        pts = [(x0, z - hh / 2), (x1 - sign * hh * 0.55, z - hh / 2), (x1, z), (x1 - sign * hh * 0.55, z + hh / 2), (x0, z + hh / 2)]
        prism_xz(a, pts, yo - 0.025, yo + 0.025, "wood")
    arrow(-0.08, 0.95, 1.9, 0.25, 1, 0.0)
    arrow(0.08, -0.92, 1.55, 0.22, -1, 0.0)
    for (x, z) in ((0.0, 1.9), (0.0, 1.55)):
        a.sphere(0.02, (x + 0.1, -0.03, z), "wood", seg=5)
        a.sphere(0.02, (x - 0.1, -0.03, z), "wood", seg=5)
    a.beam((0.0, 0.0, 1.35), (0.3, 0.0, 1.55), 0.035, "wood") if False else None
    for sx in (-1, 1):
        a.sphere(0.12, (sx * 0.12, 0.08 * sx, 0.04), "wood", scale=(1, 1, 0.5), seg=6)


def b_inn_sign(a):
    a.part("inn_sign")
    a.beam((0, 0, 0), (1.0, 0, 0), 0.06, "iron")
    pts = [(0.0, 0, -0.55), (0.1, 0, -0.3), (0.4, 0, -0.08), (0.9, 0, 0.0)]
    tube(a, pts, 0.018, "iron", seg=5)
    pts2 = [(0.9, 0, 0.0), (1.0, 0, 0.06), (1.03, 0, -0.02), (0.98, 0, -0.06)]
    tube(a, pts2, 0.014, "iron", seg=5)
    a.sphere(0.05, (1.02, 0, 0.0), "iron", seg=6)
    a.box((0.08, 0.06, 0.4), (0.0, 0, -0.3), "iron") if False else None
    for x in (0.28, 0.74):
        a.cyl(0.008, 0.07, (x, 0, -0.035), "iron", seg=4)
    # hanging board with moulded frame, crown medallion both sides
    a.box((0.55, 0.04, 0.42), (0.51, 0, -0.29), "wood")
    for sgn in (-1, 1):
        a.box((0.59, 0.02, 0.04), (0.51, sgn * 0.025, -0.08), "wood")
        a.box((0.59, 0.02, 0.04), (0.51, sgn * 0.025, -0.5), "wood")
        for sx in (-1, 1):
            a.box((0.04, 0.02, 0.42), (0.51 + sx * 0.275, sgn * 0.025, -0.29), "wood")
        a.cyl(0.14, 0.03, (0.51, sgn * 0.03, -0.29), "gold", seg=10, rot=(math.pi / 2, 0, 0))
        a.cyl(0.1, 0.02, (0.51, sgn * 0.045, -0.29), "wood", seg=10, rot=(math.pi / 2, 0, 0))
        for i in range(3):
            xx = 0.51 + (i - 1) * 0.07
            a.cyl(0.015, 0.06, (xx, sgn * 0.065, -0.265 + (0.02 if i == 1 else 0)), "gold", seg=4, r2=0.0, rot=(math.pi / 2 * (-sgn), 0, 0)) if False else a.box((0.025, 0.02, 0.07 + (0.03 if i == 1 else 0)), (xx, sgn * 0.058, -0.26), "gold")
        a.box((0.2, 0.02, 0.025), (0.51, sgn * 0.058, -0.3), "gold")


# --------------------------------------------------------------------------- #
# vehicles
# --------------------------------------------------------------------------- #
def _wheel(a, x, y, z, R, hubw=0.14, nsp=12):
    torus(a, R - 0.04, 0.045, (x, y, z), "wood", axis="x", seg=24, rseg=4, smooth=False)
    torus(a, R - 0.005, 0.014, (x, y, z), "iron", axis="x", seg=24, rseg=4, smooth=False)
    a.cyl(0.075, hubw, (x, y, z), "wood", seg=8, rot=(0, math.pi / 2, 0))
    a.cyl(0.04, hubw + 0.05, (x, y, z), "iron", seg=6, rot=(0, math.pi / 2, 0))
    for k in range(nsp):
        t = 2 * math.pi * k / nsp
        a.beam((x, y + 0.06 * math.cos(t), z + 0.06 * math.sin(t)), (x, y + (R - 0.05) * math.cos(t), z + (R - 0.05) * math.sin(t)), 0.035, "wood")


def b_carriage(a):
    a.part("carriage")
    # chassis, axles, leaf springs
    for y, R in ((-0.8, 0.58), (0.95, 0.46)):
        a.cyl(0.04, 1.9, (0, y, R), "iron", seg=6, rot=(0, math.pi / 2, 0))
        for sx in (-1, 1):
            _wheel(a, sx * 0.93, y, R, R)
            tube(a, [(sx * 0.62, y - 0.28, R + 0.45), (sx * 0.62, y - 0.1, R + 0.5), (sx * 0.62, y + 0.1, R + 0.5), (sx * 0.62, y + 0.28, R + 0.45)], 0.03, "iron", seg=4)
            a.beam((sx * 0.62, y, R + 0.5), (sx * 0.62, y, R), 0.04, "iron") if False else None
    for sx in (-1, 1):
        a.beam((sx * 0.55, -1.15, 0.85), (sx * 0.55, 1.15, 0.85), 0.07, "wood")
    # lower body: flared, bellied
    def lvl(z, hw, hl, belly=0.0):
        return [(-hw, -hl, z), (-hw - belly, 0.0, z), (-hw, hl, z), (hw, hl, z), (hw + belly, 0.0, z), (hw, -hl, z)]
    loft(a, [lvl(0.78, 0.6, 1.0), lvl(1.0, 0.74, 1.15, 0.04), lvl(1.45, 0.8, 1.2, 0.0)], "wood")
    a.box((1.7, 2.5, 0.05), (0, 0, 1.46), "wood")
    for sx in (-1, 1):
        a.box((0.2, 0.7, 0.04), (sx * 0.87, -0.05, 0.62), "wood")                  # step
    # cabin: corner posts, door panels with windows, roof
    for sx in (-1, 1):
        for y in (-0.86, 0.66):
            a.box((0.07, 0.07, 0.85), (sx * 0.74, y, 1.92), "wood")
        a.box((0.05, 1.52, 0.1), (sx * 0.74, -0.1, 1.5), "wood")
        a.box((0.05, 1.52, 0.1), (sx * 0.74, -0.1, 2.32), "wood")
        a.box((0.03, 0.62, 0.45), (sx * 0.745, -0.1, 1.95), "glass")
        a.box((0.04, 0.045, 0.45), (sx * 0.745, -0.1, 1.95), "wood")
        a.box((0.05, 1.3, 0.28), (sx * 0.745, -0.1, 1.67), "wood", rot=(0, 0, 0))
        a.cyl(0.025, 0.04, (sx * 0.78, 0.35, 1.7), "iron", seg=6, rot=(0, math.pi / 2, 0))
    a.box((1.5, 0.05, 0.85), (0, -0.86, 1.92), "wood")
    a.box((1.5, 0.05, 0.4), (0, 0.66, 1.7), "wood")
    a.box((1.46, 0.03, 0.4), (0, 0.66, 2.1), "glass")
    # curved roof
    prof = [(0.9 * math.cos(math.pi * i / 8), 2.33 + 0.28 * math.sin(math.pi * i / 8)) for i in range(9)]
    prism_xz(a, prof, -1.0, 0.8, "leather")
    a.beam((-0.55, -0.9, 2.64), (0.55, -0.9, 2.64), 0.03, "iron") if False else None
    for sx in (-1, 1):
        a.beam((sx * 0.5, -0.8, 2.58), (sx * 0.5, 0.6, 2.58), 0.025, "iron")
        for y in (-0.8, -0.1, 0.6):
            a.beam((sx * 0.5, y, 2.56), (sx * 0.5, y, 2.66), 0.025, "iron")
    # driver's box
    a.box((0.9, 0.9, 0.55), (0, 1.75, 1.2), "wood")
    a.box((1.0, 1.0, 0.07), (0, 1.75, 1.5), "leather")
    a.box((0.9, 0.1, 0.4), (0, 2.18, 1.8), "leather") if False else None
    a.box((0.95, 0.12, 0.5), (0, 1.32, 1.8), "leather")
    a.box((0.95, 0.5, 0.05), (0, 1.9, 0.98), "wood", rot=(0.5, 0, 0)) if False else None
    tube(a, [(-0.4, 2.05, 1.05), (-0.4, 2.15, 1.3), (0.4, 2.15, 1.3), (0.4, 2.05, 1.05)], 0.025, "iron", seg=4) if False else None
    a.box((0.9, 0.6, 0.08), (0, 2.2, 0.95), "wood", rot=(0.4, 0, 0))
    # pole and traces
    a.beam((0, 1.2, 0.85), (0, 3.7, 0.8), 0.08, "wood")
    a.beam((-0.45, 3.45, 0.82), (0.45, 3.45, 0.82), 0.05, "wood")
    # lamps
    for sx in (-1, 1):
        x, y, z = sx * 0.9, 0.55, 2.05
        a.box((0.1, 0.13, 0.04), (x, y, z - 0.1), "iron")
        a.box((0.12, 0.15, 0.2), (x, y, z), "glass")
        a.cyl(0.095, 0.08, (x, y, z + 0.14), "iron", r2=0.02, seg=4)
        a.sphere(0.035, (x, y, z), "flame", scale=(1, 1, 1.3), seg=6)
        a.beam((sx * 0.76, y, z - 0.05), (x, y, z - 0.08), 0.03, "iron")


# --------------------------------------------------------------------------- #
# fireplace, towers, keep
# --------------------------------------------------------------------------- #
def b_fireplace(a, w=2.0, h=1.6):
    a.part("fireplace")
    ow = (w - 0.8) / 2             # half opening width
    jx = (w - 0.4) / 2
    # hearth slab
    a.box((w + 0.3, 0.45, 0.07), (0, -0.4, 0.035), "stone")
    a.box((w + 0.1, 0.5, 0.05), (0, -0.0, 0.025), "stone")
    # jambs with plinth and capital
    for sx in (-1, 1):
        a.box((0.4, 0.5, h - 0.35), (sx * jx, 0, 0.1 + (h - 0.45) / 2 + 0.0), "stone")
        a.box((0.46, 0.56, 0.12), (sx * jx, 0, 0.12), "stone")
        a.box((0.46, 0.56, 0.1), (sx * jx, 0, h - 0.05), "stone")
        a.box((0.42, 0.52, 0.04), (sx * jx, 0, h - 0.13), "stone")
        a.cyl(0.07, h - 0.45, (sx * (jx - 0.19), -0.27, 0.15 + (h - 0.45) / 2), "stone", seg=8)
    # arched lintel
    zs, za = h - 0.45, h - 0.18
    arc_pts = [(-ow + 2 * ow * i / 10, zs + (za - zs) * math.sin(math.pi * i / 10) ** 0.7) for i in range(11)]
    poly = arc_pts + [(ow, h - 0.1), (-ow, h - 0.1)]
    prism_xz(a, poly, -0.25, 0.25, "stone")
    a.box((2 * ow, 0.55, 0.04), (0, 0, h - 0.08), "stone") if False else None
    for i in range(1, 10, 2):
        x, z = arc_pts[i]
        a.box((0.04, 0.54, 0.03), (x, 0, z - 0.005), "stone") if False else None
    # mantel shelf with moulding and corbels
    a.box((w + 0.1, 0.6, 0.14), (0, -0.02, h + 0.0), "stone") if False else None
    a.box((w, 0.56, 0.12), (0, 0, h - 0.04), "stone")
    a.box((w + 0.16, 0.66, 0.1), (0, -0.04, h + 0.07), "stone")
    a.box((w + 0.26, 0.72, 0.06), (0, -0.07, h + 0.15), "stone")
    # chimney breast, tapering, with band
    loft(a, [[(-w * 0.35, -0.5, h + 0.18), (w * 0.35, -0.5, h + 0.18), (w * 0.35, 0.3, h + 0.18), (-w * 0.35, 0.3, h + 0.18)],
             [(-w * 0.3, -0.4, h + 1.0), (w * 0.3, -0.4, h + 1.0), (w * 0.3, 0.3, h + 1.0), (-w * 0.3, 0.3, h + 1.0)],
             [(-w * 0.28, -0.36, h + 1.95), (w * 0.28, -0.36, h + 1.95), (w * 0.28, 0.3, h + 1.95), (-w * 0.28, 0.3, h + 1.95)]], "stone")
    a.box((w * 0.62, 0.5, 0.06), (0, -0.1, h + 1.0), "stone")
    a.box((w * 0.66, 0.5, 0.08), (0, -0.1, h + 1.99), "stone")
    # fire: back plate, grate, andirons, logs
    a.box((2 * ow, 0.04, zs - 0.05), (0, 0.22, 0.05 + (zs - 0.05) / 2), "iron")
    for sx in (-1, 1):
        a.box((0.04, 0.45, zs - 0.4), (sx * (ow - 0.02), 0.0, 0.05 + (zs - 0.4) / 2), "iron") if False else None
        a.box((0.05, 0.3, 0.3), (sx * (ow - 0.12), -0.0, 0.2), "iron") if False else None
        a.box((0.05, 0.05, 0.28), (sx * (ow - 0.16), -0.17, 0.19), "iron")
        a.sphere(0.04, (sx * (ow - 0.16), -0.17, 0.35), "iron", seg=6)
        a.box((0.05, 0.3, 0.05), (sx * (ow - 0.16), 0.0, 0.07), "iron")
    for i in range(6):
        a.cyl(0.012, 0.35, (0, -0.03 - i * 0.0, 0.1), "iron", seg=4, rot=(math.pi / 2, 0, 0)) if False else a.box((0.02, 0.3, 0.02), (-0.45 + i * 0.18, 0, 0.1), "iron")
    for (x, y, z, ang, L) in ((0.0, 0.0, 0.17, 0.0, 0.8), (-0.05, 0.05, 0.3, 0.3, 0.6), (0.05, -0.08, 0.15, 0.0, 0.75)):
        a.cyl(0.07, L, (x, y, z), "wood", seg=7, rot=(0, math.pi / 2, ang))


def _round_tower(a, cx, cy, r, h, roof, wins=3, dormer=False, z0=0.0):
    seg = 16
    # battered base, shaft, string courses
    lathe(a, [(r * 1.18, z0), (r * 1.14, z0 + 0.5), (r * 1.04, z0 + 0.8), (r, z0 + 1.0)], "stone", seg=seg, c=(cx, cy, 0), smooth=False, caps=False)
    lathe(a, [(r, z0 + 1.0), (r * 0.985, z0 + h * 0.5), (r * 0.97, z0 + h)], "stone", seg=seg, c=(cx, cy, 0), smooth=False, caps=False)
    for zz in (0.33, 0.62):
        lathe(a, [(r * 1.03, z0 + h * zz), (r * 1.03, z0 + h * zz + 0.14)], "stone", seg=seg, c=(cx, cy, 0), smooth=False, caps=False)
    a.cyl(r * 1.03, 0.14, (cx, cy, z0 + h * 0.33 + 0.07), "stone", seg=seg, smooth=False)
    a.cyl(r * 1.03, 0.14, (cx, cy, z0 + h * 0.62 + 0.07), "stone", seg=seg, smooth=False)
    # corbelled gallery
    for k in range(seg):
        ang = 2 * math.pi * k / seg
        for dz, dr in ((0.0, 0.1), (0.22, 0.2)):
            a.box((0.28, 0.16 + dr, 0.2), (cx + (r * 0.97 + dr / 2 + 0.04) * math.cos(ang), cy + (r * 0.97 + dr / 2 + 0.04) * math.sin(ang), z0 + h - 0.1 + dz), "stone", rot=(0, 0, ang)) if dz == 0.0 else None
    a.cyl(r + 0.28, 0.14, (cx, cy, z0 + h + 0.0), "stone", seg=seg, smooth=False)
    a.cyl(r + 0.4, 0.16, (cx, cy, z0 + h + 0.15), "stone", seg=seg, smooth=False)
    # conical roof with flared eaves
    zr = z0 + h + 0.23
    R = r + 0.7
    prof = []
    nn = 9
    for i in range(nn + 1):
        t = i / nn
        prof.append((R * (1 - t) ** 1.25 + 0.04 + (0.1 * (1 - t) ** 6) * R * 0.0, zr + roof * t - 0.12 * (1 - t) ** 8 * 1.0))
    prof[0] = (R, zr - 0.12)
    prof.insert(1, (R * 0.93, zr + 0.06))
    lathe(a, prof, "roof", seg=seg, c=(cx, cy, 0), smooth=False)
    a.cyl(0.03, 0.5, (cx, cy, zr + roof + 0.2), "roof", seg=6, r2=0.01)
    a.sphere(0.07, (cx, cy, zr + roof + 0.0), "roof", seg=6)
    # narrow arched windows in several directions
    for i in range(wins):
        ang = -math.pi / 2 + (i - (wins - 1) / 2) * 0.9
        zc = z0 + h * (0.45 + 0.17 * (i % 2)) if wins > 1 else z0 + h * 0.65
        px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
        a.box((0.5, 0.22, 0.12), (px + 0.0, py, zc - 0.62), "stone", rot=(0, 0, ang + math.pi / 2)) if False else None
        out = [(-0.17, -0.5), (0.17, -0.5), (0.17, 0.3)] + [(0.17 * math.cos(math.pi * j / 6), 0.3 + 0.23 * math.sin(math.pi * j / 6) + 0.0) for j in range(1, 6)] + [(-0.17, 0.3)]
        s, c_ = math.sin(ang + math.pi / 2), math.cos(ang + math.pi / 2)
        # surround (stone) and dark glass, oriented to face outward
        for (sc, dd, m) in ((1.45, 0.12, "stone"), (1.0, 0.18, "glass")):
            ring = []
            for (ox, oz) in out:
                ox, oz = ox * sc, oz * (sc if oz > -0.4 else 1.0)
                for dist in (r - 0.05, r - 0.05 + dd):
                    pass
            for yy in (0,):
                pass
            r0 = [(px + ox * sc * c_ - 0.03 * math.cos(ang) , py + ox * sc * s - 0.03 * math.sin(ang), zc + oz * (1.0 + (sc - 1.0) * 0.5)) for (ox, oz) in out for (ox_, oz_) in [(ox, oz)]]
            r1 = [(px + ox * sc * c_ + dd * math.cos(ang), py + ox * sc * s + dd * math.sin(ang), zc + oz * (1.0 + (sc - 1.0) * 0.5)) for (ox, oz) in out]
            loft(a, [r0, r1], m)
        a.box((0.5, 0.2, 0.08), (px + 0.1 * math.cos(ang), py + 0.1 * math.sin(ang), zc - 0.55), "stone", rot=(0, 0, ang + math.pi / 2))
    if dormer:
        ang = -math.pi / 2
        dx, dy, dz = cx + (r + 0.1) * math.cos(ang), cy + (r + 0.1) * math.sin(ang), zr + roof * 0.22
        a.box((0.8, 0.5, 0.75), (dx, dy + 0.3, dz + 0.1), "stone")
        a.box((0.34, 0.1, 0.5), (dx, dy + 0.02, dz + 0.1), "glass")
        loft(a, [[(dx - 0.5, dy + 0.58, dz + 0.45), (dx + 0.5, dy + 0.58, dz + 0.45), (dx + 0.5, dy - 0.1, dz + 0.45), (dx - 0.5, dy - 0.1, dz + 0.45)],
                 [(dx - 0.02, dy + 0.58, dz + 0.9), (dx + 0.02, dy + 0.58, dz + 0.9), (dx + 0.02, dy - 0.1, dz + 0.9), (dx - 0.02, dy - 0.1, dz + 0.9)]], "roof")


def b_tower(a, r=2.5, h=9, roof=3.5):
    a.part("tower")
    _round_tower(a, 0, 0, r, h, roof, wins=3, dormer=True)
    # buttresses
    for ang in (math.pi / 2 + 0.3, math.pi / 2 - 0.3 + math.pi, 0.2, math.pi + 0.2):
        pass


def b_castle_keep(a, w=12, d=8, h=8):
    """Ruined-gothic castle facade used as a backdrop."""
    a.part("keep")
    # battered plinth + main block
    a.box((w + 0.6, d + 0.6, 0.8), (0, 0, 0.4), "stone")
    a.box((w, d, h), (0, 0, h / 2), "stone")
    a.box((w + 0.3, d + 0.3, 0.3), (0, 0, h * 0.5), "stone")
    # buttresses along the front/back
    for i in range(5):
        x = -w / 2 + 1.8 + i * (w - 3.6) / 4
        for sy in (-1, 1):
            a.box((0.5, 0.5, h * 0.7), (x, sy * (d / 2 + 0.2), 0.35 + h * 0.35), "stone")
            a.box((0.5, 0.35, 0.5), (x, sy * (d / 2 + 0.13), h * 0.7 + 0.3), "stone", rot=(0.0, 0, 0))
    # corbel table + crenellated parapet all round
    a.box((w + 0.5, d + 0.5, 0.35), (0, 0, h + 0.0), "stone")
    nx = int(w // 1.2)
    ny = int(d // 1.2)
    for i in range(nx):
        x = -w / 2 + 0.6 + i * (w - 1.2) / (nx - 1)
        if i % 2 == 0:
            for sy in (-1, 1):
                a.box((0.7, 0.5, 0.9), (x, sy * (d / 2 + 0.05), h + 0.62), "stone")
    for j in range(ny):
        y = -d / 2 + 0.6 + j * (d - 1.2) / (ny - 1)
        if j % 2 == 0:
            for sx in (-1, 1):
                a.box((0.5, 0.7, 0.9), (sx * (w / 2 + 0.05), y, h + 0.62), "stone")
    # pitched roof hint behind the parapet
    loft(a, [[(-w / 2 + 0.4, -d / 2 + 0.4, h + 0.15), (w / 2 - 0.4, -d / 2 + 0.4, h + 0.15), (w / 2 - 0.4, d / 2 - 0.4, h + 0.15), (-w / 2 + 0.4, d / 2 - 0.4, h + 0.15)],
             [(-w / 2 + 1.6, -0.15, h + 1.6), (w / 2 - 1.6, -0.15, h + 1.6), (w / 2 - 1.6, 0.15, h + 1.6), (-w / 2 + 1.6, 0.15, h + 1.6)]], "roof")
    # flanking round towers
    for tx in (-w / 2, w / 2):
        _round_tower(a, tx, -d / 2, 1.7, h + 3, 3.2, wins=1)
    # arched windows on the facade
    for i in range(3):
        x = -3 + i * 3
        for zc in (h * 0.62,):
            out = [(-0.4, -0.9), (0.4, -0.9), (0.4, 0.6)] + [(0.4 * math.cos(math.pi * j / 6), 0.6 + 0.5 * math.sin(math.pi * j / 6)) for j in range(1, 6)] + [(-0.4, 0.6)]
            prism_xz(a, [(x + ox * 1.35, zc + oz * 1.12) for ox, oz in out], -d / 2 - 0.1, -d / 2 + 0.02, "stone")
            prism_xz(a, [(x + ox, zc + oz) for ox, oz in out], -d / 2 - 0.16, -d / 2 + 0.0, "glass")
            a.box((0.06, 0.1, 1.5), (x, -d / 2 - 0.2, zc), "stone")
            a.box((1.0, 0.7, 0.14), (x, -d / 2 - 0.2, zc - 1.0), "stone")
    for i in range(2):
        for zc in (h * 0.25,):
            for sx in (-1, 1):
                a.box((0.2, 0.2, 0.9), (sx * (2.2 + i * 2.5), -d / 2 - 0.05, zc), "glass")
    # gatehouse portal: pointed arch surround, wooden door inside
    pw, ph = 2.6, 3.6
    out = [(-pw / 2, 0), (pw / 2, 0), (pw / 2, ph - 0.5)] + [(pw / 2 * math.cos(math.pi * j / 8 * 0.5) * 0 + (pw / 2) * (1 - j / 8) ** 0.8 , ph - 0.5 + 1.0 * math.sin(math.pi * j / 8 * 0.5)) for j in range(1, 8)] + [(0, ph + 0.5)] 
    pts = [(-pw / 2, 0), (pw / 2, 0), (pw / 2, ph - 1.0)]
    for j in range(1, 9):
        t = j / 8 * math.pi / 2
        pts.append((pw / 2 * math.cos(t), ph - 1.0 + 1.5 * math.sin(t) * 1.0))
    for j in range(7, 0, -1):
        t = j / 8 * math.pi / 2
        pts.append((-pw / 2 * math.cos(t), ph - 1.0 + 1.5 * math.sin(t)))
    pts.append((-pw / 2, ph - 1.0))
    # stone surround (slightly proud), then wooden door recessed
    prism_xz(a, [(x * 1.25, z * 1.0 + (0.3 if z > 1 else 0) * 0) for x, z in pts], -d / 2 - 0.25, -d / 2 + 0.02, "stone")
    prism_xz(a, pts, -d / 2 - 0.3, -d / 2 - 0.1, "wood")
    for k in range(-3, 4):
        a.box((0.04, 0.05, 3.0), (k * 0.33, -d / 2 - 0.33, 1.7), "wood") if abs(k * 0.33) < 1.1 else None
    for z in (0.8, 2.4):
        a.box((pw - 0.3, 0.05, 0.12), (0, -d / 2 - 0.35, z), "wood")
    a.box((0.6, 0.6, 0.1), (0, -d / 2 - 0.3, 0.05), "stone") if False else None
