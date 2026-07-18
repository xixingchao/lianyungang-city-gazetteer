# -*- coding: utf-8 -*-
"""Source-backed fixes for port health quarantine OCR slips."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_port_health_quarantine_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_port_health_quarantine_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第二十九卷卫生检疫错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/中/part01/page_0506.txt; workbench/ocr/raw/中/part01/page_0506.txt"
SCOPE_START = '<h4 id="第二十九卷-第四章管理-第四节卫生检疫">第四节卫生检疫</h4>'
SCOPE_END = '<h4 id="第二十九卷-第四章管理-第五节边防检查">第五节边防检查</h4>'
REPLACEMENTS = [
    ("传染病监测病名", "流感、症疾、脊髓灰质炎", "流感、疟疾、脊髓灰质炎"),
    ("传入传出", "直接从国外传人或由国内传出", "直接从国外传入或由国内传出"),
    ("副霍乱患者", "被确诊为副霍乱轻型惠者", "被确诊为副霍乱轻型患者"),
    ("天花接种", "办理花预防接种工作", "办理天花预防接种工作"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    start = html.index(SCOPE_START)
    end = html.index(SCOPE_END, start)
    segment = html[start:end]
    counts: dict[str, int] = {}
    for label, old, new in REPLACEMENTS:
        count = segment.count(old)
        if count != 1:
            raise RuntimeError(f"expected one occurrence for {label}, got {count}: {old}")
        segment = segment.replace(old, new)
        counts[label] = count
    HTML.write_text(html[:start] + segment + html[end:], encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第二十九卷口岸 / 第七章口岸服务 / 第四节卫生检疫",
        "source": SOURCE_NOTE,
        "counts": counts,
        "principle": "仅修复 page_0506 PaddleOCR 明确支持的字词，不处理证据不足的医学术语。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第二十九卷卫生检疫错识回源修复

- 时间：{now}
- 范围：第二十九卷口岸 / 第七章口岸服务 / 第四节卫生检疫。
- 源文依据：`{SOURCE_NOTE}`。

## 修复

- `流感、症疾、脊髓灰质炎` -> `流感、疟疾、脊髓灰质炎`。
- `直接从国外传人或由国内传出` -> `直接从国外传入或由国内传出`。
- `副霍乱轻型惠者` -> `副霍乱轻型患者`。
- `办理花预防接种工作` -> `办理天花预防接种工作`。

## 原则

只采用 `page_0506` PaddleOCR 明确支持的字词；不扩展处理同页以外或证据不足的医学术语。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第二十九卷卫生检疫错识回源修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 依据 `{SOURCE_NOTE}` 修复第二十九卷卫生检疫 page_0506 可证错识：`症疾` -> `疟疾`、`传人` -> `传入`、`惠者` -> `患者`、`花预防接种` -> `天花预防接种`。
- 未处理证据不足的医学术语；不改表格数据。
- 报告：`output/reports/reader_port_health_quarantine_20260705.md`。
""",
    )

    print("port_health_quarantine_repaired")
    print(f"changes={sum(counts.values())}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
