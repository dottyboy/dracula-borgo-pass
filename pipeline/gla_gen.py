"""Blender side of the seeded places (run headless):

    blender -b --factory-startup -P pipeline/gla_gen.py -- --addon /path/levelArchitect_v2.py --kind crypt --seed 7 --out /tmp/x/crypt_s7

Loads Game Level Architect, applies the recipe for a kind of place, generates all steps with the seed and writes
<out>.glb + <out>.json (an Architect game package). pipeline/bake_places.py calls it for every variant.
"""
import importlib.util, os, sys
import bpy

# recipes: scene settings per kind of place (the numbers the hand-made dungeons used: 3 m tiles, 4.5 m levels)
BASE = dict(wfc_width=12, wfc_length=12, wfc_height=1, wfc_rooms_min=4, wfc_rooms_max=4, wfc_room_size_min=3, wfc_room_size_max=4,
            wfc_room_shape='MIXED', wfc_room_shape_sides=10, wfc_sub_levels_per_floor=1, wfc_split_level_chance=0.0,
            wfc_elevation_chance=0.0, wfc_elevation_range=0.0, wfc_tile_size=3.0, wfc_level_height=4.5, wfc_wall_height=3.6,
            wfc_wall_thickness=0.3, wfc_door_height=2.4, wfc_add_ceiling=False, wfc_iso_mode=True, wfc_torch_chance=0.6, wfc_torch_light_chance=1.0,
            wfc_prop_chance=0.5, wfc_organic_amount=0.0)
FLOORS2 = dict(wfc_height=2, wfc_rooms_min=4, wfc_rooms_max=6, wfc_room_size_min=3, wfc_room_size_max=5, wfc_room_shape='RECT',
               wfc_stairs_per_level=1, wfc_stair_bend_chance=0.0, wfc_wall_grouping='PER_FLOOR', wfc_door_grouping='PER_FLOOR')
KINDS = {"crypt": {}, "undercroft": {"wfc_room_shape": 'RECT'}, "cellar": {"wfc_room_shape": 'RECT', "wfc_prop_chance": 0.6},
         "cellar2": FLOORS2, "catacombs2": {**FLOORS2, "wfc_prop_chance": 0.6}}


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    opt = {argv[i][2:]: argv[i + 1] for i in range(0, len(argv) - 1, 2)}
    spec = importlib.util.spec_from_file_location("levelArchitect_v2", opt["addon"])
    mod = importlib.util.module_from_spec(spec)
    sys.modules["levelArchitect_v2"] = mod
    spec.loader.exec_module(mod)
    mod.register()
    scene = bpy.context.scene
    if opt["kind"] == "castle":     # a ruined castle: size and ruin vary with the seed, towers/wall as the hand-made one
        import random
        rnd = random.Random(int(opt["seed"]))
        scene.wfc_castle_width, scene.wfc_castle_depth = rnd.uniform(22, 30), rnd.uniform(18, 24)
        scene.wfc_castle_wall_height, scene.wfc_castle_wall_thickness = 7.0, 1.5
        scene.wfc_castle_tower_radius, scene.wfc_castle_tower_height = 3.2, 12.0
        scene.wfc_castle_gate, scene.wfc_castle_keep, scene.wfc_castle_ruin = True, True, rnd.uniform(0.4, 0.65)
        scene.wfc_castle_hall_props = False
        scene.wfc_seed = int(opt["seed"])
        assert 'FINISHED' in bpy.ops.object.generate_level_castle()
        out = opt["out"]
        os.makedirs(os.path.dirname(out), exist_ok=True)
        assert 'FINISHED' in bpy.ops.object.export_castle_package(filepath=out + ".glb")
        print("gla_gen done", out)
        return
    for k, v in {**BASE, **KINDS[opt["kind"]]}.items():
        setattr(scene, k, v)
    scene.wfc_random_seed = False
    scene.wfc_seed = int(opt["seed"])
    r = bpy.ops.object.generate_all_steps()
    assert 'FINISHED' in r, r
    out = opt["out"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    per_floor = scene.wfc_height > 1
    if per_floor:        # one package per floor: <out>_f0, <out>_f1 ...
        bp = bpy.data.objects[mod.BLUEPRINT_OBJECT_NAME]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bp
        bp.select_set(True)
        assert 'FINISHED' in bpy.ops.object.separate_level_by_floor()
    r = bpy.ops.object.export_game_package(filepath=out + ".glb", per_floor=per_floor)
    assert 'FINISHED' in r, r
    print("gla_gen done", out)


main()
