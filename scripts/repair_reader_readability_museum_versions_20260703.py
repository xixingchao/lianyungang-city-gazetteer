# -*- coding: utf-8 -*-
"""Restore museum version/document section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_versions_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_versions_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷馆藏版本文献回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0122.txt:3-12"
SCOPE_START = '<h4 id="第五十三卷-第五章馆藏文物-第七节版本文献">第七节版本文献</h4>'
SCOPE_END = '<h3 id="第五十三卷-第六章文物管理与保护">第六章文物管理与保护</h3>'

NEW_HTML = """<h4 id="第五十三卷-第五章馆藏文物-第七节版本文献">第七节版本文献</h4>
<p>连云港市博物馆收藏的文献、图书（线装）包括经、史、子、集约1000部。其主要来源有三：一是接收的市地志文物陈列室拨交的收藏书；二是1988年购买的藏书；三是接收武可清的捐赠。所藏图书，主要以经史为主。以清版图书为主。明版图书中姜绍书所撰《无声诗史》、明万历版郦道元著《水经注》、明弘治版宋元好问所著《中州集》皆列入善本书目。</p>
<p>清康熙版《吴诗集览》、《杜诗译注》、《全唐诗录》、《义门读书记》、《渔洋山人文略》、乾隆版《豫章先生文集》、《紫钗记全谱》、《蛮书卷》等都是比较重要的版本。</p>
<p>馆藏中的清版20余部河南各县志是一批重要图书。武可清、武可镇捐赠的连云港市清末水利学有武同举的专著及手稿300余万字，是研究江苏省水利发展史的重要文献资料。</p>
"""

EXPECTED_TEXT = [
    "《水经注》",
    "皆列入善本书目",
    "清康熙版《吴诗集览》",
    "《杜诗译注》",
    "《全唐诗录》",
    "《义门读书记》",
    "《渔洋山人文略》",
    "乾隆版《豫章先生文集》",
]
RESIDUALS = [
    "《水经注）",
    "列人善本书目",
    "<p>《豫章先生文集》",
]


def find_scope(text: str) -> tuple[int, int]:
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
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十三卷文物 / 第五章馆藏文物 / 第七节版本文献",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建版本文献节，停止在第六章文物管理与保护前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷馆藏版本文献回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第五章馆藏文物 / 第七节版本文献`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第七节版本文献`，停止在 `第六章文物管理与保护` 前。
- 修正《水经注》书名号、`列入善本书目`，补回清康熙版《吴诗集览》、《杜诗译注》、《全唐诗录》、《义门读书记》、《渔洋山人文略》及乾隆版说明。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `清末水利学有武同举` 为源页可见文字，本次保留不改。
- 后续 `第六章文物管理与保护` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷馆藏版本文献回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第五章馆藏文物 / 第七节版本文献` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第六章文物管理与保护` 前，未触碰下一章。
- 修正《水经注》书名号、`列入善本书目`，补回清康熙版《吴诗集览》、《杜诗译注》、《全唐诗录》、《义门读书记》、《渔洋山人文略》及乾隆版说明；保留源页可见文字 `清末水利学有武同举`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_versions_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum versions repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
