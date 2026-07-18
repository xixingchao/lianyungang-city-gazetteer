# -*- coding: utf-8 -*-
"""Restore sports track and field section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_track_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_track_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷田径回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0237.txt:20-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0238.txt:3-7"
)
SCOPE_START = '<h4 id="第五十六卷-第三章运动项目-第二节田径">第二节田径</h4>'
SCOPE_END = '<h4 id="第五十六卷-第三章运动项目-第三节军体类">第三节军体类</h4>'

NEW_HTML = """<p>20世纪20年代，市内田径运动只是在学校中开展，民国24年（1935年），灌云县在江苏省第八区（包括13个县、市）运动会上获得团体总分第二名。该县运动员李延祥打破400米省纪录，后参加全国运动会，在400米比赛中仍名列前茅。30年代，赣榆、东海、灌云三县举办过田径运动会；各中、小学每年都要举行一、二次运动会。</p>
<p>民国30年至民国33年（1941～1944年），在新浦南广场举行过两届田径运动会。同期，伪淮海省在徐州市举行过三届体育运动会，海州市运动员滕子复获一至三届100米和200米冠军。</p>
<p>20世纪50年代，开展“劳卫制”体育锻炼，中、小学每年春秋季常举行田径运动会，厂矿、企业、机关田径活动也趋于活跃。1951～1955年，淮北盐场举办过两届田径运动会；1956年冬，赣榆县举办第一届农民运动会，200多名运动员参赛；1956年和1958年，东海县举办过两届农民运动会。1958～1965年一至六届中学生田径运动会的团体总分新海中学、海州师范、新浦中学3校列前。</p>
<p>1972年10月，在连云港市第六届全民体育运动会田径赛中，有21人打破16项次男女市纪录。1963年10月，在南京举行的全国田径运动会上，韩永年获男子800米冠军。</p>
<p>1972年，在全国田径运动会上，范德华获链球第一名。</p>
<p>1980年，东海县运动员谭红海入选国家队，1982年在新德里举行的第九届亚运会上，获4×100米接力赛第三名和跳远第四名。1983年，在上海举行的第五届全运会上，谭红海打破了男子200米的全国纪录，名列第二，并获400米的第三名、男子4×100米接力赛第二名。1981～1983年间，谭红海获得跳远和400米两项全国冠军。1986年，在江苏省第十一届运动会上，刘海波、周振山分别打破男子少年甲组10公里竞走、标枪省纪录；韩树屏打破高校部男子丙组的链球省纪录。</p>
<p>1990年，参加江苏省第十二届运动会，苏东胜在5000米竞走、卢廷武在男子少年组的3000米、杨杰在1500米比赛中分别都打破了省纪录。</p>
<p>连云港市籍田径运动健将有5人。</p>"""

EXPECTED_TEXT = [
    "江苏省第八区（包括13个县、市）运动会上获得团体总分第二名",
    "该县运动员李延祥打破400米省纪录",
    "三县举办过田径运动会",
    "淮北盐场举办过两届田径运动会",
    "谭红海入选国家队",
    "刘海波、周振山分别打破男子少年甲组10公里竞走、标枪省纪录",
]
RESIDUALS = [
    "江400米省纪录",
    "举办过由径运动会",
    "：</p>",
    "两届由径运动会",
    "准北盐场",
    "谭红海人选国家队",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = "\n" + NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"sports track expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports track residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第三章运动项目 / 第二节田径",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建田径整节，修复跨页漏句和明确错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷田径回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第三章运动项目 / 第二节田径`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第二节田径` 整节。
- 补回首段 `江苏省第八区（包括13个县、市）运动会上获得团体总分第二名` 和 `李延祥打破400米省纪录` 等漏句。
- 修正 `由径运动会` 为 `田径运动会`，`准北盐场` 为 `淮北盐场`，`谭红海人选国家队` 为 `谭红海入选国家队`。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。
- 本轮未处理 `第三节军体类`。

## 核对说明

- PaddleOCR `page_0237.txt` 确认田径节开头至 1986 年段落。
- PaddleOCR `page_0238.txt` 确认 1986 年跨页尾句、1990 年段落和第三节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷田径回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第三章运动项目 `第二节田径` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建整节，补回首段 `江苏省第八区（包括13个县、市）运动会上获得团体总分第二名` 和 `李延祥打破400米省纪录` 等漏句。
- 修正 `由径运动会` 为 `田径运动会`，`准北盐场` 为 `淮北盐场`，`谭红海人选国家队` 为 `谭红海入选国家队`。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处；`第三节军体类` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_track_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports track section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
