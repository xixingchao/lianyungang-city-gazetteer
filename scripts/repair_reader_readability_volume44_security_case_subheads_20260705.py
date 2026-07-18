# -*- coding: utf-8 -*-
"""Repair source-backed volume 44 security/case small heading boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume44_security_case_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume44_security_case_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十四卷治安案件小标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

REPAIRS = [
    {
        "label": "一、经济保卫",
        "source": f"{SOURCE}:3377",
        "old": "<p>一、经济保卫安全防范1951年初，新海连市公安局对市区各单位布置春节安全保卫工作。",
        "new": "<h5>一、经济保卫</h5>\n<p>安全防范1951年初，新海连市公安局对市区各单位布置春节安全保卫工作。",
    },
    {
        "label": "二、文化保卫",
        "source": f"{SOURCE}:3434",
        "old": "<p>二、文化保卫文物古迹保卫1980年，市公安局、市文化局配合市博物馆建立馆藏文物档案，",
        "new": "<h5>二、文化保卫</h5>\n<p>文物古迹保卫1980年，市公安局、市文化局配合市博物馆建立馆藏文物档案，",
    },
    {
        "label": "一、杀人案件",
        "source": f"{SOURCE}:3492",
        "old": "<p>一、杀人案件1955年10月12日晚8时15分，新海连市盐河区同和街反革命分子殷某，",
        "new": "<h5>一、杀人案件</h5>\n<p>1955年10月12日晚8时15分，新海连市盐河区同和街反革命分子殷某，",
    },
    {
        "label": "二、抢劫案件",
        "source": f"{SOURCE}:3517",
        "old": "<p>二、抢劫案件民国38年（1949年）春，东海县公安局破获一起抢劫案。",
        "new": "<h5>二、抢劫案件</h5>\n<p>民国38年（1949年）春，东海县公安局破获一起抢劫案。",
    },
    {
        "label": "三、爆炸案件",
        "source": f"{SOURCE}:3540",
        "old": "<p>三、爆炸案件1980年，全市发生爆炸案件2起，破2起，其中重大案件发1起，破1起。",
        "new": "<h5>三、爆炸案件</h5>\n<p>1980年，全市发生爆炸案件2起，破2起，其中重大案件发1起，破1起。",
    },
    {
        "label": "四、强奸案件",
        "source": f"{SOURCE}:3547",
        "old": "<p>四、强奸案件1954年至1963年上半年，市区共发生强奸案件42起，破获42起，",
        "new": "<h5>四、强奸案件</h5>\n<p>1954年至1963年上半年，市区共发生强奸案件42起，破获42起，",
    },
    {
        "label": "五、流氓案件",
        "source": f"{SOURCE}:3560",
        "old": "<p>五、流氓案件1957年，新海连市发生流氓案件8起，破8起。",
        "new": "<h5>五、流氓案件</h5>\n<p>1957年，新海连市发生流氓案件8起，破8起。",
    },
    {
        "label": "六、盗窃案件",
        "source": f"{SOURCE}:3584",
        "old": "<p>六、盗窃案件1950年3月至4月初，新浦等地电线被割、盗30余档，",
        "new": "<h5>六、盗窃案件</h5>\n<p>1950年3月至4月初，新浦等地电线被割、盗30余档，",
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
        "scope": "第四十四卷治安：经济文化保卫、刑事案件侦破小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": [
            "只恢复源文独立行可证明的小标题边界，不改正文/OCR文字。",
            "安全防范、要害保卫、文物古迹保卫等细分标签本轮暂不提升为标题。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十四卷治安案件小标题边界补修

- 时间：{now}
- 范围：第四十四卷治安，经济文化保卫、刑事案件侦破。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['label']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的小标题边界，不改正文内容。\n- 细分标签未在本轮处理，避免把段首术语误升为标题。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十四卷治安案件小标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十四卷治安 8 处小标题粘正文：`一、经济保卫`、`二、文化保卫`、刑事案件侦破下 `一、杀人案件` 至 `六、盗窃案件`。
- 依据 `{SOURCE}:3377`、`:3434`、`:3492-3584` 的独立标题行；只拆 h5，不改正文/OCR文字。
- 暂缓 `安全防范`、`要害保卫`、`文物古迹保卫` 等段首标签，待更强标题层级证据。
- 报告：`output/reports/reader_readability_volume44_security_case_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
