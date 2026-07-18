# -*- coding: utf-8 -*-
"""Thirty-seventh source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch37_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch37_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十七批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "制药厂生产车间与厂区面积缺文", "old": "内设9个职能部门、2个化验室、7平方来，固定资产原值1111.58万元。", "new": "内设9个职能部门、2个化验室、7个生产车间、1个药物研究所。全厂分生产、生活两个区，占地7万平方米，建筑面积2万平方米，固定资产原值1111.58万元。", "source": "workbench/ocr/paddle_ocr/中/part01/page_0128.txt:29-31"},
    {"label": "开发区供水用水标准", "old": "12升/平方来·日", "new": "12升/平方米·日", "source": "workbench/ocr/paddle_ocr/中/part01/page_0429.txt:19-23"},
    {"label": "开发区土地费用单位", "old": "每平方来12元", "new": "每平方米12元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0429.txt:23"},
    {"label": "消防审核工业建筑面积", "old": "建筑面积482.61方平方米", "new": "建筑面积482.61万平方米", "source": "workbench/ocr/paddle_ocr/下/part01/page_0093.txt:20"},
    {"label": "东方影视中心总建筑面积", "old": "总建筑面积2平方来", "new": "总建筑面积2万平方米", "source": "workbench/ocr/paddle_ocr/下/part01/page_0448.txt:19"},
    {"label": "抗震加固建筑面积", "old": "加固建筑物122.1方平方米", "new": "加固建筑物122.1万平方米", "source": "workbench/ocr/paddle_ocr/下/part01/page_0456.txt:40"},
    {"label": "大村遗址面积", "old": "面积约2方平方米", "new": "面积约2万平方米", "source": "workbench/ocr/paddle_ocr/下/part02/page_0077.txt:28"},
    {"label": "市场面积单位", "old": "市场面积111方平方米", "new": "市场面积111万平方米", "source": "workbench/ocr/paddle_ocr/上/part02/page_0198.txt:13"},
    {"label": "鱼种池面积单位", "old": "由224平方米增至392平方来", "new": "由224平方米增至392平方米", "source": "workbench/ocr/paddle_ocr/上/part03/page_0124.txt:13"},
    {"label": "化纤厂扩建厂房面积", "old": "扩建厂房14.5方平方米", "new": "扩建厂房14.5万平方米", "source": "workbench/ocr/paddle_ocr/上/part03/page_0227.txt:34"},
    {"label": "纺织厂占地面积", "old": "占地面积0.8方平方米", "new": "占地面积0.8万平方米", "source": "workbench/ocr/paddle_ocr/上/part03/page_0241.txt:20"},
    {"label": "人造革产量单位", "old": "生产人造革2方平方米", "new": "生产人造革2万平方米", "source": "workbench/ocr/paddle_ocr/上/part03/page_0287.txt:6"},
    {"label": "贝雕厂购地面积", "old": "购地1方平方米", "new": "购地1万平方米", "source": "workbench/ocr/paddle_ocr/中/part01/page_0024.txt:23"},
    {"label": "襄河乳品厂占地面积", "old": "襄河乳品厂，占地面积2方平方米", "new": "襄河乳品厂，占地面积2万平方米", "source": "workbench/ocr/paddle_ocr/中/part01/page_0067.txt:8"},
    {"label": "肉类加工建筑面积断行残留", "old": "积10.7方平方米，固定资产原值6863万元。", "new": "积10.7万平方米，固定资产原值6863万元。", "source": "workbench/ocr/paddle_ocr/中/part01/page_0070.txt:13-14"},
    {"label": "食品公司建筑面积", "old": "建筑面积3.46方平方米", "new": "建筑面积3.46万平方米", "source": "workbench/ocr/paddle_ocr/中/part01/page_0073.txt:29"},
    {"label": "食品公司建筑面积断行残留", "old": "建筑面积5.05方平方米", "new": "建筑面积5.05万平方米", "source": "workbench/ocr/paddle_ocr/中/part01/page_0076.txt:11"},
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
    payload = {"time": now, "scope": "第三十七批正文残留回源修复", "targets": targets, "total_replacements": total, "verified_items": len(REPLACEMENTS), "principle": "只修页级 Paddle OCR 直接证明的平方米/万平方米残留及一处制药厂缺文。"}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# 第三十七批正文残留回源修复", "", f"- 时间：{now}", "- 原则：只修页级 Paddle OCR 直接证明的平方米/万平方米残留及一处制药厂缺文。", f"- 核验项：{len(REPLACEMENTS)} 项。", f"- 本次替换：{total} 处。", "- 暂缓：金额类 `方元`、水利 `方立方米/方亩`、源证不足的 `台湾丰盈木方平方来`。", "", "## 文件"]
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

    marker = "## 2026-07-04 第三十七批正文残留回源修复"
    memory = f"""
{marker}
- 修复页级 Paddle OCR 直接证明的平方米/万平方米残留及一处制药厂缺文，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/中/part01/page_0024.txt`、`page_0067.txt`、`page_0070.txt`、`page_0073.txt`、`page_0076.txt`、`page_0128.txt`、`page_0429.txt`，`workbench/ocr/paddle_ocr/下/part01/page_0093.txt`、`page_0448.txt`、`page_0456.txt`，`workbench/ocr/paddle_ocr/下/part02/page_0077.txt`，`workbench/ocr/paddle_ocr/上/part02/page_0198.txt`，`workbench/ocr/paddle_ocr/上/part03/page_0124.txt`、`page_0227.txt`、`page_0241.txt`、`page_0287.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓金额类 `方元`、水利 `方立方米/方亩`、源证不足的 `台湾丰盈木方平方来`。
- 报告：`output/reports/reader_readability_source_backed_batch37_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
