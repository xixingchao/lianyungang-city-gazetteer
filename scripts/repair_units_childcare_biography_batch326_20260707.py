# -*- coding: utf-8 -*-
"""Narrow unit, childcare, and biography residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "units_childcare_biography_batch326_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "units_childcare_biography_batch326_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_单位托幼人物传残留补修第三百二十六批.md"
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
    ("2977千干瓦", "2977千瓦", "PaddleOCR 上/part03/page_0052 为“2977千瓦”。"),
    ("160干瓦", "160千瓦", "PaddleOCR 上/part03/page_0053 为“160千瓦”。"),
    ("930干瓦", "930千瓦", "PaddleOCR 上/part03/page_0058 为“930千瓦”。"),
    ("人园儿童", "入园儿童", "PaddleOCR 上/part01/page_0261 为“入园儿童”。"),
    ("儿童人园率", "儿童入园率", "PaddleOCR 上/part01/page_0277 为“儿童入园率”。"),
    ("人园\n幼儿134587人", "入园\n幼儿134587人", "PaddleOCR 下/part01/page_0348、0353 为“入园幼儿134587人”。"),
    ("人园幼儿\n134587人", "入园幼儿\n134587人", "PaddleOCR 下/part01/page_0353 为“入园幼儿134587人”。"),
    ("人园幼儿9.5方人", "入园幼儿9.5万人", "PaddleOCR 下/part01/page_0353 为“入园幼儿9.5万人”。"),
    ("人园率80.78", "入园率80.78", "PaddleOCR 下/part01/page_0348 为托幼入园率语境；同卷 page_0299 为“入园率”。"),
    ("幼儿人园", "幼儿入园", "PaddleOCR 下/part01/page_0353 为“幼儿入园”。"),
    ("人托儿童", "入托儿童", "PaddleOCR 下/part02/page_0203、0204 为“入托儿童”。"),
    ("编人中国国民党中央军", "编入中国国民党中央军", "PaddleOCR 下/part02/page_0373 为“编入中国国民党中央军”。"),
    ("打人敌伪内部", "打入敌伪内部", "PaddleOCR 下/part02/page_0368 同页下文为“打入敌伪内部”，徐竞传语境为秘密派遣打入敌伪内部。"),
]

CHECK_TERMS = ["干瓦", "人园", "人托", "编人中国", "打人敌伪"]


def apply_replacements() -> tuple[list[dict], dict[str, int], dict[str, int]]:
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
                changes.append(
                    {
                        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                        "old": old,
                        "new": new,
                        "count": count,
                        "reason": reason,
                    }
                )
        if text != original:
            path.write_text(text, encoding="utf-8")

    residuals: dict[str, int] = {}
    for old, _new, _reason in REPLACEMENTS:
        residuals[old] = 0
        for path in TARGETS:
            if path.exists():
                residuals[old] += path.read_text(encoding="utf-8", errors="ignore").count(old)

    term_totals: dict[str, int] = {}
    for term in CHECK_TERMS:
        total = 0
        for path in TARGETS:
            if path.exists():
                total += path.read_text(encoding="utf-8", errors="ignore").count(term)
        term_totals[term] = total
    return changes, residuals, term_totals


def fmt(value: str) -> str:
    return value.replace("\n", "\\n")


def render(changes: list[dict], residuals: dict[str, int], term_totals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 单位托幼人物传残留补修 batch326",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式阅读 HTML、全书正文汇总、上中下相关分册源稿。",
        "- 依据：PaddleOCR 上/part03/page_0052、0053、0058，上/part01/page_0261、0277，下/part01/page_0348、0353，下/part02/page_0203、0204、0368、0373。",
        "- 原则：只处理水利装机单位、托幼入园/入托、人物传编入/打入等完整短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
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
        lines.append(f"- `{term}` 总残留：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int, term_totals: dict[str, int]) -> None:
    marker = "## 2026-07-07 单位托幼人物传残留补修第三百二十六批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    totals = "，".join(f"`{term}` {count}" for term, count in term_totals.items())
    block = f"""
{marker}

- 依据 PaddleOCR 上/part03/page_0052、0053、0058，上/part01/page_0261、0277，下/part01/page_0348、0353，下/part02/page_0203、0204、0368、0373，窄语境补修水利装机单位、托幼入园/入托、人物传编入/打入残留，共 {total} 处。
- 代表修复：`2977千干瓦/160干瓦/930干瓦 -> 2977千瓦/160千瓦/930千瓦`，`人园儿童/儿童人园率/人园幼儿/幼儿人园 -> 入园儿童/儿童入园率/入园幼儿/幼儿入园`，`人托儿童 -> 入托儿童`，`编人中国国民党中央军 -> 编入中国国民党中央军`，`打人敌伪内部 -> 打入敌伪内部`。
- 本批检查范围内剩余小项：{totals}。
- 报告：`output/reports/units_childcare_biography_batch326_20260707.md`；进度：`output/reports/progress/20260707_单位托幼人物传残留补修第三百二十六批.md`。
- 未作 `人/入`、`方/万` 等全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
    append_memory(total, term_totals)
    print(f"total={total}")
    print(f"residuals_nonzero={ {k: v for k, v in residuals.items() if v} }")
    print(f"term_totals={term_totals}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
