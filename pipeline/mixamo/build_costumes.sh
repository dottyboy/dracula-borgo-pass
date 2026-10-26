#!/bin/bash
# Dress the Y Bot / X Bot as every procedural human model (params from humans.json) -> assets/models/chars/sk_<id>.glb
# usage: build_costumes.sh [model_id ...]   (default: all)
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/../../assets/models/chars"
BLENDER="${BLENDER:-$HOME/Programi/blender-5.2.2/blender}"
ids=("$@")
if [ ${#ids[@]} -eq 0 ]; then ids=($(python3 -I -c "import json;print(' '.join(json.load(open('$HERE/humans.json'))))")); fi
for id in "${ids[@]}"; do
  params=$(python3 -I -c "import json;d=json.load(open('$HERE/humans.json'))['$id'];print(json.dumps(d))")
  sex=$(python3 -I -c "import json;print(json.load(open('$HERE/humans.json'))['$id']['sex'])")
  bot="Y Bot.fbx"; [ "$sex" = "f" ] && bot="X Bot.fbx"
  "$BLENDER" -b --factory-startup -P "$HERE/dress.py" -- "$HERE/$bot" "$OUT/sk_$id.glb" "$params" 2>&1 | grep -E "EXPORTED|Traceback|Error" 
done
