# -*- coding: utf-8 -*-
"""Thirty-eighth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch38_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch38_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十八批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "财政支出单位", "old": "财政支出347.5方元", "new": "财政支出347.5万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0075.txt:14"},
    {"label": "灾害直接经济损失", "old": "直接经济损失3000多方元", "new": "直接经济损失3000多万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0206.txt:25"},
    {"label": "果园投资收益", "old": "120方元，年产干果275.1吨", "new": "120万元，年产干果275.1吨", "source": "workbench/ocr/paddle_ocr/上/part01/page_0251.txt:10"},
    {"label": "出口商品交货总额", "old": "出口商品交货总额400方元", "new": "出口商品交货总额400万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0251.txt:19"},
    {"label": "财政收入", "old": "财政收入3045.9方元", "new": "财政收入3045.9万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0258.txt:26"},
    {"label": "财政总支出", "old": "财政总支出6419.5方元", "new": "财政总支出6419.5万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0258.txt:28"},
    {"label": "捕捞业固定资产", "old": "固定资产2500方元", "new": "固定资产2500万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0265.txt:25"},
    {"label": "出口商品年收购额", "old": "年收购额数方元", "new": "年收购额数万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0266.txt:24"},
    {"label": "工商业贷款", "old": "工商业贷款593方元", "new": "工商业贷款593万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0268.txt:9"},
    {"label": "税收入与财政支出", "old": "税收人1359.2方元，其它收入8.4方元；财政支出1686.5方元", "new": "税收入1359.2万元，其它收入8.4万元；财政支出1686.5万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0275.txt:11"},
    {"label": "财政拨款购置器械", "old": "市财政拨款14方元", "new": "市财政拨款14万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0298.txt:28"},
    {"label": "污染经济损失一", "old": "直接经济损失480方元", "new": "直接经济损失480万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0100.txt:26"},
    {"label": "污染经济损失二", "old": "直接经济损失40多方元", "new": "直接经济损失40多万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0100.txt:27"},
    {"label": "污染经济损失三", "old": "直接经济损失160多方元", "new": "直接经济损失160多万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0100.txt:28"},
    {"label": "工业废水治理投资", "old": "投资105方元", "new": "投资105万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0106.txt:9"},
    {"label": "生态农业建设投入", "old": "投人12方元", "new": "投入12万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0123.txt:13"},
    {"label": "生态农业经济效益", "old": "直接经济效益843方元", "new": "直接经济效益843万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0123.txt:36"},
    {"label": "工农业总产值", "old": "工农业总产值只有44904方元", "new": "工农业总产值只有44904万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0132.txt:29"},
    {"label": "新增固定资产", "old": "新增固定资产5058方元", "new": "新增固定资产5058万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0146.txt:12"},
    {"label": "质量案件价值", "old": "价值人民币73.18方元", "new": "价值人民币73.18万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0182.txt:9"},
    {"label": "粮食补贴", "old": "补贴8.15方元", "new": "补贴8.15万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0183.txt:60"},
    {"label": "粮食审计补贴与费用", "old": "补贴35.45方元；挤占商品流通费用56.92方元", "new": "补贴35.45万元；挤占商品流通费用56.92万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0184.txt:4"},
    {"label": "违纪金额", "old": "违纪金额312方元", "new": "违纪金额312万元", "source": "workbench/ocr/paddle_ocr/上/part02/page_0184.txt:21"},
    {"label": "工资调节税", "old": "45.1方元工资调节税", "new": "45.1万元工资调节税", "source": "workbench/ocr/paddle_ocr/上/part02/page_0188.txt:6"},
]


def append_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(target["changed"] for target in targets)
    payload = {
        "time": now,
        "scope": "第三十八批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修页级 Paddle OCR 直接证明的金额单位残留，不做全局方元替换。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三十八批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 Paddle OCR 直接证明的金额单位残留，不做全局 `方元` 替换。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：尚未逐页定位的其它 `方元`，以及可能涉及旧币/银元/正文结构错位的条目。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                lines.append(f"- {item['label']}：依据 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。")
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 第三十八批正文残留回源修复"
    memory = f"""
{marker}
- 修复页级 Paddle OCR 直接证明的金额单位 `方元` 残留，共 {total} 处；实际命中集中在 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 依据页：`workbench/ocr/paddle_ocr/上/part01/page_0075.txt`、`page_0206.txt`、`page_0251.txt`、`page_0258.txt`、`page_0265.txt`、`page_0266.txt`、`page_0268.txt`、`page_0275.txt`、`page_0298.txt`，`workbench/ocr/paddle_ocr/上/part02/page_0100.txt`、`page_0106.txt`、`page_0123.txt`、`page_0132.txt`、`page_0146.txt`、`page_0182.txt`、`page_0183.txt`、`page_0184.txt`、`page_0188.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`；最终阅读版本批旧串未命中。
- 暂缓尚未逐页定位的其它 `方元`，尤其可能涉及旧币、银元或正文结构错位的条目。
- 报告：`output/reports/reader_readability_source_backed_batch38_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
