#!/usr/bin/env python3
"""Step 1: book -> text chapters -> grounded entity index.

Reads the Project Gutenberg epub of Dracula, writes plain-text chapters to
book/chapters/, then scans them for every location/character/prop keyword
listed in world_bible.json and stores chapter hit counts plus the first
descriptive sentences in book/entity_index.json. The bible entries are thereby
tied to actual passages of the novel (used for in-game descriptions too).
"""
import html
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPUB = ROOT.parent / "pg345-images-3.epub"
OUT = ROOT / "book" / "chapters"


def strip_tags(s: str) -> str:
    s = re.sub(r"(?is)<(script|style).*?</\1>", "", s)
    s = re.sub(r"(?i)</(p|div|h[1-6]|br)>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\n\s*\n+", "\n\n", s).strip()


def extract() -> list[tuple[str, str]]:
    OUT.mkdir(parents=True, exist_ok=True)
    chapters = []
    with zipfile.ZipFile(EPUB) as z:
        names = [n for n in z.namelist() if n.endswith(".xhtml") and re.search(r"-h-(\d+)", n)]
        names.sort(key=lambda n: int(re.search(r"-h-(\d+)", n).group(1)))
        for n in names:
            text = strip_tags(z.read(n).decode("utf-8", "replace"))
            if len(text) < 6000:
                continue  # front matter / toc
            m = re.search(r"CHAPTER\s+([IVXL]+)", text)
            idx = len(chapters) + 1
            if idx > 27:
                continue   # epub tail = licence; chapter 28 (closing Note) comes from the PDF, see book/SOURCES.md
            title = f"chapter_{idx:02d}"
            (OUT / f"{title}.txt").write_text(text, encoding="utf-8")
            chapters.append((title, text))
    return chapters


def sentences_with(text: str, kw: re.Pattern, limit: int):
    out = []
    for s in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")):
        if kw.search(s) and 50 < len(s) < 320:
            out.append(s.strip())
            if len(out) >= limit:
                break
    return out


def main():
    bible = json.loads((ROOT / "pipeline" / "world_bible.json").read_text())
    chapters = extract()
    print(f"{len(chapters)} chapters extracted")
    index = {}
    for kind in ("locations", "characters", "props"):
        for ent in [e for e in bible[kind] if "keywords" in e]:
            kw = re.compile("|".join(ent["keywords"]), re.I)
            hits = {}
            quotes = []
            for name, text in chapters:
                c = len(kw.findall(text))
                if c:
                    hits[name] = c
                    if len(quotes) < 3:
                        quotes += sentences_with(text, kw, 3 - len(quotes))
            index[ent["id"]] = {"kind": kind, "chapter_hits": hits,
                                "total": sum(hits.values()), "quotes": quotes}
            flag = "" if hits else "   <-- NOT FOUND IN BOOK"
            print(f"{kind[:4]} {ent['id']:<22} {sum(hits.values()):>5}{flag}")
    (ROOT / "book" / "entity_index.json").write_text(
        json.dumps(index, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
