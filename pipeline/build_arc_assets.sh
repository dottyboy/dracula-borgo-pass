#!/bin/bash
# Build + preview ONLY the new assets of one personal arc:  pipeline/build_arc_assets.sh <arc id> [asset ids]
set -e
cd "$(dirname "$0")/.."
ID=$1; shift
B=/tmp/bible_arc_$ID.json
ONLY_ACT=none ONLY_ARC=$ID python3 pipeline/bible_src.py --out $B >/dev/null
OWN=$(ONLY_ACT=none ONLY_ARC=$ID python3 - <<PY
import sys,importlib
sys.path.insert(0,'pipeline')
m=importlib.import_module('acts.arc_$ID')
print(' '.join(a['id'] for a in getattr(m,'ASSETS',[])))
PY
)
WANT=${@:-$OWN}
IDS=""
for i in $WANT; do case " $OWN " in *" $i "*) IDS="$IDS $i";; esac; done
[ -z "$IDS" ] && { echo "arc $ID defines no assets"; exit 0; }
BIBLE_JSON=$B ~/Programi/blender-5.2.1/blender -b --factory-startup -P pipeline/blender_gen.py -- $IDS 2>&1 | grep -E "^built|Error|Traceback|line [0-9]+" || true
~/Programi/blender-5.2.1/blender -b --factory-startup -P pipeline/preview_asset.py -- $IDS 2>&1 | grep -E "^preview|Error" || true
