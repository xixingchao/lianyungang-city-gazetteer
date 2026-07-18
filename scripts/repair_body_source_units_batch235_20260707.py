# -*- coding: utf-8 -*-
"""Repair source-backed port and water unit residues, batch 235."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "body_source_port_water_units_batch235_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "body_source_port_water_units_batch235_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_港口供水单位残留补修第二百三十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
ITEMS = [
    ("港口货物吞吐量11方吨", "港口货物吞吐量11万吨", "上/part01/page_0073.txt", "港口货物吞吐量11万吨"),
    ("港口吞吐量256方吨", "港口吞吐量256万吨", "上/part01/page_0087.txt", "港口吞吐量256万吨，其中外贸10万吨"),
    ("年通过能力390方吨设计", "年通过能力390万吨设计", "上/part01/page_0090.txt", "新建煤炭码头按年通过能力390万吨设计"),
    ("港口货物吞吐量335方吨，其中外贸59方吨", "港口货物吞吐量335万吨，其中外贸59万吨", "上/part01/page_0094.txt", "港口货物吞吐量335万吨，其中外贸59万吨"),
    ("港口货物吞吐量242万吨，其中外贸65方吨", "港口货物吞吐量242万吨，其中外贸65万吨", "上/part01/page_0096.txt", "港口货物吞吐量242万吨，其中外贸65万吨"),
    ("港口货物吞吐量303方吨", "港口货物吞吐量303万吨", "上/part01/page_0098.txt", "港口货物吞吐量303万吨，其中外贸64万吨"),
    ("港口货物吞吐量594方吨", "港口货物吞吐量594万吨", "上/part01/page_0100.txt", "港口货物吞吐量594万吨，其中外贸199万吨"),
    ("港口货物吞吐量858方吨", "港口货物吞吐量858万吨", "上/part01/page_0109.txt", "港口货物吞吐量858万吨，其中外贸出口399万吨"),
    ("蓄水量762方吨", "蓄水量762万吨", "上/part02/page_0060.txt", "蓄水量762万吨"),
    ("容量20方吨蓄水坝", "容量20万吨蓄水坝", "上/part02/page_0061.txt", "容量20万吨蓄水坝"),
    ("蓄水量35方吨", "蓄水量35万吨", "上/part02/page_0061.txt", "蓄水量35万吨"),
    ("生活用水60方吨", "生活用水60万吨", "上/part02/page_0062.txt", "生活用水60万吨"),
    ("新建1方吨滤池1座", "新建1万吨滤池1座", "上/part02/page_0062.txt", "新建1万吨滤池1座"),
    ("设计能力10方吨/日", "设计能力10万吨/日", "上/part02/page_0062.txt", "设计能力10万吨/日"),
]


def evidence_path(rel: str) -> Path:
    volume, part, page = rel.split("/")
    return ROOT / "workbench" / "ocr" / "paddle_ocr" / volume / part / page


def ensure_evidence() -> None:
    for _, _, rel, snippet in ITEMS:
        path = evidence_path(rel)
        text = path.read_text(encoding="utf-8", errors="ignore")
        if snippet not in text:
            raise SystemExit(f"missing evidence: {path.relative_to(ROOT)}: {snippet}")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        file_items = []
        for old, new, rel, _ in ITEMS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_items.append({"old": old, "new": new, "count": count, "evidence": str(evidence_path(rel).relative_to(ROOT))})
        if file_items:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "items": file_items})

    residuals = {
        old: {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(old) for path in TARGETS}
        for old, _, _, _ in ITEMS
    }
    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 港口供水单位残留补修第二百三十五批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复上册大事记港口吞吐量、煤码头设计能力和城乡建设供水段中已由页级 PaddleOCR 证实的单位残留。",
        "- 同步正常命名正文源稿和全书正文汇总；未处理旧交付包、obsolete 或乱码副本。",
        "- 未做全局替换，未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["items"]:
            lines.append(f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['evidence']}` |")
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 港口供水单位残留补修第二百三十五批\n\n"
    memory += "- 依据上册 `part01/page_0073、0087、0090、0094、0096、0098、0100、0109` 和 `part02/page_0060、0061、0062` 页级 PaddleOCR，修复港口吞吐量、煤码头设计能力和供水段 `方吨 -> 万吨` 残留。\n"
    memory += "- 同步范围：上册正常命名正文源稿及全书正文汇总；报告：`output/reports/body_source_port_water_units_batch235_20260707.md`。\n"
    memory += "- 未处理旧交付包、obsolete 或乱码副本；未做全局替换，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
