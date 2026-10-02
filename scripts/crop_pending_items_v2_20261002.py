# -*- coding: utf-8 -*-
"""批次5-待核批量裁定 v2：按"行内字符位置"估算 x 坐标后窄窗裁切（8x）

用法: python crop_pending_items_v2_20261002.py <page> "<label>|<anchor>|<offset>" ...
  anchor = OCR 可读的邻近文本片段；offset = 目标字相对 anchor 起点的字符偏移
输出: C:\\Users\\52744\\_scratch\\vol59_pending\\p<page>_v2_<n>.png
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(r"E:\codex_Learing\project_连云港市志\repo\workbench\volume59")
OUT = Path(r"C:\Users\52744\_scratch\vol59_pending")
OUT.mkdir(parents=True, exist_ok=True)
FONT = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 30)
ZOOM = 8
WIN = 130          # 半窗（源像素），约 3 字
MAX_H = 2400


def find_line(page, anchor):
    d = json.loads((BASE / "locate_ocr" / f"page_{page:03d}.json").read_text(encoding="utf-8"))
    cands = [l for l in d["lines"] if anchor in l["text"]]
    if not cands:
        return None, None
    l = max(cands, key=lambda x: len(x["text"]))
    idx = l["text"].find(anchor)
    return l, idx


def main():
    page = int(sys.argv[1])
    specs = []
    for arg in sys.argv[2:]:
        parts = arg.split("|")
        label, anchor = parts[0], parts[1]
        off = int(parts[2]) if len(parts) > 2 and parts[2] else 0
        specs.append((label, anchor, off))
    img = Image.open(BASE / "pages" / f"page_{page:03d}.png")
    tiles = []
    for label, anchor, off in specs:
        l, idx = find_line(page, anchor)
        if l is None:
            tiles.append((label + " [未定位]", None))
            continue
        n = max(len(l["text"]), 1)
        cx = l["x0"] + (idx + off + 0.5) / n * (l["x1"] - l["x0"])
        x0 = max(0, int(cx - WIN))
        x1 = min(img.width, int(cx + WIN))
        y0 = max(0, l["y0"] - 20)
        y1 = min(img.height, l["y1"] + 20)
        crop = img.crop((x0, y0, x1, y1))
        crop = crop.resize((crop.width * ZOOM, crop.height * ZOOM), Image.LANCZOS)
        tiles.append((f"{label}  ({anchor}+{off})", crop))
    img.close()
    groups, cur, h = [], [], 0
    for label, crop in tiles:
        th = (crop.height + 42) if crop is not None else 60
        if h + th > MAX_H and cur:
            groups.append(cur)
            cur, h = [], 0
        cur.append((label, crop))
        h += th
    if cur:
        groups.append(cur)
    for gi, g in enumerate(groups, 1):
        W = max([(c.width if c is not None else 400) for _, c in g]) + 20
        H = sum(((c.height + 42) if c is not None else 60) for _, c in g) + 10
        cv = Image.new("RGB", (W, H), (250, 250, 250))
        d = ImageDraw.Draw(cv)
        y = 5
        for label, crop in g:
            d.rectangle([0, y, W, y + 38], fill=(150, 30, 30))
            d.text((8, y + 2), label, fill="white", font=FONT)
            y += 42
            if crop is not None:
                cv.paste(crop, (10, y))
                y += crop.height
        out = OUT / f"p{page:03d}_v2_{gi}.png"
        cv.save(out)
        print(out, cv.size)


if __name__ == "__main__":
    main()
