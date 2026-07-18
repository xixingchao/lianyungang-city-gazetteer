# -*- coding: utf-8 -*-
"""Split compressed CPPCC committee subheads after appendix 42-16."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_cppcc_committee_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_cppcc_committee_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_市政协后续委员会小节标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>五、咨询服务委员会1984年7月4日，": "<h4>五、咨询服务委员会</h4>\n<p>1984年7月4日，",
    "<p>六、祖国统一一联谊、对外联络委员会1985年6月29日，": "<h4>六、祖国统一一联谊、对外联络委员会</h4>\n<p>1985年6月29日，",
    "<p>七、文教卫体委员会1989年七届二次全会后": "<h4>七、文教卫体委员会</h4>\n<p>1989年七届二次全会后",
    "<p>八、社会法制委员会1989年6月28日，": "<h4>八、社会法制委员会</h4>\n<p>1989年6月28日，",
}
RESIDUALS = [
    "<p>五、咨询服务委员会1984年7月4日，",
    "<p>六、祖国统一一联谊、对外联络委员会1985年6月29日，",
    "<p>七、文教卫体委员会1989年七届二次全会后",
    "<p>八、社会法制委员会1989年6月28日，",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {old!r}, got {count}")
        text = text.replace(old, new, 1)
        changed += 1
    for residue in RESIDUALS:
        if residue in text:
            raise RuntimeError(f"compressed subhead residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十二卷政务：市政协后续委员会小节标题",
        "html_subheads_split": changed,
        "source_evidence": ["workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:34503-34532"],
        "notes": ["仅拆分最终 HTML 中源文独立成行的小节标题，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 市政协后续委员会小节标题版式修复

- 时间：{now}
- 范围：第四十二卷政务，第十二章第八节，附42-16 后续小节。
- 本次拆分标题：{changed} 处。

## 修复

- 将 `五、咨询服务委员会`、`六、祖国统一一联谊、对外联络委员会`、`七、文教卫体委员会`、`八、社会法制委员会` 从正文段首拆为小节标题。
- 仅恢复标题边界，不改正文文字。

## 依据

- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:34503-34532`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 市政协后续委员会小节标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十二卷政务第十二章第八节 `附42-16` 后续小节标题粘正文问题。
- 将 `五、咨询服务委员会`、`六、祖国统一一联谊、对外联络委员会`、`七、文教卫体委员会`、`八、社会法制委员会` 恢复为独立标题。
- 仅恢复标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_cppcc_committee_subheads_20260705.md`。
""",
    )
    print(f"html_subheads_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
