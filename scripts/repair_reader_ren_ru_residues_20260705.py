# -*- coding: utf-8 -*-
"""Repair source-clear 人/入 OCR residues in the current reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
TABLE_INDEX = ROOT / "output" / "structured_tables" / "index.html"
TABLE_JSON = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T009.json"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_ru_residues_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_ru_residues_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文人入错识批量修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

READER_REPLACEMENTS = [
    ("河流入海-埒子口", "埒子口人海", "埒子口入海", 1),
    ("河流入海-临洪口", "临洪口人海", "临洪口入海", 1),
    ("河流入海-烧香河口", "烧香河口人海", "烧香河口入海", 1),
    ("港口防污", "污水人海量", "污水入海量", 1),
    ("卫生检疫", "人境的中、外籍船舶", "入境的中、外籍船舶", 1),
    ("边防法规", "出人国境治安暂行条例", "出入国境治安暂行条例", 1),
    ("边防文书", "船只人港预报表", "船只入港预报表", 1),
    ("有线电视", "有线电视人户率", "有线电视入户率", 1),
    ("白酒生产", "瓶酒人库", "瓶酒入库", 1),
    ("计划生育", "女子人托费", "女子入托费", 1),
    ("教育统计-民国", "小学生人学率", "小学生入学率", 1),
    ("劳改教育", "犯人人学率", "犯人入学率", 1),
    ("工艺美术迁址", "迁人市工艺美术公司院内", "迁入市工艺美术公司院内", 1),
    ("工艺厂迁址", "迁人海州江化街", "迁入海州江化街", 1),
    ("铁工厂迁址", "迁人新浦", "迁入新浦", 1),
    ("电子厂迁址", "迁人连云港市", "迁入连云港市", 1),
    ("包装厂迁址", "迁人开发区", "迁入开发区", 1),
    ("海岸电台迁址", "迁人新址", "迁入新址", 1),
    ("图书馆迁址", "迁人新馆", "迁入新馆", 1),
    ("教堂迁址", "迁人新教堂", "迁入新教堂", 1),
    ("人口普查", "深人基层", "深入基层", 6),
    ("农电培训", "深人至各用电公社", "深入至各用电公社", 1),
    ("海监宣传", "深人渔村", "深入渔村", 1),
    ("美术写生", "深人港区", "深入港区", 1),
    ("文化馆农村辅导", "深人各工厂、农村", "深入各工厂、农村", 1),
    ("抗战斗争", "深人敌后", "深入敌后", 1),
    ("烈士事迹", "深人虎穴", "深入虎穴", 1),
    ("邮电网络", "进人市话网", "进入市话网", 1),
    ("商业阶段", "进人社会主义建设时期", "进入社会主义建设时期", 1),
    ("物资市场", "进人大市场", "进入大市场", 2),
    ("历史时期", "进人新的历史时期", "进入新的历史时期", 1),
    ("建设时期", "进人新的建设与发展时期", "进入新的建设与发展时期", 1),
    ("经济走势", "进人崩溃", "进入崩溃", 1),
    ("民族宗教", "进人市境内参加社会主义建设", "进入市境内参加社会主义建设", 1),
    ("豆制品合并", "并人海州蔬菜海味干菜商店", "并入海州蔬菜海味干菜商店", 1),
    ("联运站撤销", "并人县航运管理所", "并入县航运管理所", 1),
    ("邮电局合并", "并人赣榆邮电局", "并入赣榆邮电局", 1),
    ("电话网合并", "并人新浦自动网", "并入新浦自动网", 1),
    ("机构合并-商业局", "并人商业局", "并入商业局", 1),
    ("机构合并-宣传部", "并人宣传部", "并入宣传部", 1),
    ("机构合并-工业工作部", "并人工业工作部", "并入工业工作部", 1),
    ("商业合并", "并人国营商业", "并入国营商业", 2),
    ("工艺美术获奖表", "人选江苏省首届民间美术博览会", "入选江苏省首届民间美术博览会", 1),
]

STRUCTURED_REPLACEMENTS = [
    (TABLE_JSON, "工艺美术获奖表JSON", "人选江苏省首届民间美术博览会", "入选江苏省首届民间美术博览会", 1),
    (TABLE_INDEX, "结构化表索引", "人选江苏省首届民间美术博览会", "入选江苏省首届民间美术博览会", 1),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def replace_checked(text: str, label: str, old: str, new: str, expected: int) -> tuple[str, dict[str, str | int]]:
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"expected {expected} occurrence(s) for {label}, got {count}: {old}")
    return text.replace(old, new), {"label": label, "old": old, "new": new, "count": count}


def main() -> None:
    changes = []

    html = HTML.read_text(encoding="utf-8")
    for label, old, new, expected in READER_REPLACEMENTS:
        html, item = replace_checked(html, label, old, new, expected)
        changes.append({"target": str(HTML.relative_to(ROOT)).replace("\\", "/"), **item})
    HTML.write_text(html, encoding="utf-8")

    for path, label, old, new, expected in STRUCTURED_REPLACEMENTS:
        text = path.read_text(encoding="utf-8")
        text, item = replace_checked(text, label, old, new, expected)
        path.write_text(text, encoding="utf-8")
        changes.append({"target": str(path.relative_to(ROOT)).replace("\\", "/"), **item})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "principle": "仅修复上下文明确应为入/深入/进入/迁入/并入/入海/入境/入港/入户/入库/入学/入托/入选的 人 字 OCR 错识；保留人户分离、人名、古文和证据不足项。",
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文人/入错识批量修复",
        "",
        f"- 时间：{now}",
        f"- 主阅读版：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只做 exact-match 修复；保留 `人户分离`、人名、古文用例和证据不足项。",
        f"- 同步结构化表：`{TABLE_JSON.relative_to(ROOT)}`、`{TABLE_INDEX.relative_to(ROOT)}`。",
        "",
        "## 修复清单",
        "",
        "| 项 | 目标 | 原文 | 修复后 | 次数 |",
        "|---|---|---|---|---|",
    ]
    for item in changes:
        lines.append(f"| {item['label']} | `{item['target']}` | `{item['old']}` | `{item['new']}` | {item['count']} |")
    md = "\n".join(lines) + "\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 正文人/入错识批量修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_ren_ru_residues_20260705.py`，限定 exact-match 修复主阅读版中上下文明确的 `人/入` OCR 错识。
- 覆盖入海、入境、入港、入户、入库、入托、入学、迁入、深入、进入、并入、入选等 {len(READER_REPLACEMENTS)} 类片段；同步修复 `LYG-中-T009` JSON 与结构化表索引中的 `人选江苏省首届民间美术博览会`。
- 明确保留 `人户分离`、人名、古文和证据不足项，不做全局 `人` -> `入` 替换。
- 报告：`output/reports/reader_ren_ru_residues_20260705.md`。
""",
    )

    print("reader_ren_ru_residues_repaired")
    print(f"reader_changes={len(READER_REPLACEMENTS)}")
    print(f"total_changed_occurrences={sum(int(item['count']) for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
