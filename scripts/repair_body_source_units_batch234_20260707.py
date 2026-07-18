# -*- coding: utf-8 -*-
"""Repair source-backed body source unit residues, batch 234."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "body_source_units_batch234_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "body_source_units_batch234_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_正文源稿单位残留补修第二百三十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
ITEMS = [
    {
        "old": "生猪饲养量降至186.16方头",
        "new": "生猪饲养量降至186.16万头",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0074.txt",
        "snippet": "生猪饲养量降至186.16万头",
    },
    {
        "old": "加工白条肉1.74方吨",
        "new": "加工白条肉1.74万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0071.txt",
        "snippet": "加工白条肉1.74万吨、分割肉1348吨",
    },
    {
        "old": "年宰量36方头生猪",
        "new": "年宰量36万头生猪",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0073.txt",
        "snippet": "年宰量36万头生猪",
    },
    {
        "old": "暂不能利用储量905方吨",
        "new": "暂不能利用储量905万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0442.txt",
        "snippet": "暂不能利用储量905万吨",
    },
    {
        "old": "地质储量药17方吨",
        "new": "地质储量约17万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0442.txt",
        "snippet": "求得水晶矿地质储量约17万吨",
    },
    {
        "old": "探明矿工业储量2253方吨",
        "new": "探明矿工业储量2253万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0443.txt",
        "snippet": "探明矿工业储量2253万吨",
    },
    {
        "old": "探明矿石工业储量1076方吨",
        "new": "探明矿石工业储量1076万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0443.txt",
        "snippet": "探明矿石工业储量1076万吨",
    },
    {
        "old": "下层远景储量83方吨",
        "new": "下层远景储量83万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0443.txt",
        "snippet": "下层远景储量83万吨",
    },
    {
        "old": "日供水能力达9方吨",
        "new": "日供水能力达9万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0454.txt",
        "snippet": "日供水能力达9万吨",
    },
]


def ensure_evidence() -> None:
    for item in ITEMS:
        text = item["evidence"].read_text(encoding="utf-8", errors="ignore")
        if item["snippet"] not in text:
            raise SystemExit(f"missing evidence: {item['evidence'].relative_to(ROOT)}: {item['snippet']}")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        file_items = []
        for item in ITEMS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
                file_items.append({
                    "old": item["old"],
                    "new": item["new"],
                    "count": count,
                    "evidence": str(item["evidence"].relative_to(ROOT)),
                })
        if file_items:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "items": file_items})

    residuals = {
        item["old"]: {
            str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(item["old"])
            for path in TARGETS
        }
        for item in ITEMS
    }
    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文源稿单位残留补修第二百三十四批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复上册畜牧、中册食品、下册科技地矿/城建中已由页级 PaddleOCR 证实的单位残留。",
        "- 当前正式阅读稿对应位置多已正确，本批重点补正常命名正文源稿和全书汇总。",
        "- 未处理旧交付包、obsolete 或乱码文件名副本；未做全局替换，未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["items"]:
            lines.append(
                f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['evidence']}` |"
            )
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 正文源稿单位残留补修第二百三十四批\n\n"
    memory += "- 依据页级 PaddleOCR，修复源稿 `186.16方头/1.74方吨/36方头/905方吨/药17方吨/2253方吨/1076方吨/83方吨/9方吨` 等单位残留。\n"
    memory += "- 同步范围：正常命名的上册、下册正文源稿及全书正文汇总；报告：`output/reports/body_source_units_batch234_20260707.md`。\n"
    memory += "- 未处理旧交付包、obsolete 或乱码文件名副本；未做全局替换，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
