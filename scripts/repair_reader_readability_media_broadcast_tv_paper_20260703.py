# -*- coding: utf-8 -*-
"""Restore Lianyungang Radio and TV News entry from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_media_broadcast_tv_paper_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_media_broadcast_tv_paper_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷连云港广播电视报回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0139.txt:13-19"
SCOPE_START = '<p>十三、连云港广播电视报1988年7月20日创刊，连云港市广播电视局主办。江苏省内部报刊准印证号为（JS）</p>'
STABLE_SCOPE_START = '<p>十三、连云港广播电视报</p>'
SCOPE_END = '<h3 id="第五十四卷-第二章刊物">第二章刊物</h3>'

NEW_HTML = """<p>十三、连云港广播电视报</p>
<p>1988年7月20日创刊，连云港市广播电视局主办。江苏省内部报刊准印证号为（JS）第2272号。负责人赵育堂。周报，四开四版，铅印，每期印15万份，曾在连云港报社印刷厂印刷，后在铜山报社印刷厂印刷。报社地址在新浦解放西路6号。</p>
<p>《连云港广播电视报》介绍连云港市电视台、广播电台的一周节目，以及主要文艺节目及剧情。辟有“影剧评论”、“影视评论”、“专题采访”、“视听花絮”、“影视名人行踪”等栏目。</p>



"""

EXPECTED_TEXT = [
    "<p>十三、连云港广播电视报</p>",
    "江苏省内部报刊准印证号为（JS）第2272号",
    "“影视评论”、“专题采访”",
]
RESIDUALS = [
    "十三、连云港广播电视报1988年7月20日",
    "准印证号为（JS）</p>",
    "<p>第2272号。负责人赵育堂。",
    "“影视评论”“专题采访”",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.find(STABLE_SCOPE_START)
    if start < 0:
        start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    changed = int(text[start:end] != NEW_HTML)
    if changed:
        HTML.write_text(text[:start] + NEW_HTML + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return changed, {"rewrote_scope": changed, "entries_restored": 1}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第一章报纸 / 第二节行(专)业报纸 / 十三、连云港广播电视报",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建连云港广播电视报条目，停止在第二章刊物前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷连云港广播电视报回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第一章报纸 / 第二节行(专)业报纸 / 十三、连云港广播电视报`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `十三、连云港广播电视报`，停止在 `第二章刊物` 前。
- 拆开条目题名与正文粘连，合并被拆断的准印证号 `（JS）第2272号`。
- 修正栏目之间漏顿号的 `“影视评论”、“专题采访”`。
- 当前核验复跑整段替换：{changed} 处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷连云港广播电视报回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第一章报纸 / 第二节行(专)业报纸 / 十三、连云港广播电视报` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第二章刊物` 前。
- 修正题名粘连、准印证号断行和栏目顿号漏失等问题。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_media_broadcast_tv_paper_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
