#!/usr/bin/env python3
"""One-shot asset build:  python3 pipeline/build_assets.py [--force] [--only id ...]

1. bible_src.py      -> world_bible.json
2. extract_book.py   -> book/chapters + entity_index.json
3. texture_gen.py    -> assets/textures/*.png
4. blender_gen.py    -> assets/models/*.glb (+ assets/blend/*.blend)
5. manifest          -> data/manifest.json (models, slots, resolved variants, textures)
                        data/world.json    (locations, items, dialogue for the game)
Models that already exist on disk are kept unless --force is given.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPE = ROOT / "pipeline"
BLENDER = os.environ.get("BLENDER", str(Path.home() / "Programi/blender-5.2.1/blender"))


def run(*cmd):
    print("$", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True, cwd=ROOT)


def main():
    force = "--force" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else []
    run(sys.executable, PIPE / "bible_src.py")
    run(sys.executable, PIPE / "systems_src.py")
    run(sys.executable, PIPE / "extract_book.py")
    run(sys.executable, PIPE / "texture_gen.py", *(["--force"] if force else []))
    bible = json.loads((PIPE / "world_bible.json").read_text())
    todo = only or [a["id"] for a in bible["assets"]
                    if force or not (ROOT / "assets/models" / f"{a['id']}.glb").exists()]
    if todo:
        run(BLENDER, "-b", "--factory-startup", "-P", PIPE / "blender_gen.py", "--", *todo)
    make_manifest(bible)


def make_manifest(bible):
    slots = {f.stem: json.loads(f.read_text()) for f in (ROOT / "assets/models/_slots").glob("*.json")}
    tex = json.loads((ROOT / "assets/textures/_textures.json").read_text())
    models = {}
    for a in bible["assets"]:
        i = a["id"]
        s = slots[i]
        variants = {}
        dflt = bible["variants"][i]["default"]
        default_name = dflt if isinstance(dflt, str) else "default"       # a variant literally named "default" collides with the pointer key
        for vname, ov in bible["variants"][i].items():
            if vname == "default" and isinstance(ov, str):
                continue
            variants[vname] = {slot: ov.get(slot, bible["role_defaults"].get(slot, {"tex": "flat", "tint": "#ffffff"}))
                               for slot in s["slots"]}
        models[i] = {"file": f"assets/models/{i}.glb", "slots": s["slots"], "parts": s["parts"],
                     "default": default_name, "variants": variants}
    bad = [(i, v, r["tex"]) for i, m in models.items() for v, d in m["variants"].items()
           for r in d.values() if r["tex"] not in tex]
    assert not bad, f"unknown textures: {bad[:5]}"
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/manifest.json").write_text(json.dumps({"models": models, "textures": tex}, indent=1))
    world = {k: bible[k] for k in ("title", "items", "loc_data", "dialogue", "start_location", "locations", "characters", "palettes", "placements", "gates", "journal", "encounter_hooks", "acts", "arcs_list")}
    (ROOT / "data/world.json").write_text(json.dumps(world, indent=1, ensure_ascii=False))
    nv = sum(len(m["variants"]) for m in models.values())
    print(f"manifest: {len(models)} models, {nv} model/texture variants, {len(tex)} textures")


if __name__ == "__main__":
    main()
