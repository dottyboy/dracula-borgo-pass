"""Blender: rig a static AI-generated humanoid (image-to-3D GLB, arms by the sides) onto the Mixamo skeleton.

Steps: scale/place the mesh, decimate, pose a Y Bot to the mesh (arms down), copy its skin weights to the mesh by nearest
surface, put the mesh into the Mixamo T pose (the rest pose all shared animations expect) and bind it to a fresh Y Bot
skeleton. Output: skinned GLB with the Mixamo bone names.

blender -b --factory-startup -P rig_ai.py -- <model.glb> "<Y Bot.fbx>" <out.glb> [height_m] [target_tris]
"""
import bpy
import bmesh
import sys
import math
from mathutils import Vector, Matrix

args = sys.argv[sys.argv.index("--") + 1:]
src, botfile, out = args[0], args[1], args[2]
HEIGHT = float(args[3]) if len(args) > 3 else 1.9
TRIS = int(args[4]) if len(args) > 4 else 35000

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
dr = [o for o in bpy.data.objects if o.type == "MESH"][0]
for o in list(bpy.data.objects):
    if o is not dr:
        o.parent = None
dr.parent = None
for o in list(bpy.data.objects):
    if o is not dr and o.type == "EMPTY":
        bpy.data.objects.remove(o, do_unlink=True)
bpy.context.view_layer.objects.active = dr
dr.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
zs = [v.co.z for v in dr.data.vertices]
sc = HEIGHT / (max(zs) - min(zs))
for v in dr.data.vertices:
    v.co = Vector((v.co.x * sc, v.co.y * sc, (v.co.z - min(zs)) * sc))
dr.data.update()
tris0 = sum(len(p.vertices) - 2 for p in dr.data.polygons)
dec = dr.modifiers.new("dec", "DECIMATE")
dec.ratio = min(1.0, TRIS / max(1, tris0))
bpy.ops.object.modifier_apply(modifier="dec")
print("TRIS", tris0, "->", sum(len(p.vertices) - 2 for p in dr.data.polygons))


def import_bot():
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=botfile, use_anim=False)
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        if o.type == "MESH" and o.name.startswith("Cube"):
            bpy.data.objects.remove(o, do_unlink=True)
    arm_ = [o for o in new if o.type == "ARMATURE"][0]
    meshes = [o for o in new if o.type == "MESH" and o.name != "Cube"]
    return arm_, [m for m in meshes if m.name in bpy.data.objects]


# ---- posed bot (weight source)
arm, bmeshes = import_bot()
bot_scale = HEIGHT / 1.8
arm.scale = arm.scale * bot_scale
bpy.context.view_layer.update()
bpy.ops.object.select_all(action="DESELECT")
bpy.context.view_layer.objects.active = arm
orig_rest = {b.name: b.matrix_local.copy() for b in arm.data.bones}
bpy.ops.object.mode_set(mode="POSE")
down = Vector((0, 0, -1))
for side in ("Left", "Right"):
    pb = arm.pose.bones["mixamorig:%sArm" % side]
    v = (arm.matrix_world.to_3x3() @ (pb.tail - pb.head)).normalized()
    # swing the arm down but a little away from the body
    tgt = (down + Vector((0.12 if side == "Left" else -0.12, 0, 0))).normalized()
    rot = v.rotation_difference(tgt).to_matrix().to_4x4()
    wm = arm.matrix_world
    m = wm @ pb.matrix
    loc = m.translation.copy()
    m.translation = Vector()
    m = rot @ m
    m.translation = loc
    pb.matrix = wm.inverted() @ m
    bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode="OBJECT")

# duplicate the bot meshes with the pose applied (they carry the vertex groups)
posed = []
for bm_ in bmeshes:
    bm_.scale = bm_.scale
    dep = bpy.context.evaluated_depsgraph_get()
    ev = bm_.evaluated_get(dep)
    me = bpy.data.meshes.new_from_object(ev)
    ob = bpy.data.objects.new("posed_" + bm_.name, me)
    ob.matrix_world = bm_.matrix_world.copy()
    bpy.context.scene.collection.objects.link(ob)
    for g in bm_.vertex_groups:
        ob.vertex_groups.new(name=g.name)
    # new_from_object keeps vertex weights in the mesh data
    posed.append(ob)
bpy.ops.object.select_all(action="DESELECT")
for o in posed:
    o.select_set(True)
bpy.context.view_layer.objects.active = posed[0]
if len(posed) > 1:
    bpy.ops.object.join()
src_body = bpy.context.view_layer.objects.active
src_body.name = "weights_src"

# ---- transfer weights: bot (posed) -> dracula mesh
names = [g.name for g in src_body.vertex_groups]
for n in names:
    dr.vertex_groups.new(name=n)
bpy.ops.object.select_all(action="DESELECT")
dr.select_set(True)
src_body.select_set(True)
bpy.context.view_layer.objects.active = dr
bpy.ops.object.data_transfer(data_type="VGROUP_WEIGHTS", use_object_transform=True, vert_mapping="POLYINTERP_NEAREST",
                             layers_select_src="ALL", layers_select_dst="NAME", mix_mode="REPLACE", use_create=False)
# smooth + limit + normalise
bpy.context.view_layer.objects.active = dr
bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
bpy.ops.object.vertex_group_smooth(group_select_mode="ALL", factor=0.5, repeat=2)
bpy.ops.object.vertex_group_limit_total(group_select_mode="ALL", limit=4)
bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)
bpy.ops.object.mode_set(mode="OBJECT")

# ---- rest pose of the posed armature := arms down (so the mesh is "bound" in its sculpted pose) ...
md = dr.modifiers.new("Armature", "ARMATURE")
md.object = arm
dr.parent = arm
dr.matrix_parent_inverse = arm.matrix_world.inverted()
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
bpy.ops.pose.select_all(action="SELECT")
bpy.ops.pose.armature_apply(selected=False)          # apply pose as the new rest pose
bpy.ops.object.mode_set(mode="OBJECT")
# ... then pose it back into the Mixamo T pose and bake that into the mesh
bpy.ops.object.mode_set(mode="POSE")
for pb in arm.pose.bones:       # parents come first in this list
    om = orig_rest[pb.name]
    pb.matrix = om
    bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode="OBJECT")
bpy.context.view_layer.objects.active = dr
bpy.ops.object.modifier_apply(modifier="Armature")
dr.parent = None
dr.matrix_world = Matrix.Identity(4)

# ---- clean up the helper rigs and bind to a fresh bot skeleton (original T-pose rest)
for o in list(bpy.data.objects):
    if o is not dr:
        bpy.data.objects.remove(o, do_unlink=True)
arm2, bm2 = import_bot()
arm2.scale = arm2.scale * bot_scale
for o in bm2:
    bpy.data.objects.remove(o, do_unlink=True)
bpy.context.view_layer.update()
dr.parent = arm2
dr.matrix_parent_inverse = arm2.matrix_world.inverted()
md = dr.modifiers.new("Armature", "ARMATURE")
md.object = arm2
dr.name = "AiBody"
bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_yup=True, export_apply=False,
                          export_image_format="JPEG", export_jpeg_quality=90, export_animations=False, export_skins=True)
print("EXPORTED", out)
