#!/usr/bin/env python3
"""Merge book/extract/chapter_NN.json -> book/book_db.json + coverage report.
Entities with the same (case-insensitive) name are merged across chapters, keeping the chapters they appear in."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EX = ROOT / "book" / "extract"
KEYED = {"locations": "name", "characters": "name", "objects": "name", "creatures": "name",
         "vampire_lore": "rule", "asset_candidates": "name"}
LISTS = ["scenes", "puzzles", "combat", "crafting", "dialogue_samples", "quest_hooks"]


def main():
    db = {k: {} for k in KEYED}
    db.update({k: [] for k in LISTS})
    db["chapters"] = []
    files = sorted(EX.glob("chapter_*.json"))
    for f in files:
        ch = json.loads(f.read_text())
        n = ch["chapter"]
        db["chapters"].append({k: ch.get(k) for k in ("chapter", "narrator", "dates", "summary")})
        for k, key in KEYED.items():
            for e in ch.get(k, []):
                name = str(e.get(key, "")).strip()
                if not name:
                    continue
                cur = db[k].setdefault(name.lower(), {**e, "chapters": []})
                if n not in cur["chapters"]:
                    cur["chapters"].append(n)
                for fk, fv in e.items():
                    if fk not in cur or (not cur[fk] and fv):
                        cur[fk] = fv
                    elif isinstance(fv, list) and isinstance(cur[fk], list):
                        cur[fk] += [x for x in fv if x not in cur[fk]]
        for k in LISTS:
            for e in ch.get(k, []):
                db[k].append({"chapter": n, **e} if isinstance(e, dict) else {"chapter": n, "text": e})
    for k in KEYED:
        db[k] = list(db[k].values())
    (ROOT / "book" / "book_db.json").write_text(json.dumps(db, indent=1, ensure_ascii=False))
    print(f"{len(files)} chapter files merged")
    for k in list(KEYED) + LISTS:
        print(f"  {k:<18}{len(db[k]):>5}")
    miss = sorted(set(range(1, 29)) - {c['chapter'] for c in db['chapters']})
    if miss:
        print("missing chapters:", miss)


if __name__ == "__main__":
    main()
