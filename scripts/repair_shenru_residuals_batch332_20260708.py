# -*- coding: utf-8 -*-
"""Final narrow 深人 -> 深入 repairs for source-backed residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "shenru_residuals_batch332_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "shenru_residuals_batch332_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_深入残留补修第三百三十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    (
        "广泛深人地开展社会主",
        "广泛深入地开展社会主",
        "PaddleOCR 中/part02/page_0424.txt 为“广泛深入地开展社会主”。",
    ),
    (
        "随着改革开放的深人",
        "随着改革开放的深入",
        "PaddleOCR 下/part02/page_0049.txt 为“随着改革开放的深入”。",
    ),
    (
        "随着改革\n深人，多数企业推行了浮动工资等级制",
        "随着改革\n深入，多数企业推行了浮动工资等级制",
        "PaddleOCR 下/part01/page_0260.txt 为跨行“随着改革 / 深入，多数企业...”。",
    ),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_replacements() -> tuple[list[dict], int]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        original = text
        for old, new, evidence in REPLACEMENTS:
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
    residual = sum(read(path).count("深人") for path in TARGETS if path.exists())
    return changes, residual


def render(changes: list[dict], residual: int) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 深入残留补修 batch332",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正文汇总与上中下相关分册源稿。",
        "- 原则：只处理页级 PaddleOCR 明确支撑的 `深人 -> 深入` 残留；不处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", "", f"- `深人`：{residual}"])
    return "\n".join(lines) + "\n"


def append_memory(total: int, residual: int) -> None:
    marker = "## 2026-07-08 深入残留补修第三百三十二批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据页级 PaddleOCR，补修 batch331 后剩余 `深人 -> 深入` 残留，共 {total} 处，涉及 3 个唯一语境及其分册/全书汇总同步。
- 代表修复：`广泛深入地开展社会主义劳动竞赛`、`随着改革开放的深入`、跨行 `随着改革 / 深入，多数企业...`。
- 本批后检查范围 `深人` 残留 {residual} 处；报告：`output/reports/shenru_residuals_batch332_20260708.md`；进度：`output/reports/progress/20260708_深入残留补修第三百三十二批.md`。
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
