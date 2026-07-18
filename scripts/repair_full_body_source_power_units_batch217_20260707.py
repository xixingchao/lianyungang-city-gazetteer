# -*- coding: utf-8 -*-
"""Repair source summary power-unit residues already correct in formal reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_body_source_power_units_batch217_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "full_body_source_power_units_batch217_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_全书正文汇总单位残留补修第二百一十七批.md"

REPLACEMENTS = [
    ("的风能0.21于瓦", "的风能0.21千瓦"),
    ("15于瓦船带舶販1~2只", "15千瓦船带舶販1~2只"),
    ("1972年增造279于瓦灯光船", "1972年增造279千瓦灯光船"),
]

EVIDENCE = [
    (ROOT / "output" / "final_reader" / "连云港市志_全书.html", "每平方米的风能0.21千瓦"),
    (ROOT / "output" / "final_reader" / "连云港市志_全书.html", "15千瓦船带舢舰1～2只"),
    (ROOT / "output" / "final_reader" / "连云港市志_全书.html", "1972年增造279千瓦灯光船"),
    (ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md", "279千瓦灯光船"),
    (ROOT / "workbench" / "body_chapters" / "连云港市志_上册_PaddleOCR正文汇总.md", "279千瓦灯光船"),
]


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for path, needle in EVIDENCE:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if needle not in text:
            raise SystemExit(f"missing evidence {needle} in {path}")

    text = TARGET.read_text(encoding="utf-8")
    changes = []
    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        changes.append({"old": old, "new": new, "count": count})
    TARGET.write_text(text, encoding="utf-8")

    residuals = {old: text.count(old) for old, _ in REPLACEMENTS}
    payload = {"time": now, "target": str(TARGET.relative_to(ROOT)), "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 全书正文汇总单位残留补修第二百一十七批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 仅修复 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 中 3 条源稿级 `于瓦` 单位残留。",
        "- 当前正式 `output/final_reader/连云港市志_全书.html` 已为正确文本，本批不改正式阅读稿。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 原文 | 新文 | 次数 |",
        "|---|---|---:|",
    ]
    for item in changes:
        if item["count"]:
            lines.append(f"| `{item['old']}` | `{item['new']}` | {item['count']} |")
    lines.extend([
        "",
        "## 证据",
        "",
        "- `output/final_reader/连云港市志_全书.html`：`每平方米的风能0.21千瓦`、`15千瓦船带舢舰1～2只`、`1972年增造279千瓦灯光船`。",
        "- `workbench/body_chapters/连云港市志_上册_正文汇总.md` 与 `workbench/body_chapters/连云港市志_上册_PaddleOCR正文汇总.md`：水产段 `279千瓦灯光船` 已为正确单位。",
        "",
        "## 残留",
        "",
        f"- 本批 3 条旧短语残留：{sum(residuals.values())}。",
        f"- `全书_正文汇总.md` 当前 `于瓦` 总数：{text.count('于瓦')}。",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({"changed": sum(i["count"] for i in changes), "remaining_yuwa": text.count("于瓦"), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
