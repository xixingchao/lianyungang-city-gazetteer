# -*- coding: utf-8 -*-
"""Narrow numeric 方人 -> 万人 residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "numeric_people_units_batch328_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "numeric_people_units_batch328_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_数字人口单位残留补修第三百二十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_上册.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("共应接种20.49\n方人，实际接种16.8万人", "共应接种20.49\n万人，实际接种16.8万人", "PaddleOCR 下/part02/page_0173 为“共应接种20.49万人，实际接种16.8万人”。"),
    ("1.5方人", "1.5万人", "PaddleOCR 上/part01/page_0070 为“参加群众达1.5万人”。"),
    ("27.17方人", "27.17万人", "PaddleOCR 上/part01/page_0280 为“27.17万人”。"),
    ("8.4方人", "8.4万人", "PaddleOCR 上/part01/page_0293 为“在校学生8.4万人”。"),
    ("1.76方人", "1.76万人", "PaddleOCR 上/part02/page_0149 为“全民职工1.76万人”。"),
    ("1.43方人", "1.43万人", "PaddleOCR 上/part02/page_0149 为“个体劳动者1.43万人”。"),
    ("1.25方人", "1.25万人", "PaddleOCR 中/part01/page_0062 为“全民企业职工1.25万人”。"),
    ("1.6方人", "1.6万人", "PaddleOCR 中/part02/page_0159 为“职工1.6万人”。"),
    ("50方人", "50万人", "PaddleOCR 下/part01/page_0028 为“灾民50万人”。"),
    ("20方人", "20万人", "PaddleOCR 下/part01/page_0028 为“断炊者20万人”。"),
    ("10.8方人", "10.8万人", "PaddleOCR 下/part01/page_0343 为“贫协会员发展到10.8万人”。"),
    ("3.78方人", "3.78万人", "PaddleOCR 下/part02/page_0172 为“饮用山区水库水3.78万人”。"),
    ("65.13方人", "65.13万人", "PaddleOCR 下/part02/page_0181 为“受益65.13万人”。"),
]

CHECK_TERMS = [
    "1.5方人", "27.17方人", "8.4方人", "1.76方人", "1.43方人", "1.25方人", "1.6方人",
    "50方人", "20方人", "10.8方人", "3.78方人", "65.13方人", "20.49\n方人",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_replacements() -> tuple[list[dict], dict[str, int], dict[str, int]]:
    changes: list[dict] = []
    ordered = sorted(REPLACEMENTS, key=lambda item: len(item[0]), reverse=True)
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        original = text
        for old, new, reason in ordered:
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
    for old, _new, _reason in REPLACEMENTS:
        residuals[old] = sum(read(path).count(old) for path in TARGETS if path.exists())

    term_totals: dict[str, int] = {}
    for term in CHECK_TERMS:
        term_totals[term] = sum(read(path).count(term) for path in TARGETS if path.exists())
    return changes, residuals, term_totals


def fmt(value: str) -> str:
    return value.replace("\n", "\\n")


def render(changes: list[dict], residuals: dict[str, int], term_totals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 数字人口单位残留补修 batch328",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式阅读 HTML、全书正文汇总、上中下相关分册源稿。",
        "- 依据：PaddleOCR 上/part01/page_0070、0280、0293，上/part02/page_0149，中/part01/page_0062，中/part02/page_0159，下/part01/page_0028、0343，下/part02/page_0172、0173、0181。",
        "- 原则：只处理带数字且 OCR 可证的 `方人 -> 万人`；`外方人员`、`私方人员`、`官方人员`、`双方` 等正常词不处理。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            lines.append(f"- `{item['path']}`：`{fmt(item['old'])}` -> `{fmt(item['new'])}`；次数 {item['count']}；依据：{item['reason']}")
    else:
        lines.append("- 本批没有新增替换。")

    lines.extend(["", "## 残留计数", ""])
    bad = {key: value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{fmt(key)}`：{value}")
    lines.append("")
    for term, value in term_totals.items():
        lines.append(f"- `{fmt(term)}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-08 数字人口单位残留补修第三百二十八批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 上/part01/page_0070、0280、0293，上/part02/page_0149，中/part01/page_0062，中/part02/page_0159，下/part01/page_0028、0343，下/part02/page_0172、0173、0181，窄语境补修带数字人口单位残留，共 {total} 处。
- 代表修复：`1.5/27.17/8.4/1.76/1.43/1.25/1.6/50/20/10.8/3.78/65.13方人 -> 万人`，以及跨行 `共应接种20.49\n方人 -> 共应接种20.49\n万人`。
- 报告：`output/reports/numeric_people_units_batch328_20260708.md`；进度：`output/reports/progress/20260708_数字人口单位残留补修第三百二十八批.md`。
- 未作 `方/万` 全局替换；`外方人员`、`私方人员`、`官方人员`、`双方` 等正常词保留；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals, term_totals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "term_totals": term_totals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals, term_totals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    append_memory(total)
    print(f"total={total}")
    print(f"residuals_nonzero={ {k: v for k, v in residuals.items() if v} }")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
