# -*- coding: utf-8 -*-
"""Fifth exact-match pass for clear 人/入 OCR residues in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_ru_followup_batch5_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_ru_followup_batch5_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文人入错识第五批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("国家重点工程列入", "列人国家重点工程之一", "列入国家重点工程之一", 1),
    ("粮食征超议购入库", "征超议购人库达1.97万吨", "征超议购入库达1.97万吨", 2),
    ("税收检查入库", "当年人库625.5万元", "当年入库625.5万元", 1),
    ("家庭财产保险深入", "深人各行业工会", "深入各行业工会", 1),
    ("工会运动进入", "派一批党员进人各级工会", "派一批党员进入各级工会", 1),
    ("农民运动深入", "深人农村", "深入农村", 2),
    ("宣传深入人心", "深人人心", "深入人心", 1),
    ("恢复生产深入", "深人工厂、码头、矿山", "深入工厂、码头、矿山", 1),
    ("政协联系深入", "深人县区", "深入县区", 1),
    ("政协协商深入", "深人开展政治协商", "深入开展政治协商", 1),
    ("救灾深入", "深人三县灾区", "深入三县灾区", 1),
    ("拥军优属列入", "建国后，拥军优属工作列人各级政府的重要工作", "建国后，拥军优属工作列入各级政府的重要工作", 1),
    ("火炬计划列入", "被列人国家第一批“火炬计划”", "被列入国家第一批“火炬计划”", 1),
    ("重点保护列入", "列人国家重点保护", "列入国家重点保护", 1),
    ("联合国红皮书列入", "有列人联合国红皮书", "有列入联合国红皮书", 1),
    ("侵入倒闭", "侵人而倒闭", "侵入而倒闭", 1),
    ("顺层侵入体", "顺层侵人体", "顺层侵入体", 1),
    ("侵入岩类", "侵人岩类花岗石", "侵入岩类花岗石", 1),
    ("产品打入国际市场", "产品打人国际市场", "产品打入国际市场", 2),
    ("逐步打入国际市场", "逐步打人国际市场", "逐步打入国际市场", 1),
    ("打入意大利市场", "打人意大利市场", "打入意大利市场", 1),
    ("打入美国市场", "涤纶长裤打人美国市场", "涤纶长裤打入美国市场", 1),
    ("打入国民党", "打人国民党", "打入国民党", 1),
    ("打入敌伪", "打人敌伪", "打入敌伪", 2),
    ("打入沈小街据点", "打人沈小街据点", "打入沈小街据点", 1),
    ("考入第十中学", "考人江苏省立第十中学", "考入江苏省立第十中学", 1),
    ("考入同济大学", "考人上海同济大学", "考入上海同济大学", 1),
    ("考入第八师范", "考人江苏省立第八师范学校", "考入江苏省立第八师范学校", 2),
    ("考入东海中学师范科", "考人东海中学师范科", "考入东海中学师范科", 1),
    ("考入连云水产学校", "考人江苏省立连云水产学校师范班", "考入江苏省立连云水产学校师范班", 1),
    ("考入东海师范", "考人江苏省立东海师范学校", "考入江苏省立东海师范学校", 1),
    ("考入灌云初中", "考人灌云县立初级中学", "考入灌云县立初级中学", 1),
    ("考入燕京大学", "考人燕京大学", "考入燕京大学", 1),
    ("转入医学系", "转人医学系学习", "转入医学系学习", 1),
    ("加入中国共产党", "加人中国共产党", "加入中国共产党", 45),
    ("编入华中六分区", "编人华中第六军分区支队", "编入华中第六军分区支队", 1),
    ("编入滨海军区", "编人滨海军区二十三团二营五连", "编入滨海军区二十三团二营五连", 1),
    ("编入主攻团", "被编人主攻团", "被编入主攻团", 1),
    ("编入新四军", "编人新四军三师九旅二十六团", "编入新四军三师九旅二十六团", 1),
    ("深入海岛", "深人海岛", "深入海岛", 1),
    ("深入盐场演出", "深人盐场演出", "深入盐场演出", 1),
    ("深入徐圩盐场", "深人徐圩盐场", "深入徐圩盐场", 1),
    ("进入60年代", "进人60年代", "进入60年代", 1),
    ("进入市区", "进人市区", "进入市区", 2),
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
        "principle": "第五批仅修复 exact-match 且上下文可判定的 人/入 OCR 错识；正常 打人、古文、人名和表格压缩残段不处理。",
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文人/入错识第五批修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只修 exact-match 且上下文可判定的 `人/入` OCR 错识；正常 `打人`、古文、人名和表格压缩残段不处理。",
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

    marker = "## 2026-07-05 正文人/入错识第五批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_ren_ru_followup_batch5_20260705.py`，继续清理主阅读版中 exact-match 且上下文可判定的 `人/入` OCR 错识。
- 覆盖列入、入库、深入、进入、打入、考入、加入、编入、侵入等 {len(REPLACEMENTS)} 类片段，合计 {sum(item['count'] for item in changes)} 处。
- 明确跳过正常 `打人` 语义、古文、人名和表格压缩残段。
- 报告：`output/reports/reader_ren_ru_followup_batch5_20260705.md`。
""",
    )

    print("reader_ren_ru_followup_batch5_repaired")
    print(f"changes={len(changes)}")
    print(f"total_changed_occurrences={sum(item['count'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
