"""Step 3: procedural model generator. Run inside Blender (headless):

    blender -b -P pipeline/blender_gen.py -- [asset_id ...]

Reads pipeline/world_bible.json ("assets" list: id, builder, params), builds
every model from primitives, box-projects UVs at 1 UV unit = 1 metre (so
textures tile at a constant world scale), and writes

    assets/models/<id>.glb      what Godot loads
    assets/blend/<id>.blend     editable source
    assets/models/_slots.json   material slot names per model

Materials are named after their *role* (stone, wood, skin, top ...). The
engine swaps the texture per role at load time, so one mesh serves many looks.
Multi-part models (characters, creatures) export each limb as its own node with
the origin on the joint, which the game animates procedurally (no rig needed).
"""
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "assets" / "models"
BLENDS = ROOT / "assets" / "blend"


# --------------------------------------------------------------------------- #
# geometry helpers
# --------------------------------------------------------------------------- #
class Asset:
    def __init__(self, name):
        self.name = name
        self.parts = {}      # part name -> (bmesh, pivot)
        self.parents = {}    # part name -> parent part name (nodes are nested so joints can chain: shoulder -> elbow)
        self.slots = []      # material role names, index = material_index
        self.cur = None

    def part(self, name, pivot=(0, 0, 0), parent=None):
        self.parts[name] = (bmesh.new(), Vector(pivot))
        if parent:
            self.parents[name] = parent
        self.cur = name
        return self

    def prism(self, w, d, rise, center, mat, ridge_offset=0.0):
        """Gable-roof prism: ridge along X (length w), cross-section a triangle d wide (Y) and `rise` high (Z); base at center.z."""
        bm = self.parts[self.cur][0]
        cx, cy, cz = center
        v = [bm.verts.new((cx - w / 2, cy - d / 2, cz)), bm.verts.new((cx + w / 2, cy - d / 2, cz)),
             bm.verts.new((cx + w / 2, cy + d / 2, cz)), bm.verts.new((cx - w / 2, cy + d / 2, cz)),
             bm.verts.new((cx - w / 2, cy + ridge_offset, cz + rise)), bm.verts.new((cx + w / 2, cy + ridge_offset, cz + rise))]
        faces = [bm.faces.new((v[0], v[3], v[2], v[1])),         # bottom
                 bm.faces.new((v[0], v[1], v[5], v[4])),         # front slope
                 bm.faces.new((v[2], v[3], v[4], v[5])),         # back slope
                 bm.faces.new((v[0], v[4], v[3])),               # gable end -X
                 bm.faces.new((v[1], v[2], v[5]))]               # gable end +X
        idx = self._slot(mat)
        for f in faces:
            f.material_index = idx
            f.smooth = False
        bmesh.ops.recalc_face_normals(bm, faces=faces)
        return self

    def limb(self, p0, p1, r0, r1, mat, seg=10, smooth=True, cap=True):
        """Tapered cylinder from point p0 (radius r0) to p1 (radius r1)."""
        p0, p1 = Vector(p0), Vector(p1)
        d = p1 - p0
        q = d.to_track_quat("Z", "Y")
        m = Matrix.Translation((p0 + p1) / 2) @ q.to_matrix().to_4x4()
        bm = self.parts[self.cur][0]
        r = bmesh.ops.create_cone(bm, cap_ends=cap, cap_tris=False, segments=seg, radius1=r0, radius2=r1, depth=d.length, matrix=m)
        self._finish(r["verts"], mat, smooth)
        return self

    def _slot(self, mat):
        if mat not in self.slots:
            self.slots.append(mat)
        return self.slots.index(mat)

    def _finish(self, verts, mat, smooth=False):
        bm = self.parts[self.cur][0]
        faces = {f for v in verts for f in v.link_faces}
        idx = self._slot(mat)
        for f in faces:
            f.material_index = idx
            f.smooth = smooth

    @staticmethod
    def _m(center, rot=(0, 0, 0), scale=(1, 1, 1)):
        r = (Matrix.Rotation(rot[2], 4, "Z") @ Matrix.Rotation(rot[1], 4, "Y")
             @ Matrix.Rotation(rot[0], 4, "X"))
        s = Matrix.Diagonal((*scale, 1.0))
        return Matrix.Translation(center) @ r @ s

    def box(self, size, center, mat, rot=(0, 0, 0)):
        bm = self.parts[self.cur][0]
        r = bmesh.ops.create_cube(bm, size=1.0, matrix=self._m(center, rot, size))
        self._finish(r["verts"], mat)
        return self

    def cyl(self, r, h, center, mat, r2=None, seg=12, rot=(0, 0, 0), smooth=True):
        bm = self.parts[self.cur][0]
        r2 = r if r2 is None else r2
        r_ = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                                   radius1=r, radius2=r2, depth=h,
                                   matrix=self._m(center, rot))
        self._finish(r_["verts"], mat, smooth)
        return self

    def sphere(self, radius, center, mat, scale=(1, 1, 1), seg=12, rot=(0, 0, 0)):
        bm = self.parts[self.cur][0]
        r = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(4, seg // 2),
                                      radius=radius, matrix=self._m(center, rot, scale))
        self._finish(r["verts"], mat, True)
        return self

    def beam(self, a, b, thick, mat):
        """Box of square section `thick` spanning point a -> b."""
        a, b = Vector(a), Vector(b)
        d = b - a
        L = d.length
        q = d.to_track_quat("Z", "Y")
        bm = self.parts[self.cur][0]
        m = Matrix.Translation((a + b) / 2) @ q.to_matrix().to_4x4() @ Matrix.Diagonal((thick, thick, L, 1))
        r = bmesh.ops.create_cube(bm, size=1.0, matrix=m)
        self._finish(r["verts"], mat)
        return self


def project_uvs(bm, pivot):
    """Box projection, 1 UV unit per metre, in asset space."""
    uv = bm.loops.layers.uv.verify()
    for f in bm.faces:
        n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for l in f.loops:
            p = l.vert.co + pivot
            if ax == 0:
                u, v = p.y, p.z
            elif ax == 1:
                u, v = p.x, p.z
            else:
                u, v = p.x, p.y
            l[uv].uv = (u, v)


def make_material(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    return m


def realize(asset: Asset):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    root = bpy.data.objects.new(asset.name, None)
    bpy.context.scene.collection.objects.link(root)
    mats = [make_material(s) for s in asset.slots]
    objs = {}
    asset.parts_pivot = {n: Vector(v[1]) for n, v in asset.parts.items()}
    for pname, (bm, pivot) in asset.parts.items():
        bmesh.ops.translate(bm, verts=bm.verts, vec=-pivot)
        bm.normal_update()
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        project_uvs(bm, pivot)
        me = bpy.data.meshes.new(pname)
        bm.to_mesh(me)
        bm.free()
        for m in mats:
            me.materials.append(m)
        ob = bpy.data.objects.new(pname if len(asset.parts) > 1 else asset.name + "_mesh", me)
        objs[pname] = ob
        bpy.context.scene.collection.objects.link(ob)
    for pname, ob in objs.items():
        par = asset.parents.get(pname)
        if par and par in objs:
            ob.parent = objs[par]
            ob.location = asset.parts_pivot[pname] - asset.parts_pivot[par]
        else:
            ob.parent = root
            ob.location = asset.parts_pivot[pname]
    MODELS.mkdir(parents=True, exist_ok=True)
    BLENDS.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(MODELS / f"{asset.name}.glb"),
                              export_format="GLB", export_yup=True,
                              export_apply=True, export_materials="EXPORT")
    bpy.ops.wm.save_as_mainfile(filepath=str(BLENDS / f"{asset.name}.blend"))


# --------------------------------------------------------------------------- #
# builders: each takes (asset, **params) and fills it
# --------------------------------------------------------------------------- #
def b_floor(a, w=4, d=4, t=0.2, mat="stone"):
    a.part("floor").box((w, d, t), (0, 0, -t / 2), mat)


def b_wall(a, w=4, h=3, t=0.4, mat="stone", door=0.0, window=0.0):
    """Wall along X, centred on origin, base at z=0. door/window = opening width."""
    a.part("wall")
    if door > 0:
        dh = min(h - 0.5, 2.3)
        sw = (w - door) / 2
        a.box((sw, t, h), (-(w - sw) / 2, 0, h / 2), mat)
        a.box((sw, t, h), ((w - sw) / 2, 0, h / 2), mat)
        a.box((door, t, h - dh), (0, 0, dh + (h - dh) / 2), mat)
    elif window > 0:
        wy0, wy1 = 1.2, 2.4
        sw = (w - window) / 2
        a.box((sw, t, h), (-(w - sw) / 2, 0, h / 2), mat)
        a.box((sw, t, h), ((w - sw) / 2, 0, h / 2), mat)
        a.box((window, t, wy0), (0, 0, wy0 / 2), mat)
        a.box((window, t, h - wy1), (0, 0, wy1 + (h - wy1) / 2), mat)
        a.box((window + 0.1, 0.1, 0.1), (0, 0, wy0 + 0.05), "wood")
        a.box((0.06, 0.06, wy1 - wy0), (0, 0, (wy0 + wy1) / 2), "iron")
        a.box((window, 0.02, wy1 - wy0), (0, 0, (wy0 + wy1) / 2), "glass")
    else:
        a.box((w, t, h), (0, 0, h / 2), mat)
    a.box((w + 0.05, t + 0.12, 0.12), (0, 0, h - 0.06), mat)   # cornice


def b_arch(a, w=2.0, h=3.2, depth=0.6):
    a.part("arch")
    pw = 0.45
    ph = h - w / 2
    a.box((pw, depth, ph), (-(w + pw) / 2, 0, ph / 2), "stone")
    a.box((pw, depth, ph), ((w + pw) / 2, 0, ph / 2), "stone")
    n = 9
    for i in range(n):
        t0, t1 = math.pi * i / n, math.pi * (i + 1) / n
        p0 = ((w / 2 + pw / 2) * math.cos(t0), ph + (w / 2 + pw / 2) * math.sin(t0))
        p1 = ((w / 2 + pw / 2) * math.cos(t1), ph + (w / 2 + pw / 2) * math.sin(t1))
        a.beam((p0[0], 0, p0[1]), (p1[0], 0, p1[1]), 0.1, "stone")
        # chunky voussoir
        mx, mz = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        ang = (t0 + t1) / 2
        a.box((pw, depth, 0.5), (mx, 0, mz), "stone", rot=(0, ang - math.pi / 2, 0))


def b_column(a, h=3.0, r=0.3):
    a.part("column")
    a.cyl(r * 1.4, 0.25, (0, 0, 0.125), "stone", seg=10)
    a.cyl(r, h - 0.5, (0, 0, h / 2), "stone", seg=10)
    a.cyl(r * 1.5, 0.25, (0, 0, h - 0.125), "stone", seg=10)


def b_stairs(a, steps=6, w=1.6, rise=0.2, run=0.35):
    a.part("stairs")
    for i in range(steps):
        a.box((w, run, rise * (i + 1)), (0, i * run, rise * (i + 1) / 2), "stone")


def b_tower(a, r=2.5, h=9, roof=3.5):
    a.part("tower")
    a.cyl(r, h, (0, 0, h / 2), "stone", seg=14)
    a.cyl(r + 0.25, 0.4, (0, 0, h), "stone", seg=14)
    a.cyl(r + 0.4, 0.2, (0, 0, h + 0.3), "roof", seg=14)
    a.cyl(r + 0.7, roof, (0, 0, h + 0.4 + roof / 2), "roof", r2=0.05, seg=14)
    a.box((0.5, 0.2, 0.9), (0, r - 0.05, h * 0.7), "glass")


def b_castle_keep(a, w=12, d=8, h=8):
    """Blocky ruined-gothic castle facade used as a backdrop."""
    a.part("keep")
    a.box((w, d, h), (0, 0, h / 2), "stone")
    for i in range(int(w // 1.2)):
        x = -w / 2 + 0.6 + i * 1.2
        if i % 2 == 0:
            a.box((0.7, 0.7, 0.8), (x, -d / 2 + 0.35, h + 0.4), "stone")
            a.box((0.7, 0.7, 0.8), (x, d / 2 - 0.35, h + 0.4), "stone")
    for tx in (-w / 2, w / 2):
        a.cyl(1.7, h + 3, (tx, -d / 2, (h + 3) / 2), "stone", seg=12)
        a.cyl(2.1, 3.2, (tx, -d / 2, h + 3 + 1.6), "roof", r2=0.05, seg=12)
    for i in range(3):
        a.box((0.7, 0.2, 1.5), (-3 + i * 3, -d / 2 - 0.05, 4.5), "glass")
    a.box((2.4, 0.5, 3.4), (0, -d / 2 - 0.1, 1.7), "wood")


def b_door(a, w=1.1, h=2.2, t=0.1, style="plank"):
    a.part("door", pivot=(-w / 2, 0, 0))
    n = 5
    pw = w / n
    for i in range(n):
        a.box((pw - 0.01, t, h), (-w / 2 + pw * (i + 0.5), 0, h / 2), "wood")
    for z in (0.35, h - 0.35):
        a.box((w, t + 0.04, 0.1), (0, 0, z), "iron")
    a.sphere(0.06, (w / 2 - 0.12, t, h * 0.48), "iron", seg=8)
    a.box((0.12, 0.05, 0.03), (w / 2 - 0.12, t + 0.05, h * 0.48), "iron")


def b_table(a, w=1.8, d=0.9, h=0.8):
    a.part("table")
    a.box((w, d, 0.07), (0, 0, h - 0.035), "wood")
    for sx in (-1, 1):
        for sy in (-1, 1):
            a.box((0.08, 0.08, h - 0.07), (sx * (w / 2 - 0.1), sy * (d / 2 - 0.1), (h - 0.07) / 2), "wood")
    a.box((w - 0.2, 0.05, 0.08), (0, 0, 0.3), "wood")


def b_chair(a, h=0.9, seat=0.48, hist="wood"):
    a.part("chair")
    a.box((0.46, 0.46, 0.05), (0, 0, seat), "wood")
    for sx in (-1, 1):
        for sy in (-1, 1):
            a.box((0.05, 0.05, seat), (sx * 0.2, sy * 0.2, seat / 2), "wood")
    a.box((0.46, 0.05, h - seat), (0, 0.21, seat + (h - seat) / 2), "wood")
    a.box((0.4, 0.4, 0.04), (0, 0, seat + 0.045), "cloth")


def b_throne(a):
    a.part("throne")
    a.box((0.9, 0.8, 0.5), (0, 0, 0.25), "wood")
    a.box((0.8, 0.7, 0.1), (0, 0.02, 0.55), "cloth")
    a.box((0.9, 0.15, 1.8), (0, 0.33, 0.9), "wood")
    a.box((0.7, 0.1, 0.5), (0, 0.27, 1.5), "cloth")
    for sx in (-1, 1):
        a.box((0.1, 0.7, 0.35), (sx * 0.45, 0, 0.65), "wood")
        a.cyl(0.09, 0.2, (sx * 0.45, 0.33, 1.9), "iron", r2=0.0, seg=6)


def b_bed(a, w=1.4, l=2.1, posts=True):
    a.part("bed")
    a.box((w, l, 0.35), (0, 0, 0.3), "wood")
    a.box((w - 0.1, l - 0.1, 0.22), (0, 0.0, 0.57), "cloth")
    a.box((w - 0.3, 0.5, 0.15), (0, l / 2 - 0.45, 0.76), "linen")
    a.box((w, 0.1, 1.2), (0, l / 2, 0.8), "wood")
    a.box((w, 0.1, 0.7), (0, -l / 2, 0.55), "wood")
    if posts:
        for sx in (-1, 1):
            a.cyl(0.05, 2.1, (sx * w / 2, l / 2, 1.05), "wood", seg=8)
            a.cyl(0.05, 2.1, (sx * w / 2, -l / 2, 1.05), "wood", seg=8)
        a.box((w + 0.1, l + 0.1, 0.06), (0, 0, 2.1), "cloth")


def b_chest(a, w=1.0, d=0.55, h=0.5):
    a.part("chest")
    a.box((w, d, h * 0.6), (0, 0, h * 0.3), "wood")
    a.part("lid", pivot=(0, d / 2, h * 0.6))
    a.cyl(d / 2, w, (0, 0, h * 0.6), "wood", seg=10, rot=(0, math.pi / 2, 0), smooth=False)
    for x in (-w / 2 + 0.1, w / 2 - 0.1):
        a.box((0.06, d + 0.04, 0.04), (x, 0, h * 0.6), "iron")
    a.box((0.1, 0.04, 0.12), (0, -d / 2, h * 0.58), "gold")


def b_barrel(a, r=0.35, h=0.9):
    a.part("barrel")
    a.cyl(r * 0.85, h, (0, 0, h / 2), "wood", seg=12)
    a.cyl(r, h * 0.5, (0, 0, h / 2), "wood", r2=r * 0.85, seg=12)
    for z in (0.15, h * 0.5, h - 0.15):
        a.cyl(r * 1.02 if z == h * 0.5 else r * 0.9, 0.05, (0, 0, z), "iron", seg=12)


def b_candle(a, h=0.18):
    a.part("candle")
    a.cyl(0.025, h, (0, 0, h / 2), "wax", seg=8)
    a.sphere(0.02, (0, 0, h + 0.03), "flame", scale=(1, 1, 1.8), seg=6)


def b_candelabra(a, arms=3, h=1.4):
    a.part("candelabra")
    a.cyl(0.2, 0.08, (0, 0, 0.04), "gold", r2=0.12, seg=10)
    a.cyl(0.04, h, (0, 0, h / 2), "gold", seg=8)
    for i in range(arms):
        ang = i * 2 * math.pi / arms
        x, y = 0.28 * math.cos(ang), 0.28 * math.sin(ang)
        a.beam((0, 0, h - 0.15), (x, y, h - 0.02), 0.03, "gold")
        a.cyl(0.04, 0.03, (x, y, h), "gold", seg=8)
        a.cyl(0.025, 0.2, (x, y, h + 0.11), "wax", seg=8)
        a.sphere(0.02, (x, y, h + 0.24), "flame", scale=(1, 1, 1.8), seg=6)
    a.cyl(0.025, 0.2, (0, 0, h + 0.1), "wax", seg=8)
    a.sphere(0.02, (0, 0, h + 0.23), "flame", scale=(1, 1, 1.8), seg=6)


def b_lantern(a):
    a.part("lantern")
    a.box((0.22, 0.22, 0.04), (0, 0, 0.02), "iron")
    a.box((0.18, 0.18, 0.3), (0, 0, 0.19), "glass")
    for sx in (-1, 1):
        for sy in (-1, 1):
            a.box((0.025, 0.025, 0.3), (sx * 0.1, sy * 0.1, 0.19), "iron")
    a.cyl(0.14, 0.12, (0, 0, 0.4), "iron", r2=0.0, seg=4)
    a.sphere(0.04, (0, 0, 0.16), "flame", seg=6)
    a.box((0.02, 0.02, 0.2), (0, 0, 0.5), "iron")


def b_sconce(a):
    a.part("sconce")
    a.box((0.12, 0.04, 0.3), (0, 0.0, 0), "iron")
    a.box((0.06, 0.2, 0.04), (0, -0.1, -0.1), "iron")
    a.cyl(0.03, 0.2, (0, -0.18, 0.02), "wax", seg=8)
    a.sphere(0.02, (0, -0.18, 0.15), "flame", scale=(1, 1, 1.8), seg=6)


def b_crucifix(a, h=0.5):
    a.part("crucifix")
    a.box((0.06, 0.03, h), (0, 0, h / 2), "wood")
    a.box((h * 0.55, 0.03, 0.06), (0, 0, h * 0.7), "wood")
    a.box((0.025, 0.036, h * 0.9), (0, 0, h / 2), "gold")


def b_coffin(a, open_lid=False):
    a.part("coffin")
    L, W, H = 2.1, 0.8, 0.6
    a.box((W, L, 0.05), (0, 0, 0.025), "wood")
    for sx in (-1, 1):
        a.box((0.05, L, H), (sx * (W / 2 - 0.025), 0, H / 2), "wood")
    a.box((W, 0.05, H), (0, L / 2 - 0.025, H / 2), "wood")
    a.box((W, 0.05, H), (0, -L / 2 + 0.025, H / 2), "wood")
    a.box((W - 0.1, L - 0.1, 0.1), (0, 0, 0.1), "earth")
    a.part("lid", pivot=(0, -L / 2, H))
    a.box((W + 0.04, L + 0.04, 0.05), (0, 0, H + 0.025), "wood")
    a.box((0.1, 0.1, 0.02), (0, 0, H + 0.06), "gold")


def b_tomb(a):
    a.part("tomb")
    a.box((1.4, 2.6, 0.7), (0, 0, 0.35), "stone")
    a.box((1.6, 2.8, 0.15), (0, 0, 0.775), "stone")
    a.box((0.9, 0.2, 0.5), (0, -1.0, 1.0), "stone")
    a.box((0.15, 0.2, 1.0), (0, -1.0, 1.4), "stone")
    a.box((0.55, 0.2, 0.15), (0, -1.0, 1.55), "stone")


def b_gravestone(a, h=1.1, w=0.6, style="round"):
    a.part("gravestone")
    a.box((w, 0.15, h * 0.7), (0, 0, h * 0.35), "stone")
    if style == "round":
        a.cyl(w / 2, 0.15, (0, 0, h * 0.7), "stone", seg=10, rot=(math.pi / 2, 0, 0), smooth=False)
    else:
        a.cyl(w / 2, 0.3, (0, 0, h * 0.7 + 0.15), "stone", r2=0.0, seg=4)
    a.box((w * 1.5, 0.4, 0.12), (0, 0, 0.06), "stone")


def b_grave_cross(a, h=1.5):
    a.part("grave_cross")
    a.box((0.2, 0.2, 0.3), (0, 0, 0.15), "stone")
    a.box((0.14, 0.14, h), (0, 0, 0.3 + h / 2), "stone")
    a.box((h * 0.5, 0.14, 0.14), (0, 0, 0.3 + h * 0.7), "stone")


def b_book(a, w=0.22, d=0.3, t=0.05):
    a.part("book")
    a.box((w, d, t), (0, 0, t / 2), "leather")
    a.box((w - 0.02, d - 0.02, t - 0.02), (0.01, 0, t / 2), "paper")
    a.box((0.02, d, t), (-w / 2, 0, t / 2), "leather")


def b_bookshelf(a, w=1.6, h=2.2, d=0.4):
    a.part("bookshelf")
    for sx in (-1, 1):
        a.box((0.05, d, h), (sx * (w / 2 - 0.025), 0, h / 2), "wood")
    a.box((w, 0.03, h), (0, d / 2 - 0.015, h / 2), "wood")
    n = 5
    for i in range(n + 1):
        a.box((w, d, 0.04), (0, 0, i * (h - 0.04) / n + 0.02), "wood")
    for i in range(n):
        z0 = i * (h - 0.04) / n + 0.04
        x = -w / 2 + 0.1
        k = 0
        while x < w / 2 - 0.15:
            bw = 0.04 + ((k * 7) % 5) * 0.012
            bh = 0.22 + ((k * 3) % 4) * 0.04
            a.box((bw, d - 0.1, bh), (x + bw / 2, 0, z0 + bh / 2), "leather" if k % 2 else "cloth")
            x += bw + 0.005
            k += 1


def b_fireplace(a, w=2.0, h=1.6):
    a.part("fireplace")
    a.box((0.4, 0.5, h), (-(w - 0.4) / 2, 0, h / 2), "stone")
    a.box((0.4, 0.5, h), ((w - 0.4) / 2, 0, h / 2), "stone")
    a.box((w, 0.6, 0.35), (0, 0, h + 0.17), "stone")
    a.box((w * 0.7, 0.8, 1.6), (0, -0.1, h + 0.35 + 0.8), "stone")
    a.box((w - 0.8, 0.3, 0.05), (0, 0.0, 0.025), "iron")
    for i in range(3):
        a.beam((-0.3 + i * 0.3, -0.1, 0.05), (-0.2 + i * 0.3, 0.1, 0.3), 0.1, "wood")


def b_mirror(a, w=0.7, h=1.4):
    a.part("mirror")
    a.box((w + 0.12, 0.06, h + 0.12), (0, 0, h / 2 + 0.06), "gold")
    a.box((w, 0.07, h), (0, -0.02, h / 2 + 0.06), "glass")


def b_goblet(a):
    a.part("goblet")
    a.cyl(0.05, 0.02, (0, 0, 0.01), "gold", seg=10)
    a.cyl(0.012, 0.1, (0, 0, 0.07), "gold", seg=8)
    a.cyl(0.04, 0.09, (0, 0, 0.165), "gold", r2=0.055, seg=10)
    a.cyl(0.05, 0.005, (0, 0, 0.205), "wine", seg=10)


def b_bottle(a):
    a.part("bottle")
    a.cyl(0.05, 0.22, (0, 0, 0.11), "glass", seg=10)
    a.cyl(0.05, 0.08, (0, 0, 0.26), "glass", r2=0.02, seg=10)
    a.cyl(0.02, 0.07, (0, 0, 0.335), "glass", seg=8)
    a.cyl(0.02, 0.03, (0, 0, 0.37), "wood", seg=8)


def b_garlic(a):
    a.part("garlic")
    a.cyl(0.01, 0.35, (0, 0, 0.17), "plant", seg=5)
    for i in range(6):
        ang = i * math.pi / 3
        z = 0.05 + (i % 3) * 0.1
        a.sphere(0.045, (0.05 * math.cos(ang), 0.05 * math.sin(ang), z), "garlic", scale=(1, 1, 0.8), seg=8)


def b_stake(a):
    a.part("stake")
    a.cyl(0.012, 0.7, (0, 0, 0.35), "wood", r2=0.03, seg=8)
    a.cyl(0.03, 0.2, (0, 0, 0.8), "wood", seg=8)


def b_hammer(a):
    a.part("hammer")
    a.cyl(0.015, 0.35, (0, 0, 0.17), "wood", seg=6)
    a.box((0.12, 0.05, 0.05), (0, 0, 0.35), "iron")


def b_key(a):
    a.part("key")
    a.cyl(0.04, 0.012, (0, 0, 0.14), "iron", seg=10, rot=(math.pi / 2, 0, 0))
    a.box((0.015, 0.012, 0.13), (0, 0, 0.065), "iron")
    a.box((0.04, 0.012, 0.02), (0.02, 0, 0.01), "iron")
    a.box((0.03, 0.012, 0.02), (0.015, 0, 0.04), "iron")


def b_rug(a, w=2.0, d=3.0):
    a.part("rug")
    a.box((w, d, 0.02), (0, 0, 0.01), "cloth")
    a.box((w - 0.3, d - 0.3, 0.025), (0, 0, 0.012), "trim")


def b_pine(a, h=7.0):
    a.part("pine")
    a.cyl(0.25, h * 0.35, (0, 0, h * 0.175), "bark", r2=0.15, seg=8)
    for i in range(5):
        z = h * 0.25 + i * h * 0.14
        r = 1.8 - i * 0.3
        a.cyl(r, h * 0.28, (0, 0, z + h * 0.1), "foliage", r2=0.0, seg=9, smooth=False)


def b_deadtree(a, h=4.0):
    a.part("deadtree")
    a.cyl(0.3, h * 0.6, (0, 0, h * 0.3), "bark", r2=0.15, seg=7)
    a.beam((0, 0, h * 0.45), (0.9, 0.2, h * 0.8), 0.12, "bark")
    a.beam((0, 0, h * 0.55), (-0.8, -0.3, h * 0.9), 0.1, "bark")
    a.beam((0, 0, h * 0.6), (0.1, 0.7, h), 0.09, "bark")


def b_rock(a, s=1.0):
    a.part("rock")
    a.sphere(0.6 * s, (0, 0, 0.3 * s), "rock", scale=(1.2, 1.0, 0.7), seg=7)
    a.sphere(0.35 * s, (0.5 * s, 0.2 * s, 0.15 * s), "rock", scale=(1, 1, 0.7), seg=6)


def b_fence(a, w=3.0):
    a.part("fence")
    n = int(w / 0.5)
    for i in range(n + 1):
        x = -w / 2 + i * w / n
        a.box((0.05, 0.05, 1.7), (x, 0, 0.85), "iron")
        a.cyl(0.05, 0.18, (x, 0, 1.79), "iron", r2=0.0, seg=4)
    a.box((w, 0.05, 0.05), (0, 0, 0.3), "iron")
    a.box((w, 0.05, 0.05), (0, 0, 1.4), "iron")


def b_carriage(a):
    a.part("carriage")
    a.box((1.6, 2.4, 0.9), (0, 0, 1.0), "wood")
    a.box((1.5, 1.6, 0.9), (0, -0.1, 1.9), "wood")
    a.box((1.7, 1.8, 0.08), (0, -0.1, 2.38), "leather")
    a.box((0.5, 1.0, 0.8), (0, 1.8, 1.3), "wood")
    a.beam((0, 1.2, 0.9), (0, 3.6, 0.85), 0.08, "wood")
    for sx in (-1, 1):
        for y in (-0.8, 0.9):
            a.cyl(0.55, 0.08, (sx * 0.9, y, 0.55), "wood", seg=12, rot=(0, math.pi / 2, 0))
            a.cyl(0.1, 0.12, (sx * 0.9, y, 0.55), "iron", seg=8, rot=(0, math.pi / 2, 0))
    a.sphere(0.08, (0.55, 1.0, 1.35), "flame", seg=6)
    a.box((0.04, 0.5, 0.45), (-0.78, -0.1, 1.9), "glass")
    a.box((0.04, 0.5, 0.45), (0.78, -0.1, 1.9), "glass")


def b_signpost(a):
    a.part("signpost")
    a.cyl(0.06, 2.2, (0, 0, 1.1), "wood", seg=6)
    a.box((1.0, 0.05, 0.25), (0.4, 0, 1.9), "wood")
    a.box((0.9, 0.05, 0.22), (-0.3, 0, 1.55), "wood")


def b_inn_sign(a):
    a.part("inn_sign")
    a.beam((0, 0, 0), (0.9, 0, 0), 0.07, "iron")
    a.beam((0, 0, -0.5), (0.9, 0, 0), 0.04, "iron")
    a.box((0.55, 0.04, 0.45), (0.5, 0, -0.35), "wood")
    a.cyl(0.14, 0.05, (0.5, 0.03, -0.33), "gold", seg=8, rot=(math.pi / 2, 0, 0))   # crown disc


def b_bench(a, l=1.8):
    a.part("bench")
    a.box((l, 0.4, 0.06), (0, 0, 0.45), "wood")
    for sx in (-1, 1):
        a.box((0.06, 0.36, 0.45), (sx * (l / 2 - 0.1), 0, 0.225), "wood")


def b_moon(a, r=3.0):
    a.part("moon")
    a.sphere(r, (0, 0, 0), "glow", seg=16)


# ----------------------------- creatures ---------------------------------- #
def b_bat(a, span=1.0):
    a.part("body")
    a.sphere(0.1, (0, 0, 0), "fur", scale=(1, 1.6, 1), seg=8)
    a.sphere(0.07, (0, 0.17, 0.03), "fur", seg=8)
    for sx in (-1, 1):
        a.cyl(0.03, 0.1, (sx * 0.04, 0.22, 0.12), "fur", r2=0.0, seg=4)
        a.box((0.02, 0.02, 0.02), (sx * 0.03, 0.23, 0.05), "eyes")
    for sx, nm in ((-1, "wing_l"), (1, "wing_r")):
        a.part(nm, pivot=(sx * 0.05, 0, 0.03))
        a.beam((sx * 0.05, 0, 0.03), (sx * span / 2, -0.1, 0.05), 0.03, "fur")
        a.box((span / 2 * 0.9, 0.4, 0.008), (sx * (span / 4 + 0.03), -0.05, 0.03), "wing")


def b_wolf(a, scale=1.0):
    s = scale
    a.part("body")
    a.sphere(0.3 * s, (0, 0, 0.7 * s), "fur", scale=(0.8, 1.7, 0.85), seg=10)
    a.sphere(0.25 * s, (0, -0.4 * s, 0.75 * s), "fur", scale=(0.9, 1, 0.9), seg=8)
    a.cyl(0.08 * s, 0.6 * s, (0, 0.8 * s, 0.65 * s), "fur", r2=0.03, seg=6, rot=(math.pi / 2 + 0.5, 0, 0))
    a.part("head", pivot=(0, -0.65 * s, 0.9 * s))
    a.sphere(0.2 * s, (0, -0.75 * s, 0.9 * s), "fur", scale=(1, 1.1, 0.95), seg=8)
    a.box((0.13 * s, 0.3 * s, 0.1 * s), (0, -0.95 * s, 0.86 * s), "fur")
    a.box((0.04 * s, 0.04 * s, 0.03 * s), (0, -1.1 * s, 0.9 * s), "dark")
    for sx in (-1, 1):
        a.cyl(0.06 * s, 0.14 * s, (sx * 0.1 * s, -0.7 * s, 1.1 * s), "fur", r2=0.0, seg=4)
        a.box((0.03 * s, 0.03 * s, 0.03 * s), (sx * 0.08 * s, -0.9 * s, 0.94 * s), "eyes")
    for nm, (x, y) in {"leg_fl": (-1, -0.35), "leg_fr": (1, -0.35),
                       "leg_bl": (-1, 0.4), "leg_br": (1, 0.4)}.items():
        a.part(nm, pivot=(x * 0.15 * s, y * s, 0.55 * s))
        a.cyl(0.06 * s, 0.55 * s, (x * 0.15 * s, y * s, 0.28 * s), "fur", r2=0.045 * s, seg=6)


# ----------------------------- humanoids ---------------------------------- #
def b_human(a, height=1.75, build=1.0, sex="m", hair="short", beard="none",
            garment="coat", hat="none", cloak=False, hunch=0.0, age=0):
    k = height / 1.75
    sw = 0.23 * build * (0.88 if sex == "f" else 1.0)     # half shoulder width
    hip_z = 0.92 * k
    sh_z = 1.42 * k
    # torso
    a.part("torso", pivot=(0, 0, hip_z))
    top = "top"
    a.cyl(sw * 0.9, sh_z - hip_z, (0, 0, (sh_z + hip_z) / 2), top, r2=sw * 1.05, seg=10, smooth=True)
    a.box((sw * 2.1, 0.2 * build, 0.12 * k), (0, 0, sh_z - 0.05 * k), top)
    a.cyl(0.04 * k, 0.1 * k, (0, 0, sh_z + 0.07 * k), "skin", seg=8)
    if garment in ("coat", "frock"):
        a.cyl(sw * 1.05, 0.55 * k, (0, 0, hip_z - 0.2 * k), top, r2=sw * 1.25, seg=10)
    if garment in ("dress", "gown"):
        a.cyl(sw * 1.0, 0.95 * k, (0, 0, hip_z - 0.35 * k), top, r2=sw * 2.2 if garment == "gown" else sw * 1.7, seg=14)
    a.box((0.02, 0.01, sh_z - hip_z), (0, -0.15 * build, (sh_z + hip_z) / 2), "accent")  # placket / buttons
    if cloak:
        a.box((sw * 2.7, 0.04, 1.2 * k), (0, 0.17 * build, sh_z - 0.6 * k), "cloak")
        a.box((sw * 3.0, 0.3 * build, 0.12 * k), (0, 0.02, sh_z - 0.02 * k), "cloak")
        a.box((0.1 * k, 0.04, 0.3 * k), (0, -0.17 * build, sh_z - 0.1 * k), "accent")
    # head
    a.part("head", pivot=(0, 0, sh_z + 0.12 * k))
    hz = sh_z + 0.27 * k
    a.sphere(0.115 * k, (0, 0, hz), "skin", scale=(0.9, 1.0, 1.15), seg=12)
    a.box((0.04 * k, 0.04 * k, 0.05 * k), (0, -0.115 * k, hz - 0.01 * k), "skin")     # nose
    for sx in (-1, 1):
        a.box((0.02 * k, 0.015 * k, 0.015 * k), (sx * 0.04 * k, -0.1 * k, hz + 0.03 * k), "eyes")
    a.box((0.07 * k, 0.012 * k, 0.012 * k), (0, -0.1 * k, hz - 0.06 * k), "mouth")
    if hair == "short":
        a.sphere(0.12 * k, (0, 0.015 * k, hz + 0.025 * k), "hair", scale=(0.95, 1.0, 1.0), seg=10)
    elif hair == "long":
        a.sphere(0.125 * k, (0, 0.02 * k, hz + 0.02 * k), "hair", scale=(0.95, 1.0, 1.0), seg=10)
        a.box((0.2 * k, 0.07 * k, 0.4 * k), (0, 0.09 * k, hz - 0.17 * k), "hair")
    elif hair == "bun":
        a.sphere(0.12 * k, (0, 0.015 * k, hz + 0.025 * k), "hair", scale=(0.95, 1.0, 1.0), seg=10)
        a.sphere(0.06 * k, (0, 0.1 * k, hz + 0.08 * k), "hair", seg=8)
    elif hair == "slick":
        a.sphere(0.12 * k, (0, 0.03 * k, hz + 0.02 * k), "hair", scale=(0.95, 1.0, 0.95), seg=10)
    if beard in ("full", "pointed"):
        a.cyl(0.07 * k, 0.12 * k, (0, -0.07 * k, hz - 0.1 * k), "hair", r2=0.01 if beard == "pointed" else 0.05, seg=8)
    if beard in ("moustache", "full", "pointed"):
        a.box((0.1 * k, 0.025 * k, 0.025 * k), (0, -0.11 * k, hz - 0.04 * k), "hair")
    if hat == "top":
        a.cyl(0.2 * k, 0.02 * k, (0, 0, hz + 0.1 * k), "accent", seg=12)
        a.cyl(0.115 * k, 0.2 * k, (0, 0, hz + 0.2 * k), "accent", seg=12)
    elif hat == "fur":
        a.cyl(0.13 * k, 0.15 * k, (0, 0, hz + 0.1 * k), "accent", seg=10)
    elif hat == "shawl":
        a.sphere(0.135 * k, (0, 0.03 * k, hz + 0.02 * k), "accent", scale=(1, 1, 1.0), seg=10)
    # arms
    for sx, nm in ((-1, "arm_l"), (1, "arm_r")):
        px = sx * (sw + 0.05)
        a.part(nm, pivot=(px, 0, sh_z - 0.03 * k))
        a.cyl(0.05 * k, 0.32 * k, (px, 0, sh_z - 0.19 * k), top, seg=8)
        a.cyl(0.042 * k, 0.28 * k, (px, 0, sh_z - 0.47 * k), top, seg=8)
        a.sphere(0.045 * k, (px, 0, sh_z - 0.64 * k), "skin", seg=8)
    # legs
    for sx, nm in ((-1, "leg_l"), (1, "leg_r")):
        px = sx * sw * 0.45
        a.part(nm, pivot=(px, 0, hip_z))
        low = "bottom" if garment not in ("dress", "gown") else "skin"
        a.cyl(0.075 * k, 0.45 * k, (px, 0, hip_z - 0.22 * k), low, r2=0.065 * k, seg=8)
        a.cyl(0.062 * k, 0.4 * k, (px, 0, hip_z - 0.65 * k), low, r2=0.05 * k, seg=8)
        a.box((0.1 * k, 0.24 * k, 0.07 * k), (px, -0.05 * k, 0.035 * k), "shoes")


def b_figure_bust(a):
    """Small statue used as a carved bust prop."""
    a.part("bust")
    a.box((0.3, 0.25, 0.6), (0, 0, 0.3), "stone")
    a.sphere(0.12, (0, 0, 0.72), "stone", seg=10)


BUILDERS = {k[2:]: v for k, v in globals().items() if k.startswith("b_")}


def _load_overrides():
    """pipeline/props_v2.py (and pipeline/chars_v2.py) may REPLACE existing b_<name> builders with improved versions."""
    import importlib.util
    for name in ("props_v2", "props_v3", "props_v4", "props_v5", "chars_v2"):
        f = ROOT / "pipeline" / f"{name}.py"
        if not f.exists():
            continue
        spec = importlib.util.spec_from_file_location(name, f)
        mod = importlib.util.module_from_spec(spec)
        mod.math = math
        mod.Asset = Asset
        spec.loader.exec_module(mod)
        for k, v in vars(mod).items():
            if k.startswith("b_") and callable(v):
                BUILDERS[k[2:]] = v


def _load_act_builders():
    """pipeline/acts/act_N_builders.py may define extra b_<name>(a, **params) builders."""
    import importlib.util
    for f in sorted(list((ROOT / "pipeline" / "acts").glob("act_*_builders.py")) + list((ROOT / "pipeline" / "acts").glob("arc_*_builders.py"))):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        mod.math = math
        spec.loader.exec_module(mod)
        for k, v in vars(mod).items():
            if k.startswith("b_") and callable(v):
                assert k[2:] not in BUILDERS, f"{f.name}: builder {k} already exists"
                BUILDERS[k[2:]] = v


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    import os
    bible = json.loads(Path(os.environ.get("BIBLE_JSON", ROOT / "pipeline" / "world_bible.json")).read_text())
    _load_act_builders()
    _load_overrides()
    (MODELS / "_slots").mkdir(parents=True, exist_ok=True)
    for spec in bible["assets"]:
        if argv and spec["id"] not in argv:
            continue
        a = Asset(spec["id"])
        BUILDERS[spec["builder"]](a, **spec.get("params", {}))
        realize(a)
        (MODELS / "_slots" / f"{spec['id']}.json").write_text(json.dumps({"slots": a.slots, "parts": list(a.parts)}))
        print(f"built {spec['id']:<22} slots={a.slots}")


main()
