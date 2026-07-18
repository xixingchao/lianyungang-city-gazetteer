# -*- coding: utf-8 -*-
"""Narrow textile 毛巾 residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "textile_maojin_batch321_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "textile_maojin_batch321_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_纺织毛巾残留补修第三百二十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
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
    ("市毛币厂设计的22个毛巾花型图案", "市毛巾厂设计的22个毛巾花型图案", "PaddleOCR 下/part01/page_0447 为“市毛巾厂设计的22个毛巾花型图案”。"),
    ("市毛币厂“割绒刀具保护装置研究”", "市毛巾厂“割绒刀具保护装置研究”", "PaddleOCR 下/part01/page_0447 为“市毛巾厂‘割绒刀具保护装置研究’”。"),
    ("主要产品有毛币、床单", "主要产品有毛巾、床单", "PaddleOCR 上/part03/page_0243 为“主要产品有毛巾、床单”。"),
    ("有人力毛币织机44台，年产面币30.4万条", "有人力毛巾织机44台，年产面巾30.4万条", "PaddleOCR 上/part03/page_0248 为“有人力毛巾织机44台，年产面巾30.4万条”。"),
    ("粘棉交织提\n花毛币", "粘棉交织提\n花毛巾", "PaddleOCR 上/part03/page_0254 为“粘棉交织提花毛巾”。"),
    ("市第五毛币厂等5家", "市第五毛巾厂等5家", "PaddleOCR 上/part03/page_0249 为“市第五毛巾厂等5家”。"),
    ("毛市织机329台", "毛巾织机329台", "PaddleOCR 上/part03/page_0249 为“毛巾织机329台”。"),
    ("市毛巾币厂逐渐恢复床单生产", "市毛巾厂逐渐恢复床单生产", "PaddleOCR 上/part03/page_0250 为“市毛巾厂逐渐恢复床单生产”。"),
    ("关于毛币、床单专", "关于毛巾、床单专", "PaddleOCR 上/part03/page_0250 为“关于毛巾、床单专业性生产”。"),
    ("设备主要有毛币织", "设备主要有毛巾织", "PaddleOCR 上/part03/page_0254 为“设备主要有毛巾织机”。"),
    ("枕币能力为490万条", "枕巾能力为490万条", "PaddleOCR 上/part03/page_0254 为“枕巾能力为490万条”。"),
    ("连云港市毛市五厂", "连云港市毛巾五厂", "PaddleOCR 上/part03/page_0249 为“连云港市毛巾五厂”。"),
    ("市毛市厂\n先后与南京、徐州、盐城等市及县毛市厂", "市毛巾厂\n先后与南京、徐州、盐城等市及县毛巾厂", "PaddleOCR 上/part03/page_0249 为“市、县毛巾厂建立毛巾半成品生产协作关系”。"),
    ("市床单厂从市毛市厂内分出", "市床单厂从市毛巾厂内分出", "PaddleOCR 上/part03/page_0254 为“市床单厂从市毛巾厂内分出”。"),
    ("连云港市毛市厂\n“环球”牌割绒印花枕巾", "连云港市毛巾厂\n“环球”牌割绒印花枕巾", "PaddleOCR 上/part03/page_0273 为“连云港市毛巾厂 ‘环球’牌割绒印花枕巾”。"),
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
    for old, _new, _reason in REPLACEMENTS:
        residuals[old] = 0
        for path in TARGETS:
            if path.exists():
                residuals[old] += path.read_text(encoding="utf-8", errors="ignore").count(old)
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 纺织毛巾残留补修 batch321",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/中册/下册 HTML、正式正文汇总及相关分册正文源稿。",
        "- 依据：PaddleOCR 下/part01/page_0447，上/part03/page_0243、0248、0249、0250、0254、0273。",
        "- 原则：只处理完整短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：未能形成完整短语证据的其它 `毛币/毛市` 残留留待后续逐页核对。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        old = item["old"].replace("\n", "\\n")
        new = item["new"].replace("\n", "\\n")
        lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['reason']}")
    lines.extend(["", "## 残留计数", ""])
    bad = {key.replace("\n", "\\n"): value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-07 纺织毛巾残留补修第三百二十一批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据上下册 PaddleOCR 文本，窄语境补修纺织章与下册科技页 `毛巾` 误识别残留：`市毛币厂 -> 市毛巾厂`、`毛币/面币/枕币 -> 毛巾/面巾/枕巾`、`毛市厂/毛市五厂 -> 毛巾厂/毛巾五厂` 等，共 {total} 处。
- 报告：`output/reports/textile_maojin_batch321_20260707.md`；进度：`output/reports/progress/20260707_纺织毛巾残留补修第三百二十一批.md`。
- 未能形成完整短语证据的其它 `毛币/毛市` 残留留待后续逐页核对；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals}
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
