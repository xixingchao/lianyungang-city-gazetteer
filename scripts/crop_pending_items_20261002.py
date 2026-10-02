# -*- coding: utf-8 -*-
"""批次5-待核批量裁定：按页生成"目标字放大合成图"（anchor 定位 + 8x 裁切）

用法: python crop_pending_items_20261002.py <page> "<label>|<anchor keyword>|<L|R>" ...
输出: C:\\Users\\52744\\_scratch\\vol59_pending\\p<page>_<n>.png（每张 ≤ 8 个 tile）
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
MAX_H = 2400


def find_anchor(page, kw):
    """在 OCR 缓存里找包含 kw 的行，返回 (x0,y0,x1,y1) 或 None"""
    d = json.loads((BASE / "locate_ocr" / f"page_{page:03d}.json").read_text(encoding="utf-8"))
    best = None
    for l in d["lines"]:
        if kw and kw in l["text"]:
            if best is None or len(l["text"]) > len(best["text"]):
                best = l
    return best


def main():
    page = int(sys.argv[1])
    specs = []
    for arg in sys.argv[2:]:
        label, anchor, side = (arg.split("|") + ["", "L"])[:3]
        specs.append((label, anchor, side))
    img = Image.open(BASE / "pages" / f"page_{page:03d}.png")
    tiles = []
    for label, anchor, side in specs:
        a = find_anchor(page, anchor)
        if a is None:
            tiles.append((label + " [未定位]", None))
            continue
        y0 = max(0, a["y0"] - 18)
        y1 = min(img.height, a["y1"] + 18)
        WIN = 250  # 固定窄窗（约 6 字），保证 8x 后宽度可读
        if side == "R":
            x0 = max(0, a["x0"] - 60)
            x1 = min(img.width, a["x0"] + WIN)
        else:
            x0 = max(0, a["x1"] - WIN + 60)
            x1 = min(img.width, a["x1"] + 60)
        crop = img.crop((x0, y0, x1, y1))
        crop = crop.resize((crop.width * ZOOM, crop.height * ZOOM), Image.LANCZOS)
        tiles.append((f"{label}  ({anchor})", crop))
    img.close()
    # 合成（每张 ≤ MAX_H）
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
        out = OUT / f"p{page:03d}_{gi}.png"
        cv.save(out)
        print(out, cv.size)


if __name__ == "__main__":
    main()
