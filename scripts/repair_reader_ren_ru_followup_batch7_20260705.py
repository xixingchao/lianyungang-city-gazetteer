# -*- coding: utf-8 -*-
"""Seventh exact-match pass for clear 人/入 OCR residues in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_ru_followup_batch7_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_ru_followup_batch7_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文人入错识第七批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("转入正常生产", "开始转人正常生产", "开始转入正常生产", 1),
    ("柴草转入盐河", "转人盐河外运", "转入盐河外运", 2),
    ("商户转入工业", "转人工业生产", "转入工业生产", 1),
    ("漕运转入汴河", "转人汴河", "转入汴河", 1),
    ("下达储转入储蓄", "转人储蓄", "转入储蓄", 1),
    ("县党部转入地下", "各县党部转人地下活动", "各县党部转入地下活动", 1),
    ("共产党活动转入地下", "共产党活动转人地下", "共产党活动转入地下", 1),
    ("成人教育转入提高", "一部分人转人提高文化水平和专业技术的学习", "一部分人转入提高文化水平和专业技术的学习", 1),
    ("外县市转入", "外县市转人13人", "外县市转入13人", 1),
    ("转入北京大学", "转人北京大学", "转入北京大学", 1),
    ("工资计划列入地方管理", "列人地方管理", "列入地方管理", 1),
    ("知青办列入编制", "列人各区、局、公社、直属厂矿革委会正式编制", "列入各区、局、公社、直属厂矿革委会正式编制", 1),
    ("未列入调资范围", "未列人调资范围", "未列入调资范围", 1),
    ("妇女保护列入", "妇女保护列人工作日程", "妇女保护列入工作日程", 1),
    ("生产竞赛列入章程", "组织生产竞赛列人《职工总会章程（草案）》", "组织生产竞赛列入《职工总会章程（草案）》", 1),
    ("小学卫生列入计划", "将小学卫生工作列人学校工作计划", "将小学卫生工作列入学校工作计划", 1),
    ("劳动列入课表", "将劳动列人课表", "将劳动列入课表", 1),
    ("课外活动列入课表", "将课外活动列人课表", "将课外活动列入课表", 1),
    ("生产劳动课列入", "生产劳动课列人课表", "生产劳动课列入课表", 1),
    ("科技费用列入预算", "科技三项费用列人财政预算", "科技三项费用列入财政预算", 1),
    ("加入所在国国籍", "加人所在国的国籍", "加入所在国的国籍", 1),
    ("加入国民党", "加人国民党", "加入国民党", 2),
    ("考入陆军讲武堂", "考人江苏陆军讲武堂步兵科一期", "考入江苏陆军讲武堂步兵科一期", 1),
    ("考入南京国立第四中山大学", "考人南京国立第四中山大学", "考入南京国立第四中山大学", 1),
    ("考入私立南京中学", "考人私立南京中学", "考入私立南京中学", 1),
    ("考入峄县农业中学", "考人山东省峰县农业中学", "考入山东省峰县农业中学", 1),
    ("考入江苏省立第十一中学", "考人江苏省立第十一中学", "考入江苏省立第十一中学", 1),
    ("考入保定讲武堂", "毕业后考人保定讲武堂", "毕业后考入保定讲武堂", 1),
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
        "principle": "第七批继续修复 exact-match 且上下文可判定的 人/入 OCR 错识；结构串行和表格压缩残段暂不处理。",
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文人/入错识第七批修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只修 exact-match 且上下文可判定的 `人/入` OCR 错识；结构串行和表格压缩残段暂不处理。",
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

    marker = "## 2026-07-05 正文人/入错识第七批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_ren_ru_followup_batch7_20260705.py`，继续清理主阅读版中 exact-match 且上下文可判定的 `人/入` OCR 错识。
- 覆盖转入、列入、加入、考入等 {len(REPLACEMENTS)} 类片段，合计 {sum(item['count'] for item in changes)} 处。
- 明确跳过 `人库合`、人物条目串行、表格压缩残段等需要回源或结构处理的问题。
- 报告：`output/reports/reader_ren_ru_followup_batch7_20260705.md`。
""",
    )

    print("reader_ren_ru_followup_batch7_repaired")
    print(f"changes={len(changes)}")
    print(f"total_changed_occurrences={sum(item['count'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
