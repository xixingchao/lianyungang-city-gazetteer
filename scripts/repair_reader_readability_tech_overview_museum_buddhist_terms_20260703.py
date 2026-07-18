# -*- coding: utf-8 -*-
"""Repair two source-backed Buddhist/medical term OCR errors in reader text."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_tech_overview_museum_buddhist_terms_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_tech_overview_museum_buddhist_terms_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_科技概述与馆藏造像错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part01/page_0414.txt:16-18; "
    "workbench/ocr/paddle_ocr/下/part02/page_0110.txt:7-18"
)

REPLACEMENTS = [
    (
        "清末，海州沈云需等人兴办了13家农、工、商企业，锦屏磷矿开创了我国采磷工业的先河。当时美国牧师慕庚扬在海州创办了义德医院，西医传人境内。民国2年（1913年），中国水利专家板浦人武同举与法国河海工程师格锐奈联手首次对江苏海岸进行测量",
        "清末，海州沈云霈等人兴办了13家农、工、商企业，锦屏磷矿开创了我国采磷工业的先河。当时美国牧师慕庚扬在海州创办了义德医院，西医传入境内。民国2年（1913年），中国水利专家板浦人武同举与法国河海工程师格锐奈联手首次对江苏海岸进行测量",
    ),
    (
        "造像幢为灰白色大理石雕成，高20厘米，宽8厘米，为一经幢形的四面造像。幢顶平展，有二层檐，四角有弧形翘棱，四面正中各有一个造像浅，分别为菩萨和佛的浅浮雕。或缨络披肩，或高宝冠；有的面目清秀，有的面貌丰满，皆著圆领裂裟，衣纹飘熟，线条流畅。结蹦跌坐于平台之上。",
        "造像幢为灰白色大理石雕成，高20厘米，宽8厘米，为一经幢形的四面造像龛。幢顶平展，有二层檐，四角有弧形翘棱，四面正中各有一个造像浅龛，分别为菩萨和佛的浅浮雕。或缨络披肩，或高髻宝冠；有的面目清秀，有的面貌丰满，皆著圆领袈裟，衣纹飘飘，线条流畅。结跏趺坐于平台之上。",
    ),
    (
        "北齐武平三年（572年)铭石造像，高25厘米，宽11厘米，为青灰色片麻岩雕成的浅浮雕立佛像。高肉馨，面目清瘦，双眼微合，嘴唇紧闭，鼻梁短而鼻头大。脖颈细长，外披通户式裂裟，足立于平台。",
        "北齐武平三年（572年）铭石造像，高25厘米，宽11厘米，为青灰色片麻岩雕成的浅浮雕立佛像。高肉髻，面目清瘦，双眼微合，嘴唇紧闭，鼻梁短而鼻头大。脖颈细长，外披通肩式袈裟，足立于平台。",
    ),
]

EXPECTED_TEXT = [
    "沈云霈等人兴办了13家农、工、商企业",
    "西医传入境内",
    "造像龛",
    "高髻宝冠",
    "圆领袈裟，衣纹飘飘",
    "结跏趺坐于平台之上",
    "高肉髻",
    "通肩式袈裟",
]
RESIDUALS = [
    "沈云需等人兴办了13家",
    "西医传人境内",
    "为一经幢形的四面造像。幢顶",
    "造像浅，分别为菩萨",
    "高宝冠；",
    "圆领裂裟",
    "衣纹飘熟",
    "结蹦跌坐",
    "高肉馨，面目清瘦",
    "通户式裂裟",
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
        "scope": "第五十一卷科技概述；第五十三卷馆藏文物东魏/北齐造像段",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本修正少量明确错识，不扩大改写范围。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 科技概述与馆藏造像错识回源修复

- 时间：{now}
- 范围：`第五十一卷科技 / 概述`；`第五十三卷文物 / 第五章馆藏文物 / 第一节玉石器` 中东魏造像幢、北齐石造像两段
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按 `page_0414.txt` 修正 `沈云霈`、`西医传入境内`。
- 按 `page_0110.txt` 修正 `造像龛`、`高髻宝冠`、`圆领袈裟`、`衣纹飘飘`、`结跏趺坐`、`高肉髻`、`通肩式袈裟`。
- 首次运行已写入 3 处目标短段替换；稳定复跑替换：{changed} 处。

## 核对说明

- 仅修复源页已有明确文本的短段；未处理同页之后的其它馆藏条目。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 科技概述与馆藏造像错识回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十一卷科技概述、第五十三卷馆藏文物东魏造像幢和北齐石造像短段进行回源修复。
- 源文依据：`{SOURCE_NOTE}`。
- 修正 `沈云霈`、`西医传入境内`、`造像龛`、`高髻宝冠`、`圆领袈裟`、`衣纹飘飘`、`结跏趺坐`、`高肉髻`、`通肩式袈裟` 等明确错识。
- 首次运行已写入 3 处目标短段替换；稳定复跑替换 {changed} 处。
- 报告：`output/reports/reader_readability_tech_overview_museum_buddhist_terms_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("tech overview / museum Buddhist terms repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
