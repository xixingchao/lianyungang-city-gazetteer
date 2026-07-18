# -*- coding: utf-8 -*-
"""Third source-verified readability repair batch for Volume 20."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_chemical_batch3_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_chemical_batch3_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十卷化学工业高置信错识第三批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十卷-化学工业">第二十卷化学工业</h2>'
SCOPE_END = '<h2 id="第二十一卷-机械工业">第二十一卷机械工业</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0170.txt:30-31; page_0174.txt:27-28; page_0176.txt:1-4; page_0181.txt:20-23; page_0187.txt:66-68; page_0188.txt:15-16,25"
REPLACEMENTS = [
    ("GB434", "GB434－82", "GB434-82"),
    ("压缩机型号1", "L3.3一15/320", "L3.3-15/320"),
    ("压缩机型号2", "L3.3-17/320压缩机5台", "L3.3-17/320 压缩机 5 台"),
    ("铜液泵型号", "3WTI-15/130铜液泵", "3WTI - 15/130 铜液泵"),
    ("二氯异氰尿酸钠1", "二氯异氟尿酸钠生产装置", "二氯异氰尿酸钠生产装置"),
    ("异氰尿酸钠改产", "1990年10月该改产异氰尿酸钠", "1990年10月该厂改产异氰尿酸钠"),
    ("二氯异氰尿酸钠2", "二氯异氟尿酸钠10吨", "二氯异氰尿酸钠10吨"),
    ("a淀粉酶1", "a一淀粉酶", "a-淀粉酶"),
    ("丙烯酸树脂", "内烯酸树脂", "丙烯酸树脂"),
    ("乳胶皱纹手套", "乳胶绝纹工作手套", "乳胶皱纹工作手套"),
    ("出口创汇引号", "授予出口创汇先进企业\"称号", "授予“出口创汇先进企业”称号"),
    ("鳞片石墨", "生产磷片石墨200吨", "生产鳞片石墨200吨"),
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    original = text[start:end]
    segment = original
    counts: dict[str, int] = {}
    for label, old, new in REPLACEMENTS:
        count = segment.count(old)
        if count:
            segment = segment.replace(old, new)
        elif new not in segment:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    if segment != original:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [new for _label, _old, new in REPLACEMENTS if new not in segment]
    residuals = [old for _label, old, new in REPLACEMENTS if old in segment and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_changes = sum(counts.values())
    verified_items = len(REPLACEMENTS)
    payload = {
        "time": now,
        "scope": "第二十卷化学工业第三批",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": verified_items,
        "current_run_replacements": current_changes,
        "counts": counts,
        "principle": "继续只修第二十卷内页级 OCR 直接证明的残留错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第二十卷化学工业高置信错识第三批回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{verified_items} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 重点：修正 GB434、设备型号连接符、二氯异氰尿酸钠、a-淀粉酶、丙烯酸树脂、乳胶皱纹手套、鳞片石墨等残留错识。",
        "- 保留：设备长串和表格串行中仍无法用 OCR 稳定断句的内容未改。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第二十卷化学工业高置信错识第三批回源修复

- 继续对第二十卷化学工业残留错识进行小批回源修复。
- 源文依据：`{SOURCE}`。
- 修复示例：`GB434－82`→`GB434-82`，`二氯异氟尿酸钠`→`二氯异氰尿酸钠`，`a一淀粉酶`→`a-淀粉酶`，`内烯酸树脂`→`丙烯酸树脂`，`乳胶绝纹工作手套`→`乳胶皱纹工作手套`，`磷片石墨`→`鳞片石墨`。
- 本批核验修复 {verified_items} 项；报告：`output/reports/reader_readability_chemical_batch3_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第二十卷化学工业高置信错识第三批回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
