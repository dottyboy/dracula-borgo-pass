#!/usr/bin/env python3
"""Print every model available for use in locations: id, size hint, material roles, variants.
   python3 pipeline/list_assets.py [filter]        (includes assets of acts if ONLY_ACT is set)"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
import bible_src

flt = sys.argv[1] if len(sys.argv) > 1 else ""
b = bible_src.BIBLE
tex = sorted(p.name.replace("_albedo.png", "") for p in (ROOT / "assets/textures").glob("*_albedo.png"))
print("TEXTURES:", ", ".join(tex), "\n")
for a in b["assets"]:
    if flt and flt not in a["id"]:
        continue
    sf = ROOT / "assets/models/_slots" / f"{a['id']}.json"
    roles = json.loads(sf.read_text())["slots"] if sf.exists() else ["(not built yet)"]
    vs = [k for k in b["variants"].get(a["id"], {}) if k != "default"]
    print(f"{a['id']:<18} {a['builder']:<12} {str(a.get('params', ''))[:44]:<46} roles={','.join(roles)}  variants={','.join(vs[:12])}")
