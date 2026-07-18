# -*- coding: utf-8 -*-
"""Resync previously source-backed readability fixes that resurfaced in current deliverables."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_preverified_residue_resync_batch229_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_preverified_residue_resync_batch229_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_已回源正文残留同步回填第二百二十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("该场遂步增加茶树种植面积", "该场逐步增加茶树种植面积", "reader_readability_source_backed_batch9_20260704"),
    ("中药加工炮制生产由原来的手\n工操作遂步被机械设备所代替", "中药加工炮制生产由原来的手\n工操作逐步被机械设备所代替", "reader_readability_source_backed_batch9_20260704"),
    ("中药加工炮制生产由原来的手工操作遂步被机械设备所代替", "中药加工炮制生产由原来的手工操作逐步被机械设备所代替", "reader_readability_source_backed_batch9_20260704"),
    ("远期可遂步实行工业与民用分两片相对集中供热", "远期可逐步实行工业与民用分两片相对集中供热", "reader_readability_source_backed_batch9_20260704"),
    ("土地有偿使用开始遂步转向土地使用权有偿出让、转让和土地包片开发", "土地有偿使用开始逐步转向土地使用权有偿出让、转让和土地包片开发", "reader_readability_source_backed_batch9_20260704"),
    ("随着港口装卸机械的遂步增多", "随着港口装卸机械的逐步增多", "reader_readability_source_backed_batch9_20260704"),
    ("近现代遂步发展为汽车、火车、轮船运载", "近现代逐步发展为汽车、火车、轮船运载", "reader_readability_source_backed_batch9_20260704"),
    ("遂步完善、配套措施", "逐步完善、配套措施", "reader_readability_source_backed_batch9_20260704"),
    ("棉供应计划、市场安排和批发业务遂步转由供销合作社负责", "棉供应计划、市场安排和批发业务逐步转由供销合作社负责", "reader_readability_source_backed_batch10_20260704"),
    ("工厂和企业的自主权遂步扩大", "工厂和企业的自主权逐步扩大", "reader_readability_source_backed_batch10_20260704"),
    ("计划外超产物资充许自销", "计划外超产物资允许自销", "reader_readability_source_backed_batch10_20260704"),
    ("民政部门督促检查，遂步改“五保户”供给为村统筹、乡统筹", "民政部门督促检查，逐步改“五保户”供给为村统筹、乡统筹", "reader_readability_source_backed_batch10_20260704"),
    ("遂步实现街有街牌、路有路牌、巷有巷牌、门有门牌、村有村牌", "逐步实现街有街牌、路有路牌、巷有巷牌、门有门牌、村有村牌", "reader_readability_source_backed_batch10_20260704"),
    ("各医院遂步添置", "各医院逐步添置", "reader_readability_source_backed_batch10_20260704"),
    ("一日海上丝绸之路，二\n日西域通往内地的陆地丝绸之路逐遂步问东延伸所至", "一曰海上丝绸之路，二\n曰西域通往内地的陆地丝绸之路逐步向东延伸所至", "reader_readability_source_backed_batch12_20260704"),
    ("一日海上丝绸之路，二日西域通往内地的陆地丝绸之路逐遂步问东延伸所至", "一曰海上丝绸之路，二曰西域通往内地的陆地丝绸之路逐步向东延伸所至", "reader_readability_source_backed_batch12_20260704"),
]


def ensure_prior_reports() -> None:
    missing = []
    for _, _, report_stem in ITEMS:
        path = ROOT / "output" / "reports" / f"{report_stem}.json"
        if not path.exists():
            missing.append(str(path.relative_to(ROOT)))
    if missing:
        raise SystemExit("missing prior evidence reports: " + "; ".join(sorted(set(missing))))


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_prior_reports()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        file_items = []
        for old, new, report_stem in ITEMS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_items.append({"old": old, "new": new, "count": count, "prior_report": f"output/reports/{report_stem}.json"})
        if text != original:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "items": file_items})

    residuals = {
        old: {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(old) for path in TARGETS}
        for old, _, _ in ITEMS
    }
    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 已回源正文残留同步回填第二百二十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 只重放 20260704 已有回源报告确认过的正文可读性修复。",
        "- 修复当前阅读稿/源稿中被旧稿覆盖回来的 `遂步`、`充许` 等残留。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 既有证据报告 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["items"]:
            lines.append(f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['prior_report']}` |")
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 已回源正文残留同步回填第二百二十九批\n\n"
    memory += "- 依据 `output/reports/reader_readability_source_backed_batch9_20260704.json`、`batch10_20260704.json`、`batch12_20260704.json`，重放此前已回源确认的 `遂步/充许/逐遂步问东` 修复。\n"
    memory += "- 同步范围：当前中册/下册/全书阅读稿及相关正文源稿；报告：`output/reports/reader_preverified_residue_resync_batch229_20260707.md`。\n"
    memory += "- 本批不做新的全局替换；只处理既有证据报告明确确认项，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
