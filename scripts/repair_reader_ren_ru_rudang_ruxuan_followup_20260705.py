# -*- coding: utf-8 -*-
"""Small exact-match pass for clear 入党/入选 OCR residues in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_ru_rudang_ruxuan_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_ru_rudang_ruxuan_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文入党入选与郁华民条目补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

YU_HUAMIN_OLD = (
    "<p>）原名立三，东海县牛山乡郁圩村人。民国17年（1928年）秋加郁华民（1906~"
    "入中国共产党，并任圩支部宣传委员，领导牛山等19个村庄的抗捐斗争。民国22年在邮圩小学"
    "组织青年读书会，组织青年抗日义勇团。此时与党组织失去联系。抗日战争期间，以郁圩小学为"
    "阵地，组织宣传队宣传抗日救亡，用自家的财产作为党的活动经费，建立苏皖纵队陇海游击支队。"
    "民国29年任抗日民主政府创办的述宿海中学、滨海中学等校校长。民国31年重新人党。民国37年"
    "11月受命接管东海师范，任校长。1979年任连云港市教育局顾问。</p>"
)

YU_HUAMIN_NEW = (
    "<p>郁华民（1906~）原名立三，东海县牛山乡郁圩村人。民国17年（1928年）秋加入中国共产党，"
    "并任圩支部宣传委员，领导牛山等19个村庄的抗捐斗争。民国22年在邮圩小学组织青年读书会，"
    "组织青年抗日义勇团。此时与党组织失去联系。抗日战争期间，以郁圩小学为阵地，组织宣传队"
    "宣传抗日救亡，用自家的财产作为党的活动经费，建立苏皖纵队陇海游击支队。民国29年任抗日"
    "民主政府创办的述宿海中学、滨海中学等校校长。民国31年重新入党。民国37年11月受命接管"
    "东海师范，任校长。1979年任连云港市教育局顾问。</p>"
)

REPLACEMENTS = [
    ("妇女运动女青年入党", "女青年人党", "女青年入党", 1),
    ("党员轮训入党", "人党的9000多名党员", "入党的9000多名党员", 1),
    ("国民党集体入党", "集体人党", "集体入党", 1),
    ("填写入党申请书", "填写人党申请书", "填写入党申请书", 1),
    ("郑鹤12月入党", "12月人党", "12月入党", 1),
    ("篆刻作品入选江苏省", "作品人选江苏省", "作品入选江苏省", 3),
    ("摄影作品入选全国", "作品人选全国", "作品入选全国", 1),
    ("张理渔归入选参展", "张理的《渔归》人选参展", "张理的《渔归》入选参展", 1),
    ("雕塑作品入选江苏省", "雕塑作品，都人选江苏省美术展览", "雕塑作品，都入选江苏省美术展览", 1),
    ("培养入党对象", "培养人党对象", "培养入党对象", 1),
    ("张理劈山建海港入选参展", "张理的《劈山建海港》人选参展", "张理的《劈山建海港》入选参展", 1),
    ("繁忙的集市入选全国展览", "许金芳的《繁忙的集市》人选全国举办的“欢笑的农村”展览", "许金芳的《繁忙的集市》入选全国举办的“欢笑的农村”展览", 1),
    ("篆刻作品集选入", "作品被选人《篆刻作品集》", "作品被选入《篆刻作品集》", 1),
    ("重新填写入党申请书", "重新填人党申请书", "重新填写入党申请书", 1),
    ("地毯图案集选入", "被选人《江苏省地毯图案集", "被选入《江苏省地毯图案集", 1),
    ("国家石材样品库选入", "被选人国家石材样品库", "被选入国家石材样品库", 1),
    ("中国现代小说选选入", "被选人《中国现代小说选》", "被选入《中国现代小说选》", 1),
    ("学习活动深入开展", "深人开展", "深入开展", 1),
    ("足球运动员入选省队", "人选江苏省男子足球队", "入选江苏省男子足球队", 1),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []

    count = html.count(YU_HUAMIN_OLD)
    if count == 1:
        html = html.replace(YU_HUAMIN_OLD, YU_HUAMIN_NEW, 1)
        changes.append({"label": "郁华民条目姓名错位与重新入党", "count": 1, "expected": 1, "status": "changed"})
    elif count == 0 and html.count(YU_HUAMIN_NEW) >= 1:
        changes.append({"label": "郁华民条目姓名错位与重新入党", "count": 0, "expected": 1, "status": "already_applied"})
    else:
        raise RuntimeError(f"expected 郁华民错位条目 once, got {count}")

    for label, old, new, expected in REPLACEMENTS:
        count = html.count(old)
        if count == expected:
            html = html.replace(old, new)
            changes.append({"label": label, "old": old, "new": new, "count": count, "expected": expected, "status": "changed"})
        elif count == 0 and html.count(new) >= expected:
            changes.append({"label": label, "old": old, "new": new, "count": 0, "expected": expected, "status": "already_applied"})
        else:
            raise RuntimeError(f"expected {expected} occurrence(s) for {label}, got {count}: {old}")

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sources = [
        "workbench/ocr/raw/下/part02/page_0384.txt",
        "workbench/ocr/raw/下/part02/page_0385.txt",
        "workbench/ocr/raw/下/part02/page_0386.txt",
    ]
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "principle": "只修 exact-match 且上下文可判定的 入党/入选 OCR 残留，并补修郁华民人物条目姓名错位。",
        "sources": sources,
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文入党入选与郁华民条目补修",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只修 exact-match 且上下文可判定的 `人/入` OCR 残留；不做裸全局替换。",
        "",
        "## 依据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in sources)
    lines.extend(["", "## 修复清单", "", "| 项 | 本次变更 | 目标次数 | 状态 |", "|---|---:|---:|---|"])
    for item in changes:
        lines.append(f"| {item['label']} | {item['count']} | {item.get('expected', item['count'])} | {item.get('status', 'changed')} |")
    md = "\n".join(lines) + "\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 正文入党入选与郁华民条目补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_ren_ru_rudang_ruxuan_followup_20260705.py`，补修主阅读版中入党、入选相关 `人/入` OCR 残留。
- 依据 `workbench/ocr/raw/下/part02/page_0384.txt` 与 `page_0385.txt`，将郁华民人物简介从姓名错位恢复为完整条目，并修正 `重新入党`。
- 依据 `workbench/ocr/raw/下/part02/page_0386.txt` 修正郑鹤 `12月入党`。
- 本脚本覆盖 {sum(item.get('expected', item['count']) for item in changes)} 处目标修复；可重复运行，已应用项会记录为 `already_applied`。
- 报告：`output/reports/reader_ren_ru_rudang_ruxuan_followup_20260705.md`。
""",
    )

    print("reader_ren_ru_rudang_ruxuan_followup_repaired")
    print(f"changes={len(changes)}")
    print(f"total_changed_occurrences={sum(item['count'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
