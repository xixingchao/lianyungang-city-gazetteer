# -*- coding: utf-8 -*-
"""Repair source-verified money-unit OCR slips across several volumes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_multi_volume_money_units_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_multi_volume_money_units_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_多卷金额单位错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part01/page_0280.txt:17-25; page_0284.txt:30; "
    "page_0290.txt:36; page_0395.txt:35-36; page_0424.txt:17; page_0432.txt:28; "
    "page_0485.txt:18; workbench/ocr/paddle_ocr/中/part02/page_0074.txt:32; "
    "page_0134.txt:9-20; page_0188.txt:4; workbench/ocr/paddle_ocr/下/part01/page_0315.txt:18"
)

REPLACEMENTS = [
    ("第二十三卷建材-灌云水泥投资", "灌云县水泥厂投资425方元", "灌云县水泥厂投资425万元", "中/part01/page_0280.txt:17-25"),
    ("第二十三卷建材-水泥制品产值", "工业总产值300方元", "工业总产值300万元", "中/part01/page_0284.txt:30"),
    ("第二十三卷建材-耐火材料投资", "耐火材料广投资42方元", "耐火材料厂投资42万元", "中/part01/page_0290.txt:36"),
    ("第二十七卷乡镇企业-以工补农", "拿出151方元用于以工补农", "拿出151万元用于以工补农", "中/part01/page_0395.txt:35"),
    ("第二十七卷乡镇企业-教育事业", "95方元用于教育事业", "95万元用于教育事业", "中/part01/page_0395.txt:35-36"),
    ("第二十七卷乡镇企业-集体福利", "63方元用于农村集体福利事业", "63万元用于农村集体福利事业", "中/part01/page_0395.txt:35-36"),
    ("第二十七卷乡镇企业-其它事业投入", "在其它事业上也投人366方元", "在其它事业上也投入366万元", "中/part01/page_0395.txt:35-36"),
    ("第二十八卷开发区-建设投资", "基本建设总投资繁计23082方元", "基本建设总投资累计23082万元", "中/part01/page_0424.txt:17"),
    ("第二十八卷开发区-企业产值", "实现产值1867.8方元、税利148方元", "实现产值1867.8万元、税利148万元", "中/part01/page_0432.txt:28"),
    ("第二十九卷口岸-外供销售额", "实现销售额2504方元", "实现销售额2504万元", "中/part01/page_0485.txt:18"),
    ("第三十一卷邮电-集邮收入", "集邮业务收入达48.5方元", "集邮业务收入达48.5万元", "中/part02/page_0074.txt:32"),
    ("第三十三卷商业-地方品种收购值", "收购值由200万元增加到647方元", "收购值由200万元增加到647万元", "中/part02/page_0134.txt:9"),
    ("第三十三卷商业-省外调给", "调给省外321方元", "调给省外321万元", "中/part02/page_0134.txt:14"),
    ("第三十三卷商业-供销社调给", "调给市区供销社306方元", "调给市区供销社306万元", "中/part02/page_0134.txt:20"),
    ("第三十五卷外贸-医用敷料", "收购值为1550.17方元", "收购值为1550.17万元", "中/part02/page_0188.txt:4"),
    ("第四十九卷社团-福利设施资金", "资金达7219方元", "资金达7219万元", "下/part01/page_0315.txt:18"),
]

SKIPPED = [
    "金融卷、税务卷等剩余 `方元` 仍需逐页定位，本批不处理。",
    "文化卷的 `方元户的追求` 是作品名，不是金额单位。",
]


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    for label, old, new, _source in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        elif new not in text:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    HTML.write_text(text, encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    missing = [new for _label, _old, new, _source in REPLACEMENTS if new not in text]
    residuals = [old for _label, old, new, _source in REPLACEMENTS if old in text and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    items = [
        {"label": label, "old": old, "new": new, "source": source, "count": counts[label]}
        for label, old, new, source in REPLACEMENTS
    ]
    payload = {
        "time": now,
        "scope": "第二十三、二十七、二十八、二十九、三十一、三十三、三十五、四十九卷",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 可直接证明为 `万元` 的金额单位错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 多卷金额单位错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：修正多卷中页级 OCR 明确为 `万元` 的 `方元` 错识，并同步修正同源短错 `投人/繁计/广`。",
        "- 保留：" + "；".join(SKIPPED),
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 多卷金额单位错识回源修复

- 对第二十三、二十七、二十八、二十九、三十一、三十三、三十五、四十九卷做金额单位错识小批回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `425方元/300方元/42方元/151方元/95方元/63方元/366方元/23082方元/1867.8方元/148方元/2504方元/48.5方元/647方元/321方元/306方元/1550.17方元/7219方元` → 对应 `万元`，并同步修正同源短错 `投人`→`投入`、`繁计`→`累计`、`广`→`厂`。
- 金融卷、税务卷等剩余 `方元` 仍需逐页定位；文化卷 `方元户的追求` 为作品名，本批不处理。
- 报告：`output/reports/reader_readability_multi_volume_money_units_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 多卷金额单位错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
