# -*- coding: utf-8 -*-
"""Forty-eighth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch48_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch48_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十八批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "民国水灾连云市赈款", "old": "连云市5千方元", "new": "连云市5千万元", "source": "workbench/ocr/paddle_ocr/下/part01/page_0028.txt:23"},
    {"label": "扶贫资金救灾款", "old": "救灾款33.66方元", "new": "救灾款33.66万元", "source": "workbench/ocr/paddle_ocr/下/part01/page_0034.txt:11"},
    {"label": "扶贫资金救济款和低息农贷款", "old": "救济款13.21\n方元。地方财政款32.44万元，低息农贷款121.77方元", "new": "救济款13.21\n万元。地方财政款32.44万元，低息农贷款121.77万元", "source": "workbench/ocr/paddle_ocr/下/part01/page_0034.txt:15-16"},
    {"label": "福利募捐留用资金", "old": "留用96方元", "new": "留用96万元", "source": "workbench/ocr/paddle_ocr/下/part01/page_0040.txt:7"},
    {"label": "殡仪馆火化炉房造价", "old": "总造价3方元", "new": "总造价3万元", "source": "workbench/ocr/paddle_ocr/下/part01/page_0053.txt:28"},
    {"label": "劳动服务公司无息贷款", "old": "无息贷款424方元", "new": "无息贷款424万元", "source": "workbench/ocr/paddle_ocr/下/part01/page_0242.txt:11"},
    {"label": "劳动保护重点项目投资", "old": "投资153.9方元", "new": "投资153.9万元", "source": "workbench/ocr/paddle_ocr/下/part01/page_0278.txt:19"},
    {"label": "侨务捐赠金额及币种", "old": "折合人民币400多方元，其中轿车、面包车12辆，香港同胞费培捐款10方\n港市在其家乡学校建一“培秀楼”；美籍华人夏浩原捐赠给灌云陡沟中学3万元人民市", "new": "折合人民币400多万元，其中轿车、面包车12辆，香港同胞费培捐款10万\n港币在其家乡学校建一“培秀楼”；美籍华人夏浩原捐赠给灌云陡沟中学3万元人民币", "source": "workbench/ocr/paddle_ocr/下/part01/page_0302.txt:20-21"},
    {"label": "共保合同集体福利资金", "old": "资金达7219方元", "new": "资金达7219万元", "source": "workbench/ocr/paddle_ocr/下/part01/page_0315.txt:18"},
    {"label": "科技三项经费表单位", "old": "1978~1990年连云港市科技三项经费一览表\n表 51 - 6\n单位：方元", "new": "1978~1990年连云港市科技三项经费一览表\n表 51 - 6\n单位：万元", "source": "workbench/ocr/paddle_ocr/下/part01/page_0427.txt:22-24"},
    {"label": "东海县文化馆收入", "old": "年均收人约3.5方元", "new": "年均收入约3.5万元", "source": "workbench/ocr/paddle_ocr/下/part02/page_0048.txt:5"},
    {"label": "东海县文化馆收入", "old": "年均收入约3.5方元", "new": "年均收入约3.5万元", "source": "workbench/ocr/paddle_ocr/下/part02/page_0048.txt:5"},
    {"label": "缪秋杰盐补贴款", "old": "49方元盐补贴款", "new": "49万元盐补贴款", "source": "workbench/ocr/paddle_ocr/下/part02/page_0353.txt:30"},
    {"label": "对外开放市里集资", "old": "市里集资七千方元", "new": "市里集资七千万元", "source": "workbench/ocr/paddle_ocr/下/part02/page_0424.txt:11"},
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
        "scope": "第四十八批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "依据下册 part01/part02 PaddleOCR 分页文本修复民政、劳动、侨务、科技、文化和附录段金额单位残留。",
        "deferred": ["旧人民市/银元语境、物资流通资金、商业蔬菜销售额等仍继续待核。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十八批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：依据下册 part01/part02 PaddleOCR 分页文本修复民政、劳动、侨务、科技、文化和附录段金额单位残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：旧人民市/银元语境、物资流通资金、商业蔬菜销售额等仍继续待核。",
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

    marker = "## 2026-07-04 第四十八批正文残留回源修复"
    memory = f"""
{marker}
- 依据下册 part01/part02 PaddleOCR 分页文本，修复民政、劳动、侨务、科技、文化和附录段 `方元` 金额单位残留及同源行相邻币种错字，共 {total} 处。
- 同步目标：`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md`、`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`；最终阅读版未命中这些旧串。
- 暂缓旧人民市/银元语境、物资流通资金、商业蔬菜销售额等未完整闭合项。
- 报告：`output/reports/reader_readability_source_backed_batch48_20260704.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
