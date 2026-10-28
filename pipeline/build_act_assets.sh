#!/bin/bash
# Build and preview ONLY the assets of one act (safe to run while other acts are being authored):
#   pipeline/build_act_assets.sh <act number> [asset_id ...]
set -e
cd "$(dirname "$0")/.."
N=$1; shift
B=/tmp/bible_act$N.json
ONLY_ACT=$N python3 pipeline/bible_src.py --out $B >/dev/null
if [ $# -eq 0 ]; then IDS=$(python3 -c "import json;print(' '.join(a['id'] for a in json.load(open('$B'))['assets'] if a['id'] not in {x.stem for x in __import__('pathlib').Path('assets/models').glob('*.glb')} or True))"); else IDS="$@"; fi
# only the act's own assets (those not in the base set)
ACT_IDS=$(python3 - <<PY
import json,sys
b=json.load(open('$B'))
mine=[a['id'] for a in b['assets']]
import importlib,os
os.environ['ONLY_ACT']='$N'
sys.path.insert(0,'pipeline')
m=importlib.import_module('acts.act_$N')
own={a['id'] for a in getattr(m,'ASSETS',[])}
want='$IDS'.split()
print(' '.join(i for i in want if i in own))
PY
)
[ -z "$ACT_IDS" ] && { echo "act $N defines no assets"; exit 0; }
BIBLE_JSON=$B ~/Programi/blender-5.2.2/blender -b --factory-startup -P pipeline/blender_gen.py -- $ACT_IDS 2>&1 | grep -E "^built|Error|Traceback|line [0-9]+" || true
~/Programi/blender-5.2.2/blender -b --factory-startup -P pipeline/preview_asset.py -- $ACT_IDS 2>&1 | grep -E "^preview|Error" || true
