# -*- coding: utf-8 -*-
"""Restore literary periodicals section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_media_literary_periodicals_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_media_literary_periodicals_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷文艺刊物回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0140.txt:43-55; page_0141.txt:3-15"
SCOPE_START = '<h4 id="第五十四卷-第二章刊物-第一节文艺刊物">第一节文艺刊物</h4>'
SCOPE_END = '<h4 id="第五十四卷-第二章刊物-第二节专业刊物">第二节专业刊物</h4>'

NEW_HTML = """<h4 id="第五十四卷-第二章刊物-第一节文艺刊物">第一节文艺刊物</h4>
<p>一、飞轮</p>
<p>民国23年（1934年）创刊，由海属地区地下党—“社联”主席陈新明主办。社长陈新明，经理黄榘门，编辑李超然、武淑祖（女）、黄盛庚、李庆华（曾用名李石华）、沈华年、李鹏年等并为该社理事。32开本，铅印，新浦振东印务馆印刷，期发行量700多份。国民党东海县党部登记注册。</p>
<p>《飞轮》杂志印刷精美，以诗歌、散文、小说、评论等文艺形式，宣传抗日爱国思想。陈新明特邀文坛名人臧克家、孙佳讯等人撰稿，颇受读者欢迎。</p>
<p>陈新明在第一、二期上发表杂文《论幽默》和《艺术的功能》，公开提倡文艺战斗性，宣传无产阶级文艺思想。陈新明和编辑李超然旋因“赤色”嫌疑，被国民党东海县党部逮捕，两月后在社会各社团的帮助下，保释出狱。刊物共出版5期，于当年年底停刊。</p>
<p>二、连云港文学</p>
<p>连云港市文学艺术界联合会主办。季刊，16开本，每期64～72页。1983年，经中共江苏省委宣传部和江苏省新闻出版局批准，公开发行，江苏期刊登记证第112号，邮发代号28-29，期发行量2000～5000份。赣榆县中学印刷厂印刷。原在邮局发行，1988年起由连云港报社发行部代办发行。编辑4人，姜威、彭云先后任主编。</p>
<p>《连云港文学》主要发表小说、诗歌、散文、故事、报告文学、民间故事、影视剧本、文学评论，以及本地作者的美术、摄影、书法、篆刻等作品。</p>
<p>该刊前身是《群众文艺》。《群众文艺》创刊于1971年，为内部交流刊物。连云港市革命委员会政工组主办，刘国华任主编。1976年转为市文化局主办，改名《连云港文艺》。</p>
<p>1980年，市文联成立，《连云港文艺》由文联主办。1983年改名《连云港文学》。</p>
<p>《连云港文学》从《群众文艺》创刊起，近20年中发表文艺作品5000多件，其中有500多件汇编成《连云浪花》、《激浪奔腾》、《螺号响了》、《盐的故事》、《连云港民间传说》等书。</p>
<p>经费由市文联每年拨给2万元，不足部分靠广告、社会赞助弥补。</p>
"""

EXPECTED_TEXT = [
    "<p>一、飞轮</p>",
    "地下党—“社联”主席陈新明",
    "经理黄榘门",
    "<p>二、连云港文学</p>",
    "每期64～72页",
    "邮发代号28-29",
    "改名《连云港文艺》",
    "《连云港文学》从《群众文艺》创刊起",
    "《连云浪花》、《激浪奔腾》",
    "《连云港民间传说》等书",
]
RESIDUALS = [
    "<p>、飞轮民国23年",
    "地下党—社联”主席",
    "经理黄门",
    "二、连云港文学连云港市文学艺术界联合会",
    "每期64~72页",
    "邮发代号28－29",
    "<p>：《连云港文学》",
    "改名连云港文艺》",
    "<p>多件汇编成",
    "《连云浪花）",
    "《连云港民间传说等书",
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
    return changed, {"rewrote_scope": changed, "entries_restored": 2}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第二章刊物 / 第一节文艺刊物",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建文艺刊物节，停止在第二节专业刊物前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷文艺刊物回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第二章刊物 / 第一节文艺刊物`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、飞轮`、`二、连云港文学`，停止在 `第二节专业刊物` 前。
- 修正 `一、飞轮` 题名漏字、`“社联”` 引号、`黄榘门` 人名缺字。
- 拆开 `二、连云港文学` 题名正文粘连，补回 `《连云港文学》从《群众文艺》创刊起...` 段首，修正书名号残缺。
- 当前核验复跑整段替换：{changed} 处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷文艺刊物回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第二章刊物 / 第一节文艺刊物` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第二节专业刊物` 前。
- 修正 `一、飞轮` 题名漏字、`“社联”` 引号、`黄榘门` 人名缺字、`二、连云港文学` 题名粘连和《连云浪花》《连云港民间传说》等书名号残缺。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_media_literary_periodicals_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
