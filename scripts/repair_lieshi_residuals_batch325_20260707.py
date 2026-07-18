# -*- coding: utf-8 -*-
"""Narrow 烈土 -> 烈士 residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "lieshi_residuals_batch325_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "lieshi_residuals_batch325_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_烈士残留补修第三百二十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_上册.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("朱爱周烈土\n墓", "朱爱周烈士\n墓", "PaddleOCR 下/part02/page_0088 为“朱爱周烈士墓”。"),
    ("朱爱周烈土墓", "朱爱周烈士墓", "PaddleOCR 下/part02/page_0088 为“朱爱周烈士墓”。"),
    ("吴伦东烈土事迹展览", "吴伦东烈士事迹展览", "PaddleOCR 下/part01/page_0025 为“吴伦东烈士”；同页为烈士褒扬段。"),
    ("吴伦东烈土塑像", "吴伦东烈士塑像", "PaddleOCR 下/part01/page_0025 为“吴伦东烈士”；同页为烈士褒扬段。"),
    ("吴伦东烈土大会", "吴伦东烈士大会", "PaddleOCR 下/part01/page_0025 为“追认吴伦东烈士大会”。"),
    ("吕祥璧烈土永垂不朽", "吕祥璧烈士永垂不朽", "PaddleOCR 下/part02/page_0089 为“吕祥璧烈士永垂不朽”。"),
    ("祭扫海烈土纪念塔", "祭扫淮海烈士纪念塔", "PaddleOCR 下/part01/page_0323 为“祭扫淮海烈士纪念塔”。"),
    ("海烈土纪念塔", "海烈士纪念塔", "PaddleOCR 下/part01/page_0323 为“淮海烈士纪念塔”；仅兜底修正士字。"),
    ("抗日烈土纪念塔", "抗日烈士纪念塔", "PaddleOCR 下/part01/page_0024、中/part02/page_0115 为“抗日烈士纪念塔”。"),
    ("烈土纪念塔前", "烈士纪念塔前", "PaddleOCR 下/part02/page_0088、0089 相关段为烈士纪念建筑语境。"),
    ("烈土褒扬", "烈士褒扬", "PaddleOCR 下/part01/page_0024 为“三、烈士褒扬”。"),
    ("烈土的英名", "烈士的英名", "PaddleOCR 下/part01/page_0025、中/part01/page_0306 为“烈士的英名”。"),
    ("烈土英名", "烈士英名", "PaddleOCR 下/part01/page_0024 为“烈士英名”。"),
    ("烈土事迹", "烈士事迹", "PaddleOCR 下/part01/page_0024 为“烈士事迹”。"),
    ("烈土\n墓", "烈士\n墓", "PaddleOCR 下/part01/page_0024、0025 与下/part02/page_0089 为“烈士墓”。"),
    ("烈土墓", "烈士墓", "PaddleOCR 下/part01/page_0024、0025 与下/part02/page_0089 为“烈士墓”。"),
    ("烈\n土公墓", "烈\n士公墓", "PaddleOCR 下/part01/page_0025 为“烈士公墓”。"),
    ("烈土公墓", "烈士公墓", "PaddleOCR 下/part01/page_0025 为“烈士公墓”。"),
]


def apply_replacements() -> tuple[list[dict], dict[str, int], int]:
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

    lieshi_tu_total = 0
    for path in TARGETS:
        if path.exists():
            lieshi_tu_total += path.read_text(encoding="utf-8", errors="ignore").count("烈土")
    return changes, residuals, lieshi_tu_total


def render(changes: list[dict], residuals: dict[str, int], lieshi_tu_total: int) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 烈士残留补修 batch325",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式阅读 HTML、全书正文汇总、上册/中册/下册相关分册源稿。",
        "- 依据：PaddleOCR 下/part01/page_0024、0025、0323，下/part02/page_0088、0089，中/part02/page_0115，中/part01/page_0306。",
        "- 原则：只处理烈士陵园、纪念塔、烈士墓、公墓、英名、事迹等完整短语；未作全局 `烈土 -> 烈士`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            old = item["old"].replace("\n", "\\n")
            new = item["new"].replace("\n", "\\n")
            lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['reason']}")
    else:
        lines.append("- 本批没有新增替换。")

    lines.extend(["", "## 残留计数", ""])
    bad = {key: value for key, value in residuals.items() if value}
    if not bad and lieshi_tu_total == 0:
        lines.append("- 本批检查短语与 `烈土` 在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key.replace(chr(10), '\\n')}`：{value}")
        lines.append(f"- `烈土` 总残留：{lieshi_tu_total}")
    return "\n".join(lines) + "\n"


def append_memory(total: int, lieshi_tu_total: int) -> None:
    marker = "## 2026-07-07 烈士残留补修第三百二十五批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 下/part01/page_0024、0025、0323，下/part02/page_0088、0089，中/part02/page_0115，中/part01/page_0306，窄语境补修烈士相关残留：`烈土褒扬/抗日烈土纪念塔/烈土的英名/烈土事迹/烈土墓/烈土公墓/吴伦东烈土/朱爱周烈土墓/吕祥璧烈土永垂不朽` 等，共 {total} 处。
- 对 `祭扫海烈土纪念塔` 依据页级 OCR 修为 `祭扫淮海烈士纪念塔`；本批检查范围内 `烈土` 总残留为 {lieshi_tu_total}。
- 报告：`output/reports/lieshi_residuals_batch325_20260707.md`；进度：`output/reports/progress/20260707_烈士残留补修第三百二十五批.md`。
- 未作全局 `烈土 -> 烈士`；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals, lieshi_tu_total = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "lieshi_tu_total": lieshi_tu_total,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals, lieshi_tu_total)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    append_memory(total, lieshi_tu_total)
    print(f"total={total}")
    print(f"lieshi_tu_total={lieshi_tu_total}")
    print(f"residuals_nonzero={ {k: v for k, v in residuals.items() if v} }")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
