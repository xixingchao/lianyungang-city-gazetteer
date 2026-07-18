# -*- coding: utf-8 -*-
"""Repair final source-checked 投人 -> 投入 slips, leaving one complex tourism residue."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_touru_batch4_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_touru_batch4_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_投人投入第四批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part02/page_0095.txt:17,19; page_0296.txt:26; "
    "workbench/ocr/paddle_ocr/下/part01/page_0443.txt:17; page_0444.txt:24,40; "
    "page_0447.txt:13; page_0457.txt:10"
)

REPLACEMENTS = [
    ("金融贷款投入", "投人贷款8400万元", "投入贷款8400万元", "金融章贷款源段"),
    ("民主人士运动", "领导他们投人土地改革", "领导他们投入土地改革", "政党章源段"),
    ("农业投入视察", "农业的投人情况视察", "农业的投入情况视察", "政务章源段"),
    ("增产节约标题", "投人增产节约运动", "投入增产节约运动", "政务章源段"),
    ("增收节支运动", "投人“增产节约、增收节支”运动", "投入“增产节约、增收节支”运动", "政务章源段"),
    ("科技化工生产", "开发获得成功，并投人生产", "开发获得成功，并投入生产", "下/part01/page_0443.txt:17"),
    ("科技水泵生产", "混流泵，均投人生产", "混流泵，均投入生产", "下/part01/page_0444.txt:24"),
    ("科技挂车批产", "挂车，鉴定后投人批量生产", "挂车，鉴定后投入批量生产", "下/part01/page_0444.txt:40"),
    ("科技造纸批产", "经鉴定后投人批量生产", "经鉴定后投入批量生产", "下/part01/page_0447.txt:13"),
    ("茅口水厂使用", "一期工程竣工投人使用", "一期工程竣工投入使用", "科技建设源段"),
]

SKIPPED = [
    "第三十二卷名胜旅游 `臭敬梓、投人，开发旅游资源` 源页为 `吴敬梓、` + `投入，开发旅游资源...`，需要段落级回源重排，本批不单点修。"
]


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    for label, old, new, _source in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        elif new not in text:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    HTML.write_text(text, encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    missing = [new for _label, _old, new, _source in REPLACEMENTS if new not in text]
    residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in text]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


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


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    items = [
        {"label": label, "old": old, "new": new, "source": source, "count": counts[label]}
        for label, old, new, source in REPLACEMENTS
    ]
    payload = {
        "time": now,
        "scope": "金融、政党、政务、科技 `投人` 残留第四批",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复可由源页或同段源文支撑为 `投入` 的长短语；复杂串行残文保留待段落级处理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 投人/投入第四批回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验条目：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 保留：第三十二卷名胜旅游复杂串行残文，待段落级回源。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 投人/投入第四批回源修复

- 对金融、政党、政务、科技中的 `投人` 残留做第四批回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `投人贷款/投人土地改革/农业的投人情况/投人增产节约运动/投人生产/投人批量生产/投人使用` 等 10 处为 `投入`。
- 保留第三十二卷名胜旅游 `臭敬梓、投人，开发旅游资源`：源页显示应涉及 `吴敬梓、` 与下一行 `投入，开发旅游资源...`，需段落级回源重排。
- 报告：`output/reports/reader_readability_touru_batch4_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 投人/投入第四批回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
