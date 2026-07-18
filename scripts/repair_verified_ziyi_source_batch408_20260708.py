# -*- coding: utf-8 -*-
"""Repair source 自已 residues for batch 408, preserving 不能自已."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "上" / "序与凡例.md",
    ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷_人口（part01_部分）.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]

READERS = [
    ROOT / "output" / "final_reader" / "连云港市志_上册.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
]

REPORT = ROOT / "output" / "reports" / "verified_ziyi_source_batch408_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_ziyi_source_batch408_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_自已残留源稿补修第四百零八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 自已残留源稿补修第四百零八批"
PRESERVE = "不能自已"
TOKEN = "__PRESERVE_BU_NENG_ZI_YI_BATCH408__"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def contexts(text: str, needle: str) -> list[str]:
    out: list[str] = []
    start = 0
    while True:
        idx = text.find(needle, start)
        if idx < 0:
            break
        out.append(text[max(0, idx - 45):idx + len(needle) + 55].replace("\n", "\\n"))
        start = idx + 1
    return out


def repair(path: Path) -> dict[str, object]:
    before = read(path)
    preserved = before.count(PRESERVE)
    work = before.replace(PRESERVE, TOKEN)
    changed = work.count("自已")
    work = work.replace("自已", "自己").replace(TOKEN, PRESERVE)
    if changed:
        path.write_text(work, encoding="utf-8")
    after = read(path)
    remaining = [ctx for ctx in contexts(after, "自已") if PRESERVE not in ctx]
    return {
        "path": rel(path),
        "changed": changed,
        "preserved_bunengziyi": preserved,
        "remaining_unprotected": len(remaining),
        "remaining_contexts": remaining,
    }


def scan(path: Path) -> dict[str, object]:
    text = read(path)
    remaining = [ctx for ctx in contexts(text, "自已") if PRESERVE not in ctx]
    return {"path": rel(path), "self_hits": text.count("自己"), "preserved_bunengziyi": text.count(PRESERVE), "remaining_unprotected": len(remaining), "remaining_contexts": remaining}


def write_report(results: list[dict[str, object]], reader_scan: list[dict[str, object]]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(int(item["changed"]) for item in results)
    lines = [
        "# 自已残留源稿补修 batch408",
        "",
        f"- 生成时间：{now}",
        "- 范围：现行正文源稿与上册/全书正文汇总；当前 reader 只复扫。",
        "- 修复：`自已 -> 自己`，保护固定书面语/古文 `不能自已`。",
        "- 跳过：OCR 源文件、`paddle_上`、`PaddleOCR正文汇总`、backup、obsolete、历史交付包。",
        "- 图片处理：未打开、展示或嵌入图片。",
        f"- 本批修复：{total} 处。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(f"- `{item['path']}`：修复 {item['changed']} 处，保留 `不能自已` {item['preserved_bunengziyi']} 处，未保护残留 {item['remaining_unprotected']} 处。")
    lines.extend(["", "## Reader 复扫"])
    for item in reader_scan:
        lines.append(f"- `{item['path']}`：保留 `不能自已` {item['preserved_bunengziyi']} 处，未保护 `自已` 残留 {item['remaining_unprotected']} 处。")
    lines.extend(["", "## 残留上下文"])
    leftovers = []
    for item in [*results, *reader_scan]:
        for ctx in item["remaining_contexts"]:
            leftovers.append(f"- `{item['path']}`：{ctx}")
    lines.extend(leftovers or ["- 无未保护残留。"])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps({"time": now, "changed": total, "results": results, "reader_scan": reader_scan}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory(total: int) -> None:
    block = f"""{MARKER}

- 对现行正文源稿和上册/全书正文汇总补修 `自已 -> 自己`，保护固定书面语/古文 `不能自已`；本批修复 {total} 处。
- 范围不含 OCR 源文件、`paddle_上`、`PaddleOCR正文汇总`、backup、obsolete、历史交付包；当前 reader 只复扫，未打开、展示或嵌入图片。
- 报告：`output/reports/verified_ziyi_source_batch408_20260708.md`；进度：`output/reports/progress/20260708_自已残留源稿补修第四百零八批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    if next_start < 0:
        MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    else:
        MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + old[next_start:], encoding="utf-8")


def main() -> None:
    results = [repair(path) for path in TARGETS if path.exists()]
    reader_scan = [scan(path) for path in READERS if path.exists()]
    write_report(results, reader_scan)
    total = sum(int(item["changed"]) for item in results)
    update_memory(total)
    print(json.dumps({"changed": total, "report": str(REPORT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
