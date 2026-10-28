#!/usr/bin/env python3
"""Objectives and hints for the acts and arcs that have none written by hand.

    python3 pipeline/gen_objectives.py replay_journals.txt

Input: the REPLAYJOURNAL lines the replays print (`godot ... -- --act=N ...` / `--arc=ID`), i.e. the journal entries the
solution path writes, in order. Every such entry becomes one objective ("Visit X", "Talk to Y", "Examine Z") found from where
data/world.json grants it, with three hints: nudge, where, what to do. Keys already present in data/objectives.json (hand-written,
e.g. Act I) are kept untouched. The replays then check that all required objectives are done at the end of the act.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def walk(o, path, found, key="journal"):
    if isinstance(o, dict):
        if isinstance(o.get(key), str):
            found.setdefault(o[key], []).append(path)
        for k, v in o.items():
            walk(v, path + [k], found, key)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + [i], found, key)


def main():
    world = json.load(open(os.path.join(ROOT, "data", "world.json")))
    out_path = os.path.join(ROOT, "data", "objectives.json")
    objectives = json.load(open(out_path)) if os.path.exists(out_path) else {}
    locname = {l["id"]: l["name"] for l in world["locations"]}
    found = {}
    walk(world["loc_data"], ["loc_data"], found)
    walk(world["dialogue"], ["dialogue"], found)
    talk_npc = {}                       # dialogue id -> (location, speaker name): any NPC or prop with a "talk"
    def find_talk(o, loc, name):
        if isinstance(o, dict):
            nm = o.get("name") or name
            if isinstance(o.get("talk"), str):
                talk_npc.setdefault(o["talk"], (loc, nm or o.get("id", "")))
            for v in o.values():
                find_talk(v, loc, nm)
        elif isinstance(o, list):
            for v in o:
                find_talk(v, loc, name)
    for lid, ld in world["loc_data"].items():
        find_talk(ld, lid, None)
    for line in open(sys.argv[1]):
        m = re.match(r"REPLAYJOURNAL (\S+) ?(.*)", line.strip())
        if not m:
            continue
        key, ids = m.group(1), [i for i in m.group(2).split(",") if i]
        if key in objectives:
            continue
        lst = []
        for jid in ids:
            if jid not in world["journal"] or any(o["id"] == "o_" + jid for o in lst):
                continue
            title = world["journal"][jid]["title"]
            src = found.get(jid, [])
            text, where, what = title, "", ""
            if src:
                p = src[0]
                if p[0] == "loc_data":
                    loc = p[1]
                    ld = world["loc_data"][loc]
                    nm = locname.get(loc, loc)
                    if p[2] == "on_enter":
                        text, where, what = f"Visit {nm}", f"It is in {nm}.", f"Go to {nm}."
                    elif p[2] == "props":
                        prop = ld["props"][p[3]]
                        pn = prop.get("name") or prop["id"]
                        text, where, what = f"Examine {pn}", f"Look around {nm}.", f"Examine {pn} in {nm}."
                    elif p[2] == "npcs":
                        npc = ld["npcs"][p[3]]
                        pn = npc.get("name") or npc["id"]
                        text, where, what = f"Talk to {pn}", f"Look for someone in {nm}.", f"Talk to {pn} in {nm}."
                elif p[0] == "dialogue":
                    d = p[1]
                    if d in talk_npc:
                        loc, pn = talk_npc[d]
                        nm = locname.get(loc, loc)
                        text, where, what = f"Talk to {pn}", f"Someone in {nm} has something to say.", f"Talk to {pn} in {nm}."
            if not where:
                text, where, what = f"Find out: {title}", "Keep exploring and talking to people.", f"Look for what the journal entry '{title}' is about."
            lst.append({"id": "o_" + jid, "text": text, "done": "journal:" + jid,
                        "hints": ["Try the places you have not been to yet, and talk to everyone.", where, what]})
        merged = []                    # the same task twice (two beats at one NPC): one objective, done when both are
        for o in lst:
            same = next((m for m in merged if m["text"] == o["text"]), None)
            if same:
                same["done"] += "&" + o["done"]
            else:
                merged.append(o)
        objectives[key] = merged
        print(key, len(merged), "objectives")
    json.dump(objectives, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
