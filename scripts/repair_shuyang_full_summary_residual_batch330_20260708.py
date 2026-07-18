# -*- coding: utf-8 -*-
"""Full-summary-only remaining 沭阳 residual repairs with phrase evidence."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
REPORT = ROOT / "output" / "reports" / "shuyang_full_summary_residual_batch330_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "shuyang_full_summary_residual_batch330_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总沭阳余项补修第三百三十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("赣榆、述阳大旱，人相食，儿女", "赣榆、沭阳大旱，人相食，鬻儿女", "PaddleOCR 上/part01/page_0051 为“赣榆、沭阳大旱，人相食，鬻儿女”。"),
    ("新述河、新沂河和苏北述阳", "新沭河、新沂河和苏北沭阳", "PaddleOCR 上/part01/page_0190 为“新沭河、新沂河和苏北沭阳”。"),
    ("海州、赣榆、述阳皆阜、蝗", "海州、赣榆、沭阳皆旱、蝗", "PaddleOCR 上/part01/page_0209 为“海州、赣榆、沭阳皆旱、蝗”。"),
    ("赣榆、述阳蝗害", "赣榆、沭阳蝗害", "PaddleOCR 上/part01/page_0209 为“赣榆、沭阳蝗害”。"),
    ("海州、述阳卵时地震，从乾及翼", "海州、沭阳卯时地震，从乾及巽", "PaddleOCR 上/part01/page_0210 为“海州、沭阳卯时地震，从乾及巽”。"),
    ("东海、述阳、怀仁4县", "东海、沭阳、怀仁4县", "PaddleOCR 上/part01/page_0214 为“东海、沭阳、怀仁4县”。"),
    ("东海、述阳、赣榆、涟水5县", "东海、沭阳、赣榆、涟水5县", "PaddleOCR 上/part01/page_0214 为“东海、沭阳、赣榆、涟水5县”。"),
    ("海州升直隶州，辖赣榆、述阳2县", "海州升直隶州，辖赣榆、沭阳2县", "PaddleOCR 上/part01/page_0239 为“海州升直隶州，辖赣榆、沭阳2县”。"),
    ("改道经述阳从海州蔷薇河入海，海州水惠频仍", "改道经沭阳从海州蔷薇河入海，海州水患频仍", "分册源稿已为沭阳；PaddleOCR 上/part02/page_0268 为“沭阳从海州蔷薇河入海，海州水患频仍”。"),
    ("河又南流至述阳经海州入海，海州水惠频仍", "河又南流至沭阳经海州入海，海州水患频仍", "PaddleOCR 上/part02/page_0268 为“河又南流至沭阳经海州入海，海州水患频仍”。"),
    ("引沐入赣虽有利于述阳", "引沭入赣虽有利于沭阳", "PaddleOCR 上/part02/page_0268 为“引沭入赣虽有利于沭阳”。"),
    ("境外述阳、临述县述河水系", "境外沭阳、临沭县沭河水系", "PaddleOCR 上/part03/page_0063 为“境外沭阳、临沭县沭河水系”。"),
    ("河述阳站洪峰不大于6000立方米每秒。普河临洪闸", "河沭阳站洪峰不大于6000立方米每秒。蔷薇河临洪闸", "PaddleOCR 上/part03/page_0066 为“河沭阳站洪峰不大于6000立方米每秒。蔷薇河临洪闸”。"),
    ("灌云、东海、赣榆、述阳、涟水五县", "灌云、东海、赣榆、沭阳、涟水五县", "PaddleOCR 上/part03/page_0159 为“灌云、东海、赣榆、沭阳、涟水五县”。"),
    ("东海、赣榆、灌云、述阳、涟水等五县", "东海、赣榆、灌云、沭阳、涟水等五县", "分册源稿同步；PaddleOCR 中/part02/page_0327 为“东海、赣榆、灌云、沭阳、涟水等五县”。"),
    ("楚州（今淮安市)经述阳、海州", "楚州（今淮安市)经沭阳、海州", "分册源稿同步；PaddleOCR 中/part02/page_0019 为“经沭阳、海州”。"),
    ("青述线青湖至述阳", "青沭线青湖至沭阳", "PaddleOCR 中/part02/page_0022 为“青沭线 青湖至沭阳”。"),
    ("宿述灌线宿迁经述阳吴集人灌云县境", "宿沭灌线宿迁经沭阳吴集入灌云县境", "PaddleOCR 中/part02/page_0022 为“宿沭灌线宿迁经沭阳吴集入灌云县境”。"),
    ("述阳人郭姓", "沭阳人郭姓", "PaddleOCR 中/part02/page_0123 为“沭阳人郭姓”。"),
    ("灌云、响水、述阳、东海", "灌云、响水、沭阳、东海", "PaddleOCR 中/part02/page_0142 为“灌云、响水、沭阳、东海”。"),
    ("赣榆、述阳二县", "赣榆、沭阳二县", "PaddleOCR 中/part02/page_0211 为“赣榆、沭阳二县”。"),
    ("述阳、赣榆等地", "沭阳、赣榆等地", "PaddleOCR 中/part02/page_0253 为“沭阳、赣榆等地”。"),
    ("灌云、赣榆、述阳、郊城五县", "灌云、赣榆、沭阳、郯城五县", "PaddleOCR 中/part02/page_0401 为“灌云、赣榆、沭阳、郯城五县”。"),
    ("第一中心县委在东灌述地区，辖灌云、述阳两县", "第一中心县委在东灌沭地区，辖灌云、沭阳两县", "PaddleOCR 中/part02/page_0401 为“东灌沭地区，辖灌云、沭阳两县”。"),
    ("述阳独立团", "沭阳独立团", "PaddleOCR 中/part02/page_0408 为“沭阳独立团”。"),
    ("江苏省述阳云英粉填料厂", "江苏省沭阳云英粉填料厂", "PaddleOCR 中/part02/page_0469 为“江苏省沭阳云英粉填料厂”。"),
    ("海州、赣榆、述阳士民捐助，建石室书院，招一州二邑诸生肆业", "海州、赣榆、沭阳士民捐助，建石室书院，招一州二邑诸生肄业", "PaddleOCR 下/part02/page_0348 为“海州、赣榆、沭阳士民捐助，建石室书院，招一州二邑诸生肄业”。"),
    ("销往东海、灌云、述阳、临述、日照等地", "销往东海、灌云、沭阳、临沭、日照等地", "PaddleOCR 中/part01/page_0034 为“销往东海、灌云、沭阳、临沭、日照等地”。"),
    ("仲兆率余部至述阳烂泥塘", "仲兆琚率余部至沭阳烂泥塘", "PaddleOCR 下/part01/page_0156 为“仲兆琚率余部至沭阳烂泥塘”。"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_replacements() -> tuple[list[dict], int]:
    text = read(TARGET)
    changes: list[dict] = []
    for old, new, evidence in sorted(REPLACEMENTS, key=lambda item: len(item[0]), reverse=True):
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            changes.append({"old": old, "new": new, "count": count, "evidence": evidence})
    if changes:
        TARGET.write_text(text, encoding="utf-8")
    residual = read(TARGET).count("述阳")
    return changes, residual


def render(changes: list[dict], residual: int) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 全书汇总沭阳余项补修 batch330",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：仅 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。",
        "- 原则：只处理剩余 `述阳` 中由分册源稿或 PaddleOCR 明确支撑的成句残留，并同步修正同句 OCR 错字；不作全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", "", f"- `述阳`：{residual}"])
    return "\n".join(lines) + "\n"


def append_memory(total: int, residual: int) -> None:
    marker = "## 2026-07-08 全书汇总沭阳余项补修第三百三十批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 继续限定 `workbench/body_chapters/连云港市志_全书_正文汇总.md`，依据分册源稿和 PaddleOCR 成句证据，补修剩余 `述阳` 及同句 OCR 错字，共 {total} 处。
- 同步修正代表项：`新述河/述阳 -> 新沭河/沭阳`、`引沐入赣 -> 引沭入赣`、`临述县述河 -> 临沭县沭河`、`普河临洪闸 -> 蔷薇河临洪闸`、`青述线/宿述灌线 -> 青沭线/宿沭灌线` 等。
- 本批后全书汇总 `述阳` 残留 {residual} 处；报告：`output/reports/shuyang_full_summary_residual_batch330_20260708.md`；进度：`output/reports/progress/20260708_全书汇总沭阳余项补修第三百三十批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residual = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "residual": residual, "changes": changes}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    content = render(changes, residual)
    REPORT.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")
    append_memory(total, residual)
    print(f"total={total}")
    print(f"residual={residual}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
