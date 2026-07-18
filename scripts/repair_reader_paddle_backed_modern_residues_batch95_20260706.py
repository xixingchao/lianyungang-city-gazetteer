# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern prose residues, batch 95."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch95_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch95_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_现代正文残留Paddle回源补修第九十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "农业机械机动犁耙",
        "old": "机动犁、等产品",
        "new": "机动犁、耙等产品",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0194.txt:29-30",
    },
    {
        "label": "农业机械增加一批",
        "old": "增加一一批",
        "new": "增加一批",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0194.txt:31-32",
    },
    {
        "label": "农业机械一定生产规模",
        "old": "形成一一定的生产规模",
        "new": "形成一定的生产规模",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0194.txt:34",
    },
    {
        "label": "空调器各一台",
        "old": "组装式空调器各台，市振兴大厦营业厅空调冷冻机采用漠化锂吸收式制冷机，为全市第\n家使用溴化锂吸收式制冷机组单位",
        "new": "组装式空调器各一台，市振兴大厦营业厅空调冷冻机采用溴化锂吸收式制冷机，为全市第一\n家使用溴化锂吸收式制冷机组单位",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0318.txt:13-14",
    },
    {
        "label": "空调器各一台 HTML",
        "old": "组装式空调器各台，市振兴大厦营业厅空调冷冻机采用漠化锂吸收式制冷机，为全市第家使用溴化锂吸收式制冷机组单位",
        "new": "组装式空调器各一台，市振兴大厦营业厅空调冷冻机采用溴化锂吸收式制冷机，为全市第一家使用溴化锂吸收式制冷机组单位",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0318.txt:13-14",
    },
    {
        "label": "水运海道入临洪河",
        "old": "木帆船多经海道人临洪河至新浦",
        "new": "木帆船多经海道入临洪河至新浦",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0054.txt:32-33",
    },
    {
        "label": "邮路新浦至赣榆",
        "old": "新浦室赣榆的委办汽车邮路",
        "new": "新浦至赣榆的委办汽车邮路",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0067.txt:26-28",
    },
    {
        "label": "邮路二级干线自办汽车",
        "old": "二级于线自办汽车邮路",
        "new": "二级干线自办汽车邮路",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0067.txt:30",
    },
    {
        "label": "云华宾馆第一家",
        "old": "连云港市第家中外合作饭店",
        "new": "连云港市第一家中外合作饭店",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0117.txt:8",
    },
    {
        "label": "新浦第一家专业浴池",
        "old": "新浦出现第家专业浴池",
        "new": "新浦出现第一家专业浴池",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0155.txt:5",
    },
    {
        "label": "财政节支一定作用",
        "old": "起了一一定作用",
        "new": "起了一定作用",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0304.txt:6-7",
    },
    {
        "label": "麻醉药品一定条件",
        "old": "必须具备一一定条件",
        "new": "必须具备一定条件",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0199.txt:35",
    },
]

LEFT_UNTOUCHED = [
    "`集用空调` Paddle 页级文本同读，本批未猜改。",
    "`劳改队撤销，并人徐州第四监狱` Paddle 同读为 `并人`，继续保留。",
    "大量 `深人/并人/于线` 候选只按具体页证据处理，不做全局替换。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        for item in items:
            item["verified"] = verify.count(item["new"])
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Source-backed modern prose OCR residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with Paddle OCR page evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 现代正文残留补修第九十五批：Paddle 页级回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的少量现代正文 OCR 残留。",
        "- 只处理 PaddleOCR 页级文本能够闭合的精确短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次运行新增替换：{payload['changed_this_run']} 处",
        f"- 当前核验覆盖：{payload['verified_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第九十五批：现代正文残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 Paddle 页级回源，修复农业机械段 `机动犁、耙`、`增加一批`、`一定的生产规模`，建筑空调段 `各一台/溴化锂/第一家`，水运 `海道入临洪河`，邮路 `新浦至赣榆/二级干线`，旅游 `第一家中外合作饭店/第一家专业浴池`，财政与医政药政重复 `一` 残留。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch95_20260706.md`。
- 边界：`集用空调` 与 `劳改队撤销，并人徐州第四监狱` 均因 Paddle 同读暂不猜改；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
