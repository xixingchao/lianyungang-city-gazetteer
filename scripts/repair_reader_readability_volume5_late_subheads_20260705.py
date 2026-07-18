# -*- coding: utf-8 -*-
"""Repair source-backed late volume 5 small heading boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume5_late_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume5_late_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第五卷后段小标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/连云港市志_上册_正文汇总.md"

REPAIRS = [
    {
        "label": "三、处理利用（粪便管理）",
        "source": f"{SOURCE}:18748",
        "old": "<p>三、处理利用20世纪40年代初期，新浦粪便大都送到铁路南的大粪场堆放、晒干，销往农村。",
        "new": "<h5>三、处理利用</h5>\n<p>20世纪40年代初期，新浦粪便大都送到铁路南的大粪场堆放、晒干，销往农村。",
    },
    {
        "label": "五、抗日山烈士陵园",
        "source": f"{SOURCE}:18837",
        "old": "<p>五、抗日山烈士陵园抗日山原名马鞍山，位于赣榆县城西部夹谷山南。",
        "new": "<h5>五、抗日山烈士陵园</h5>\n<p>抗日山原名马鞍山，位于赣榆县城西部夹谷山南。",
    },
    {
        "label": "六、东海温泉",
        "source": f"{SOURCE}:18843",
        "old": "<p>六、东海温泉位于东海县西北部，又称羽山温泉。",
        "new": "<h5>六、东海温泉</h5>\n<p>位于东海县西北部，又称羽山温泉。",
    },
    {
        "label": "三、猴嘴公园",
        "source": f"{SOURCE}:18863",
        "old": "<p>三、猴嘴公园该公园于1980年底建成，占地720亩。",
        "new": "<h5>三、猴嘴公园</h5>\n<p>该公园于1980年底建成，占地720亩。",
    },
    {
        "label": "三、道路绿化",
        "source": f"{SOURCE}:18892",
        "old": "<p>三、道路绿化解放路绿化 解放路是市区主要繁华道路之一，东西向，全长3900米。",
        "new": "<h5>三、道路绿化</h5>\n<p>解放路绿化 解放路是市区主要繁华道路之一，东西向，全长3900米。",
    },
    {
        "label": "五、生产绿地",
        "source": f"{SOURCE}:18940",
        "old": "<p>五、生产绿地建国初期，本市没有育苗基地。",
        "new": "<h5>五、生产绿地</h5>\n<p>建国初期，本市没有育苗基地。",
    },
    {
        "label": "一、产籍管理",
        "source": f"{SOURCE}:18964",
        "old": "<p>一、产籍管理地籍管理建国前称为地籍整理。",
        "new": "<h5>一、产籍管理</h5>\n<p>地籍管理建国前称为地籍整理。",
    },
    {
        "label": "二、产权管理",
        "source": f"{SOURCE}:19125",
        "old": "<p>二、产权管理产权接管、变更 民国35年（1946年）3月23日，国民政府东海县成立东海县房产评价委员会。",
        "new": "<h5>二、产权管理</h5>\n<p>产权接管、变更 民国35年（1946年）3月23日，国民政府东海县成立东海县房产评价委员会。",
    },
    {
        "label": "一、建房",
        "source": f"{SOURCE}:19182",
        "old": "<p>一、建房新石器时代有原始居房。",
        "new": "<h5>一、建房</h5>\n<p>新石器时代有原始居房。",
    },
    {
        "label": "三、交易",
        "source": f"{SOURCE}:193? / {SOURCE}:5968(paddle)",
        "old": "<p>三、交易房屋交易 20世纪40年代，房屋交易极少。",
        "new": "<h5>三、交易</h5>\n<p>房屋交易 20世纪40年代，房屋交易极少。",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed: list[dict[str, str]] = []
    for item in REPAIRS:
        count = text.count(item["old"])
        if count != 1:
            raise RuntimeError(f"expected one match for {item['label']}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"label": item["label"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五卷城乡建设后段：环境卫生、园林建设、房产小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["只恢复源文可证明的小标题边界，不改正文；不重建表格。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五卷后段小标题边界补修

- 时间：{now}
- 范围：第五卷城乡建设后段，环境卫生、园林建设、房产。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['label']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的小标题边界，不改正文内容。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第五卷后段小标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第五卷后段 10 处小标题粘正文：环境卫生 `三、处理利用`，园林建设 `五、抗日山烈士陵园`、`六、东海温泉`、`三、猴嘴公园`、`三、道路绿化`、`五、生产绿地`，房产 `一、产籍管理`、`二、产权管理`、`一、建房`、`三、交易`。
- 依据 `{SOURCE}` 与 `workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 对应独立标题行；只拆 h5，不改正文。
- 报告：`output/reports/reader_readability_volume5_late_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
