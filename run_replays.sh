#!/bin/bash
# Replays every act's validator plan in the real engine (headless). Usage: ./run_replays.sh [acts...]
cd "$(dirname "$0")"
G=${GODOT:-$HOME/Programi/godot4/Godot_v4.7.1-stable_linux.x86_64}
ACTS=${@:-1 2 3 4 5 6}
for n in $ACTS; do
  python3 pipeline/validate_story.py --act $n >/dev/null || { echo "act $n: validator FAILED"; continue; }
  timeout 600 $G --headless --path . -- ${REGION:+--region} --act=$n --seed=$((100+n)) --world=default 2>&1 | grep -E "FAIL|REPLAY|note:|ERROR|SCRIPT" | head -30
done
