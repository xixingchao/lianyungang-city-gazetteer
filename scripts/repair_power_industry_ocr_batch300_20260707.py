# -*- coding: utf-8 -*-
"""Narrow PaddleOCR-backed repairs for the power industry chapter."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "power_industry_ocr_batch300_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "power_industry_ocr_batch300_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_电力工业页级OCR补修第三百批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
]

REPLACEMENTS = [
    (
        "向一市三县皇放射式展布",
        "向一市三县呈放射式展布",
        "PaddleOCR 中/part01/page_0346 为“呈放射式展布”。",
    ),
    (
        "引人徐州电网电力",
        "引入徐州电网电力",
        "PaddleOCR 中/part01/page_0346 为“引入徐州电网电力”。",
    ),
    (
        "35伏升压站增至37500千伏安",
        "35千伏升压站增至37500千伏安",
        "PaddleOCR 中/part01/page_0346 为“35千伏升压站”。",
    ),
    (
        "长180.9公单；110千伏变电所5\n公单；35千伏线路53条",
        "长180.9公里；110千伏变电所5\n座，主变7台，总容量101500千伏安，比1970年增长5.77倍；35千伏线路53条",
        "PaddleOCR 中/part01/page_0346 为“长180.9公里；110千伏变电所5座，主变7台，总容量101500千伏安，比1970年增长5.77倍；35千伏线路53条”。",
    ),
    (
        "长180.9公单；110千伏变电所5公单；35千伏线路53条",
        "长180.9公里；110千伏变电所5座，主变7台，总容量101500千伏安，比1970年增长5.77倍；35千伏线路53条",
        "PaddleOCR 中/part01/page_0346 为“长180.9公里；110千伏变电所5座，主变7台，总容量101500千伏安，比1970年增长5.77倍；35千伏线路53条”。",
    ),
    (
        "长180.9公单；110千伏变电所5\n\n公单；35千伏变电所24座，主变41台，总容量91170千伏安，是1970年的2倍",
        "长180.9公里；110千伏变电所5\n\n座，主变7台，总容量101500千伏安，比1970年增长5.77倍；35千伏线路53条，长704.1公里；35千伏变电所24座，主变41台，总容量91170千伏安，是1970年的2倍",
        "PaddleOCR 中/part01/page_0346 为完整线路、变电所和容量数据。",
    ),
    (
        "长180.9公单；110千伏变电所5 公单；35千伏变电所24座，主变41台，总容量91170千伏安，是1970年的2倍",
        "长180.9公里；110千伏变电所5 座，主变7台，总容量101500千伏安，比1970年增长5.77倍；35千伏线路53条，长704.1公里；35千伏变电所24座，主变41台，总容量91170千伏安，是1970年的2倍",
        "PaddleOCR 中/part01/page_0346 为完整线路、变电所和容量数据。",
    ),
    (
        "长180.9公单；110千伏变电所5\n公单；35千伏变电所24座，主变41台，总容量91170千伏安，是1970年的2倍",
        "长180.9公里；110千伏变电所5\n座，主变7台，总容量101500千伏安，比1970年增长5.77倍；35千伏线路53条，长704.1公里；35千伏变电所24座，主变41台，总容量91170千伏安，是1970年的2倍",
        "PaddleOCR 中/part01/page_0346 为完整线路、变电所和容量数据。",
    ),
    (
        "长180.9公单；110千伏变电所5</p><p>公单；35千伏变电所24座，主变41台，总容量91170千伏安，是1970年的2倍",
        "长180.9公里；110千伏变电所5</p><p>座，主变7台，总容量101500千伏安，比1970年增长5.77倍；35千伏线路53条，长704.1公里；35千伏变电所24座，主变41台，总容量91170千伏安，是1970年的2倍",
        "PaddleOCR 中/part01/page_0346 为完整线路、变电所和容量数据。",
    ),
    (
        "1976年10月15日工投运",
        "1976年10月15日竣工投运",
        "PaddleOCR 中/part01/page_0348 为“1976年10月15日竣工投运”。",
    ),
    (
        "35.千伏平十线降压为22千伏运行",
        "35千伏平十线降压为22千伏运行",
        "PaddleOCR 中/part01/page_0349 为“35千伏平十线降压为22千伏运行”。",
    ),
    (
        "该变电所主要接受阴电网电力",
        "该变电所主要接受淮阴电网电力",
        "PaddleOCR 中/part01/page_0351 为“主要接受淮阴电网电力”。",
    ),
]

CHECK_TERMS = [
    "向一市三县皇放射式展布",
    "引人徐州电网电力",
    "35伏升压站增至37500千伏安",
    "长180.9公单",
    "110千伏变电所5公单",
    "1976年10月15日工投运",
    "35.千伏平十线降压为22千伏运行",
    "该变电所主要接受阴电网电力",
]


def apply_replacements() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new, reason in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                changes.append({
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "old": old,
                    "new": new,
                    "count": count,
                    "reason": reason,
                })
        if text != original:
            path.write_text(text, encoding="utf-8")
    residuals: dict[str, int] = {}
    for term in CHECK_TERMS:
        residuals[term] = 0
        for path in TARGETS:
            if path.exists():
                residuals[term] += path.read_text(encoding="utf-8", errors="ignore").count(term)
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 电力工业页级 OCR 补修 batch300",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书 HTML、正式中册 HTML、正式全书正文汇总、中册 part01 正文源稿。",
        "- 依据：`workbench/ocr/paddle_ocr/中/part01/page_0346.txt`、`page_0348.txt`、`page_0349.txt`、`page_0351.txt`。",
        "- 原则：只处理电力工业章页级 OCR 明确支持的窄短语；不处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['reason']}")
    lines.extend(["", "## 残留计数", ""])
    bad = {key: value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-07 电力工业页级OCR补修第三百批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 中册 part01 第 346、348、349、351 页，窄语境补修电力工业章残字：`皇放射式 -> 呈放射式`、`引人徐州电网 -> 引入徐州电网`、`35伏升压站 -> 35千伏升压站`、`公单 -> 公里/座...`、`日工投运 -> 竣工投运`、`35.千伏 -> 35千伏`、`接受阴电网 -> 接受淮阴电网`，共 {total} 处。
- 报告：`output/reports/power_industry_ocr_batch300_20260707.md`；进度：`output/reports/progress/20260707_电力工业页级OCR补修第三百批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    append_memory(total)
    print(f"total={total}")
    print(f"residuals_nonzero={ {k: v for k, v in residuals.items() if v} }")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
