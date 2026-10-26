#!/usr/bin/env python3
"""Import a Game Level Architect export into this project as a playable dungeon.

    python3 pipeline/import_dungeon.py /path/to/level.glb crypt [options]

Takes level.glb + level.json (Architect: Export tab -> "Export Game Package", or the Castle tab's "Export Castle
Package"), copies them to assets/dungeons/dungeon_crypt.glb and data/dungeons/dungeon_crypt.json and runs
`godot --headless --import`. Play it with:   godot --path . -- --loc=dungeon_crypt

Options
  --ambient "#5a463c,0.9,#0b0707"   ambient colour, energy, fog colour
  --from chapel_crypt:5.0,-3.0      add a door prop to that story location (x,z) leading into the dungeon; walking back onto
                                    the entrance tile returns there
  --from-name "Narrow stair"        label of that door
  --exit-to some_location           the level's exit tile leads on to this location
  --sky night                       sky panorama for outdoor packages (castle)
  --no-lights                       drop the package's lights (a daylight place)
  --no-moon                         outdoor: no moon prop
  --no-import                       skip the godot import step
"""
import argparse, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GODOT = os.path.expanduser("~/Programi/godot4/Godot_v4.7.1-stable_linux.x86_64")


def siblings(glb):
    """For a per-floor package (<stem>_f0, <stem>_f1 ...) all floors in order; else just the one."""
    stem, _ = os.path.splitext(glb)
    m = re.match(r"^(.*)_f(\d+)$", stem)
    if not m:
        return [glb]
    found = []
    k = 0
    while os.path.isfile(f"{m.group(1)}_f{k}.glb") and os.path.isfile(f"{m.group(1)}_f{k}.json"):
        found.append(f"{m.group(1)}_f{k}.glb")
        k += 1
    return found or [glb]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("glb")
    ap.add_argument("name")
    ap.add_argument("--ambient")
    ap.add_argument("--from", dest="from_loc")
    ap.add_argument("--from-name", default="A way down")
    ap.add_argument("--exit-to")
    ap.add_argument("--sky")
    ap.add_argument("--no-lights", action="store_true")
    ap.add_argument("--no-moon", action="store_true")
    ap.add_argument("--no-import", action="store_true")
    a = ap.parse_args()
    files = siblings(a.glb)
    multi = len(files) > 1 or "_f" in os.path.basename(a.glb)
    pkgs = []
    for g in files:
        js = os.path.splitext(g)[0] + ".json"
        if not os.path.isfile(g) or not os.path.isfile(js):
            print("need both", g, "and", js)
            return 1
        with open(js) as fh:
            pkg = json.load(fh)
        if not str(pkg.get("format", "")).startswith("gla-export/"):
            print("not a Level Architect export")
            return 1
        pkgs.append((g, pkg))
    ids = []
    for i, (g, pkg) in enumerate(pkgs):
        k = pkg.get("floor_index")
        ids.append(f"dungeon_{a.name}_f{k if k is not None else i}" if multi else "dungeon_" + a.name)
    by_floor = {pkg.get("floor_index", i): ids[i] for i, (g, pkg) in enumerate(pkgs)}
    os.makedirs(os.path.join(ROOT, "assets", "dungeons"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "data", "dungeons"), exist_ok=True)
    for i, (g, pkg) in enumerate(pkgs):
        did = ids[i]
        if a.ambient:
            col, en, fog = a.ambient.split(",")
            pkg["ambient"] = {"color": col, "energy": float(en), "fog": fog}
        elif not pkg.get("ambient") and pkg.get("interior", True):
            pkg["ambient"] = {"color": "#5a463c", "energy": 0.9, "fog": "#0b0707"}
        first = i == 0
        if a.from_loc and first:
            loc, xz = a.from_loc.split(":")
            x, z = [float(v) for v in xz.split(",")]
            pkg["entrance_from"] = {"loc": loc, "pos": [x, z], "name": a.from_name, "look": "A passage leading down into the dark."}
        if a.exit_to and pkg.get("exit"):
            pkg.setdefault("links", {})["exit_to"] = a.exit_to
        if a.sky:
            pkg["sky"] = a.sky
        if a.no_lights:
            pkg["lights"] = []
        if a.no_moon:
            pkg["moon"] = False
        # stair links -> this location's triggers (stairs_out) and the neighbours' spawn points (arrivals)
        pkg["stairs_out"] = []
        for lk in pkg.get("stair_links", []):
            rec = lk["up"] if lk["direction"] == "up" else lk["down"]
            pkg["stairs_out"].append({"trigger": [rec["trigger"][0], rec["trigger"][2]], "arrive": [rec["arrive"][0], rec["arrive"][2]],
                                      "to": by_floor[lk["to_floor"]]})
        pkg["glb"] = did + ".glb"
        pkg["id"] = did
    for i, (g, pkg) in enumerate(pkgs):
        for st in pkg["stairs_out"]:
            target = next(p for j, (gg, p) in enumerate(pkgs) if ids[j] == st["to"])
            target.setdefault("arrivals", {})[ids[i]] = st["arrive"]
    for i, (g, pkg) in enumerate(pkgs):
        did = ids[i]
        shutil.copy(g, os.path.join(ROOT, "assets", "dungeons", did + ".glb"))
        with open(os.path.join(ROOT, "data", "dungeons", did + ".json"), "w") as fh:
            json.dump(pkg, fh, indent=1)
        rects = sum(len(f["walk_rects"]) for f in pkg["floors"])
        print(f"imported {did}: {rects} walk rectangles, {len(pkg['lights'])} lights, entrance={pkg['entrance'] is not None}, stairs={len(pkg['stairs_out'])}")
    if not a.no_import and os.path.exists(GODOT):
        subprocess.run([GODOT, "--headless", "--path", ROOT, "--import"], check=False, capture_output=True)
        print("godot import done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
