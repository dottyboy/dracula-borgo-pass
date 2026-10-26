#!/usr/bin/env python3
"""Character portraits / concept art through the Pollinations image API (free, key required).

    export POLLINATIONS_KEY=sk_...      (or put the key alone in ~/.config/pollinations_key; never in the project)
    python3 pipeline/portraits.py --dry-run          # print the prompts only, no network
    python3 pipeline/portraits.py [--only id ...] [--model black-forest-labs/flux.1-schnell] [--force]

Prompts are built from the book database (appearance text extracted from the novel) plus a fixed art style so
the whole cast matches. Output: assets/portraits/<id>.png and assets/portraits/_prompts.json (prompt + model + seed,
so any portrait can be reproduced). Models: free ones are flux.1-schnell, flux.2-klein-4b, z-image-turbo
(see https://gen.pollinations.ai/models, field paid_only).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "portraits"
STYLE = ("dark gothic oil painting portrait, 1890s Victorian era, Bram Stoker's Dracula atmosphere, "
         "dramatic chiaroscuro candlelight, muted palette with deep reds, painterly, head and shoulders, "
         "no text, no watermark, no signature")

# id -> name fragments to collect book appearance text from, + fallback description
CAST = {
    "harker": (["Jonathan Harker"], "young English solicitor, clean-shaven, earnest, in a tweed travelling suit"),
    "dracula_old": (["=Count Dracula"], "tall old man, aquiline face, long white moustache, completely clean-shaven otherwise, NO beard, clad in black from head to foot, pale cold skin, red-tinged lips"),
    "dracula_young": (["rejuvenated"], "tall thin man, beaky nose, black moustache and pointed beard, hard cruel sensual face, white teeth, in a black frock coat and top hat"),
    "mina": (["Mina Harker", "Mina Murray"], "sweet-faced dainty young Victorian woman, dark hair, intelligent eyes, schoolmistress dress"),
    "lucy": (["Lucy Westenra"], "beautiful young English woman, golden hair, pale complexion, white nightgown"),
    "lucy_undead": (["Un-Dead"], "undead woman in grave-cerements, crimson lips, sharp canines, radiant unnatural beauty"),
    "vanhelsing": (["Van Helsing"], "elderly Dutch professor, bushy eyebrows meeting over the nose, iron jaw, sharp kind eyes, small beard"),
    "seward": (["Seward"], "young doctor, strong jaw, good forehead, asylum superintendent, tired eyes"),
    "renfield": (["Renfield"], "lunatic patient in asylum clothing, wild eyes, great physical strength, feverish"),
    "quincey": (["Quincey"], "young fresh-looking American from Texas, bowie knife at belt, wide-brimmed hat, friendly grin"),
    "arthur": (["Arthur Holmwood", "Godalming"], "tall handsome young English lord, curly hair, noble bearing"),
    "brides": (["Brides"], "three beautiful pale vampire women, voluptuous lips, white teeth, swaying forms in white gowns, ruddy colour"),
    "innkeeper": (["landlord", "hostess"], "Transylvanian innkeeper's wife in folk dress, worried, holding a crucifix"),
    "szgany": (["Szgany", "Gypsy"], "Szgany horseman, black hair, proud look, bright coloured sash, centaur-like in the saddle"),
    "captain": (["Captain"], "weathered Russian sea captain, grey-streaked beard, oilskin coat, tired determined eyes, a crucifix and rosary wound in his hands, storm lamp light"),
    "driver": (["unnamed driver"], "tall driver with a long brown beard, great black hat hiding his face, very bright eyes glinting red"),
}


def load_db():
    p = ROOT / "book" / "book_db.json"
    return json.loads(p.read_text())["characters"] if p.exists() else []


def prompt_for(cid, db):
    frags, base = CAST[cid]
    bits = []
    for c in db:
        nm = str(c.get("name", "")).lower()
        if any((nm == f[1:].lower()) if f.startswith("=") else (f.lower() in nm) for f in frags):
            for k in ("appearance", "clothing"):
                v = str(c.get(k) or "").strip()
                if v and "not given" not in v and v not in bits:
                    bits.append(v)
    book = "; ".join(bits)
    if len(book) > 380:
        book = book[:380].rsplit(";", 1)[0]
    return f"{base}. {book}. {STYLE}".replace("..", ".")


def key():
    k = os.environ.get("POLLINATIONS_KEY")
    if not k:
        f = Path.home() / ".config" / "pollinations_key"
        if f.exists():
            k = f.read_text().strip()
    return k


def fetch(prompt, model, seed, k, size=768):
    q = urllib.parse.urlencode({"model": model, "width": size, "height": size, "seed": seed})
    url = f"https://gen.pollinations.ai/image/{urllib.parse.quote(prompt)}?{q}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {k}", "User-Agent": "VampireAdventure/0.1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read(), r.headers.get("Content-Type", "")


def _to_png(path):
    """The service may return JPEG; Godot needs real PNG data behind a .png name. Also shrink to 512 px."""
    from PIL import Image
    Image.open(path).convert("RGB").resize((512, 512), Image.LANCZOS).save(path, "PNG")


def main():
    a = sys.argv[1:]
    model = a[a.index("--model") + 1] if "--model" in a else "black-forest-labs/flux.1-schnell"
    only = [x for x in a[a.index("--only") + 1:] if not x.startswith("--")] if "--only" in a else list(CAST)
    db = load_db()
    OUT.mkdir(parents=True, exist_ok=True)
    meta_f = OUT / "_prompts.json"
    meta = json.loads(meta_f.read_text()) if meta_f.exists() else {}
    k = key()
    if "--dry-run" in a or not k:
        for cid in only:
            print(f"[{cid}] {prompt_for(cid, db)}\n")
        if not k and "--dry-run" not in a:
            print("No POLLINATIONS_KEY set (get a secret key at https://enter.pollinations.ai) - nothing generated.")
        return
    for i, cid in enumerate(only):
        dest = OUT / f"{cid}.png"
        if dest.exists() and "--force" not in a:
            print("skip", cid)
            continue
        prompt = prompt_for(cid, db)
        seed = 1000 + i
        try:
            data, ctype = fetch(prompt, model, seed, k)
        except urllib.error.HTTPError as e:
            print(f"{cid}: HTTP {e.code} {e.read()[:200]!r}")
            continue
        if not ctype.startswith("image/"):
            print(f"{cid}: unexpected {ctype}: {data[:200]!r}")
            continue
        dest.write_bytes(data)
        _to_png(dest)
        meta[cid] = {"prompt": prompt, "model": model, "seed": seed, "type": ctype}
        meta_f.write_text(json.dumps(meta, indent=1))
        print("saved", dest.name, len(data), "bytes")
        time.sleep(1.5)


if __name__ == "__main__":
    main()
