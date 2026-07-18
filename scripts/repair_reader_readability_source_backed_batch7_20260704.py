# -*- coding: utf-8 -*-
"""Repair an eighth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch7_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch7_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第八批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
FIRST_RUN_REPLACEMENTS = 28
FIRST_RUN_TARGETS = {
    str(ROOT / "output" / "final_reader" / "连云港市志_全书.html"): 14,
    str(ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"): 14,
}

REPLACEMENTS = [
    ("糖果产量单位", "产糖果849饨", "产糖果849吨", "workbench/ocr/paddle_ocr/中/part01/page_0066.txt:4"),
    ("糖果段标点", "81.27%产品以果香型硬糖为", "81.27%；产品以果香型硬糖为", "workbench/ocr/paddle_ocr/中/part01/page_0066.txt:4"),
    ("果酒稳步发展", "生产进人稳步发展时期", "生产进入稳步发展时期", "workbench/ocr/paddle_ocr/中/part01/page_0085.txt:30"),
    ("果酒稳步发展断行", "生产进人稳步发展时\n期", "生产进入稳步发展时\n期", "workbench/ocr/paddle_ocr/中/part01/page_0085.txt:30"),
    ("果酒宝石红", "酒液皇宝石红", "酒液呈宝石红", "workbench/ocr/paddle_ocr/中/part01/page_0085.txt:34"),
    ("白羽半干白葡萄酒", "白羽半于白葡萄酒", "白羽半干白葡萄酒", "workbench/ocr/paddle_ocr/中/part01/page_0085.txt:36; page_0086.txt:6,30; page_0094.txt:5"),
    ("果酒骨干企业", "轻工业重点骨于企业", "轻工业重点骨干企业", "workbench/ocr/paddle_ocr/中/part01/page_0094.txt:28"),
    ("石英晶体滤波器进入80年代", "研制任务。进人80年代，企业先后", "研制任务。进入80年代，企业先后", "workbench/ocr/paddle_ocr/中/part01/page_0245.txt:37"),
    ("耳塞机进入80年代", "产量逐年增长。进人80年代，则", "产量逐年增长。进入80年代，则", "workbench/ocr/paddle_ocr/中/part01/page_0250.txt:6"),
    ("广播箱输入阻抗", "变压器输人阻抗57K", "变压器输入阻抗57K", "workbench/ocr/paddle_ocr/中/part01/page_0250.txt:12"),
    ("建筑施工进入市区", "进人市区施工的外地施工队伍", "进入市区施工的外地施工队伍", "workbench/ocr/paddle_ocr/中/part01/page_0324.txt:25"),
    ("供电交换机进入省系统", "交换机进人省系统网", "交换机进入省系统网", "workbench/ocr/paddle_ocr/中/part01/page_0356.txt:26"),
    ("港口输入交流电", "海州发电厂输人交流电", "海州发电厂输入交流电", "workbench/ocr/paddle_ocr/中/part01/page_0447.txt:35"),
    ("仓储车皮进入专用线", "车皮进人仓库专用线", "车皮进入仓库专用线", "workbench/ocr/paddle_ocr/中/part01/page_0466.txt:37"),
    ("进口食品进入国内", "食品进人国内。至1989年", "食品进入国内。至1989年", "workbench/ocr/paddle_ocr/中/part01/page_0509.txt:14"),
]

SKIPPED = [
    "`方吨啤酒灌装线`：同章仅见产能和其它灌装线证据，未取得同句设备清单异源证据，本批暂缓。",
    "`时有长落`：PaddleOCR/raw 均同形，疑似 `涨落` 但缺少强证据，本批暂缓。",
    "其它 `进人/输人/加人/方吨`：继续按页回源，不做全局替换。",
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
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["changed"] for item in targets)
    payload = {
        "time": now,
        "scope": "第八批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "first_run_replacements": FIRST_RUN_REPLACEMENTS,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复 PaddleOCR 或同页异源文本明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第八批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修 PaddleOCR 或同页异源文本明确支撑的长上下文问题。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 首次执行替换：{FIRST_RUN_REPLACEMENTS} 处；本次复跑新增：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        first_run = FIRST_RUN_TARGETS.get(target["target"], target["changed"])
        lines.append(f"- `{target['target']}`：首次执行 {first_run} 处；本次复跑新增 {target['changed']} 处")
    lines.extend(["", "## 修复项"])
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    lines.extend(["", "## 暂缓"])
    for item in SKIPPED:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-04 第八批正文残留回源修复

- 对最终阅读版和正文汇总补做 15 项回源修复，首次执行替换 {FIRST_RUN_REPLACEMENTS} 处；本次复跑新增 {total} 处。
- 修复范围包括食品糖果、果酒、电子元器件、建筑取费、电力通信、港口供电、口岸仓储和进口食品监督中的 `饨/进人/输人/骨于/半于/皇` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch7_20260704.md`。
- 暂缓：`方吨啤酒灌装线`、`时有长落` 以及其它未逐页核证残留。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第八批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
