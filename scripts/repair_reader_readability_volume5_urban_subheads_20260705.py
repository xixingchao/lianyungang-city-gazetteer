# -*- coding: utf-8 -*-
"""Repair source-backed small heading boundaries in volume 5."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume5_urban_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume5_urban_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第五卷城乡建设小标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/连云港市志_上册_正文汇总.md"

REPAIRS = [
    {
        "label": "一、下水道",
        "source": f"{SOURCE}:17384",
        "old": "<p>一、下水道明洪武二十四年（1391年），在海州城西北角新建水西门，专供城内排水用。</p>",
        "new": "<h5>一、下水道</h5>\n<p>明洪武二十四年（1391年），在海州城西北角新建水西门，专供城内排水用。</p>",
    },
    {
        "label": "三、河道整治",
        "source": f"{SOURCE}:17829",
        "old": "<p>三、河道整治清康熙四十二年（1703年），海州通判申崇厚在海州西南12.5公里的托山庙建坝，借山水冲激法以防蔷薇河淤塞。清嘉庆九年（1804年），海州知州唐仲冕组织开掘东自新浦口、西抵海州城东门的甲子河。</p>",
        "new": "<h5>三、河道整治</h5>\n<p>清康熙四十二年（1703年），海州通判申崇厚在海州西南12.5公里的托山庙建坝，借山水冲激法以防蔷薇河淤塞。清嘉庆九年（1804年），海州知州唐仲冕组织开掘东自新浦口、西抵海州城东门的甲子河。</p>",
    },
    {
        "label": "一、设置",
        "source": f"{SOURCE}:18201",
        "old": "<p>一、设置20世纪20年代，新浦、海州、墟沟、老窑和猴嘴先后出现接柱形玻璃油灯路灯，共30馀盏。",
        "new": "<h5>一、设置</h5>\n<p>20世纪20年代，新浦、海州、墟沟、老窑和猴嘴先后出现接柱形玻璃油灯路灯，共30馀盏。",
    },
    {
        "label": "二、光源",
        "source": f"{SOURCE}:18249",
        "old": "<p>二、光源20世纪20年代，新浦等地主要采用接柱形玻璃油灯作道路照明。20年代末，新浦开始安装白炽灯路灯。从40年代初起，城区普遍采用白炽灯作道路照明。</p>",
        "new": "<h5>二、光源</h5>\n<p>20世纪20年代，新浦等地主要采用接柱形玻璃油灯作道路照明。20年代末，新浦开始安装白炽灯路灯。从40年代初起，城区普遍采用白炽灯作道路照明。</p>",
    },
    {
        "label": "一、客运畜力车",
        "source": f"{SOURCE}:18482",
        "old": "<p>一、客运畜力车清末民初，东海和灌云城乡主要以土驴车（即独轮车）和客运毛驴作为交通工具。",
        "new": "<h5>一、客运畜力车</h5>\n<p>清末民初，东海和灌云城乡主要以土驴车（即独轮车）和客运毛驴作为交通工具。",
    },
    {
        "label": "二、客运人力车",
        "source": f"{SOURCE}:18487",
        "old": "<p>二、客运人力车民国9年（1920年），胶轮黄包车成为当地最主要的客运工具。",
        "new": "<h5>二、客运人力车</h5>\n<p>民国9年（1920年），胶轮黄包车成为当地最主要的客运工具。",
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
        "scope": "第五卷城乡建设：市政建设、公用事业小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["只将源文独立小标题拆为 h5，不改正文。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五卷城乡建设小标题边界补修

- 时间：{now}
- 范围：第五卷城乡建设，第二章市政建设、第三章公用事业。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['label']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的小标题边界，不改正文内容。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第五卷城乡建设小标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第五卷城乡建设 6 处段首小标题粘正文：`一、下水道`、`三、河道整治`、`一、设置`、`二、光源`、`一、客运畜力车`、`二、客运人力车`。
- 依据 `{SOURCE}` 中对应独立标题行或前段后置标题边界；只拆 h5，不改正文。
- 报告：`output/reports/reader_readability_volume5_urban_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
