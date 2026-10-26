#!/usr/bin/env python3
"""Static checks + solvability simulation for one story act.

    python3 pipeline/validate_story.py --act 2 [--seed-options] [--plan data/plans/act_2.json]

* Loads the base world (bible_src) plus ONLY that act (env ONLY_ACT), so acts can be authored in parallel.
* Static checks: ids, assets/variants, items, flags, dialogue graph, encounters, journal, coordinates.
* Simulation: monotone closure from ACT["start"] (flags/items only grow; negative conditions are treated optimistically).
  It follows exactly the engine's rules (scripts/location.gd _primary order: fight > talk > end_text > go > take > set;
  use_item; on_enter; dialogue branches) and must reach ACT["exit_to"] (a location id, or "END" for the last act).
* Writes a replayable plan (list of actions) that `godot -- --replay=act_N.json` executes in the real engine.
Exit code 0 only if there are no errors and the exit is reachable.
"""
import copy
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))

KNOWN_DO = {"say", "give", "take", "set", "unset", "goto", "talk", "card", "journal", "recruit", "protagonist", "heal", "fight", "end", "meet", "stat", "arc_end"}
TEXTURES = {p.name.replace("_albedo.png", "") for p in (ROOT / "assets/textures").glob("*_albedo.png")}


class V:
    def __init__(self):
        self.errors, self.warns = [], []

    def err(self, m):
        self.errors.append(m)

    def warn(self, m):
        self.warns.append(m)


def load(act, arc=None):
    os.environ["ONLY_ACT"] = str(act)
    if arc:
        os.environ["ONLY_ARC"] = arc
        os.environ["ONLY_ACT"] = "none"
    import importlib
    import bible_src
    importlib.reload(bible_src)
    import systems_src
    importlib.reload(systems_src)
    return bible_src.BIBLE, systems_src.SYSTEMS


# ------------------------------------------------------------------ conditions
def cond_names(c):
    out = []
    for part in str(c or "").split("&"):
        part = part.strip().lstrip("!")
        if part:
            out.append(part)
    return out


def parse_cond(part):
    part = part.strip().lstrip("!")
    for pre in ("has:", "flag:", "journal:", "party:", "prot:", "roster:", "meta:"):
        if part.startswith(pre):
            return pre[:-1], part[len(pre):]
    return "flag", part


class State:
    def __init__(self, start=None):
        start = start or {}
        self.flags = set(start.get("flags", []))
        it = start.get("items", {})
        self.items = dict(it) if isinstance(it, dict) else {k: 1 for k in it}
        self.journal = set()
        self.party = set(start.get("party", []))
        self.roster = set(start.get("party", []))
        self.prot = start.get("protagonist", "")

    def clone(self):
        c = State()
        c.flags, c.items, c.journal, c.party, c.prot = set(self.flags), dict(self.items), set(self.journal), set(self.party), self.prot
        return c

    def ok(self, cond):
        for part in str(cond or "").split("&"):
            part = part.strip()
            if not part:
                continue
            neg = part.startswith("!")
            kind, name = parse_cond(part)
            if kind == "has":
                r = self.items.get(name, 0) > 0
            elif kind == "journal":
                r = name in self.journal
            elif kind == "party":
                r = name in self.party
            elif kind == "prot":
                r = self.prot == name
            elif kind == "roster":
                r = name in self.roster
            elif kind == "meta":
                r = True
            else:
                r = name in self.flags
            if r == neg:
                return False
        return True

    def apply(self, dolist):
        """Engine semantics of Game.run for state-changing verbs (order matters: protagonist etc.)."""
        for a in dolist:
            if "give" in a:
                self.items[a["give"]] = self.items.get(a["give"], 0) + 1
            if "take" in a:
                self.items[a["take"]] = max(0, self.items.get(a["take"], 0) - 1)
                if self.items[a["take"]] == 0:
                    del self.items[a["take"]]
            if "set" in a:
                self.flags.add(a["set"])
            if "unset" in a:
                self.flags.discard(a["unset"])
            if "journal" in a:
                self.journal.add(a["journal"])
            if "recruit" in a:
                self.party.add(a["recruit"])
                self.roster.add(a["recruit"])
            if "meet" in a:
                self.roster.add(a["meet"])
            if "protagonist" in a:
                self.prot = a["protagonist"]


# ------------------------------------------------------------------ static checks
def static_checks(v, bible, systems, act):
    ids_assets = {a["id"] for a in bible["assets"]}
    locs = bible["loc_data"]
    items = dict(bible["items"])
    sys_items = systems["items"]
    dialogues = bible["dialogue"]
    mine = set(act_locations(bible, act))
    for lid in mine:
        ld = locs[lid]
        if not any(m["id"] == lid for m in bible["locations"]):
            v.err(f"{lid}: no entry in LOCATIONS (name/desc)")
        for k in ("cells", "wall", "floor", "ambient", "camera", "lights", "spawn", "props", "interior"):
            if k not in ld:
                v.err(f"{lid}: missing key {k}")
        if "cells" not in ld:
            continue
        w, d = ld["cells"][0] * 4, ld["cells"][1] * 4
        if ld.get("wall") not in bible["variants"].get("wall_4", {}) or ld.get("floor") not in bible["variants"].get("floor_4x4", {}):
            v.err(f"{lid}: wall/floor variant unknown ({ld.get('wall')}/{ld.get('floor')})")
        seen = set()
        for p in ld.get("props", []) + ld.get("npcs", []):
            if p["id"] in seen:
                v.err(f"{lid}: duplicate entity id {p['id']}")
            seen.add(p["id"])
            if p["asset"] not in ids_assets:
                v.err(f"{lid}.{p['id']}: unknown asset {p['asset']}")
            elif p["variant"] not in bible["variants"][p["asset"]]:
                v.err(f"{lid}.{p['id']}: unknown variant {p['variant']} for {p['asset']}")
            x, _, z = p["pos"]
            lim = 1.0 if ld.get("interior", True) else 14.0
            if abs(x) > w / 2 + lim or abs(z) > d / 2 + lim:
                v.warn(f"{lid}.{p['id']}: position {x},{z} outside room {w}x{d}")
            for cn in cond_names(p.get("if")):
                pass
        if not ld.get("interior", True) is False and ld.get("walls") is None and ld.get("interior", True):
            v.warn(f"{lid}: interior room without walls")
        for ent in ld.get("props", []) + ld.get("npcs", []):
            it = ent.get("interact", {})
            if "take" in it and it["take"] not in items and it["take"] not in sys_items:
                v.err(f"{lid}.{ent['id']}: take unknown item {it['take']}")
            if "go" in it and it["go"] not in locs and it["go"] != act["exit_to"]:
                v.err(f"{lid}.{ent['id']}: go to unknown location {it['go']}")
            if "talk" in it and it["talk"] not in dialogues:
                v.err(f"{lid}.{ent['id']}: unknown dialogue {it['talk']}")
            if "fight" in it and it["fight"] not in systems["encounters"]:
                v.err(f"{lid}.{ent['id']}: unknown encounter {it['fight']}")
            for item_id, dolist in it.get("use_item", {}).items():
                if item_id not in items and item_id not in sys_items:
                    v.err(f"{lid}.{ent['id']}: use_item unknown item {item_id}")
                check_do(v, bible, systems, f"{lid}.{ent['id']}.use_item", dolist, act)
            for key in ("go_cond",):
                check_cond(v, bible, f"{lid}.{ent['id']}.{key}", it.get(key), act)
            check_cond(v, bible, f"{lid}.{ent['id']}.if", ent.get("if"), act)
        for i, e in enumerate(ld.get("on_enter", [])):
            check_cond(v, bible, f"{lid}.on_enter[{i}].if", e.get("if"), act)
            check_do(v, bible, systems, f"{lid}.on_enter[{i}]", e.get("do", []), act, on_enter=True)
    for i, meta in items.items():
        if "asset" in meta and meta["asset"] not in ids_assets:
            v.err(f"item {i}: unknown asset {meta['asset']}")
    for did, dlg in dialogues.items():
        if did not in act_dialogues(bible, act):
            continue
        if dlg["start"] not in dlg["nodes"]:
            v.err(f"dialogue {did}: start node missing")
        for nid, n in dlg["nodes"].items():
            for k in ("speaker", "text"):
                if k not in n:
                    v.err(f"dialogue {did}.{nid}: missing {k}")
            check_do(v, bible, systems, f"dialogue {did}.{nid}", n.get("do", []), act)
            if "next" in n and n["next"] not in dlg["nodes"]:
                v.err(f"dialogue {did}.{nid}: next -> unknown node {n['next']}")
            for ch in n.get("choices", []):
                if "text" not in ch:
                    v.err(f"dialogue {did}.{nid}: choice without text")
                if "next" in ch and ch["next"] not in dlg["nodes"]:
                    v.err(f"dialogue {did}.{nid}: choice next unknown {ch['next']}")
                check_cond(v, bible, f"dialogue {did}.{nid}.choice", ch.get("cond"), act)
                check_do(v, bible, systems, f"dialogue {did}.{nid}.choice", ch.get("do", []), act)
    for g, opts in bible["gates"].items():
        for o in opts:
            if o["needs"] not in items and o["needs"] not in sys_items:
                v.err(f"gate {g}: needs unknown item {o['needs']}")
    for item, holders in bible["placements"].items():
        if item not in items and item not in sys_items:
            v.err(f"placement: unknown item {item}")
        for h in holders:
            if not any(p["id"] == h["prop"] for ld in locs.values() for p in ld.get("props", [])):
                v.err(f"placement {item}: holder prop {h['prop']} not found")
    for j in act_journal(bible, act):
        e = bible["journal"][j]
        if not all(k in e for k in ("title", "text")):
            v.err(f"journal {j}: needs title and text")
    for enc, hooks in bible["encounter_hooks"].items():
        if enc not in systems["encounters"]:
            v.err(f"encounter hook for unknown encounter {enc}")
        for k, dolist in hooks.items():
            check_do(v, bible, systems, f"hook {enc}.{k}", dolist, act)
    for eid, e in systems["encounters"].items():
        for en in e["enemies"]:
            if en not in systems["enemies"]:
                v.err(f"encounter {eid}: unknown enemy {en}")
    for en, e in systems["enemies"].items():
        if e["model"] not in ids_assets:
            v.err(f"enemy {en}: unknown model {e['model']}")


def resolve_defaults(bible):
    """Default seed resolution (first option of every gate / first holder of every placement), as WorldGen would pick."""
    b = copy.deepcopy(bible)
    for g, opts in b["gates"].items():
        for ld in b["loc_data"].values():
            for p in ld.get("props", []):
                if p["id"] == g:
                    p["interact"]["go_cond"] = opts[0]["cond"]
    for item, holders in b["placements"].items():
        for ld in b["loc_data"].values():
            for p in ld.get("props", []):
                if p.get("interact", {}).get("take") == item:
                    p["interact"].pop("take", None)
        for ld in b["loc_data"].values():
            for p in ld.get("props", []):
                if p["id"] == holders[0]["prop"]:
                    p.setdefault("interact", {})["take"] = item
    return b


def act_locations(bible, act):
    return [k for k in bible["loc_data"] if k not in BASE_LOCS or act["id"] == 1]


def act_dialogues(bible, act):
    return [k for k in bible["dialogue"] if k not in BASE_DIALOGUE or act["id"] == 1]


def act_journal(bible, act):
    return list(bible["journal"].keys())


BASE_LOCS, BASE_DIALOGUE = set(), set()


def check_cond(v, bible, where, cond, act):
    for part in str(cond or "").split("&"):
        part = part.strip()
        if not part:
            continue
        kind, name = parse_cond(part)
        if kind == "has" and name not in bible["items"] and name not in SYSTEMS_ITEMS:
            v.err(f"{where}: condition has:{name} unknown item")
        if kind == "journal" and name not in bible["journal"]:
            v.err(f"{where}: condition journal:{name} unknown entry")
        if kind == "party" and name not in SYSTEMS_PARTY:
            v.err(f"{where}: condition party:{name} unknown member")


SYSTEMS_ITEMS, SYSTEMS_PARTY = {}, {}


def check_do(v, bible, systems, where, dolist, act, on_enter=False):
    for a in dolist:
        for k in a:
            if k not in KNOWN_DO:
                v.err(f"{where}: unknown action verb '{k}'")
        if "give" in a and a["give"] not in bible["items"] and a["give"] not in systems["items"]:
            v.err(f"{where}: give unknown item {a['give']}")
        if "journal" in a and a["journal"] not in bible["journal"]:
            v.err(f"{where}: journal entry {a['journal']} not defined")
        if "recruit" in a and a["recruit"] not in systems["party"]:
            v.err(f"{where}: recruit unknown member {a['recruit']}")
        if "meet" in a and a["meet"] not in systems["party"]:
            v.err(f"{where}: meet unknown member {a['meet']}")
        if "stat" in a and (not isinstance(a["stat"], dict) or a["stat"].get("member") not in systems["party"]):
            v.err(f"{where}: stat needs a dict with a valid member")
        if "protagonist" in a and a["protagonist"] not in systems["party"]:
            v.err(f"{where}: protagonist must be a party member id ({a['protagonist']})")
        if "goto" in a and a["goto"] not in bible["loc_data"] and a["goto"] != act["exit_to"]:
            v.err(f"{where}: goto unknown location {a['goto']}")
        if "talk" in a and a["talk"] not in bible["dialogue"]:
            v.err(f"{where}: talk unknown dialogue {a['talk']}")
        if "fight" in a and a["fight"] not in systems["encounters"]:
            v.err(f"{where}: fight unknown encounter {a['fight']}")
        if on_enter and ("talk" in a or "fight" in a or ("goto" in a and "card" not in a)):
            v.err(f"{where}: on_enter may only use say/card(+goto)/journal/set/give/recruit/protagonist/heal (no talk/fight/bare goto)")


# ------------------------------------------------------------------ simulation
class Sim:
    """Position-aware planner. The player stands in one location; doors (`go` props whose go_cond holds) can be walked,
    one-way transitions strand everything behind them, so the planner finishes the region it can return to
    before moving forward. Effects are monotone (flags/items only grow)."""

    def __init__(self, bible, systems, act):
        self.b, self.s, self.act = bible, systems, act
        self.st = State(act["start"])
        self.cur = act["start"]["location"]
        self.plan = []
        self.done = set()
        self.visited = {self.cur}
        self.reached_exit = False
        self.consumed = set()
        self.reach_ever = {self.cur}

    # ---- walking
    def edges(self, loc):
        out = []
        for ent in self.b["loc_data"][loc].get("props", []):
            it = ent.get("interact", {})
            if "go" in it and self.visible(ent) and self.st.ok(it.get("go_cond", "")) and "talk" not in it and "fight" not in it:
                out.append((it["go"], ent))
        return out

    def bfs(self, src):
        prev = {src: None}
        q = [src]
        while q:
            c = q.pop(0)
            if c not in self.b["loc_data"]:
                continue
            for to, ent in self.edges(c):
                if to not in prev:
                    prev[to] = c
                    q.append(to)
        return prev

    def path(self, src, dst):
        prev = self.bfs(src)
        if dst not in prev:
            return None
        out = []
        c = dst
        while c != src:
            out.append(c)
            c = prev[c]
        return list(reversed(out))

    def arrive(self, loc):
        self.visited.add(loc)
        self.reach_ever.add(loc)
        ld = self.b["loc_data"].get(loc)
        if not ld:
            return
        for i, e in enumerate(ld.get("on_enter", [])):
            key = ("enter", loc, i)
            if key in self.done or not self.st.ok(e.get("if", "")):
                continue
            self.done.add(key)
            self.plan.append({"kind": "enter", "loc": loc, "index": i})
            self.apply(e["do"], loc)
            break

    def walk(self, dst):
        p = self.path(self.cur, dst)
        for n in p or []:
            self.cur = n
            self.arrive(n)

    def visible(self, ent):
        return self.st.ok(ent.get("if", ""))

    # ---- effects
    def apply(self, dolist, loc):
        for a in dolist:
            if "take" in a:
                self.consumed.add(a["take"])
        self.st.apply(dolist)
        for a in dolist:
            if "fight" in a:
                self.win_fight(a["fight"], loc)
            if "end" in a and self.act["exit_to"] == "END":
                self.reached_exit = True
            if "arc_end" in a and self.act["exit_to"] == "ARC_END":
                self.reached_exit = True
        for a in dolist:
            if "goto" in a:
                self.jump(a["goto"])

    def jump(self, target):
        if target == self.act["exit_to"]:
            self.reached_exit = True
        elif target in self.b["loc_data"]:
            self.cur = target
            self.arrive(target)

    def win_fight(self, enc, loc):
        key = f"won:{enc}"
        if key in self.st.flags:
            return
        self.st.flags.add(key)
        self.apply(self.b["encounter_hooks"].get(enc, {}).get("on_win", []), loc)

    # ---- candidate actions at a location
    def candidates(self, loc):
        out = []
        ld = self.b["loc_data"][loc]
        for ent in ld.get("props", []) + ld.get("npcs", []):
            if not self.visible(ent):
                continue
            it = ent.get("interact", {})
            eid = ent["id"]
            for item, dolist in it.get("use_item", {}).items():
                k = ("use", eid, item)
                if self.st.items.get(item, 0) > 0 and k not in self.done:
                    out.append({"key": k, "kind": "use", "loc": loc, "eid": eid, "item": item, "do": dolist})
            k = ("primary", eid)
            if "fight" in it and f"won:{it['fight']}" not in self.st.flags:
                if k not in self.done:
                    out.append({"key": k, "kind": "fight", "loc": loc, "eid": eid, "enc": it["fight"], "do": [{"fight": it["fight"]}]})
                continue
            if "talk" in it:
                out.extend(self.dialogue_candidates(loc, eid, it["talk"]))
                continue
            if "end_text" in it:
                if self.st.ok(it.get("go_cond", "")) and k not in self.done:
                    out.append({"key": k, "kind": "primary", "loc": loc, "eid": eid, "do": [{"end": "x"}]})
                continue
            if "go" in it:
                if self.st.ok(it.get("go_cond", "")):
                    if it["go"] == self.act["exit_to"] and ("go", eid) not in self.done:
                        out.append({"key": ("go", eid), "kind": "door", "loc": loc, "eid": eid, "to": it["go"], "do": [{"goto": it["go"]}], "late": True})
                elif "set" in it and it["set"] not in self.st.flags and k not in self.done:
                    out.append({"key": k, "kind": "primary", "loc": loc, "eid": eid, "do": [{"set": it["set"]}]})
                continue
            if "take" in it:
                if k not in self.done:
                    out.append({"key": k, "kind": "primary", "loc": loc, "eid": eid, "do": [{"give": it["take"]}]})
                continue
            if "set" in it and it["set"] not in self.st.flags and k not in self.done:
                out.append({"key": k, "kind": "primary", "loc": loc, "eid": eid, "do": [{"set": it["set"]}]})
        return out

    def dialogue_candidates(self, loc, eid, did):
        """Exact conversation semantics: state evolves along each path (node/choice `do` take effect immediately, as in
        the engine), conditions are evaluated against that evolving state. Each node (per local state) is expanded once."""
        dlg = self.b["dialogue"][did]
        out = []
        base = self.st
        stack = [(dlg["start"], [], [], base.clone(), ())]
        seen = set()
        steps = 0
        while stack and steps < 1500:
            steps += 1
            nid, path, acc, local, visits = stack.pop()
            if visits.count(nid) >= 2:
                continue
            visits = visits + (nid,)
            n = dlg["nodes"][nid]
            do_n = list(n.get("do", []))
            local = local.clone()
            local.apply(do_n)
            acc2 = acc + do_n
            sig = (nid, frozenset(local.flags - base.flags), frozenset(local.items.items()) ^ frozenset(base.items.items()), frozenset(local.journal - base.journal), local.prot)
            if sig in seen:
                continue
            seen.add(sig)
            if do_n:
                self.add_talk(out, loc, eid, did, path, acc2, nid)
            choices = [c for c in n.get("choices", []) if local.ok(c.get("cond", ""))]
            if not choices:
                if "next" in n:
                    stack.append((n["next"], path, acc2, local, visits))
                continue
            for c in choices:
                p2 = path + [c["text"]]
                do_c = list(c.get("do", []))
                acc3 = acc2 + do_c
                l2 = local.clone()
                l2.apply(do_c)
                if do_c:
                    self.add_talk(out, loc, eid, did, p2, acc3, nid + "/" + c["text"])
                if "next" in c and not c.get("end", False):
                    stack.append((c["next"], p2, acc3, l2, visits))
        return out

    def add_talk(self, out, loc, eid, did, path, dolist, nid=""):
        key = ("dlg", did, nid, tuple(path))
        if key in self.done:
            return
        score = 0
        for a in dolist:
            if "give" in a:
                score += 1
            if "set" in a and a["set"] not in self.st.flags:
                score += 1
            if "journal" in a and a["journal"] not in self.st.journal:
                score += 1
            if "recruit" in a and a["recruit"] not in self.st.party:
                score += 1
            if "goto" in a or "end" in a or "arc_end" in a:
                score += 1
            if "fight" in a and f"won:{a['fight']}" not in self.st.flags:
                score += 1
        if score:
            out.append({"key": key, "kind": "talk", "loc": loc, "eid": eid, "dialogue": did, "path": list(path), "do": dolist, "score": score})

    # ---- planner
    def run(self):
        self.arrive(self.cur)
        for _ in range(600):
            if self.reached_exit:
                break
            prev = self.bfs(self.cur)
            region = set(prev)
            back = {l for l in region if l in self.bfs(l) and self.cur in self.bfs(l)}
            pick = None
            for group, late_ok in ((back, False), (region - back, False), (region, True)):
                best = None
                for l in sorted(group):
                    if l not in self.b["loc_data"]:
                        continue
                    for c in self.candidates(l):
                        if c.get("late") and not late_ok:
                            continue
                        if c.get("late") is None and late_ok and False:
                            continue
                        d = len(self.path(self.cur, l) or []) if l != self.cur else 0
                        key = (d, -c.get("score", 0))
                        if best is None or key < best[0]:
                            best = (key, c)
                if best:
                    pick = best[1]
                    break
            if pick is None:
                break
            self.done.add(pick["key"])
            self.walk(pick["loc"])
            self.plan.append({k: v for k, v in pick.items() if k not in ("key", "do", "late", "score")})
            self.apply(pick["do"], pick["loc"])
        return self.reached_exit

    @property
    def reach(self):
        return self.reach_ever

    @property
    def entered(self):
        return {f"{k[1]}:{k[2]}" for k in self.done if k[0] == "enter"}


def main():
    a = sys.argv[1:]
    arc_id = a[a.index("--arc") + 1] if "--arc" in a else None
    act_n = int(a[a.index("--act") + 1]) if "--act" in a else 1
    bible, systems = load(act_n, arc_id)
    if arc_id:
        arc = next((x for x in bible["arcs_list"] if x["id"] == arc_id), None)
        if arc is None:
            print(f"arc {arc_id} not found (pipeline/acts/arc_{arc_id}.py)")
            sys.exit(2)
        act = dict(id=0, title=arc["title"], start=arc["start"], exit_to="ARC_END")
        act_n = 0
    else:
        act = next((x for x in bible["acts"] if x["id"] == act_n), None)
    v = V()
    if act is None and act_n == 1 and not arc_id:
        act = {"id": 1, "title": "Transylvania", "start": {"location": bible["start_location"], "protagonist": "harker", "party": ["harker"], "items": {}, "flags": []}, "exit_to": "END"}
    if act is None:
        print(f"act {act_n} not found (pipeline/acts/act_{act_n}.py)")
        sys.exit(2)
    global SYSTEMS_ITEMS, SYSTEMS_PARTY
    SYSTEMS_ITEMS, SYSTEMS_PARTY = systems["items"], systems["party"]
    for k in ("id", "title", "start", "exit_to"):
        if k not in act:
            v.err(f"ACT missing key {k}")
    base_bible, _ = None, None
    if act_n != 1:
        os.environ["ONLY_ACT"] = "none"
        os.environ.pop("ONLY_ARC", None)
        import importlib
        import bible_src
        importlib.reload(bible_src)
        BASE_LOCS.update(bible_src.BIBLE["loc_data"].keys())
        BASE_DIALOGUE.update(bible_src.BIBLE["dialogue"].keys())
        os.environ["ONLY_ACT"] = str(act_n) if not arc_id else "none"
        if arc_id:
            os.environ["ONLY_ARC"] = arc_id
        importlib.reload(bible_src)
    static_checks(v, bible, systems, act)
    if "--world" in a:
        resolved = json.loads(Path(a[a.index("--world") + 1]).read_text())
        for lid in list(bible["loc_data"]):
            if lid in resolved["locations"]:
                bible["loc_data"][lid] = resolved["locations"][lid]
    else:
        bible = resolve_defaults(bible)
    sim = Sim(bible, systems, act)
    ok = sim.run()
    mine = set(act_locations(bible, act))
    for lid in sorted(mine - sim.reach):
        v.warn(f"location {lid} is never reached from the start")
    for lid in sorted(mine):
        for i, e in enumerate(bible["loc_data"][lid].get("on_enter", [])):
            if f"{lid}:{i}" not in sim.entered and lid in sim.reach:
                v.warn(f"{lid}: on_enter[{i}] never triggers (condition not met on arrival)")
    if not ok:
        v.err(f"EXIT '{act['exit_to']}' is NOT reachable - the act cannot be completed")
        v.err(f"  reached locations: {sorted(sim.reach)}; flags: {sorted(sim.st.flags)}; items: {sorted(sim.st.items)}")
    # items required but consumed
    for it in sim.consumed:
        v.warn(f"item '{it}' is removed by a 'take' action; make sure nothing later needs it")
    # seed variation options: re-run with each placement holder / gate option
    if "--seed-options" in a:
        for item, holders in bible["placements"].items():
            for h in holders:
                b2 = copy.deepcopy(bible)
                for ld in b2["loc_data"].values():
                    for p in ld.get("props", []):
                        if p.get("interact", {}).get("take") == item:
                            p["interact"].pop("take", None)
                        if p["id"] == h["prop"]:
                            p.setdefault("interact", {})["take"] = item
                s2 = Sim(b2, systems, act)
                if not s2.run():
                    v.err(f"seed option: placing {item} at {h['prop']} makes the act unsolvable")
        for g, opts in bible["gates"].items():
            for o in opts:
                b2 = copy.deepcopy(bible)
                for ld in b2["loc_data"].values():
                    for p in ld.get("props", []):
                        if p["id"] == g:
                            p["interact"]["go_cond"] = o["cond"]
                if not Sim(b2, systems, act).run():
                    v.err(f"seed option: gate {g} -> {o['cond']} makes the act unsolvable")
    for m in v.warns:
        print("WARN ", m)
    for m in v.errors:
        print("ERROR", m)
    out = Path(a[a.index("--plan") + 1]) if "--plan" in a else ROOT / "data" / "plans" / (f"arc_{arc_id}.json" if arc_id else f"act_{act_n}.json")
    if ok and not v.errors:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"act": arc_id or act_n, "arc": arc_id or "", "start": act["start"], "exit_to": act["exit_to"], "plan": sim.plan}, indent=1))
    print(f"{'arc ' + arc_id if arc_id else 'act ' + str(act_n)}: {len(mine)} locations ({len(sim.reach & mine)} reachable), plan {len(sim.plan)} steps, "
          f"{len(v.errors)} errors, {len(v.warns)} warnings -> {'OK' if ok and not v.errors else 'FAILED'}")
    sys.exit(0 if ok and not v.errors else 1)


if __name__ == "__main__":
    main()
