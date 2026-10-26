#!/bin/bash
# Rebuild + preview specific base-world assets with the current builders:  pipeline/rebuild_assets.sh <asset id> [...]
# (writes assets/models/<id>.glb and /tmp/asset_previews/<id>.png). Safe to run next to other asset builds (per-asset files).
set -e
cd "$(dirname "$0")/.."
python3 pipeline/bible_src.py --out /tmp/bible_rebuild_$$.json >/dev/null
BIBLE_JSON=/tmp/bible_rebuild_$$.json ~/Programi/blender-5.2.1/blender -b --factory-startup -P pipeline/blender_gen.py -- "$@" 2>&1 | grep -E "^built|Error|Traceback|line [0-9]+" || true
~/Programi/blender-5.2.1/blender -b --factory-startup -P pipeline/preview_asset.py -- "$@" 2>&1 | grep -E "^preview|Error" || true
rm -f /tmp/bible_rebuild_$$.json
