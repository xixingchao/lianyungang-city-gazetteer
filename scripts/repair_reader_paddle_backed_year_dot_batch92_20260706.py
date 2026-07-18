# -*- coding: utf-8 -*-
"""Repair Paddle-backed stray dots before 年, batch 92."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_year_dot_batch92_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_year_dot_batch92_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_年份点号残留Paddle回源补修第九十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "冷饮业1970年",
        "old": "1970.年，连云港市海州弹花制冰厂",
        "new": "1970年，连云港市海州弹花制冰厂",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0091.txt:8",
    },
    {
        "label": "制碘1959年10月",
        "old": "1959.年10月，市化工研究所",
        "new": "1959年10月，市化工研究所",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0154.txt:9",
    },
    {
        "label": "胶体磨1984至1990年",
        "old": "1984～1990.年共生产218台",
        "new": "1984～1990年共生产218台",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0264.txt:32",
    },
    {
        "label": "粮价1953年4月1日",
        "old": "1953.年4月1日，全面调整粮价",
        "new": "1953年4月1日，全面调整粮价",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0232.txt:17",
    },
    {
        "label": "海陵县参议会1941年",
        "old": "民国30年（1941.年）8月17日",
        "new": "民国30年（1941年）8月17日",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0500.txt:7",
    },
    {
        "label": "灌云县工会1969年",
        "old": "1969.年，灌云县革命委员会",
        "new": "1969年，灌云县革命委员会",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0308.txt:33",
    },
    {
        "label": "教师工资1954年调整后",
        "old": "1954.年调整后，人均134.78分",
        "new": "1954年调整后，人均134.78分",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0406.txt:4",
    },
    {
        "label": "灌云电影站1963年",
        "old": "1963.年，经县政府批准",
        "new": "1963年，经县政府批准",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0039.txt:28",
    },
    {
        "label": "图书馆科技组1977年",
        "old": "1977.年，科技组撤并",
        "new": "1977年，科技组撤并",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0068.txt:10",
    },
    {
        "label": "新华书店1954年",
        "old": "1954.年根据江苏省新华书店规定",
        "new": "1954年根据江苏省新华书店规定",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0070.txt:24",
    },
    {
        "label": "王宣大1978年",
        "old": "1978.年，负责筹建连云港市机械研究所",
        "new": "1978年，负责筹建连云港市机械研究所",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0395.txt:38",
    },
    {
        "label": "沈来龙1982年入党",
        "old": "1982.年加入中国共产党",
        "new": "1982年加入中国共产党",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0397.txt:28",
    },
]

LEFT_UNTOUCHED = [
    "上册/源稿中若干 YYYY.年 残留未进入当前主阅读版，本批未顺手清理。",
    "`1990.年连云港市市级学会、协会、研究会一览表` 为源稿表题残留，待表源链路单独处理。",
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
        "scope": "Paddle-backed stray-dot-before-year repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact YYYY.年 contexts with PaddleOCR support are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 年份点号残留补修第九十二批：Paddle 回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/全书汇总中的 `YYYY.年` 点号残留。",
        "- 只处理 PaddleOCR 同页明确读为 `YYYY年` 的精确短语。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第九十二批：年份点号残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做窄范围回源修复，处理 `1970.年`、`1959.年10月`、`1984～1990.年`、`1953.年4月1日`、`1941.年`、`1969.年`、`1954.年调整后`、`1963.年`、`1977.年`、`1954.年根据`、`1978.年负责筹建`、`1982.年加入` 等年份点号残留。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_year_dot_batch92_20260706.md`。
- 边界：源稿中未进入当前主阅读版的若干 `YYYY.年`、表题类 `1990.年连云港市市级学会...` 未顺手清理；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
