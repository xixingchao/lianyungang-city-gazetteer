# -*- coding: utf-8 -*-
"""Repair source-backed 划人/引人 readability residues in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_huaren_yinren_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_huaren_yinren_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_划人引人残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "old": "从1959年起将中央预算收入的盐税划人市级预算收入管理",
        "new": "从1959年起将中央预算收入的盐税划入市级预算收入管理",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0282.txt:20-22",
    },
    {
        "old": "1968年税务经费又划人行政支出",
        "new": "1968年税务经费又划入行政支出",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0297.txt:17-18",
    },
    {
        "old": "浦西区委（1949.10~1950.12划人东海县）",
        "new": "浦西区委（1949.10~1950.12划入东海县）",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0421.txt:31",
    },
    {
        "old": "1953年1月1日，新海连市划人江苏省，归徐州地区行政专员公署管辖",
        "new": "1953年1月1日，新海连市划入江苏省，归徐州地区行政专员公署管辖",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0075.txt:17-18; workbench/body_chapters/连云港市志_全书_正文汇总.md:89815-89817",
    },
    {
        "old": "云台公社及南城镇由灌云县划人连云港市云台区",
        "new": "云台公社及南城镇由灌云县划入连云港市云台区",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0285.txt:8-10; workbench/body_chapters/连云港市志_全书_正文汇总.md:90670-90672",
    },
    {
        "old": "陆续划人4家工厂为福利企业",
        "new": "陆续划入4家工厂为福利企业",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0040.txt:12-13",
    },
    {
        "old": "关于对“四类分子”规划人社的规定",
        "new": "关于对“四类分子”规划入社的规定",
        "source": "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:4189",
    },
    {
        "old": "1962年2月灌云县引人电网电源后",
        "new": "1962年2月灌云县引入电网电源后",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0341.txt:26-27",
    },
    {
        "old": "连云港地区电网通过新（沂)牛（山）线引人徐州电网电力",
        "new": "连云港地区电网通过新（沂)牛（山）线引进徐州电网电力",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0330.txt:24-25; workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:18671-18672",
    },
    {
        "old": "将西部和西南方向山洪引人排淡河",
        "new": "将西部和西南方向山洪引入排淡河",
        "source": "output/reports/conversion_source_risk_20260703.json:24945; workbench/ocr/raw/中/part01/page_0425.txt:4-5",
    },
    {
        "old": "把竞争机制引人干部管理",
        "new": "把竞争机制引入干部管理",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0438.txt:36-37",
    },
    {
        "old": "颇引人人胜",
        "new": "颇引人入胜",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0105.txt:22-23",
    },
]

SKIPPED = [
    {
        "text": "冬天引人盐田卤水",
        "reason": "方言词条 OCR 音标与释义混排，PaddleOCR/raw 同为 `引人`，本轮缺少可靠异源证据，暂不改。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0328.txt:19-20",
    }
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    applied = []
    for item in REPLACEMENTS:
        count = text.count(item["old"])
        if count != 1:
            raise RuntimeError(f"expected one occurrence for {item['old']!r}, found {count}")
        text = text.replace(item["old"], item["new"])
        applied.append({**item, "count": count})
    HTML.write_text(text, encoding="utf-8")

    verify = HTML.read_text(encoding="utf-8")
    leftovers = {item["old"]: verify.count(item["old"]) for item in REPLACEMENTS}
    if any(leftovers.values()):
        raise RuntimeError(f"replacement verification failed: {leftovers}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "最终阅读版 划人/引人 小批残留",
        "reader_path": str(HTML),
        "current_run_replacements": sum(item["count"] for item in applied),
        "applied": applied,
        "skipped": SKIPPED,
        "principle": "仅按长上下文和源证据修复，不做 `划人→划入`、`引人→引入` 全局替换。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 划人/引人残留回源修复",
        "",
        f"- 时间：{now}",
        "- 范围：最终阅读版 `划人/引人` 小批残留。",
        f"- 阅读器：`{HTML}`",
        f"- 本轮替换：{payload['current_run_replacements']} 处。",
        "- 原则：只做长上下文替换，不做全局字形替换。",
        "",
        "## 修复清单",
    ]
    for item in applied:
        lines.append(f"- `{item['old']}` → `{item['new']}`；源：`{item['source']}`")
    lines.extend(["", "## 暂缓", f"- `{SKIPPED[0]['text']}`：{SKIPPED[0]['reason']} 源：`{SKIPPED[0]['source']}`", ""])
    md = "\n".join(lines)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    memory = f"""
## 2026-07-04 划人/引人残留回源修复

- 对最终阅读版 `划人/引人` 小批残留做 12 处源证据修复。
- 修复范围包括财政预算、税务经费、区委沿革、行政区划、社会福利企业、电网、开发区排水、干部管理和石棚山石刻。
- 源文依据见：`output/reports/reader_readability_huaren_yinren_residual_20260704.md`。
- 未处理 `冬天引人盐田卤水`：方言词条音标/释义混排，PaddleOCR/raw 同形，缺少可靠异源证据，后续需定点复核。
- 本轮后预期 `划人` 清零，`引人` 仅保留方言疑难项。
"""
    upsert_memory(MEMORY, "## 2026-07-04 划人/引人残留回源修复", memory)
    print(json.dumps({"current_run_replacements": payload["current_run_replacements"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
