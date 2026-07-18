# -*- coding: utf-8 -*-
"""Thirty-ninth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch39_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch39_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十九批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "工商检查挽回损失", "old": "挽回经济损失13.11方元", "new": "挽回经济损失13.11万元", "source": "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:12335；同锚 LYG-S-0500"},
    {"label": "工商万元以上案件", "old": "其中方元以上案件10起", "new": "其中万元以上案件10起", "source": "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:12338；同锚 LYG-S-0500"},
    {"label": "沂北除涝东门河投资", "old": "投资108.6方元，大东门河", "new": "投资108.6万元，大浚东门河", "source": "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:17978；同锚 LYG-S-0590"},
    {"label": "蔷薇河复堤投资", "old": "投资54.92方元，完成土方", "new": "投资54.92万元，完成土方", "source": "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:18324；同锚 LYG-S-0594"},
    {"label": "洪门桥东堤投资", "old": "投资125方元，完成土方35万立方来", "new": "投资125万元，完成土方35万立方米", "source": "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:18347；同锚 LYG-S-0595"},
    {"label": "淡水捕捞队网具", "old": "用3方元购置网具", "new": "用3万元购置网具", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:7733；同锚 LYG-S-0732"},
    {"label": "造纸企业固定资产", "old": "固定资产原值3780方元", "new": "固定资产原值3780万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:10706；同锚 LYG-S-0781"},
    {"label": "造纸企业利税", "old": "实现利税7.1方元", "new": "实现利税7.1万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:10852；同锚 LYG-S-0784"},
    {"label": "树脂工业产值", "old": "完成工业产值229方元", "new": "完成工业产值229万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:15102；同锚 LYG-S-0891"},
    {"label": "塑料十二厂投资", "old": "市塑料十二广投资30方元", "new": "市塑料十二厂投资30万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:15241；同锚 LYG-S-0892"},
    {"label": "东方拉链厂投资", "old": "东方拉链厂，投资351方元", "new": "东方拉链厂，投资351万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:15863；同锚 LYG-S-0894"},
    {"label": "塑料四厂历史产值利税", "old": "历史最高产值为1988年的1207.2方元，利税220方元", "new": "历史最高产值为1988年的1207.2万元，利税220万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:15959；同锚 LYG-S-0897"},
    {"label": "塑料八厂设备投资", "old": "企业先后共投资475方元", "new": "企业先后共投资475万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:16037；同锚 LYG-S-0898"},
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
        "scope": "第三十九批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "按同锚 PaddleOCR 正文核对，只修可定位的上册金额残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三十九批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：按同锚 PaddleOCR 正文核对，只修可定位的上册金额残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：raw OCR 本身仍为 `方元` 且无同锚 PaddleOCR 正文佐证的其它残留。",
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

    marker = "## 2026-07-04 第三十九批正文残留回源修复"
    memory = f"""
{marker}
- 修复同锚 PaddleOCR 正文直接证明的上册金额 `方元` 残留，共 {total} 处。
- 同步目标：`output/final_reader/连云港市志_全书.html`、`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/连云港市志_上册_正文汇总.md`、`workbench/body_chapters/上/第四卷至第十卷（part02）.md`、`workbench/body_chapters/上/第十卷至第十六卷（part03）.md`。
- 证据锚：`workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 的 LYG-S-0500、0590、0594、0595，及 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 的 LYG-S-0732、0781、0784、0891、0892、0894、0897、0898。
- 暂缓 raw OCR 本身仍为 `方元` 且无同锚 PaddleOCR 正文佐证的其它残留。
- 报告：`output/reports/reader_readability_source_backed_batch39_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
