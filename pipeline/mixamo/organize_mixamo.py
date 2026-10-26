#!/usr/bin/env python3
"""Clean a folder of Mixamo FBX downloads: normalise names, drop duplicates.

usage: organize_mixamo.py <raw_dir> <out_dir> [--dry]
Clips are grouped by their folder (pack zip / female / loose): the same name in different groups is a different
clip (male vs female idle, mutant walk vs walk). Output is <group>/<name>.fbx.
Duplicate = same group + normalised name (case/spacing only; "(2)" variants are different clips) or identical file content (sha256).
When both an in-place and a root-motion version of a clip exist, the in-place one is kept.
"""
import hashlib, re, shutil, sys
from pathlib import Path


def norm(stem: str) -> str:
    s = stem.replace("(", " ").replace(")", " ")     # "(2)" marks a different Mixamo variant, keep it
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()
    return s


def is_in_place(stem: str) -> bool:
    return "in_place" in norm(stem) or "inplace" in norm(stem)


def key(stem: str) -> str:
    return norm(stem).replace("_in_place", "").replace("_inplace", "")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    if len(args) != 2:
        sys.exit(__doc__)
    raw, out = Path(args[0]), Path(args[1])
    files = sorted(raw.rglob("*.fbx"))
    best: dict[str, Path] = {}
    seen_hash: dict[str, Path] = {}
    dropped = []
    for f in files:
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        if h in seen_hash:
            dropped.append((f, "same content as " + seen_hash[h].name))
            continue
        seen_hash[h] = f
        grp = f.parent.relative_to(raw).as_posix()
        k = (grp + "/" if grp != "." else "") + key(f.stem)
        cur = best.get(k)
        if cur is None:
            best[k] = f
        elif is_in_place(f.stem) and not is_in_place(cur.stem):
            dropped.append((cur, "replaced by in-place " + f.name))
            best[k] = f
        else:
            dropped.append((f, "duplicate name of " + cur.name))
    if not dry:
        out.mkdir(parents=True, exist_ok=True)
    for k, f in sorted(best.items()):
        print("keep ", k)
        if not dry:
            (out / k).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, out / (k + ".fbx"))
    for f, why in dropped:
        print("drop ", f.name, "--", why)
    print(f"{len(best)} kept, {len(dropped)} dropped, from {len(files)} files")


if __name__ == "__main__":
    main()
