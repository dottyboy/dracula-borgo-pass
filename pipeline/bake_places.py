#!/usr/bin/env python3
"""Bake seed variants of the generated places with Game Level Architect (needs Blender + the add-on).

    python3 pipeline/bake_places.py --addon /path/levelArchitect_v2.py [--variants 4] [--only crypt]

For every single-floor place below writes <id>__v1 ... <id>__vN (glb + json) next to the hand-picked original, which stays
variant 0. The game picks one by world seed (Dungeon.variant_id). A candidate is kept only when entrance and exit are
connected and it has enough rooms; otherwise the next seed is tried. Story, ambient and door hooks come from the original.
"""
import argparse, json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLENDER = os.path.expanduser("~/Programi/blender-5.2.2/blender")
GODOT = os.path.expanduser("~/Programi/godot4/Godot_v4.7.1-stable_linux.x86_64")
PLACES = {"dungeon_crypt": "crypt", "dungeon_abbey_undercroft": "undercroft", "dungeon_asylum_cellar": "cellar",
          "dungeon_carfax_cellar": "cellar2", "dungeon_kingstead_catacombs": "catacombs2",
          "dungeon_castle_ruin": "castle"}   # the last two have floors _f0, _f1
MULTI = ('cellar2', 'catacombs2')
KEEP = ("ambient", "entrance_from", "links", "interior", "sky", "moon")


def connected(pkg):
    """Entrance and exit lie in one walkable area (flood fill over the walk rectangles' cells)."""
    ts = float(pkg["tile_size"])
    cells = set()
    for fl in pkg["floors"]:
        for x0, z0, x1, z1 in fl["walk_rects"]:
            for i in range(round(min(x0, x1) / ts + 0.5), round(max(x0, x1) / ts - 0.5) + 1):
                for j in range(round(min(z0, z1) / ts + 0.5), round(max(z0, z1) / ts - 0.5) + 1):
                    cells.add((i, j))
    if not pkg.get("entrance") or not pkg.get("exit"):
        return False
    def cell(p):
        return (round(p[0] / ts), round(p[2] / ts))
    a, b = cell(pkg["entrance"]["pos"]), cell(pkg["exit"]["pos"])
    if a not in cells or b not in cells:
        return False
    seen, todo = {a}, [a]
    while todo:
        i, j = todo.pop()
        for n in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if n in cells and n not in seen:
                seen.add(n)
                todo.append(n)
    return b in seen


def whole(pkg):
    """All walkable cells of the floor form one area."""
    ts = float(pkg["tile_size"])
    cells = set()
    for x0, z0, x1, z1 in pkg["floors"][0]["walk_rects"]:
        for i in range(round(min(x0, x1) / ts + 0.5), round(max(x0, x1) / ts - 0.5) + 1):
            for j in range(round(min(z0, z1) / ts + 0.5), round(max(z0, z1) / ts - 0.5) + 1):
                cells.add((i, j))
    start = next(iter(cells))
    seen, todo = {start}, [start]
    while todo:
        i, j = todo.pop()
        for n in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if n in cells and n not in seen:
                seen.add(n)
                todo.append(n)
    return len(seen) == len(cells)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--addon", required=True)
    ap.add_argument("--variants", type=int, default=4)
    ap.add_argument("--only")
    a = ap.parse_args()
    tmp = os.path.join(ROOT, "build", "places")
    os.makedirs(tmp, exist_ok=True)
    for pid, kind in PLACES.items():
        if a.only and a.only != kind:
            continue
        multi = kind in MULTI
        ids = [f"{pid}_f{k}" for k in range(2)] if multi else [pid]
        bases = [json.load(open(os.path.join(ROOT, "data", "dungeons", b + ".json"))) for b in ids]
        made, seed = 0, 100 + 1000 * list(PLACES).index(pid)
        while made < a.variants and seed < 600 + 1000 * list(PLACES).index(pid):
            seed += 1
            out = os.path.join(tmp, f"{kind}_{seed}")
            subprocess.run([BLENDER, "-b", "--factory-startup", "-P", os.path.join(ROOT, "pipeline", "gla_gen.py"), "--",
                            "--addon", a.addon, "--kind", kind, "--seed", str(seed), "--out", out], check=True, capture_output=True)
            pkgs = [json.load(open(out + (f"_f{k}" if multi else "") + ".json")) for k in range(len(ids))]
            if multi:
                ok = all(len(p["rooms"]) >= 2 and whole(p) for p in pkgs) and all(p.get("stair_links") for p in pkgs) \
                    and pkgs[0].get("entrance") and pkgs[-1].get("exit")
            else:
                ok = len(pkgs[0]["rooms"]) >= 3 and (kind == "castle" or connected(pkgs[0]))
            if not ok:
                print(f"{pid}: seed {seed} rejected")
                continue
            made += 1
            for k, (pkg, base) in enumerate(zip(pkgs, bases)):
                vid = f"{ids[k]}__v{made}"
                for key in KEEP:
                    if key in base:
                        pkg[key] = base[key]
                if "lights" in base and not base["lights"]:      # a daylight place stays unlit
                    pkg["lights"] = []
                pkg["glb"], pkg["id"] = vid + ".glb", ids[k]
                if multi:        # stairs refer to the floors by their base ids; the game resolves the variant
                    pkg["stairs_out"], pkg["arrivals"] = [], {}
                    for lk in pkg.get("stair_links", []):
                        rec = lk["up"] if lk["direction"] == "up" else lk["down"]
                        pkg["stairs_out"].append({"trigger": [rec["trigger"][0], rec["trigger"][2]], "arrive": [rec["arrive"][0], rec["arrive"][2]],
                                                  "to": ids[lk["to_floor"]]})
                    for lk in pkg.get("stair_links", []):
                        other = pkgs[lk["to_floor"]]
                        for l2 in other.get("stair_links", []):
                            if l2["to_floor"] == k:
                                rec2 = l2["up"] if l2["direction"] == "up" else l2["down"]
                                pkg["arrivals"][ids[lk["to_floor"]]] = [rec2["arrive"][0], rec2["arrive"][2]]
                shutil.copy(out + (f"_f{k}" if multi else "") + ".glb", os.path.join(ROOT, "assets", "dungeons", vid + ".glb"))
                json.dump(pkg, open(os.path.join(ROOT, "data", "dungeons", vid + ".json"), "w"), indent=1)
            print(f"{pid}__v{made}: seed {seed}, {sum(p['floors'][0]['cells'] for p in pkgs)} cells, {sum(len(p['rooms']) for p in pkgs)} rooms")
    if os.path.exists(GODOT):
        subprocess.run([GODOT, "--headless", "--path", ROOT, "--import"], check=False, capture_output=True)
        print("godot import done")


if __name__ == "__main__":
    sys.exit(main())
