#!/bin/bash
# Full pipeline for a RANDOM seed: resolve the seeded world in the engine, plan every act on it, replay in the engine.
#   ./run_seed_test.sh <seed> [acts...]
cd "$(dirname "$0")"
G=${GODOT:-$HOME/Programi/godot4/Godot_v4.7.1-stable_linux.x86_64}
SEED=$1; shift
ACTS=${@:-1 2 3 4 5 6}
python3 pipeline/build_assets.py >/dev/null 2>&1
W=$($G --headless --path . -- --genworld=$SEED 2>&1 | grep "world written" | sed 's/.*: //')
for n in $ACTS; do
  python3 pipeline/validate_story.py --act $n --world "$W" --plan /tmp/plan_${SEED}_$n.json | tail -1
  [ -f /tmp/plan_${SEED}_$n.json ] && timeout 600 $G --headless --path . -- --replay=/tmp/plan_${SEED}_$n.json --seed=$SEED --world=resolved 2>&1 | grep -E "FAIL|REPLAY|SCRIPT"
done
