# -*- coding: utf-8 -*-
"""Audit reader + v2 for flattened table remnants (non-section table dumps).

A flattened remnant is a visible text run outside any structured-table <section>
that reproduces a table's title together with its data. Verified remnants were
cleared on 2026-10-06; this audit guards against regressions.
"""
from __future__ import annotations

import glob
import html as H
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SECTION_RE = re.compile(r'<section class="verified-table-block.*?</section>', re.S)
TAG_RE = re.compile(r"<[^>]+>")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")
PH_RE = re.compile(r"\{\{STRUCTURED_TABLE:[^}]+\}\}")
CM_RE = re.compile(r"<!--.*?-->", re.S)


def title_core(t: dict) -> str:
    s = re.sub(r"[（(][^）)]*[）)]", "", str(t.get("title", "")))
    return re.sub(r"[表\s\d\-~～、，,。．\.：:；;（）()\[\]《》]", "", s)


def load_titles() -> list[tuple[str, str]]:
    out = []
    for part in ("上", "中", "下"):
        for f in glob.glob(str(ROOT / "workbench" / "table_entries" / part / "data" / "*.json")):
            try:
                t = json.loads(Path(f).read_text(encoding="utf-8"))
            except Exception:
                continue
            tc = title_core(t)
            if len(tc) >= 6:
                out.append((t["table_id"], tc))
    return out


def looks_like_dump(s: str) -> bool:
    if len(s) < 40:
        return False
    digits = sum(c.isdigit() for c in s)
    if digits / len(s) < 0.20:
        return False
    if s.count("。") + s.count("？") + s.count("！") > 1:
        return False
    return len([n for n in NUM_RE.findall(s) if len(n) >= 2]) >= 8


def main() -> None:
    issues = 0
    titles = load_titles()
    raw = READER.read_text(encoding="utf-8")
    pieces = SECTION_RE.split(raw)
    for pi, piece in enumerate(pieces):
        for li, line in enumerate(piece.split("\n")):
            s = H.unescape(TAG_RE.sub("", line)).strip()
            if not looks_like_dump(s):
                continue
            compact = re.sub(r"[\s\u3000]", "", s)
            for tid, tc in titles:
                if tc in compact:
                    issues += 1
                    print(f"[reader] piece{pi} line{li} 疑似残文({tid}): {s[:90]}")
                    break
    for f in sorted(glob.glob(str(ROOT / "workbench" / "body_chapters_v2" / "*.md"))):
        txt = CM_RE.sub("\x00", PH_RE.sub("\x00", Path(f).read_text(encoding="utf-8")))
        for li, line in enumerate(txt.split("\n")):
            s = re.sub(r"^#+\s*", "", line).strip()
            if not looks_like_dump(s):
                continue
            compact = re.sub(r"[\s\u3000]", "", s)
            for tid, tc in titles:
                if tc in compact:
                    issues += 1
                    print(f"[v2:{Path(f).name}] line{li} 疑似残文({tid}): {s[:90]}")
                    break
    print(f"issues={issues}")


if __name__ == "__main__":
    main()
