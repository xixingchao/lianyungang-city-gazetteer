# -*- coding: utf-8 -*-
"""Restore cultural relics survey section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_survey_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_survey_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷文物普查回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0123.txt:3-30"
SCOPE_START = '<h4 id="第五十三卷-第六章文物管理与保护-第二节文物普查">第二节文物普查</h4>'
SCOPE_END = '<h4 id="第五十三卷-第六章文物管理与保护-第三节文物保护单位公布与维修">第三节文物保护单位公布与维修</h4>'

NEW_HTML = """<h4 id="第五十三卷-第六章文物管理与保护-第二节文物普查">第二节文物普查</h4>
<p>一、第一次普查</p>
<p>1957年，江苏省文物工作队在徐海地区进行大范围的文物普查时，在连云港市境内发现属于新石器至汉代各个历史时期的二涧村、九龙口、大村遗址，以及东海青湖和赣榆下庙墩遗址，从而为研究这一地区的新石器时代文化发展序列，乃至商周与秦汉史提供了丰富的实物资料。</p>
<p>二、第二次普查</p>
<p>1979年冬在市区、郊县进行了局部范围的文物普查，1980年上半年结束，期间市博物馆考古人员对将军崖岩画进行照像和绘图。1980年邀请北京有关专家对孔望山摩崖造像的题材重新鉴定。中国历史博物馆史树青教授首次指出孔望山摩崖造像含有佛教内容，认定它是一处宗教题材为主的石刻群，对于我国佛教史、艺术史和中外关系史等的研究，都具有重要意义。孔望山摩崖造像题材的重新鉴定被考古界公认为1980年我国五大考古成果之一。</p>
<p>三、第三次普查</p>
<p>1984年4月10日至1985年10月1日，由市政府组织成立连云港市文物普查领导小组，在全市三县四区的广大范围内进行了一次更大规模的文物普查。</p>
<p>普查中，收集群众提供的文物线索5283条，其中流散文物3662条，革命文物和革命史迹48条，古文化遗址与古墓葬494条，历史遗迹212条，石刻碑碣345条，古树名木38条。在所登记的流散文物线索中，已征集的文物共1599件。</p>
<p>四、普查补课</p>
<p>1987年，由市文管会发起并组织市县博物馆及县区干部在全市范围内，重点对1984年普查成果进行复核审定和“补课”。在这次审核过程中，又新补查到了位于东连岛海滨的西汉界域刻石，它是我国迄今发现最早的界域刻石。</p>
"""

EXPECTED_TEXT = [
    "一、第一次普查</p>",
    "下庙墩遗址",
    "二、第二次普查</p>",
    "三、第三次普查</p>",
    "四、普查补课</p>",
    "我国迄今发现最早的界域刻石",
]
RESIDUALS = [
    "一、第一次普查1957年",
    "下届墩遗址",
    "二、第二次普查1979年",
    "三、第三次普查1984年",
    "四、普查补课1987年",
    "最卓的界域刻石",
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
        "scope": "第五十三卷文物 / 第六章文物管理与保护 / 第二节文物普查",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建文物普查节，停止在第三节文物保护单位公布与维修前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷文物普查回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第六章文物管理与保护 / 第二节文物普查`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第二节文物普查`，停止在 `第三节文物保护单位公布与维修` 前。
- 拆开 `一、第一次普查`、`二、第二次普查`、`三、第三次普查`、`四、普查补课` 与正文粘连，修正 `下庙墩遗址`、`最早的界域刻石`。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `照像` 为源页可见用字，本次保留不改。
- 后续 `第三节文物保护单位公布与维修` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷文物普查回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第六章文物管理与保护 / 第二节文物普查` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第三节文物保护单位公布与维修` 前，未触碰后续维修条目。
- 拆开 `一、第一次普查`、`二、第二次普查`、`三、第三次普查`、`四、普查补课` 与正文粘连，修正 `下庙墩遗址`、`最早的界域刻石`；保留源页用字 `照像`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_survey_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum survey repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
