# -*- coding: utf-8 -*-
"""Twenty-second source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch22_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch22_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十二批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "淮海工学院校名误识",
        "准海工学院",
        "淮海工学院",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5468-5470；workbench/body_chapters/连云港市志_全书_正文汇总.md:171740-171741",
    ),
    (
        "淮海大学校名漏字",
        "1985年建海大学",
        "1985年建淮海大学",
        "workbench/ocr/paddle_ocr/下/part01/page_0348.txt:18-20",
    ),
    (
        "吴伦东烈士句 OCR 残留（HTML）",
        "<p>1982年12月30日，中共连云港市委、市人民政府召开追认吴伦东烈土大会，宣读江苏省人民政府关于授予为保卫民兵训练枪支、与盗窃罪犯搏斗中牺牲的市毛巾广工人吴伦东革命烈士”称号的决定。</p>",
        "<p>1982年12月30日，中共连云港市委、市人民政府召开表彰吴伦东烈士大会，宣读江苏省人民政府关于授予为保卫民兵训练枪支、与盗窃罪犯搏斗中牺牲的市毛巾厂工人吴伦东“革命烈士”称号的决定。</p>",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5279-5281",
    ),
    (
        "吴伦东烈士句 OCR 残留（正文汇总）",
        "1982年12月30日，中共连云港市委、市人民政府召开追认吴伦东烈土大会，宣读江\n苏省人民政府关于授予为保卫民兵训练枪支、与盗窃罪犯搏斗中牺牲的市毛巾广工人吴\n伦东革命烈士”称号的决定。",
        "1982年12月30日，中共连云港市委、市人民政府召开表彰吴伦东烈士大会，宣读江\n苏省人民政府关于授予为保卫民兵训练枪支、与盗窃罪犯搏斗中牺牲的市毛巾厂工人吴\n伦东“革命烈士”称号的决定。",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5279-5281",
    ),
]

CHECK_RESIDUALS = [
    "准海工学院",
    "1985年建海大学",
    "吴伦东烈土大会",
    "市毛巾广工人吴伦东",
]


def append_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [needle for needle in CHECK_RESIDUALS if needle in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["changed"] for item in targets)
    payload = {
        "time": now,
        "scope": "第二十二批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复已由页级 OCR 或同章正文互证的校名、人名烈士称号残留。",
        "deferred": ["60方平方米/20方人", "进人省级先进水平", "红领币禁赌宣传队"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十二批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修已由页级 OCR 或同章正文互证的校名、人名烈士称号残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：`60方平方米/20方人`、`进人省级先进水平`、`红领币禁赌宣传队`，尚未完成可靠回源。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for label, _old, _new, source in REPLACEMENTS:
        count = sum(item["count"] for target in targets for item in target["items"] if item["label"] == label)
        lines.append(f"- {label}：依据 `{source}`；命中 {count} 处。")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-04 第二十二批正文残留回源修复"
    memory = f"""
{marker}
- 修复 `准海工学院` -> `淮海工学院`、`1985年建海大学` -> `1985年建淮海大学`、吴伦东烈士句中的 `烈土/毛巾广/引号` 残留。
- 依据：`workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5279-5281`、`:5468-5470`，`workbench/ocr/paddle_ocr/下/part01/page_0348.txt:18-20`，以及教育章正文互证 `workbench/body_chapters/连云港市志_全书_正文汇总.md:171740-171741`。
- 暂缓未充分回源项：`60方平方米/20方人`、`进人省级先进水平`、`红领币禁赌宣传队`。
- 报告：`output/reports/reader_readability_source_backed_batch22_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
