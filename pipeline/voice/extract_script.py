#!/usr/bin/env python3
"""Extract every speakable line of the game into voice/script.jsonl (one JSON object per line) + voice/summary.json.

Sources: dialogue nodes (NPC and protagonist lines), player choices, prop/NPC "look" texts and pickup texts, location
descriptions, item descriptions, journal entries, story cards. Each line gets a stable id (sha1 of its source path), a
canonical character, a `kind` (dialogue | player | narration | journal | card | item) and empty `emotion` / `delivery`
fields for the tagging pass (see docs/VOICE_PLAN.md).

usage: python3 pipeline/voice/extract_script.py
"""
import hashlib
import json
import collections
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
W = json.load(open(os.path.join(ROOT, "data", "world.json")))

ALIASES = {
    "Mina": "mina", "Mina Harker": "mina", "Mina Murray": "mina",
    "Jonathan": "harker", "Jonathan Harker": "harker", "Harker": "harker",
    "Van Helsing": "vanhelsing", "Professor Van Helsing": "vanhelsing", "Prof. Van Helsing": "vanhelsing",
    "Seward": "seward", "Dr. Seward": "seward", "John Seward": "seward",
    "Quincey": "quincey", "Quincey Morris": "quincey", "Mr. Morris": "quincey",
    "Arthur": "arthur", "Arthur Holmwood": "arthur", "Lord Godalming": "arthur",
    "Lucy": "lucy", "Lucy Westenra": "lucy", "Renfield": "renfield", "R. M. Renfield": "renfield",
    "Count Dracula": "dracula", "Dracula": "dracula", "The Count": "dracula", "The Master": "dracula",
    "Narrator": "narrator",
}


def sid(path: str) -> str:
    return hashlib.sha1(path.encode()).hexdigest()[:10]


TALK = {}                                   # dialogue id -> (npc model, variant) of the NPC that starts it
for _lid, _ld in W["loc_data"].items():
    for _n in _ld.get("npcs", []):
        _t = _n.get("interact", {}).get("talk")
        if _t:
            TALK[_t] = (_n.get("asset", ""), _n.get("variant", ""))

lines = []


def add(path, kind, speaker, text, **ctx):
    text = (text or "").strip()
    if not text:
        return
    char = ALIASES.get(speaker, "narrator" if kind in ("narration", "journal", "card", "item") else "npc:" + speaker)
    if char.startswith("npc:") and ctx.get("dialogue") in TALK:
        ctx["npc_model"], ctx["npc_variant"] = TALK[ctx["dialogue"]]
    lines.append({"id": sid(path), "source": path, "kind": kind, "speaker": speaker, "character": char, "text": text,
                  "emotion": "", "delivery": "", **ctx})


for dk, dd in W["dialogue"].items():
    for nid, nd in dd["nodes"].items():
        add("dialogue:%s:%s" % (dk, nid), "dialogue", nd.get("speaker", ""), nd.get("text", ""), dialogue=dk)
        for i, ch in enumerate(nd.get("choices", [])):
            t = ch.get("text", "")
            if t and not t.startswith("["):                 # [stage directions] are not spoken
                add("choice:%s:%s:%d" % (dk, nid, i), "player", "player", t, dialogue=dk)
        for j, a in enumerate(nd.get("do", [])):
            if "card" in a:
                add("card:%s:%s:%d" % (dk, nid, j), "card", "Narrator", a["card"], dialogue=dk)

for lid, ld in W["loc_data"].items():
    for p in ld.get("props", []) + ld.get("npcs", []):
        it = p.get("interact", {})
        for key in ("look", "take_text", "use_text", "fail_text"):
            if isinstance(it.get(key), str):
                add("%s:%s:%s:%s" % ("look", lid, p.get("id"), key), "narration", "Narrator", it[key], loc=lid)
for loc in W["locations"]:
    add("locdesc:" + loc["id"], "narration", "Narrator", loc.get("desc", ""), loc=loc["id"])
for iid, it in W["items"].items():
    add("item:" + iid, "item", "Narrator", it.get("desc", ""))
for jid, j in W["journal"].items():
    add("journal:" + jid, "journal", "Narrator", j.get("text", ""), journal_source=j.get("source", ""))

seen = set()
uniq = []
for l in lines:
    if l["id"] in seen:
        continue
    seen.add(l["id"])
    uniq.append(l)
os.makedirs(os.path.join(ROOT, "voice"), exist_ok=True)
with open(os.path.join(ROOT, "voice", "script.jsonl"), "w") as f:
    for l in uniq:
        f.write(json.dumps(l, ensure_ascii=False) + "\n")

by_char = collections.defaultdict(lambda: [0, 0])
by_kind = collections.defaultdict(lambda: [0, 0])
for l in uniq:
    by_char[l["character"]][0] += 1
    by_char[l["character"]][1] += len(l["text"])
    by_kind[l["kind"]][0] += 1
    by_kind[l["kind"]][1] += len(l["text"])
total = sum(v[1] for v in by_kind.values())
summary = {"lines": len(uniq), "characters_total": total, "approx_hours_at_15_chars_per_sec": round(total / 15 / 3600, 1),
           "by_kind": by_kind, "by_character": dict(sorted(by_char.items(), key=lambda kv: -kv[1][1]))}
json.dump(summary, open(os.path.join(ROOT, "voice", "summary.json"), "w"), indent=1)
print(json.dumps({k: summary[k] for k in ("lines", "characters_total", "approx_hours_at_15_chars_per_sec")}))
print("kinds:", {k: v for k, v in by_kind.items()})
print("named characters:", {k: v for k, v in summary["by_character"].items() if not k.startswith("npc:")})
pools = collections.Counter()
for l in uniq:
    if l["character"].startswith("npc:"):
        pools[l.get("npc_model", "unknown")] += len(l["text"])
print("npc pools (chars):", dict(pools))
npc = [(k, v) for k, v in summary["by_character"].items() if k.startswith("npc:")]
print("npc speakers:", len(npc), "lines", sum(v[0] for _, v in npc), "chars", sum(v[1] for _, v in npc))
