# -*- coding: utf-8 -*-
"""Content-level gap audit for the 上册 (using repo OCR).

For every OCR page, measure how many of its 'big numbers' (>=3 digits) appear in
the delivered reader. Pages whose numbers are largely absent = content missing
from the book (dropped tables / dropped prose), independent of table numbers.
"""
from __future__ import annotations

import glob
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
NUM = re.compile(r"\d{3,}(?:\.\d+)?")


def page_text(path: Path) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    if isinstance(data, dict):
        for key in ("text", "lines", "ocr_text", "result"):
            v = data.get(key)
            if isinstance(v, str):
                return v
            if isinstance(v, list):
                out = []
                for item in v:
                    if isinstance(item, str):
                        out.append(item)
                    elif isinstance(item, dict):
                        out.append(str(item.get("text", "")))
                if out:
                    return "\n".join(out)
    if isinstance(data, list):
        out = []
        for item in data:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                out.append(str(item.get("text", "")))
        return "\n".join(out)
    return ""


def main() -> None:
    reader = READER.read_text(encoding="utf-8")
    # 收录所有出现在 reader 中的数字串（含表格与正文）
    reader_nums = set(NUM.findall(reader))
    print("reader 数字串(≥3位)去重:", len(reader_nums))
    rows = []
    for part in ("上_1", "上_2", "上_3"):
        files = sorted(glob.glob(str(ROOT / "workbench" / "ocr_v2" / "ocr" / "rapid" / part / "page_*.json")))
        for f in files:
            txt = page_text(Path(f))
            nums = [n for n in NUM.findall(txt) if len(n.split(".")[0]) >= 3]
            if len(nums) < 8:
                continue
            miss = [n for n in nums if n not in reader_nums]
            ratio = len(miss) / len(nums)
            digit_ratio = sum(c.isdigit() for c in txt) / max(1, len(txt))
            if ratio >= 0.6:
                rows.append((part, Path(f).stem, len(nums), round(ratio, 2), round(digit_ratio, 2), miss[:6], txt[:70].replace("\n", " ")))
    rows.sort(key=lambda r: (-r[3], r[0]))
    print(f"候选页(数字缺失率≥60%): {len(rows)}")
    for part, name, n, ratio, dr, miss, head in rows[:40]:
        print(f"  [{part}/{name}] 数字{n} 缺失{ratio} 数字密度{dr} 未收录样例{miss} | {head}")


if __name__ == "__main__":
    main()
