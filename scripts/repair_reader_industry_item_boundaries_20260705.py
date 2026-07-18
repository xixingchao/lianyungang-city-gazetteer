# -*- coding: utf-8 -*-
"""Restore source-backed industry item boundaries in the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_industry_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_industry_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_工业产品企业条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("四、东海县家具厂", "该厂位于东海县牛山镇牛山南路56号，为县属集体所有制企业，与东海特种纤维复合材料厂两块牌子，一套班子。", "workbench/ocr/raw/上/part03/page_0217.txt:4"),
    ("五、灌云县家具厂", "该厂位于灌云县伊山镇通淮路，为镇属集体所有制企业。", "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:12536"),
    ("三、连云港市连毅实业有限公司", "该厂位于新浦区解放东路62号，为市属三资企业。", "workbench/ocr/raw/上/part03/page_0224.txt:20"),
    ("四、连云港连合兴灯饰有限公司", "该厂位于新浦区解放东路62号，为市属三资企业。", "workbench/ocr/raw/上/part03/page_0224.txt:29"),
    ("五、连云港市家用电器总厂", "该厂位于新浦区海连西路21号，为市属全民所有制企业。", "workbench/ocr/raw/上/part03/page_0225.txt:4"),
    ("二、床单", "连云港市床单生产始于民国18年（1929年）。", "workbench/ocr/raw/上/part03/page_0250.txt:4"),
    ("四、赣榆县针织厂", "该厂位于赣榆县青口镇华中路27号，为县属集体所有制企业。", "workbench/ocr/raw/上/part03/page_0253.txt:17"),
    ("三、粗纺呢绒", "连云港市呢绒生产始于20世纪80年代中期。", "workbench/ocr/raw/上/part03/page_0260.txt:10"),
    ("二、塑料单丝", "境内投产塑料单丝始于20世纪60年代中期。", "workbench/ocr/raw/上/part03/page_0284.txt:17"),
    ("三、塑料袋类", "境内投产塑料袋类始于1966年。", "workbench/ocr/raw/上/part03/page_0284.txt:31"),
    ("七、人造革", "连云港市生产人造革始于1976年初。", "workbench/ocr/raw/上/part03/page_0286.txt:34"),
    ("九、箱类", "境内生产塑料箱类产品始于1982年。", "workbench/ocr/raw/上/part03/page_0288.txt:10"),
    ("二、连云港市塑料制品二厂", "该厂位于新浦解放东路东首，为市属全民所有制企业，成立于1957年7月。", "workbench/ocr/raw/上/part03/page_0291.txt:4"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for title, lead, source in ITEMS:
        old = f"<p>{title}{lead}"
        new = f"<h5>{title}</h5>\n<p>{lead}"
        old_count = html.count(old)
        if old_count == 1:
            html = html.replace(old, new, 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and html.count(new) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {title} once, got {old_count}")
        changes.append({"label": title, "status": status, "changed": changed, "source": source})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 工业产品企业条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按源 OCR 分行恢复上册工业卷 13 处产品/企业条目标题边界，仅拆标题，不改正文文字。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        lines.append(f"  - `{change['source']}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 工业产品企业条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_industry_item_boundaries_20260705.py`，按源 OCR/正文分行恢复上册工业卷 13 处产品/企业条目标题边界，覆盖家具、电光源家用电器、针织复制、塑料等小节。
- 源页证据包括：`workbench/ocr/raw/上/part03/page_0217.txt:4`、`page_0224.txt:20/29`、`page_0225.txt:4`、`page_0250.txt:4`、`page_0253.txt:17`、`page_0260.txt:10`、`page_0284.txt:17/31`、`page_0286.txt:34`、`page_0288.txt:10`、`page_0291.txt:4`。
- 报告：`output/reports/reader_industry_item_boundaries_20260705.md`。
""",
    )

    print("reader_industry_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
