# -*- coding: utf-8 -*-
"""Forty-fifth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch45_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch45_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十五批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "首饰玩具销售收入", "old": "入608.72方元", "new": "入608.72万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0029.txt:13"},
    {"label": "刺绣厂电脑绣花机购置", "old": "用7.3方元从苏州购置", "new": "用7.3万元从苏州购置", "source": "workbench/ocr/paddle_ocr/中/part01/page_0042.txt:35"},
    {"label": "刺绣厂利税总额", "old": "利税总额14.16方元", "new": "利税总额14.16万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0042.txt:36"},
    {"label": "糕点加工产值", "old": "完成产值39.3方元", "new": "完成产值39.3万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0064.txt:11"},
    {"label": "糖果企业产值", "old": "产值103方元", "new": "产值103万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0068.txt:7"},
    {"label": "灌云县食品公司产值", "old": "产值807方元", "new": "产值807万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0071.txt:20"},
    {"label": "肉类加工厂产值", "old": "当年产值5222方元", "new": "当年产值5222万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0074.txt:6"},
    {"label": "肉类罐头产值", "old": "产值2050.9方元", "new": "产值2050.9万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0077.txt:21"},
    {"label": "赣榆县啤酒厂投资", "old": "投资295方元新建", "new": "投资295万元新建", "source": "workbench/ocr/paddle_ocr/中/part01/page_0087.txt:26"},
    {"label": "果酒企业利税", "old": "利税172方元", "new": "利税172万元", "source": "workbench/ocr/merged/连云港市志_中_part01_OCR汇总.md:6772"},
    {"label": "酶制剂调味品利税", "old": "利税365方元", "new": "利税365万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0104.txt:7"},
    {"label": "江苏化肥厂投资", "old": "投资6341方元", "new": "投资6341万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0165.txt:13"},
    {"label": "机械工业总产值", "old": "工业总产值13650方元", "new": "工业总产值13650万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0194.txt:14"},
    {"label": "灌云县水泥厂投资", "old": "投资425方元", "new": "投资425万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0280.txt:25"},
    {"label": "住宅区工程投资", "old": "总投资9000方元", "new": "总投资9000万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0298.txt:30"},
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
        "scope": "第四十五批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "依据中册 part01 PaddleOCR 分页文本修复工艺美术、食品、化工、机械、建材和建筑业金额单位残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十五批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：依据中册 part01 PaddleOCR 分页文本修复工艺美术、食品、化工、机械、建材和建筑业金额单位残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
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

    marker = "## 2026-07-04 第四十五批正文残留回源修复"
    memory = f"""
{marker}
- 依据中册 part01 PaddleOCR 分页文本，修复工艺美术、食品、化工、机械、建材和建筑业段 `方元` 金额单位残留，共 {total} 处。
- 同步目标：`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`；最终阅读版未命中这些旧串。
- 未处理 `投资40多方元` 等普通 OCR 仍不充分或尚未定位到 PaddleOCR 明确证据的项目。
- 报告：`output/reports/reader_readability_source_backed_batch45_20260704.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
