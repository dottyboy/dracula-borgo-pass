"""Blender: export Mixamo characters and the shared animation library as GLB for Godot.

blender -b --factory-startup -P export_mixamo.py -- char "<Character FBX>" <out.glb> [tex_size]
blender -b --factory-startup -P export_mixamo.py -- lib  "<Rig FBX>" <out.glb>      (all clips from clips.json)
"""
import bpy, sys, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[sys.argv.index("--") + 1:]
mode = args[0]


def import_fbx(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path, use_anim=True)
    return [o for o in bpy.data.objects if o not in before]


def drop_junk(objs):
    for o in objs:
        if o.type == "MESH" and o.name.startswith("Cube"):
            bpy.data.objects.remove(o, do_unlink=True)


def export(out, **kw):
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_yup=True, export_apply=False,
                              export_image_format="JPEG", export_jpeg_quality=88, **kw)


if mode == "char":
    path, out = args[1], args[2]
    size = int(args[3]) if len(args) > 3 else 1024
    objs = import_fbx(path)
    drop_junk(objs)
    for img in bpy.data.images:
        if img.size[0] > size:
            img.scale(size, size)
    export(out, export_animations=False, export_skins=True)
    print("EXPORTED", out)
else:
    rig, out = args[1], args[2]
    objs = import_fbx(rig)
    arm = [o for o in objs if o.type == "ARMATURE"][0]
    for o in objs:
        if o.type == "MESH":
            bpy.data.objects.remove(o, do_unlink=True)
    for a in list(bpy.data.actions):
        bpy.data.actions.remove(a)
    clips = json.load(open(os.path.join(HERE, "clips.json")))
    arm.animation_data_create()
    for name, rel in clips.items():
        new = import_fbx(os.path.join(HERE, "clean", rel + ".fbx"))
        tmp = [o for o in new if o.type == "ARMATURE"][0]
        act = tmp.animation_data.action
        act.name = name
        slot = act.slots[0]
        tr = arm.animation_data.nla_tracks.new()
        tr.name = name
        st = tr.strips.new(name, int(act.frame_range[0]), act)
        st.action_slot = slot
        for o in new:
            bpy.data.objects.remove(o, do_unlink=True)
    for o in bpy.data.objects:
        o.select_set(o == arm)
    export(out, export_animations=True, export_animation_mode="NLA_TRACKS", export_skins=True,
           export_nla_strips=True, export_force_sampling=True, export_frame_step=1,
           use_selection=True)
    print("EXPORTED", out, len(clips))
