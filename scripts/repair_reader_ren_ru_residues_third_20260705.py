# -*- coding: utf-8 -*-
"""Third exact-match pass for clear 人/入 OCR residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_ru_residues_third_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_ru_residues_third_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文人入错识第三批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("锦屏磷矿入选原矿", "人选原矿品位", "入选原矿品位", 1),
    ("矿粉列入计划", "列人国家计划", "列入国家计划", 2),
    ("蔷薇河通入海州", "通人海州城内", "通入海州城内", 1),
    ("太白涧流入农田", "曲折流人山下农田", "曲折流入山下农田", 1),
    ("吕母攻入县城", "攻人县城", "攻入县城", 1),
    ("卷烟输入", "经海港输人卷烟", "经海港输入卷烟", 2),
    ("棉布输入", "港口输人棉布", "港口输入棉布", 1),
    ("羊皮货源", "大量流人", "大量流入", 1),
    ("蔬菜商店并入", "并人食品公司", "并入食品公司", 1),
    ("洗染合作社并入", "并人国营店", "并入国营店", 1),
    ("油坊并入", "并人新海油厂", "并入新海油厂", 1),
    ("油厂并入", "并人粮食加工总厂", "并入粮食加工总厂", 1),
    ("生产资料企业并入", "并人相应的专业公司", "并入相应的专业公司", 1),
    ("物资服务公司并入", "并人连云港市物资贸易中心", "并入连云港市物资贸易中心", 1),
    ("财政局并入", "并人市财政局", "并入市财政局", 2),
    ("工商统一税", "并人工商统一税", "并入工商统一税", 3),
    ("营业税并入", "并人营业税", "并入营业税", 1),
    ("企业利润入库", "利润人库", "利润入库", 1),
    ("农业税征实入库", "征实人库", "征实入库", 1),
    ("支出基数", "应进人支出基数", "应进入支出基数", 1),
    ("征管法制轨道", "运行进人了法制轨道", "运行进入了法制轨道", 1),
    ("外轮进入港口", "进人连云港港口", "进入连云港港口", 1),
    ("就业年龄", "进人就业年龄", "进入就业年龄", 1),
    ("干部班子", "进人县处级领导班子", "进入县处级领导班子", 1),
    ("发展阶段", "跃人新的发展阶段", "跃入新的发展阶段", 1),
    ("政策贯彻", "深人贯彻", "深入贯彻", 1),
    ("优抚子女入学入托", "子女人学入托", "子女入学入托", 1),
    ("教徒子女入学", "平民子女人学", "平民子女入学", 1),
    ("学生入学年龄", "学生人学年龄", "学生入学年龄", 1),
    ("篮球队入选", "人选江苏银行系统篮球代表队", "入选江苏银行系统篮球代表队", 1),
    ("女篮入选", "并人选国家女子篮球队", "并入选国家女子篮球队", 1),
    ("淮阴东", "准阴东", "淮阴东", 1),
    ("淮东安抚使", "请准东安抚使", "请淮东安抚使", 1),
    ("淮水流域", "准水流域非道利病表", "淮水流域非道利病表", 1),
    ("淮海水师", "借准海水师巡逻船", "借淮海水师巡逻船", 1),
    ("淮系年表", "准系年表全编", "淮系年表全编", 1),
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
        "principle": "第三批仍仅修复词组级可判定的 人/入 与 准/淮 OCR 错识；保留古文、人名、表格压缩段和无把握项。",
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文人/入错识第三批修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只修词组级可判定项；古文、人名、表格压缩段和无把握项暂不处理。",
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

    marker = "## 2026-07-05 正文人/入错识第三批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_ren_ru_residues_third_20260705.py`，继续清理词组级可判定的 `人/入` 残留，并顺带修正同批明确的 `准/淮` 错识。
- 覆盖入选、列入、通入、流入、攻入、输入、并入、入库、进入、深入、入学，以及 `淮阴东/淮东安抚使/淮水/淮海水师/淮系` 等 {len(REPLACEMENTS)} 类片段。
- 跳过古文、人名、表格压缩段和无把握项。
- 报告：`output/reports/reader_ren_ru_residues_third_20260705.md`。
""",
    )

    print("reader_ren_ru_residues_third_repaired")
    print(f"changes={len(changes)}")
    print(f"total_changed_occurrences={sum(item['count'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
