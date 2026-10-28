"""Act II extra 3D models: the Russian schooner Demeter and her helm. Model front is -Y (bow) in Blender."""
import math


def _hull(length, beam, depth, n=24, bow=1.55, stern_from=0.78, sheer=1.0):
    """Hull stations from bow (-Y) to stern (+Y): returns rings (left gunwale -> keel -> right gunwale) and a point function."""
    levels = (0.0, 0.14, 0.32, 0.55, 0.78, 1.0)

    def pt(t, s, side):
        f = math.sin(min(1.0, t * bow + 0.06) * math.pi / 2) ** 0.85
        half = beam / 2 * f * (1.0 - 0.18 * max(0.0, t - stern_from) / (1.0 - stern_from))          # fuller amidships, tucked at the counter
        top = depth + sheer * (0.38 * (1 - t) ** 2 + 0.10 * t * t)                          # sheer: bow and stern sweep up
        keel = 0.10 + 0.55 * (1 - t) ** 4 + 0.22 * t ** 6                          # cutwater / run
        w = half * (0.10 + 0.90 * s ** 0.62)
        return (side * w, -length / 2 + length * t, keel + s * (top - keel))

    rings = []
    for i in range(n + 1):
        t = i / n
        left = [pt(t, s, -1) for s in reversed(levels)]
        right = [pt(t, s, 1) for s in levels]
        rings.append(left + right)
    return rings, pt, levels


def _sail(a, p0, w, h, belly, axis_y=True, tear=0.0, mat="cloth", nx=7, nz=8, slope=0.38):
    """A billowing gaff sail in the Y-Z plane: p0 = foot of the luff (at the mast), w = length along the boom, h = luff height.
    The head slopes down aft (`slope`), panels alternate with patches, the leech is ragged where `tear` is set."""
    x0, y0, z0 = p0
    grid = [[(x0 + belly * math.sin(math.pi * (i / nx) ** 0.9) * math.sin(math.pi * (j / nz) * 0.92 + 0.15),
              y0 + w * i / nx, z0 + h * (j / nz) * (1 - slope * (i / nx))) for j in range(nz + 1)] for i in range(nx + 1)]
    for i in range(nx):
        for j in range(nz):
            if tear and i >= nx - 2 and j >= nz - 3 and (i + j) % 2 == 0:
                continue                                                       # ragged leech
            m = "patch" if (i * 3 + j * 5) % 11 == 0 else mat
            q = (grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1])
            a.quad(*q, m)
            a.quad(*q[::-1], m)
    for j in range(2, nz, 3):                                                  # reef bands
        for i in range(nx):
            a.limb(grid[i][j], grid[i + 1][j], 0.012, 0.012, "rope", seg=3, smooth=False, cap=False)


def _rigging(a, base_z, mast_y, mast_h, half_beam, rail_z, mat="rope"):
    """Shrouds from the mast head to the rail on both sides, with ratlines."""
    top = (0, mast_y, base_z + mast_h * 0.86)
    for side in (-1, 1):
        for off in (-0.45, 0.0, 0.45):
            foot = (side * half_beam, mast_y + off, rail_z)
            a.beam(top, foot, 0.025, mat)
        for k in range(1, 9):
            u = k / 10.0
            za = rail_z + (top[2] - rail_z) * u
            xa = side * (half_beam * (1 - u))
            a.beam((xa, mast_y - 0.45 * (1 - u), za), (xa, mast_y + 0.45 * (1 - u), za), 0.02, mat)


def _mast(a, my, mh, base_z, half_beam, rail_z, gaff=2.4, boom=2.9, belly=0.35, furled=False):
    a.cyl(0.11, mh, (0, my, base_z + mh / 2), "wood", r2=0.07, seg=10)
    a.cyl(0.14, 0.35, (0, my, base_z + 0.2), "iron", seg=10)                          # mast coat
    a.box((0.7, 0.55, 0.06), (0, my, base_z + mh * 0.78), "wood")                     # top
    a.cyl(0.05, 0.9, (0, my, base_z + mh + 0.35), "wood", seg=6)                      # topmast stub
    a.beam((0, my, base_z + 1.5), (0, my + boom, base_z + 1.25), 0.1, "wood")          # boom
    a.beam((0, my, base_z + mh * 0.82), (0, my + gaff, base_z + mh * 0.62), 0.07, "wood")   # gaff
    if furled:
        a.limb((0, my + 0.1, base_z + 1.58), (0, my + boom - 0.1, base_z + 1.42), 0.17, 0.15, "cloth", seg=8)
    else:
        _sail(a, (0.0, my + 0.15, base_z + 1.4), boom - 0.2, mh * 0.62, belly, tear=1)
    _rigging(a, base_z, my, mh, half_beam, rail_z)
    a.beam((0, my, base_z + mh * 0.95), (0, my - 3.0, base_z + 0.7), 0.025, "rope")   # forestay / backstay


def b_a2_schooner(a, length=9.0, beam=2.6, depth=1.0):
    a.part("a2_schooner")
    rings, pt, levels = _hull(length, beam, depth)
    a.loft(rings, "tar", smooth=False)
    top_l = [r[0] for r in rings]
    top_r = [r[-1] for r in rings]
    for i in range(len(rings) - 1):                                                    # deck planking
        a.quad(top_l[i], top_r[i], top_r[i + 1], top_l[i + 1], "wood")
    a.polygon(rings[-1][::-1], "tar")                                                  # transom
    n = len(rings) - 1
    # hull strakes: a white wale and a dark wale following the sheer
    for lvl, mat, th in ((4, "trim", 0.05), (2, "wood", 0.035)):
        for side in (0, 1):
            idx = (len(levels) - 1 - lvl) if side == 0 else (len(levels) + lvl)
            for i in range(n):
                a.limb(rings[i][idx], rings[i + 1][idx], th, th, mat, seg=4, smooth=False, cap=False)
    # bulwarks, rail cap and stanchions
    for side in (-1, 1):
        for i in range(n):
            p0, p1 = pt(i / n, 1.0, side), pt((i + 1) / n, 1.0, side)
            dy, dz = p1[1] - p0[1], p1[2] - p0[2]
            ang = math.atan2(dz, dy)
            c = ((p0[0] + p1[0]) / 2 * 0.97, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2 + 0.27)
            L = math.hypot(dy, dz) * 1.03
            a.box((0.07, L, 0.54), c, "wood", rot=(ang, 0, 0))
            a.box((0.14, L, 0.05), (c[0], c[1], c[2] + 0.29), "trim", rot=(ang, 0, 0))
            if i % 3 == 0 and 2 < i < n - 1:
                a.box((0.06, 0.08, 0.7), (c[0] * 0.96, c[1], c[2] + 0.05), "wood")
    a.box((beam * 0.62, 0.1, 0.5), (0, length / 2 - 0.04, depth + 0.4), "wood")         # taffrail
    # rudder, tiller, name board
    a.box((0.12, 0.5, 1.1), (0, length / 2 + 0.28, 0.55), "iron")
    a.beam((0, length / 2 - 0.8, depth + 0.72), (0, length / 2 - 0.1, depth + 0.55), 0.07, "wood")
    a.box((beam * 0.5, 0.05, 0.16), (0, length / 2 + 0.05, depth * 0.78), "trim")
    for wx in (-0.5, 0.0, 0.5):
        a.box((0.2, 0.04, 0.16), (wx, length / 2 + 0.06, depth * 0.46), "iron")        # stern lights
    # bowsprit, stem head, anchors
    a.limb((0, -length / 2 + 0.2, depth + 0.45), (0, -length / 2 - 1.5, depth + 0.9), 0.1, 0.06, "wood")
    a.beam((0, -length / 2 - 1.4, depth + 0.88), (0, -length / 2 + 0.6, 0.2), 0.03, "iron")        # bobstay
    for sx in (-1, 1):
        a.beam((sx * 0.5, -length / 2 + 1.1, depth + 0.1), (sx * 0.62, -length / 2 + 0.85, depth - 0.25), 0.1, "wood")   # cathead
        a.sphere(0.1, (sx * 0.64, -length / 2 + 0.85, depth - 0.33), "iron")
        a.box((0.2, 0.05, 0.35), (sx * (beam * 0.32), -length / 2 + 1.5, depth - 0.3), "iron")        # anchor flukes
    # deck house, skylight, companionway, hatch coaming
    hy = length / 2 - 1.7
    a.box((1.5, 1.8, 0.75), (0, hy, depth + 0.55), "wood")
    a.box((1.6, 1.9, 0.07), (0, hy, depth + 0.95), "trim")
    for sx in (-1, 1):
        a.box((0.04, 0.4, 0.28), (sx * 0.76, hy - 0.4, depth + 0.62), "iron")          # windows
        a.box((0.04, 0.4, 0.28), (sx * 0.76, hy + 0.4, depth + 0.62), "iron")
    a.box((0.55, 0.05, 0.62), (0, hy - 0.91, depth + 0.5), "tar")                      # door
    a.box((0.7, 0.55, 0.22), (0, hy + 0.2, depth + 1.07), "wood")                      # skylight
    a.box((0.62, 0.45, 0.04), (0, hy + 0.2, depth + 1.2), "iron")
    a.box((0.9, 1.0, 0.16), (0, -length / 2 + 2.3, depth + 0.08), "wood")              # hatch coaming
    a.box((0.76, 0.86, 0.04), (0, -length / 2 + 2.3, depth + 0.17), "tar")
    a.cyl(0.19, 0.3, (0.0, -length / 2 + 1.5, depth + 0.1), "iron", seg=8)             # windlass
    a.box((0.55, 0.3, 0.16), (0.0, hy + 1.35, depth + 0.1), "wood")                    # binnacle base
    a.cyl(0.1, 0.4, (0.0, hy + 1.35, depth + 0.4), "iron", seg=8)
    # dinghy bottom-up on the deck, coiled rope, barrel
    a.limb((0.62, -0.6, depth + 0.2), (0.62, 0.9, depth + 0.2), 0.3, 0.3, "wood", seg=8)
    a.limb((-0.55, 0.9, depth + 0.12), (-0.55, 1.5, depth + 0.12), 0.18, 0.18, "rope", seg=8)
    a.cyl(0.16, 0.45, (-0.7, 0.2, depth + 0.25), "wood", seg=10)
    # masts with gaffs, booms, sails and shrouds; jib between bowsprit and the foremast
    half = beam / 2 * 0.92
    _mast(a, -1.1, 6.6, depth + 0.1, half, depth + 0.35, gaff=2.3, boom=2.6, furled=False)
    _mast(a, 1.3, 6.0, depth + 0.1, half, depth + 0.35, gaff=2.0, boom=2.8, belly=0.3, furled=True)
    _sail(a, (0.0, -length / 2 - 1.1, depth + 1.0), 3.3, 3.6, 0.25, tear=1, nx=4)


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


def b_a2_deckshell(a, length=26.0, beam=8.3, depth=0.9):
    """The Demeter's hull around the walkable deck of one scene: deck level = z of the model's origin plane (put it at y = -depth),
    bow towards -Y. The scene's own floor slab lies on top; this gives it a hull, bulwarks, rail, bowsprit, stern and rudder."""
    a.part("a2_deckshell")
    rings, pt, levels = _hull(length, beam, depth, n=30, bow=3.2, stern_from=0.88, sheer=0.3)
    a.loft(rings, "tar")
    n = len(rings) - 1
    for i in range(n):                                        # flat deck just under the scene's floor slab
        q = [(r[k][0], r[k][1], depth - 0.05) for r in (rings[i], rings[i + 1]) for k in (0, -1)]
        a.quad(q[0], q[1], q[3], q[2], "wood")
    a.polygon(rings[-1][::-1], "tar")
    for lvl, mat, th in ((4, "trim", 0.06), (2, "wood", 0.04)):
        for side in (0, 1):
            idx = (len(levels) - 1 - lvl) if side == 0 else (len(levels) + lvl)
            for i in range(n):
                a.limb(rings[i][idx], rings[i + 1][idx], th, th, mat, seg=4, smooth=False, cap=False)
    for side in (-1, 1):
        for i in range(n):
            p0, p1 = pt(i / n, 1.0, side), pt((i + 1) / n, 1.0, side)
            dy, dz = p1[1] - p0[1], p1[2] - p0[2]
            ang = math.atan2(dz, dy)
            c = ((p0[0] + p1[0]) / 2 * 0.985, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2 + 0.3)
            L = math.hypot(dy, dz) * 1.03
            a.box((0.1, L, 0.6), c, "wood", rot=(ang, 0, 0))
            a.box((0.2, L, 0.06), (c[0], c[1], c[2] + 0.33), "trim", rot=(ang, 0, 0))
            if i % 2 == 0:
                a.box((0.08, 0.1, 0.82), (c[0] * 0.97, c[1], c[2] + 0.08), "wood")
    # stern: taffrail, rudder, stern lights; bow: bowsprit, bobstay, catheads, anchors
    a.box((beam * 0.7, 0.14, 0.6), (0, length / 2 - 0.05, depth + 0.45), "wood")
    a.box((0.16, 0.7, 1.6), (0, length / 2 + 0.4, 0.2), "iron")
    for wx in (-1.2, -0.4, 0.4, 1.2):
        a.box((0.34, 0.05, 0.26), (wx, length / 2 + 0.06, depth * 0.5), "iron")
    a.box((beam * 0.6, 0.06, 0.22), (0, length / 2 + 0.05, depth * 0.82), "trim")
    bx = -length / 2
    a.limb((0, bx + 0.3, depth + 0.55), (0, bx - 2.6, depth + 1.3), 0.15, 0.08, "wood")
    a.beam((0, bx - 2.5, depth + 1.28), (0, bx + 0.8, 0.2), 0.04, "iron")
    for sx in (-1, 1):
        a.beam((sx * 0.7, bx + 1.4, depth + 0.1), (sx * 0.9, bx + 1.0, depth - 0.4), 0.14, "wood")
        a.sphere(0.13, (sx * 0.92, bx + 1.0, depth - 0.5), "iron")
        a.cyl(0.07, 0.5, (sx * 1.6, bx + 2.4, depth - 0.15), "iron", seg=6, rot=(math.pi / 2, 0, 0))
        a.box((0.28, 0.06, 0.5), (sx * 1.9, bx + 2.0, depth - 0.45), "iron")


def b_a2_mast(a, mh=7.4, half_beam=4.1, gaff=3.2, boom=3.8):
    """A mast with furled mainsail, gaff, boom and shrouds that reach the bulwark half_beam away (deck level z = 0)."""
    a.part("a2_mast")
    _mast(a, 0.0, mh, 0.0, half_beam, 0.55, gaff=gaff, boom=boom, furled=True)
    for sx in (-1, 1):
        a.box((0.08, 1.4, 0.08), (sx * half_beam * 0.92, 0, 0.55), "wood")           # chains plate
    a.box((0.9, 0.9, 0.28), (0, 0, 0.14), "wood")                                      # mast partners
    for k in range(4):
        a.cyl(0.04, 0.5, (0.55 * math.cos(k * 1.57), 0.55 * math.sin(k * 1.57), 0.55), "wood", seg=6)   # belaying pins


