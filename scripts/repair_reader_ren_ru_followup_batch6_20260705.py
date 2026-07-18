# -*- coding: utf-8 -*-
"""Sixth exact-match pass for clear 人/入 OCR residues in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_ru_followup_batch6_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_ru_followup_batch6_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文人入错识第六批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("加入初级社高级社", "加人到初级社、高级社", "加入到初级社、高级社", 2),
    ("杨光銮加入共产党", "加人共产党的杨光銮", "加入共产党的杨光銮", 1),
    ("监所检察深入实际", "深人实际", "深入实际", 1),
    ("复查范围列入", "列人复查范围", "列入复查范围", 1),
    ("黄安舰编入现役", "编人现役", "编入现役", 1),
    ("保安队编入主力", "编人主力", "编入主力", 1),
    ("赣榆保安大队编入", "被编人九十八军", "被编入九十八军", 1),
    ("三团编入苏皖纵队", "三团被编人八路军苏皖纵队陇海南进支队三团", "三团被编入八路军苏皖纵队陇海南进支队三团", 1),
    ("县大队编入独立团", "编人海赣独立团", "编入海赣独立团", 1),
    ("海陵县大队编入", "编人该团", "编入该团", 1),
    ("灌云县大队编入", "被编人灌云县警卫团", "被编入灌云县警卫团", 1),
    ("竹庭独立团编入", "编人华东野战军三纵", "编入华东野战军三纵", 1),
    ("预备役登记编入", "登记编人预备役", "登记编入预备役", 1),
    ("人防办列入编制", "列人市革委会正式编制", "列入市革委会正式编制", 1),
    ("民兵训练计划列入", "列人民兵训练计划", "列入民兵训练计划", 1),
    ("进入一级战备", "进人一级战备", "进入一级战备", 1),
    ("进入人防工事", "进人人防工事", "进入人防工事", 1),
    ("进入山东", "进人山东", "进入山东", 1),
    ("进入滨海地区", "进人滨海地区", "进入滨海地区", 1),
    ("进入东海县境", "进人东海县境", "进入东海县境", 1),
    ("打入国际市场", "打人国际市场", "打入国际市场", 3),
    ("加入国民党", "加人中国国民党", "加入中国国民党", 1),
    ("加入抗日队伍", "加人抗日队伍", "加入抗日队伍", 1),
    ("加入红军", "加人中国工农红军", "加入中国工农红军", 1),
    ("打入伪军内部", "打人伪军内部", "打入伪军内部", 1),
    ("编入东海常备大队", "编人东海县常备大队", "编入东海县常备大队", 1),
    ("加入共产党", "加人共产党", "加入共产党", 1),
    ("加入共青团", "加人中国共产主义青年团", "加入中国共产主义青年团", 1),
    ("加入共青团短语", "加人共青团", "加入共青团", 1),
    ("加入北京人民艺术剧院", "加人北京人民艺术剧院", "加入北京人民艺术剧院", 1),
    ("加入中国共产党缺字1", "加人中国共党", "加入中国共党", 1),
    ("加入中国共产党串行2", "加人中国共产秦兆祯", "加入中国共产秦兆祯", 1),
    ("加入中国共产党串行3", "加人中国共产周国林", "加入中国共产周国林", 1),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for label, old, new, expected in REPLACEMENTS:
        count = html.count(old)
        if count != expected:
            raise RuntimeError(f"expected {expected} occurrence(s) for {label}, got {count}: {old}")
        html = html.replace(old, new)
        changes.append({"label": label, "old": old, "new": new, "count": count})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "principle": "第六批继续修复 exact-match 且上下文可判定的 人/入 OCR 错识；不处理段落串行重排。",
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文人/入错识第六批修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只修 exact-match 且上下文可判定的 `人/入` OCR 错识；段落串行、缺字和表格压缩问题另行处理。",
        "",
        "## 修复清单",
        "",
        "| 项 | 原文 | 修复后 | 次数 |",
        "|---|---|---|---|",
    ]
    for item in changes:
        lines.append(f"| {item['label']} | `{item['old']}` | `{item['new']}` | {item['count']} |")
    md = "\n".join(lines) + "\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 正文人/入错识第六批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_ren_ru_followup_batch6_20260705.py`，继续清理主阅读版中 exact-match 且上下文可判定的 `人/入` OCR 错识。
- 覆盖加入、深入、列入、编入、进入、打入等 {len(REPLACEMENTS)} 类片段，合计 {sum(item['count'] for item in changes)} 处。
- 对人物条目串行造成的 `加人中国共产...` 仅修 `加人` -> `加入`，未在本批重排段落边界。
- 报告：`output/reports/reader_ren_ru_followup_batch6_20260705.md`。
""",
    )

    print("reader_ren_ru_followup_batch6_repaired")
    print(f"changes={len(changes)}")
    print(f"total_changed_occurrences={sum(item['count'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
