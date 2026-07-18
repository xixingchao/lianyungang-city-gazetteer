# -*- coding: utf-8 -*-
"""Forty-seventh source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch47_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch47_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十七批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "地产小百货收购值", "old": "收购值由200万元增加到647方元", "new": "收购值由200万元增加到647万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0134.txt:9"},
    {"label": "百货调给省外商品值", "old": "调给省外321方元", "new": "调给省外321万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0134.txt:14"},
    {"label": "百货调给市区供销社", "old": "调给市区供销社306方元", "new": "调给市区供销社306万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0134.txt:20"},
    {"label": "百货调给邻县商品值", "old": "调给邻县919方元", "new": "调给邻县919万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0134.txt:41"},
    {"label": "进口粮接运站开办费", "old": "商业部拨开办费60方元", "new": "商业部拨开办费60万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0249.txt:12"},
    {"label": "控购罚没款", "old": "罚没款150余方元", "new": "罚没款150余万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0308.txt:20"},
    {"label": "飞天特种润滑油厂产值", "old": "三年实现产值\n1030方元", "new": "三年实现产值\n1030万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0370.txt:6-7"},
    {"label": "工行信托部投资贷款", "old": "发放投资贷款200方元", "new": "发放投资贷款200万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0371.txt:23"},
    {"label": "交通运输船舶车辆更新贷款", "old": "发放贷款176方元", "new": "发放贷款176万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0371.txt:32"},
    {"label": "长城信用卡存款余额", "old": "存款余额为人民币35.45方元", "new": "存款余额为人民币35.45万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0375.txt:26"},
]


def append_once(path: Path, marker: str, content: str) -> None:
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
        "scope": "第四十七批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "依据中册 part02 PaddleOCR 分页文本修复商业、粮食储运、财政和金融段金额单位残留。",
        "deferred": ["蔬菜销售额70多方元：未在 PaddleOCR 分页文本中取得万元闭合证据。", "物资流通10029/1541方元：OCR 数字表与正文单位未闭合，继续待核。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十七批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：依据中册 part02 PaddleOCR 分页文本修复商业、粮食储运、财政和金融段金额单位残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：蔬菜销售额、物资流通资金等未取得完整闭合证据的 `方元` 残留。",
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

    marker = "## 2026-07-04 第四十七批正文残留回源修复"
    memory = f"""
{marker}
- 依据中册 part02 PaddleOCR 分页文本，修复商业、粮食储运、财政和金融段 `方元` 金额单位残留，共 {total} 处。
- 同步目标：`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`；最终阅读版未命中这些旧串。
- 暂缓蔬菜销售额、物资流通资金等未取得完整闭合证据的残留，继续待核。
- 报告：`output/reports/reader_readability_source_backed_batch47_20260704.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
