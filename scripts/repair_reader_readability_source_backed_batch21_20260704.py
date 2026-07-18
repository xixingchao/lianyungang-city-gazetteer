# -*- coding: utf-8 -*-
"""Repair a twenty-first small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch21_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch21_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十一批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "青少年团体段首补全",
        "\n习雷锋报告会近千次",
        "\n“学雷锋、树新风”活动1963年，市各级团组织开展“向雷锋同志学习”活动，举办学习雷锋报告会近千次",
        "workbench/ocr/paddle_ocr/下/part01/page_0324.txt:21-22",
    ),
    (
        "学习雷锋",
        "学寸雷锋",
        "学习雷锋",
        "workbench/ocr/paddle_ocr/下/part01/page_0324.txt:23-24",
    ),
    (
        "授予吴伦东称号",
        "团市委授为保护民兵枪支光荣献身的市毛巾广工人吴伦东",
        "团市委授予为保护民兵枪支光荣献身的市毛巾厂工人吴伦东",
        "workbench/ocr/paddle_ocr/下/part01/page_0324.txt:28-29",
    ),
    (
        "吴伦东烈士展览",
        "吴伦东烈土塑像，举办吴伦东烈土事迹展览。1984年春节前岁",
        "吴伦东烈士塑像，举办吴伦东烈士事迹展览。1984年春节前夕",
        "workbench/ocr/paddle_ocr/下/part01/page_0324.txt:29",
    ),
    (
        "离退休老干部",
        "慰问离退休老于部、老职工",
        "慰问离退休老干部、老职工",
        "workbench/ocr/paddle_ocr/下/part01/page_0324.txt:33",
    ),
    (
        "青年候车亭漏句",
        "团市委号召市区各级团组织承建“青年候车亭”，市区1987年，为纪念",
        "团市委号召市区各级团组织承建“青年候车亭”，市区15个系统30多个单位的团组织参加，并对活动中表现突出的38个先进单位进行表彰。1987年，为纪念",
        "workbench/ocr/paddle_ocr/下/part01/page_0324.txt:34-36",
    ),
    (
        "戍守边疆",
        "并对成守边疆的连云港市籍的人民解放军战士进行慰问",
        "并对戍守边疆的连云港市籍的人民解放军战士进行慰问",
        "workbench/ocr/paddle_ocr/下/part01/page_0324.txt:37-38",
    ),
    (
        "蓖麻小种植",
        "开展葩麻小种植竞赛",
        "开展蓖麻小种植竞赛",
        "workbench/ocr/paddle_ocr/下/part01/page_0328.txt:6-7",
    ),
    (
        "红领巾竞赛",
        "全国红领币读书读报竞赛",
        "全国红领巾读书读报竞赛",
        "workbench/ocr/paddle_ocr/下/part01/page_0328.txt:7-8",
    ),
    (
        "勤巧小队引号",
        "各族儿童“勤巧小队友谊赛，全市52个少先队小队获全国勤巧小队奖”",
        "各族儿童“勤巧小队”友谊赛，全市52个少先队小队获“全国勤巧小队奖”",
        "workbench/ocr/paddle_ocr/下/part01/page_0328.txt:10-12",
    ),
    (
        "风华杯竞赛",
        "全国创造性活动一一风华杯”竞赛",
        "全国创造性活动—“风华杯”竞赛",
        "workbench/ocr/paddle_ocr/下/part01/page_0328.txt:12-13",
    ),
]

SKIPPED = [
    "其它章节里的 `烈土/红领币/毛巾广/准海工学院` 残留未逐页核对，本批不做全局替换。",
    "上册大事记 `提拨` 跨页 OCR 只证明原识别形态，未取得校勘强证据，继续暂缓。",
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
        "scope": "第二十一批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复下册社团页级 OCR 明确支撑的短上下文残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十一批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修下册社团页级 OCR 明确支撑的短上下文残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for item in targets[0]["items"]:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`；依据 `{item['source']}`；命中 {item['count']} 处/文件。")
    lines += ["", "## 暂缓", *[f"- {item}" for item in SKIPPED], ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-04 第二十一批正文残留回源修复"
    memory = f"""
{marker}
- 对 `output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 同步执行第二十一批社团章节回源修复。
- 本批依据 `workbench/ocr/paddle_ocr/下/part01/page_0324.txt` 和 `page_0328.txt`，修复青少年团体/少先队段中的 `学寸雷锋`、`毛巾广工人`、`烈土塑像`、`老于部`、`成守边疆`、`葩麻`、`红领币`、`勤巧小队`、`风华杯` 等残留。
- 明细报告：`output/reports/reader_readability_source_backed_batch21_20260704.md`。
"""
    upsert_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
