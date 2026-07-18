# -*- coding: utf-8 -*-
"""Repair narrowly source-backed reader OCR residues, batch 90."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch90_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch90_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第九十批_Paddle回源残留.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "陶庵西小区海拔",
        "old": "在海拨136米的山坡上建有一个蓄水池",
        "new": "在海拔136米的山坡上建有一个蓄水池",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0304.txt:27",
    },
    {
        "label": "爪墩旧石器地点海拔与地名",
        "old": "在马陵山中段海拨91米的瓜墩上",
        "new": "在马陵山中段海拔91米的爪墩上",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0075.txt:16",
    },
    {
        "label": "传教士别墅标题",
        "old": "五、传教土别墅",
        "new": "五、传教士别墅",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0098.txt:13",
    },
    {
        "label": "基督教明乐林传教士",
        "old": "美国传教土明乐林用救济物资",
        "new": "美国传教士明乐林用救济物资",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0271.txt:24",
    },
    {
        "label": "海州西门外耶稣堂传教士",
        "old": "美国传教土建立的海州西门外耶稣堂",
        "new": "美国传教士建立的海州西门外耶稣堂",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0272.txt:26",
    },
    {
        "label": "上海大旅社年份标点与合璧",
        "old": "民国22年（1933.年）上海人所建。为石结构中西合壁式两层楼房",
        "new": "民国22年（1933年）上海人所建。为石结构中西合璧式两层楼房",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:25663; workbench/ocr/raw/上/part02/page_0092.txt:7",
    },
    {
        "label": "上海大旅社年份标点与合璧源稿断行",
        "old": "民国22年（1933.年）上海人所建。为石结构中西合壁式两\n层楼房",
        "new": "民国22年（1933年）上海人所建。为石结构中西合璧式两\n层楼房",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:25663; workbench/ocr/raw/上/part02/page_0092.txt:7",
    },
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
        "scope": "Paddle/raw source-backed modern reader residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "principle": "Only exact contexts with OCR or raw-source support are changed; broad 海拨/中西合壁 sweeps are excluded.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第九十批：Paddle/原始 OCR 回源残留",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的现代正文错字残留。",
        "- 只处理已有 PaddleOCR 或原始 OCR 证据闭合的精确短语。",
        "- 不做 `海拨`、`中西合壁` 等全局替换，避免误改未核段落。",
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
    lines.extend([
        "",
        "## 未处理边界",
        "",
        "- 上册自然环境等源稿中的多处 `海拨` 未纳入本批，需逐页回源后再处理。",
        "- 东亚旅社、味芳楼、万康祥等其他 `中西合壁` 未做全局替换，等待逐条证据。",
        "- 用户提示的整本转换错乱风险需另起抽样/重转换审计；本批仅清理可确定短语。",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第九十批：Paddle/原始 OCR 回源残留

- 继续按主阅读版 `output/final_reader/连云港市志_全书.html` 做窄范围回源修复，处理陶庵西小区 `海拔136米`、爪墩旧石器地点 `海拔91米/爪墩`、三处 `传教士`、上海大旅社 `1933年/中西合璧式`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_residues_batch90_20260706.md`。
- 边界：未做 `海拨` 和 `中西合壁` 全局替换；用户提示整本转换文字可能有系统性问题，后续需单独做抽样/重转换审计；未展示、未嵌入图片。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第九十批：Paddle/原始 OCR 回源残留", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
