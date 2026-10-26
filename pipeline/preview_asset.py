"""Render a quick PNG preview of generated assets (run in Blender):
   blender -b --factory-startup -P pipeline/preview_asset.py -- <asset_id> [<asset_id> ...]
Writes /tmp/asset_previews/<id>.png from assets/blend/<id>.blend (flat grey shading, shape check only)."""
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent
OUT = Path("/tmp/asset_previews")
OUT.mkdir(exist_ok=True)
for aid in sys.argv[sys.argv.index("--") + 1:]:
    bpy.ops.wm.open_mainfile(filepath=str(ROOT / "assets" / "blend" / f"{aid}.blend"))
    sc = bpy.context.scene
    pts = [o.matrix_world @ Vector(c) for o in sc.objects if o.type == "MESH" for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    c, size = (lo + hi) / 2, max((hi - lo).length, 0.3)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    cam.location = c + Vector((-0.8, -1.0, 0.6)).normalized() * size * 1.3
    cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.rotation_euler = (0.9, 0.2, 0.6)
    sc.collection.objects.link(sun)
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "STUDIO"
    sc.display.shading.color_type = "MATERIAL"
    sc.render.resolution_x = sc.render.resolution_y = 480
    sc.world = bpy.data.worlds.new("w")
    sc.world.color = (0.12, 0.12, 0.15)
    sc.render.filepath = str(OUT / f"{aid}.png")
    bpy.ops.render.render(write_still=True)
    print("preview", OUT / f"{aid}.png")
