# -*- coding: utf-8 -*-
"""Fortieth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第一卷_自然环境.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷_人口（part01_部分）.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch40_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch40_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "大事记财政支出", "old": "财政支出347.5方元", "new": "财政支出347.5万元", "source": "workbench/body_chapters/paddle_上/总述与大事记.md:1629；同锚 LYG-S-0075"},
    {"label": "自然环境洪灾损失", "old": "直接经济损失3000多方元", "new": "直接经济损失3000多万元", "source": "workbench/ocr/paddle_ocr/上/part01/page_0206.txt:25；分章同锚 LYG-S-0206"},
    {"label": "东海县财政收入支出", "old": "税收入1359.2方元，其它收入8.4方元；财政支出1686.5方元", "new": "税收入1359.2万元，其它收入8.4万元；财政支出1686.5万元", "source": "workbench/body_chapters/paddle_上/第三卷_区县概况.md:1552；同锚 LYG-S-0275"},
    {"label": "人口服务站财政拨款", "old": "市财政拨款14方元", "new": "市财政拨款14万元", "source": "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:1938；同锚 LYG-S-0298"},
    {"label": "生态农业建设投入", "old": "投入12方元用于生态农业建设", "new": "投入12万元用于生态农业建设", "source": "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:7994；同锚 LYG-S-0424"},
    {"label": "文化用纸固定资产", "old": "固定资产原值2100方元", "new": "固定资产原值2100万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:10784；同锚 LYG-S-0782"},
    {"label": "造纸工业产值与创汇", "old": "完成工业产值180方元，出口创汇28方元", "new": "完成工业产值180万元，出口创汇28万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:10912；同锚 LYG-S-0785"},
    {"label": "报刊印刷利税", "old": "利税134.06方元", "new": "利税134.06万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:11076；同锚 LYG-S-0790"},
    {"label": "纸箱厂产值", "old": "当年产值16方元", "new": "当年产值16万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:11300；同锚 LYG-S-0794"},
    {"label": "轻工利税", "old": "成利税266方元", "new": "成利税266万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:11571；同锚 LYG-S-0799"},
    {"label": "木织机产值", "old": "值0.42方元", "new": "值0.42万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:13981；同锚 LYG-S-0856"},
    {"label": "毛巾产值", "old": "实现产值503方元", "new": "实现产值503万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:14146；同锚 LYG-S-0860"},
    {"label": "纺织厂利润", "old": "创利润3.9方元", "new": "创利润3.9万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:14194；同锚 LYG-S-0861"},
    {"label": "服装产值", "old": "实现产值5827方元", "new": "实现产值5827万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:14645；同锚 LYG-S-0871"},
    {"label": "化工产品利税", "old": "利税5.2方元", "new": "利税5.2万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:15501；同锚 LYG-S-0889"},
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
        "scope": "第四十批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "优先清理上册分章会回流的金额残留，依据同锚 PaddleOCR 正文或页级 OCR。",
        "deferred": ["第十卷至第十六卷 `方元在浦南农场筹建` 缺前置金额数字，暂缓。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：优先清理上册分章会回流的金额残留，依据同锚 PaddleOCR 正文或页级 OCR。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：第十卷至第十六卷 `方元在浦南农场筹建` 缺前置金额数字，暂缓。",
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

    marker = "## 2026-07-04 第四十批正文残留回源修复"
    memory = f"""
{marker}
- 修复上册分章会回流的金额 `方元` 残留，共 {total} 处，依据同锚 PaddleOCR 正文或页级 OCR。
- 同步目标：`output/final_reader/连云港市志_全书.html`、`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/连云港市志_上册_正文汇总.md` 及相关上册分章。
- 证据文件主要为 `workbench/body_chapters/paddle_上/总述与大事记.md`、`第三卷_区县概况.md`、`第四卷_人口（part01_部分）.md`、`第四卷至第十卷（part02）.md`、`第十卷至第十六卷（part03）.md`，另沿用 `workbench/ocr/paddle_ocr/上/part01/page_0206.txt`。
- 暂缓第十卷至第十六卷 `方元在浦南农场筹建`，因缺前置金额数字，不能只改单位。
- 报告：`output/reports/reader_readability_source_backed_batch40_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
