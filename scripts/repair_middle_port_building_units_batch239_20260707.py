# -*- coding: utf-8 -*-
"""Repair middle-volume port/building/geology unit residues, batch 239."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "middle_port_building_units_batch239_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_port_building_units_batch239_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册港口建材单位残留补修第二百三十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
ITEMS = [
    ("年产1方吨石灰膏", "年产1万吨石灰膏", "中/part01/page_0279.txt", "年产1万吨石灰膏"),
    ("年总产量达11.43方吨", "年总产量达11.43万吨", "中/part01/page_0279.txt", "年总产量达11.43万吨"),
    ("形成5方吨年", "形成5万吨年", "中/part01/page_0280.txt", "形成5万吨年"),
    ("锦屏磷矿1.5方吨磷酸厂", "锦屏磷矿1.5万吨磷酸厂", "中/part01/page_0299.txt", "锦屏磷矿1.5万吨磷酸厂"),
    ("1.5方吨发酵间", "1.5万吨发酵间", "中/part01/page_0320.txt", "1.5万吨发酵间"),
    ("3方吨包装间", "3万吨包装间", "中/part01/page_0320.txt", "3万吨包装间"),
    ("水晶总储量25.54方吨", "水晶总储量25.54万吨", "中/part01/page_0391.txt", "水晶总储量25.54万吨"),
    ("可采资源总量约2.55方吨", "可采资源总量约2.55万吨", "中/part01/page_0391.txt", "可采资源总量约2.55万吨"),
    ("年开采量30方吨", "年开采量30万吨", "中/part01/page_0393.txt", "年开采量30万吨"),
    ("4个方吨级以上深水杂", "4个万吨级以上深水杂", "中/part01/page_0438.txt", "2.5万吨级船舶"),
    ("2.5方吨级船舶", "2.5万吨级船舶", "中/part01/page_0438.txt", "2.5万吨级船舶"),
    ("堆存10方吨煤炭", "堆存10万吨煤炭", "中/part01/page_0444.txt", "堆存10万吨煤炭"),
    ("年上半年14.7方吨", "年上半年14.7万吨", "中/part01/page_0451.txt", "年上半年14.7万吨"),
    ("达118方吨", "达118万吨", "中/part01/page_0451.txt", "达118万吨"),
    ("22.17方吨", "22.17万吨", "中/part01/page_0451.txt", "22.17万吨"),
    ("磷矿石33方吨", "磷矿石33万吨", "中/part01/page_0457.txt", "磷矿石33万吨"),
    ("载重1.08方吨", "载重1.08万吨", "中/part01/page_0457.txt", "载重1.08万吨"),
    ("准北海盐5.62方吨", "淮北海盐5.62万吨", "中/part01/page_0459.txt", "淮北海盐5.62万吨"),
    ("122.66方吨", "122.66万吨", "中/part01/page_0471.txt", "122.66万吨"),
]


def evidence_path(rel: str) -> Path:
    volume, part, page = rel.split("/")
    return ROOT / "workbench" / "ocr" / "paddle_ocr" / volume / part / page


def ensure_evidence() -> None:
    missing = []
    for _, _, rel, snippet in ITEMS:
        path = evidence_path(rel)
        text = path.read_text(encoding="utf-8", errors="ignore")
        if snippet not in text:
            missing.append(f"{path.relative_to(ROOT)}: {snippet}")
    if missing:
        raise SystemExit("missing evidence:\n" + "\n".join(missing))


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
        "# 中册港口建材单位残留补修第二百三十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复中册建材、地勘、港口煤盐矿石吞吐等段落中已由页级 PaddleOCR 证实的单位残留。",
        "- 同步中册正文源稿和全书正文汇总；未处理旧交付包、obsolete 或乱码副本。",
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
    memory += "\n\n## 2026-07-07 中册港口建材单位残留补修第二百三十九批\n\n"
    memory += "- 依据中册页级 PaddleOCR，修复建材、地勘、港口煤盐矿石吞吐段 `方吨/方吨级 -> 万吨/万吨级` 残留，并同步 `准北海盐 -> 淮北海盐`。\n"
    memory += "- 同步范围：`第十七卷至第二十九卷（中part01）.md` 与全书正文汇总；报告：`output/reports/middle_port_building_units_batch239_20260707.md`。\n"
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
