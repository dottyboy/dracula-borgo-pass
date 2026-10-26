"""Blender: dress a bare Mixamo mannequin (Y Bot / X Bot) as one of the game's human models and export a skinned GLB.

The look comes from the same parameters as the procedural humans (pipeline/bible_src.py HUMANS -> humans.json): height,
sex, hair, beard, garment (coat|frock|dress|gown), hat, cloak, fangs. Materials are named after the colour roles of the
game's variants (skin, eyes, sclera, mouth, hair, top, bottom, shoes, accent, cloak), so Assets.apply_variant recolours the
skinned character exactly like the procedural one.

Garments are inflated shells of the body (they inherit its skin weights); skirt / coat tails / cloak are hanging grids on
chain bones "cloth_<name>_c<col>_b<i>" driven by a SpringBoneSimulator3D in Godot (MixamoRig.add_cloth_physics).

blender -b --factory-startup -P dress.py -- "<Bot FBX>" <out.glb> '<json params>'
params: {"sex": "m", "hair": "short", "beard": "none", "garment": "coat", "hat": "none", "cloak": false, "fangs": false}
"""
import bpy
import bmesh
import sys
import json
import math
from mathutils import Vector, Matrix

args = sys.argv[sys.argv.index("--") + 1:]
src, out = args[0], args[1]
P = {"sex": "m", "hair": "short", "beard": "none", "garment": "coat", "hat": "none", "cloak": False, "fangs": False}
P.update(json.loads(args[2]) if len(args) > 2 else {})

ROLE_COL = {"skin": "#e8c3a0", "eyes": "#201510", "sclera": "#f0ece4", "mouth": "#8a3a3a", "hair": "#4a3322",
            "top": "#5a4632", "bottom": "#3a3128", "shoes": "#2a1d14", "accent": "#2a2a2a", "cloak": "#111111"}


def hexlin(h):
    return [(int(h[i:i + 2], 16) / 255.0) ** 2.2 for i in (1, 3, 5)]


bpy.ops.import_scene.fbx(filepath=src, use_anim=True)
for o in list(bpy.data.objects):
    if o.type == "MESH" and o.name.startswith("Cube"):
        bpy.data.objects.remove(o, do_unlink=True)
arm = [o for o in bpy.data.objects if o.type == "ARMATURE"][0]
for a in list(bpy.data.actions):
    bpy.data.actions.remove(a)

# ---- one body mesh
parts = [o for o in bpy.data.objects if o.type == "MESH"]
bpy.ops.object.select_all(action="DESELECT")
for o in parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
body = bpy.context.view_layer.objects.active
body.name = "body"
body.data.materials.clear()
MW = body.matrix_world.copy()
MWI = MW.inverted()
AMI = arm.matrix_world.inverted()
names = {i: g.name for i, g in enumerate(body.vertex_groups)}
GROUPS = [g.name for g in body.vertex_groups]

MATS = {}
for role, col in ROLE_COL.items():
    m = bpy.data.materials.new(role)
    m.use_nodes = True
    bs = m.node_tree.nodes["Principled BSDF"]
    bs.inputs["Base Color"].default_value = (*hexlin(col), 1)
    bs.inputs["Roughness"].default_value = 0.85
    if role in ("top", "cloak", "accent", "bottom"):
        m.use_backface_culling = False
    MATS[role] = m


def base(n):
    n = n.replace("mixamorig:", "")
    for p in ("Left", "Right"):
        if n.startswith(p):
            n = n[len(p):]
    return n


def cat_of(n):
    b = base(n)
    if b in ("Head", "HeadTop_End", "Neck"):
        return "head"
    if b.startswith("Hand"):
        return "hand"
    if b in ("Shoulder", "Spine", "Spine1", "Spine2", "Hips"):
        return "torso"
    if b in ("Arm", "ForeArm"):
        return "arm"
    if b in ("UpLeg", "Leg"):
        return "leg"
    if b in ("Foot", "ToeBase", "Toe_End"):
        return "foot"
    return "other"


def bone_world(name, tail=False):
    b = arm.data.bones[name]
    return arm.matrix_world @ (b.tail_local if tail else b.head_local)


# ---- classify body faces
bm = bmesh.new()
bm.from_mesh(body.data)
dl = bm.verts.layers.deform.verify()
bm.faces.ensure_lookup_table()
face_cat = []
face_z = []
for f in bm.faces:
    w = {}
    for v in f.verts:
        for gi, wt in v[dl].items():
            c = cat_of(names[gi])
            w[c] = w.get(c, 0.0) + wt
    face_cat.append(max(w, key=w.get) if w else "other")
    face_z.append(sum((MW @ v.co).z for v in f.verts) / len(f.verts))
H = max((MW @ v.co).z for v in bm.verts)
k = H / 1.75

hand_l = bone_world("mixamorig:LeftHand")
hand_r = bone_world("mixamorig:RightHand")


def face_pos(f):
    return MW @ f.calc_center_median()


def select(pred):
    return [i for i, f in enumerate(bm.faces) if pred(i, f)]


dress = P["garment"] in ("dress", "gown")
BOOT_Z = 0.24 * H
sets = {
    "cuff": select(lambda i, f: face_cat[i] == "arm" and min((face_pos(f) - hand_l).length, (face_pos(f) - hand_r).length) < 0.075 * k),
    "boots": select(lambda i, f: face_cat[i] == "foot" or (face_cat[i] == "leg" and face_z[i] < BOOT_Z)),
}
taken = set(sets["cuff"]) | set(sets["boots"])
sets["top"] = select(lambda i, f: face_cat[i] == "torso")
sets["legs"] = []
sets["cuff"] = []
sets["boots"] = select(lambda i, f: face_cat[i] == "foot")

new_obj = {}


def new_skinned(name, mesh):
    ob = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = arm
    ob.matrix_parent_inverse = body.matrix_parent_inverse.copy()
    ob.matrix_world = MW.copy()
    md = ob.modifiers.new("Armature", "ARMATURE")
    md.object = arm
    return ob


def shell(name, idxs, role, thick, smooth):
    if not idxs:
        return None
    sb = bm.copy()
    sb.faces.ensure_lookup_table()
    keep = set(idxs)
    sb_del = [sb.faces[i] for i in range(len(sb.faces)) if i not in keep]
    bmesh.ops.delete(sb, geom=sb_del, context="FACES")
    me = bpy.data.meshes.new(name)
    sb.to_mesh(me)
    sb.free()
    me.materials.append(MATS[role])
    ob = new_skinned(name, me)
    for g in GROUPS:
        ob.vertex_groups.new(name=g)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.data.objects:
        o.select_set(o == ob)
    if smooth:
        sm = ob.modifiers.new("smooth", "SMOOTH")
        sm.factor = 0.7
        sm.iterations = smooth
        bpy.ops.object.modifier_move_to_index(modifier="smooth", index=0)
        bpy.ops.object.modifier_apply(modifier="smooth")
    b2 = bmesh.new()
    b2.from_mesh(me)
    b2.normal_update()
    for v in b2.verts:
        v.co += v.normal * (thick / 0.01)             # mesh is in cm
    b2.to_mesh(me)
    b2.free()
    for p in me.polygons:
        p.use_smooth = True
    return ob


shell("coat", sets["top"], "top", 0.016, 9)
shell("boots", sets["boots"], "shoes", 0.017, 2)


# ---- sleeves and trouser legs: smooth lofted tubes along the bone chains (they bend cleanly at elbow / knee)
def tube(name, joints, radii, role, bones, seg=14, rings=7, blend=0.07, squash=1.0, cap_start=True, cap_end=True):
    """joints: world points; radii at each joint; bones: bone name for each segment (len(joints)-1)."""
    pts = [Vector(j) for j in joints]
    segs = []
    arclen = [0.0]
    for i in range(len(pts) - 1):
        arclen.append(arclen[-1] + (pts[i + 1] - pts[i]).length)
    verts, ring_idx, wts = [], [], []
    ref = Vector((0, -1, 0))
    for i in range(len(pts) - 1):
        d = (pts[i + 1] - pts[i])
        L = d.length
        dn = d.normalized()
        u = dn.cross(ref)
        if u.length < 1e-4:
            u = dn.cross(Vector((1, 0, 0)))
        u.normalize()
        v = dn.cross(u).normalized()
        for r_ in range(rings + (1 if i == len(pts) - 2 else 0)):
            t = r_ / rings
            c = pts[i] + d * t
            rad = radii[i] + (radii[i + 1] - radii[i]) * t
            ring = []
            for a in range(seg):
                ang = 2 * math.pi * a / seg
                verts.append(c + (u * math.cos(ang) * rad * squash) + (v * math.sin(ang) * rad))
                ring.append(len(verts) - 1)
            ring_idx.append(ring)
            s_ = arclen[i] + L * t
            w = {}
            # blend with neighbouring bone near the joints
            bi = i
            w[bones[bi]] = 1.0
            if i > 0 and t * L < blend:
                f = 0.5 + 0.5 * (t * L) / blend
                w = {bones[i]: f, bones[i - 1]: 1 - f}
            elif i < len(bones) - 1 and (1 - t) * L < blend:
                f = 0.5 + 0.5 * ((1 - t) * L) / blend
                w = {bones[i]: f, bones[i + 1]: 1 - f}
            wts.append((ring, w))
    faces = []
    for a_ring, b_ring in zip(ring_idx[:-1], ring_idx[1:]):
        for a in range(seg):
            a2 = (a + 1) % seg
            faces.append((a_ring[a], a_ring[a2], b_ring[a2], b_ring[a]))
    if cap_start:
        c = len(verts)
        verts.append(pts[0] - (pts[1] - pts[0]).normalized() * radii[0] * 0.6)
        faces += [(c, ring_idx[0][(a + 1) % seg], ring_idx[0][a]) for a in range(seg)]
        wts.append(([c], {bones[0]: 1.0}))
    if cap_end:
        c = len(verts)
        verts.append(pts[-1] + (pts[-1] - pts[-2]).normalized() * radii[-1] * 0.3)
        faces += [(c, ring_idx[-1][a], ring_idx[-1][(a + 1) % seg]) for a in range(seg)]
        wts.append(([c], {bones[-1]: 1.0}))
    me = bpy.data.meshes.new(name)
    me.from_pydata([MWI @ v for v in verts], [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(MATS[role])
    ob = new_skinned(name, me)
    for g_ in GROUPS:
        ob.vertex_groups.new(name=g_)
    for idxs, w in wts:
        for bn, wv in w.items():
            ob.vertex_groups[bn].add(list(idxs), wv, "ADD")
    return ob


b_ = 1.0
for side in ("Left", "Right"):
    sh = bone_world("mixamorig:%sArm" % side)
    el = bone_world("mixamorig:%sForeArm" % side)
    wr = bone_world("mixamorig:%sHand" % side)
    ext = (sh - el).normalized() * 0.015 * k
    tube("sleeve_" + side, [sh + ext, el, wr], [0.057 * k, 0.047 * k, 0.037 * k], "top",
         ["mixamorig:%sArm" % side, "mixamorig:%sForeArm" % side], cap_start=True, cap_end=False)
    cuff_a = wr - (wr - el).normalized() * 0.05 * k
    tube("cuff_" + side, [cuff_a, wr], [0.040 * k, 0.040 * k], "accent", ["mixamorig:%sForeArm" % side], rings=1, cap_start=False, cap_end=False)
    hp = bone_world("mixamorig:%sUpLeg" % side)
    kn = bone_world("mixamorig:%sLeg" % side)
    an = bone_world("mixamorig:%sFoot" % side)
    if not dress:
        up = (hp - kn).normalized()
        tube("trouser_" + side, [hp + up * 0.03 * k, kn, an + Vector((0, 0, 0.1 * k))], [0.092 * k, 0.062 * k, 0.047 * k], "bottom",
             ["mixamorig:%sUpLeg" % side, "mixamorig:%sLeg" % side], cap_start=True, cap_end=False)
    # boot shaft
    tube("shaft_" + side, [kn + (an - kn) * 0.62, an], [0.056 * k, 0.050 * k], "shoes", ["mixamorig:%sLeg" % side], rings=2, cap_start=False, cap_end=False)

# remove everything but head / neck / hands from the body
rm = [bm.faces[i] for i in range(len(bm.faces)) if face_cat[i] not in ("head", "hand")]
bmesh.ops.delete(bm, geom=rm, context="FACES")
bm.to_mesh(body.data)
body.data.materials.append(MATS["skin"])
for p in body.data.polygons:
    p.use_smooth = True
bm.free()

# ---- measurements from the (kept) head and from all garment verts
head_pts = []
for v in body.data.vertices:
    for g in v.groups:
        if base(names[g.group]) in ("Head", "HeadTop_End") and g.weight > 0.5:
            head_pts.append(MW @ v.co)
            break
hx0, hx1 = min(p.x for p in head_pts), max(p.x for p in head_pts)
hy0, hy1 = min(p.y for p in head_pts), max(p.y for p in head_pts)
hz0, hz1 = min(p.z for p in head_pts), max(p.z for p in head_pts)
HC = Vector(((hx0 + hx1) / 2, (hy0 + hy1) / 2, (hz0 + hz1) / 2))
hr = (hy1 - hy0) / 2 / 0.98                        # depth radius (original model: 0.112)
hk = hr / 0.112                                   # scale to the procedural proportions
hz = HC.z
hy = HC.y
SLICE = []
for ob in bpy.data.objects:
    if ob.type == "MESH" and ob.name in ("coat", "trousers", "boots", "body"):
        for v in ob.data.vertices:
            p = MW @ v.co
            if abs(p.x) < 0.32:
                SLICE.append(p)


def slice_extent(z, tol=0.04):
    pts = [p for p in SLICE if abs(p.z - z) < tol]
    if not pts:
        return 0.15, 0.12, 0.0, 0.0
    xs = [p.x for p in pts]
    ys = [p.y for p in pts]
    return (max(xs) - min(xs)) / 2, (max(ys) - min(ys)) / 2, (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2


# ---- rigid accessory builder (bmesh primitives, skinned 100% to one bone)
acc = {}


def acc_obj(role, bone):
    key = (role, bone)
    if key not in acc:
        me = bpy.data.meshes.new("acc_%s_%s" % (role, base(bone)))
        me.materials.append(MATS[role])
        ob = new_skinned(me.name, me)
        ob.vertex_groups.new(name=bone)
        acc[key] = (ob, bmesh.new())
    return acc[key]


def prim(kind, loc, scl, role, bone="mixamorig:Head", rot=(0, 0, 0), seg=10, r2=None):
    ob, b = acc_obj(role, bone)
    mat = Matrix.Translation(MWI @ Vector(loc))
    # object-space scale/rot in world axes, then to body local (cm)
    rotm = Matrix.Rotation(rot[2], 4, "Z") @ Matrix.Rotation(rot[1], 4, "Y") @ Matrix.Rotation(rot[0], 4, "X")
    sc = Matrix.Diagonal((scl[0], scl[1], scl[2], 1.0))
    world = Matrix.Translation(Vector(loc)) @ rotm @ sc
    local = MWI @ world
    if kind == "sphere":
        res = bmesh.ops.create_uvsphere(b, u_segments=seg, v_segments=max(4, seg // 2 + 1), radius=1.0, matrix=local)
    elif kind == "cyl":
        res = bmesh.ops.create_cone(b, cap_ends=True, segments=seg, radius1=1.0, radius2=(r2 if r2 is not None else 1.0), depth=1.0, matrix=local)
    else:
        res = bmesh.ops.create_cube(b, size=1.0, matrix=local)
    return res


def flush_acc():
    for (role, bone), (ob, b) in acc.items():
        b.to_mesh(ob.data)
        b.free()
        for p in ob.data.polygons:
            p.use_smooth = True
        ob.vertex_groups[bone].add(list(range(len(ob.data.vertices))), 1.0, "REPLACE")


def limb(p0, p1, r0, r1, role, bone="mixamorig:Head", seg=8):
    p0, p1 = Vector(p0), Vector(p1)
    mid = (p0 + p1) / 2
    d = p1 - p0
    L = d.length
    z = Vector((0, 0, 1))
    q = z.rotation_difference(d.normalized())
    e = q.to_euler()
    # cone from r0 (bottom, p0) to r1 (top, p1): create_cone radius1 at -depth/2
    prim("cyl", mid, (r0, r0, L), role, bone, rot=(e.x, e.y, e.z), seg=seg, r2=(r1 / r0 if r0 > 1e-6 else 0.0))


# ---- head
sx_ = 1
fem = P["sex"] == "f"
prim("cyl", (HC.x, hy - hr * 0.5, hz - hr * 0.2), (0.0, 0.0, 0.0), "skin")  # placeholder (zero size) to ensure skin acc exists
acc.pop(("skin", "mixamorig:Head"), None)
# nose
prim("cube", (0, hy - hr * 0.97, hz - 0.012 * hk), (0.026 * hk, 0.036 * hk, 0.052 * hk), "skin", rot=(-0.25, 0, 0))
for sx in (-1, 1):
    prim("sphere", (sx * hr * 0.9, hy + 0.01 * hk, hz - 0.005 * hk), (0.022 * hk * 0.4, 0.022 * hk * 0.8, 0.022 * hk * 1.2), "skin", seg=6)   # ears
    prim("sphere", (sx * 0.04 * hk, hy - hr * 0.88, hz + 0.028 * hk), (0.0165 * hk, 0.0165 * hk * 0.6, 0.0165 * hk * 0.8), "sclera", seg=6)
    prim("sphere", (sx * 0.04 * hk, hy - hr * 0.95, hz + 0.028 * hk), (0.0095 * hk,) * 3, "eyes", seg=6)
    prim("cube", (sx * 0.041 * hk, hy - hr * 0.93, hz + 0.052 * hk), (0.04 * hk, 0.012 * hk, 0.012 * hk), "hair" if P["hair"] != "bald" else "skin", rot=(0, sx * 0.16, 0))
prim("cube", (0, hy - hr * 0.93, hz - 0.058 * hk), (0.06 * hk, 0.012 * hk, 0.012 * hk), "mouth")
if P["fangs"]:
    for sx in (-1, 1):
        limb((sx * 0.018 * hk, hy - hr * 0.94, hz - 0.052 * hk), (sx * 0.018 * hk, hy - hr * 0.96, hz - 0.085 * hk), 0.007 * hk, 0.001, "sclera", seg=4)
hair = P["hair"]
hy_h = hy
if hair == "short":
    prim("sphere", (0, hy_h + 0.018 * hk, hz + 0.028 * hk), (hr * 1.07 * 0.9, hr * 1.07, hr * 1.07 * 1.02), "hair", seg=12)
elif hair == "long":
    prim("sphere", (0, hy_h + 0.02 * hk, hz + 0.025 * hk), (hr * 1.1 * 0.92, hr * 1.1 * 1.02, hr * 1.1 * 1.04), "hair", seg=12)
    limb((0, hy_h + hr * 0.7, hz + 0.02 * hk), (0, hy_h + hr * 0.85, hz - 0.36 * hk), hr * 0.85, hr * 0.55, "hair", seg=8)
elif hair == "bun":
    prim("sphere", (0, hy_h + 0.018 * hk, hz + 0.028 * hk), (hr * 1.07 * 0.9, hr * 1.07, hr * 1.07 * 1.02), "hair", seg=12)
    prim("sphere", (0, hy_h + hr * 0.95, hz + 0.075 * hk), (0.058 * hk,) * 3, "hair", seg=8)
elif hair == "slick":
    prim("sphere", (0, hy_h + 0.028 * hk, hz + 0.018 * hk), (hr * 1.06 * 0.9, hr * 1.06 * 1.03, hr * 1.06 * 0.98), "hair", seg=12)
    limb((0, hy_h + hr * 0.8, hz + 0.05 * hk), (0, hy_h + hr * 1.05, hz - 0.1 * hk), hr * 0.7, hr * 0.45, "hair", seg=8)
if P["beard"] in ("moustache", "full", "pointed"):
    for sx in (-1, 1):
        limb((sx * 0.006, hy - hr * 0.94, hz - 0.045 * hk), (sx * 0.055 * hk, hy - hr * 0.85, hz - 0.052 * hk), 0.012 * hk, 0.006 * hk, "hair", seg=6)
if P["beard"] == "full":
    prim("sphere", (0, hy - 0.045 * hk, hz - 0.1 * hk), (hr * 0.82 * 0.95, hr * 0.82 * 0.9, hr * 0.82 * 1.1), "hair", seg=10)
elif P["beard"] == "pointed":
    limb((0, hy - hr * 0.7, hz - 0.1 * hk), (0, hy - hr * 0.78, hz - 0.2 * hk), 0.04 * hk, 0.005 * hk, "hair", seg=8)

r = hr
hat = P["hat"]
hzz = hz
if hat == "top":
    prim("cyl", (0, hy, hzz + 0.1 * hk), (r * 1.75, r * 1.75, 0.018 * hk), "accent", seg=14)
    prim("cyl", (0, hy, hzz + 0.2 * hk), (r * 1.02, r * 1.02, 0.2 * hk), "accent", seg=14, r2=0.93)
    prim("cyl", (0, hy, hzz + 0.135 * hk), (r * 1.06, r * 1.06, 0.035 * hk), "cloak", seg=14)
elif hat == "bowler":
    prim("cyl", (0, hy, hzz + 0.1 * hk), (r * 1.6, r * 1.6, 0.015 * hk), "accent", seg=14)
    prim("sphere", (0, hy, hzz + 0.115 * hk), (r * 1.05, r * 1.05, r * 1.05 * 0.85), "accent", seg=12)
elif hat == "wide":
    prim("cyl", (0, hy, hzz + 0.095 * hk), (r * 2.5, r * 2.5, 0.012 * hk), "accent", seg=16, r2=0.92)
    prim("cyl", (0, hy, hzz + 0.16 * hk), (r * 1.1, r * 1.1, 0.12 * hk), "accent", seg=12, r2=0.86)
elif hat == "fur":
    prim("cyl", (0, hy, hzz + 0.11 * hk), (r * 1.15, r * 1.15, 0.13 * hk), "accent", seg=10, r2=0.87)
    prim("sphere", (0, hy, hzz + 0.17 * hk), (r * 1.1, r * 1.1, r * 1.1 * 0.5), "accent", seg=10)
elif hat == "cap":
    prim("sphere", (0, hy + 0.005, hzz + 0.075 * hk), (r * 1.08, r * 1.08, r * 1.08 * 0.6), "accent", seg=12)
    prim("cube", (0, hy - r * 1.05, hzz + 0.075 * hk), (r * 1.5, r * 0.9, 0.012 * hk), "accent")
elif hat == "shawl":
    prim("sphere", (0, hy + 0.02 * hk, hzz + 0.02 * hk), (r * 1.12, r * 1.12 * 1.05, r * 1.12), "accent", seg=12)
    prim("sphere", (0, hy + 0.06 * hk, hzz - 0.14 * hk), (r * 1.7 * 1.1, r * 1.7 * 0.8, r * 1.7 * 0.55), "accent", seg=12)
elif hat == "bonnet":
    prim("sphere", (0, hy + 0.03 * hk, hzz + 0.03 * hk), (r * 1.12, r * 1.12 * 1.1, r * 1.12 * 1.05), "accent", seg=12)

# ---- chest details (rigid on the chest bone)
spine2 = bone_world("mixamorig:Spine2")
chest_z = spine2.z - 0.04 * k
rx, ry, ox, oy = slice_extent(chest_z)
fy = oy - ry - 0.012
if P["garment"] in ("coat", "frock"):
    prim("cube", (ox, fy - 0.004, chest_z), (0.075, 0.014, 0.22 * k), "accent", bone="mixamorig:Spine2")
    for i in range(3):
        prim("sphere", (ox, fy - 0.012, chest_z - 0.12 * k + i * 0.07 * k), (0.011 * k,) * 3, "accent", bone="mixamorig:Spine2", seg=6)
    nz = bone_world("mixamorig:Neck").z
    nrx, nry, nox, noy = slice_extent(nz - 0.01, 0.03)
    prim("cube", (nox, noy - nry - 0.01, nz - 0.01), (0.1, 0.05, 0.03 * k), "accent", bone="mixamorig:Neck")
if fem:
    for sx in (-1, 1):
        prim("sphere", (ox + sx * 0.065, fy + 0.02, chest_z - 0.025 * k), (0.05 * k, 0.05 * k * 0.9, 0.05 * k * 0.9), "top", bone="mixamorig:Spine2", seg=8)
# belt / waistband
hips = bone_world("mixamorig:Hips")
bz = hips.z + 0.09 * k
brx, bry, box_, boy = slice_extent(bz)
prim("cyl", (box_, boy, bz), (brx * 1.12, bry * 1.12, 0.035 * k), "accent", bone="mixamorig:Spine", seg=16)
flush_acc()

# ---- hanging cloth (skirt / coat tails / cloak) on chain bones
chain_defs = []


def ring_pos(z, t, a, flare, pad, rscale):
    rx, ry, ox, oy = slice_extent(z)
    rx = max(rx, 0.13) * rscale + pad + flare * (t ** 1.4)
    ry = max(ry, 0.10) * rscale + pad + flare * 0.8 * (t ** 1.4)
    return Vector((ox + rx * math.sin(a), oy - ry * math.cos(a), z))


def adiff(a, b, closed):
    d = a - b
    if closed:
        d = (d + math.pi) % (2 * math.pi) - math.pi
    return abs(d)


def make_cloth(name, z_top, z_bot, a0, a1, cols, rings, chains, parent, flare, pad, closed, role, rscale=1.0):
    verts, rows = [], []
    ncol = cols if closed else cols + 1
    for kk in range(rings + 1):
        t = kk / rings
        z = z_top + (z_bot - z_top) * t
        row = []
        for j in range(ncol):
            a = a0 + (a1 - a0) * (j / cols)
            verts.append(ring_pos(z, t, a, flare, pad, rscale))
            row.append(len(verts) - 1)
        rows.append(row)
    faces = []
    for kk in range(rings):
        for j in range(ncol if closed else ncol - 1):
            j2 = (j + 1) % ncol
            faces.append((rows[kk][j], rows[kk][j2], rows[kk + 1][j2], rows[kk + 1][j]))
    me = bpy.data.meshes.new(name)
    me.from_pydata([MWI @ v for v in verts], [], faces)
    me.update()
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(MATS[role])
    ob = new_skinned(name, me)
    nb = 3
    joints = [round(i * rings / nb) for i in range(nb + 1)]
    ang_c = [a0 + (a1 - a0) * (m / (chains if closed else chains - 1)) for m in range(chains)]
    bpy.context.view_layer.objects.active = arm
    for o in bpy.data.objects:
        o.select_set(o == arm)
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm.data.edit_bones
    par = eb[parent]
    chain_names = []
    for m, ac in enumerate(ang_c):
        pts = [ring_pos(z_top + (z_bot - z_top) * (ji / rings), ji / rings, ac, flare, pad, rscale) for ji in joints]
        cn = []
        for i in range(nb):
            b = eb.new("cloth_%s_c%d_b%d" % (name, m, i))
            b.head = AMI @ pts[i]
            b.tail = AMI @ pts[i + 1]
            b.parent = par if i == 0 else eb[cn[-1]]
            b.use_connect = False
            cn.append(b.name)
        chain_names.append(cn)
    bpy.ops.object.mode_set(mode="OBJECT")
    for cn in chain_names:
        for n in cn:
            ob.vertex_groups.new(name=n)
    step = max(1, joints[1] - joints[0])
    for kk, row in enumerate(rows):
        for j, vi in enumerate(row):
            a = a0 + (a1 - a0) * (j / cols)
            ds = sorted(range(chains), key=lambda m: adiff(ang_c[m], a, closed))
            m1, m2 = ds[0], ds[1]
            d1, d2 = adiff(ang_c[m1], a, closed), adiff(ang_c[m2], a, closed)
            w1 = d2 / (d1 + d2) if d1 + d2 > 1e-6 else 1.0
            for mm, wm in ((m1, w1), (m2, 1 - w1)):
                cn = chain_names[mm]
                if kk == 0:
                    ob.vertex_groups[cn[0]].add([vi], wm, "ADD")
                    continue
                if kk >= joints[-1]:
                    hs = [0.0] * (len(cn) - 1) + [1.0]
                else:
                    hs = [max(0.0, 1 - abs(kk - joints[i]) / step) for i in range(len(cn))]
                tot = sum(hs) or 1.0
                for i, h in enumerate(hs):
                    if h > 0:
                        ob.vertex_groups[cn[i]].add([vi], wm * h / tot, "ADD")
    return ob


g = P["garment"]
z_top = hips.z + 0.02
if g in ("coat", "frock"):
    hem_frac = 0.52 if g == "coat" else 0.36
    make_cloth("skirt", z_top, hips.z - hem_frac * k * 0.9, math.radians(24), math.radians(336), 30, 8, 8, "mixamorig:Hips", 0.05, 0.035, False, "top")
elif g in ("dress", "gown"):
    wide = 0.36 if g == "gown" else 0.28
    make_cloth("skirt", z_top, 0.05 * H, 0.0, 2 * math.pi, 30, 9, 10, "mixamorig:Hips", wide, 0.07, True, "top", 1.15)
if P["cloak"]:
    sp = spine2.z + 0.06
    make_cloth("cape", sp, 0.20 * H, math.radians(105), math.radians(255), 16, 8, 6, "mixamorig:Spine2", 0.12, 0.07, False, "cloak", 0.9)

bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_yup=True, export_apply=False,
                          export_image_format="JPEG", export_animations=False, export_skins=True)
print("EXPORTED", out)
