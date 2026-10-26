#!/bin/bash
# Real-engine replay of personal arcs. Usage: ./run_arc_replays.sh [arc ids...]   (default: every pipeline/acts/arc_*.py)
cd "$(dirname "$0")"
G=${GODOT:-$HOME/Programi/godot4/Godot_v4.7.1-stable_linux.x86_64}
python3 pipeline/build_assets.py >/dev/null 2>&1
IDS=${@:-$(ls pipeline/acts/arc_*.py | grep -v builders | sed 's#.*/arc_##; s#\.py##')}
for id in $IDS; do
  python3 pipeline/validate_story.py --arc $id | tail -1
  [ -f data/plans/arc_$id.json ] && timeout 600 $G --headless --path . -- --arc=$id --seed=900 --world=default 2>&1 | grep -E "FAIL|REPLAY|SCRIPT|note:"
done
