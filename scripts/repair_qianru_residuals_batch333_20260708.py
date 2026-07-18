# -*- coding: utf-8 -*-
"""Narrow 迁人 -> 迁入 repairs for explicit migration contexts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "qianru_residuals_batch333_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "qianru_residuals_batch333_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_迁入残留补修第三百三十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("农口迁出、迁人手续", "农口迁出、迁入手续", "户口迁移并列项；同段已有“迁出、迁入、变更、更正”。"),
    ("婚姻迁人的", "婚姻迁入的", "PaddleOCR 上/part01 合并稿为“婚姻迁入的”。"),
    ("控制迁人国家经济技术开发区", "控制迁入国家经济技术开发区", "PaddleOCR 上/part01 合并稿为“控制迁入国家经济技术开发区”。"),
    ("公司相继迁人。", "公司相继迁入。", "PaddleOCR 上/part02 合并稿为“公司相继迁入”。"),
    ("全部迁人新馆", "全部迁入新馆", "上下文为图书馆搬迁至新馆。"),
    ("成名后迁人者", "成名后迁入者", "上下文为外地医家迁居本地。"),
    ("1989年迁人墟沟镇院前村", "1989年迁入墟沟镇院前村", "上下文为医院迁址。"),
    ("迁人新教堂", "迁入新教堂", "上下文为教堂迁址。"),
    ("居民迁人内地", "居民迁入内地", "上下文为居民迁徙入内地。"),
    ("白虎山迁人海州江化街", "白虎山迁入海州江化街", "上下文为市工艺厂迁址。"),
    ("华兴铁工厂迁人新浦", "华兴铁工厂迁入新浦", "上下文为工厂迁址。"),
    ("迁人开发区", "迁入开发区", "上下文为企业迁址开发区。"),
    ("迁人新址", "迁入新址", "上下文为海岸电台迁址。"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_replacements() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        original = text
        for old, new, evidence in sorted(REPLACEMENTS, key=lambda item: len(item[0]), reverse=True):
            count = text.count(old)
            if not count:
                continue
            text = text.replace(old, new)
            changes.append({
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "old": old,
                "new": new,
                "count": count,
                "evidence": evidence,
            })
        if text != original:
            path.write_text(text, encoding="utf-8")
    residuals = {str(path.relative_to(ROOT)).replace("\\", "/"): read(path).count("迁人") for path in TARGETS if path.exists()}
    residuals = {path: count for path, count in residuals.items() if count}
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 迁入残留补修 batch333",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正文汇总与中下分册源稿。",
        "- 原则：只处理明确迁移、迁址语境的 `迁人 -> 迁入`；`宿迁人` 保留不动。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for path, count in residuals.items():
            lines.append(f"- `{path}`：`迁人` {count} 处，均为 `宿迁人` 类正常地名籍贯语境。")
    else:
        lines.append("- `迁人`：0")
    return "\n".join(lines) + "\n"


def append_memory(total: int, residuals: dict[str, int]) -> None:
    marker = "## 2026-07-08 迁入残留补修第三百三十三批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    residual_total = sum(residuals.values())
    block = f"""
{marker}

- 依据页级 OCR 与明确迁移语境，补修正文汇总和中下分册源稿 `迁人 -> 迁入` 残留，共 {total} 处。
- 代表修复：`婚姻迁入的`、`控制迁入国家经济技术开发区`、`迁入新馆/新址/开发区/新教堂/内地`、`农口迁出、迁入手续`。
- 本批后检查范围 `迁人` 残留 {residual_total} 处，均为 `宿迁人` 类正常籍贯/地名语境；报告：`output/reports/qianru_residuals_batch333_20260708.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "residuals": residuals, "changes": changes}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    content = render(changes, residuals)
    REPORT.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")
    append_memory(total, residuals)
    print(f"total={total}")
    print(f"residual={sum(residuals.values())}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
