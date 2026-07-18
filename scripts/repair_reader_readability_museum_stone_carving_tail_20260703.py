# -*- coding: utf-8 -*-
"""Repair source-backed residues around museum stone carvings."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_stone_carving_tail_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_stone_carving_tail_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷石刻石雕相邻错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0102.txt:20-34; "
    "workbench/ocr/paddle_ocr/下/part02/page_0107.txt:24-36; "
    "workbench/ocr/paddle_ocr/下/part02/page_0123.txt:10-16"
)

REPLACEMENTS = [
    (
        "<p>像高均在50厘米左右，大都保存尚好，俗称6像为“六神”，“六神台”即由此得名。摩崖造像在六神台东侧，共36尊，有坐像，有立像，造像保存不好，像的头部全被凿去。有造像铭一处，文日“仙山方士”。摩崖造像顶部有八形凿槽，沿槽有方形小柱洞分布，说明古时有棚式建筑。所有摩崖造像都复盖在这棚式建筑内。经考证，摩崖造像是在唐会昌灭佛事件中被毁，因六神台势险难攀，故6像能得以保存，以佛造像的须弥座式考之，伊芦山佛造像是盛唐时佛教艺术遗迹。</p>\n<p>三、石东连岛界域刻石位于连云区连岛乡东连岛村东端的羊窝峰下北坡。地理位置为北纬34°45'0\"，东径11929°18”。刻石临海而立，距海平面约8米。</p>",
        "<p>像高均在50厘米左右，大都保存尚好，俗称6像为“六神”，“六神台”即由此得名。摩崖造像在六神台东侧，共36尊，有坐像，有立像，造像保存不好，像的头部全被凿去。有造像铭一处，文曰“仙山方士”。摩崖造像顶部有八形凿槽，沿槽有方形小柱洞分布，说明古时有棚式建筑。所有摩崖造像都复盖在这棚式建筑内。经考证，摩崖造像是在唐会昌灭佛事件中被毁，因六神台势险难攀，故6像能得以保存，以佛造像的须弥座式考之，伊芦山佛造像是盛唐时佛教艺术遗迹。</p>\n<p>三、石刻</p>\n<p>东连岛界域刻石位于连云区连岛乡东连岛村东端的羊窝峰下北坡。地理位置为北纬34°45'0\"，东径11929°18”。刻石临海而立，距海平面约8米。</p>",
    ),
    (
        "<p>一、石象、石蟾蜍石象在孔望山摩崖造像东约100米处，是就一块天然大石的原形圆雕而成。石质为混合花岗岩，雕成石象后长4.9米，宽3.45米，高2.6米。石象通体无透雕，周身密布阴刻细线。象右腹有长方形线刻，内无题学。左有用阴线双钩刻出的象石”二学，隶书。靠左前腿上部刻象奴一人，为平面浅浮雕。象奴头束丁字形发，左手持钩，衣汉代服式。象左前足后部还有隶书刻圆字，已模糊不清。石象四足皆有阴线刻的仰瓣莲花，题材与佛教有关。</p>\n<p>石蟾蜍在孔望山摩崖造像南约200米处，是就一块直径为2.9米的圆形大石的天然形状圆雕而成。石蟾长2.4米，宽2.2米，高0.9米，吻部及前肢有残缺。背上有阴线刻鳞形图案，腿部有阴刻斑点状花纹。石蟾蜍与当时人们的宗教信仰有关，与石象同为汉东海庙神坛上供奉的灵物。</p>\n<p>石象和石蟾，雕刻技法虽皆属立体圆雕性质，然通体不见镂空处，并遍布阴线条，最终没有跨出汉画像石艺术的门槛，显示出汶代石刻艺术浑厚质朴的特色。从雕刻手法上看，二刻都是与孔望山摩崖造像同时的作品。其中石象有后人补刻和改刻的痕迹，如“象石”二字即为明人题勤。象耳、鼻、尾三部分改刻痕迹更明显，年代也更晚。</p>",
        "<p>一、石象、石蟾蜍</p>\n<p>石象在孔望山摩崖造像东约100米处，是就一块天然大石的原形圆雕而成。石质为混合花岗岩，雕成石象后长4.9米，宽3.45米，高2.6米。石象通体无透雕，周身密布阴刻细线。象右腹有长方形线刻，内无题字。左有用阴线双钩刻出的“象石”二字，隶书。靠左前腿上部刻象奴一人，为平面浅浮雕。象奴头束丁字形发，左手持钩，衣汉代服式。象左前足后部还有隶书刻圆字，已模糊不清。石象四足皆有阴线刻的仰瓣莲花，题材与佛教有关。</p>\n<p>石蟾蜍在孔望山摩崖造像南约200米处，是就一块直径为2.9米的圆形大石的天然形状圆雕而成。石蟾蜍长2.4米，宽2.2米，高0.9米，吻部及前肢有残缺。背上有阴线刻鳞形图案，腿部有阴刻斑点状花纹。石蟾蜍与当时人们的宗教信仰有关，与石象同为汉东海庙神坛上供奉的灵物。</p>\n<p>石象和石蟾蜍，雕刻技法虽皆属立体圆雕性质，然通体不见镂空处，并遍布阴线条，最终没有跨出汉画像石艺术的门槛，显示出汉代石刻艺术浑厚质朴的特色。从雕刻手法上看，二刻都是与孔望山摩崖造像同时的作品。其中石象有后人补刻和改刻的痕迹，如“象石”二字即为明人题勒。象耳、鼻、尾三部分改刻痕迹更明显，年代也更晚。</p>",
    ),
    (
        "认定它是一处宗教题材为主的石刻群，对手我国佛教史、艺术史和中外关系史等的研究，都具有重要意义。",
        "认定它是一处宗教题材为主的石刻群，对于我国佛教史、艺术史和中外关系史等的研究，都具有重要意义。",
    ),
]

EXPECTED_TEXT = [
    "文曰“仙山方士”",
    "<p>三、石刻</p>",
    "<p>一、石象、石蟾蜍</p>",
    "内无题字",
    "“象石”二字",
    "汉代石刻艺术浑厚质朴",
    "明人题勒",
    "对于我国佛教史、艺术史和中外关系史",
]
RESIDUALS = [
    "文日“仙山方士”",
    "三、石东连岛界域刻石",
    "内无题学",
    "象石”二学",
    "汶代石刻艺术",
    "明人题勤",
    "对手我国佛教史",
]


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    total = 0
    for old, new in REPLACEMENTS:
        n = text.count(old)
        if n > 1:
            raise RuntimeError(f"replacement matched too many times: {old[:40]}... {n}")
        if n == 1:
            text = text.replace(old, new, 1)
            total += 1
        counts[old[:24]] = n
    if total:
        HTML.write_text(text, encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    missing = [item for item in EXPECTED_TEXT if item not in text]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in text]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return total, counts


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十三卷文物 / 石刻石雕相邻段",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本修正相邻短段明确错识，不做全局替换。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷石刻石雕相邻错识回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第四章石刻石雕` 相邻短段
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按 `page_0102.txt` 修正六神台佛教造像尾段 `文曰`，并拆出 `三、石刻` 小标题。
- 按 `page_0107.txt` 修正石象、石蟾蜍段的 `题字`、`“象石”二字`、`汉代`、`题勒` 等错识，并拆出 `一、石象、石蟾蜍` 小标题。
- 按 `page_0123.txt` 修正第二次普查段 `对于我国佛教史`。
- 本次运行替换：{changed} 处。

## 核对说明

- `复盖` 为源页用字，本次保留不改。
- 仅处理已由页级 OCR 明确支持的短段，未对全书 `文日` 等词做批量处理。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷石刻石雕相邻错识回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第四章石刻石雕` 相邻短段进行回源修复。
- 源文依据：`{SOURCE_NOTE}`。
- 修正六神台佛教造像尾段 `文曰`、`三、石刻` 小标题，石象石蟾段 `题字`、`“象石”二字`、`汉代`、`题勒`，以及第二次普查段 `对于我国佛教史`。
- 保留源页用字 `复盖`；未对全书 `文日` 做批量替换。
- 首次运行替换 {changed} 处；复跑应为 0 处。
- 报告：`output/reports/reader_readability_museum_stone_carving_tail_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum stone carving adjacent residues repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
