# -*- coding: utf-8 -*-
"""批次5-结构化：方言卷双审版 → 接入全书交付

1) 生成 方言卷 最终 MD（概述+第一~五章，含页锚）
2) 替换 body_chapters_v2/第五十二卷至第六十卷及附录（下part02）.md 中的 第五十九卷方言 段
3) 替换 output/final_reader/连云港市志_全书.html 中 id="第五十九卷-方言" 到 id="第六十卷-人物" 之间内容
备份: workbench/volume59/structured/backup_接入前/
用法: python integrate_volume59_into_book_20261002.py [--apply]
"""
import html as H
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TR = ROOT / "workbench" / "volume59" / "transcripts"
ST = ROOT / "workbench" / "volume59" / "structured"
BK = ST / "backup_接入前"
BODY = ROOT / "workbench" / "body_chapters_v2" / "第五十二卷至第六十卷及附录（下part02）.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

CH_MAP = [
    ("概述", "概述", [1]),
    ("第一章方言差别", "第一章　方言差别", range(2, 5)),
    ("第二章语音系统", "第二章　语音系统", range(5, 9)),
    ("第三章同音字汇", "第三章　同音字汇", range(9, 19)),
    ("第五章语法特点", "第五章　语法特点", range(45, 49)),
]

SKIP_P1 = ("【卷首题框", "第五十九卷", "方　言", "#### 概述", "概述")


def md_page(pno: int) -> str:
    fp = TR / f"page_{pno:03d}.md"
    if not fp.exists():
        return ""
    t = fp.read_text(encoding="utf-8", errors="replace")
    # 去掉 frontmatter 与页面注记段
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)
    t = re.split(r"## 页面注记", t)[0]
    lines = []
    for line in t.splitlines():
        if line.startswith("# ") or line.startswith("【页眉】"):
            continue
        if line.startswith("## "):
            lines.append("#### " + line[3:].strip())
        elif line.startswith("- "):
            lines.append(line)
        elif line.strip():
            lines.append(line)
    return "\n".join(lines)


def build_volume_md() -> str:
    vocab = json.loads((ST / "vocab_entries.json").read_text(encoding="utf-8"))
    out = ["## 第五十九卷方言", ""]
    out.append("<!-- page-anchor: vol59-p001 -->")
    out.append("### 概述")
    for line in md_page(1).splitlines():
        if any(line.strip().startswith(s) for s in SKIP_P1):
            continue
        out.append(line)
    # 第一~三章
    for title, h, rng in CH_MAP:
        if h in ("概述", "第五章　语法特点"):
            continue
        out.append("### " + h)
        for pno in rng:
            out.append("<!-- page-anchor: vol59-p%03d -->" % pno)
            out.append(md_page(pno))
    # 第四章（结构化）
    out.append("### 第四章方言词汇")
    out.append("<!-- page-anchor: vol59-p019 -->")
    out.append("本章记录连云港市城区的方言词约1600条，和普通话相同的则不收。词条按韵、声、调的次序排列。"
               "首字相同的同义词排在一起，第一条顶格，其他各词缩一格排列。字的右上角加“=”，表示用同音字代替。"
               "轻声音节不标调值。（以下为双审版结构化词条，1395条）")
    cur_sec = None
    for e in vocab:
        sec = e["section"] or ""
        if sec != cur_sec:
            cur_sec = sec
            out.append("#### " + sec)
        note = "（" + e["notes"] + "）" if e.get("notes") else ""
        out.append("- " + e["word"] + "　" + e["ipa"] + "　" + e["gloss"] + note)
    # 第五章
    out.append("### 第五章　语法特点")
    for pno in range(45, 49):
        out.append("<!-- page-anchor: vol59-p%03d -->" % pno)
        out.append(md_page(pno))
    return "\n".join(out)


def _zh_quotes(s: str) -> str:
    """ASCII 双引号按出现次序配对替换为中文引号（阅读版门禁要求，避免 &quot; 转义残留）。"""
    out, open_q = [], True
    for ch in s:
        if ch == '"':
            out.append("“" if open_q else "”")
            open_q = not open_q
        else:
            out.append(ch)
    return "".join(out)


def _esc(s: str) -> str:
    return H.escape(_zh_quotes(s), quote=False)


def to_html_block(md_text: str) -> str:
    """MD → 全书阅读版 HTML 片段（h2/h3/h4/p/ul/table）"""
    parts = []
    in_ul = False
    lines = md_text.splitlines()
    k = 0
    while k < len(lines):
        line = lines[k]
        if line.startswith("<!-- page-anchor"):
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            parts.append(line.strip())
            k += 1
            continue
        if line.startswith("|"):
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            tbl = []
            while k < len(lines) and lines[k].startswith("|"):
                tbl.append(lines[k])
                k += 1
            parts.append("<table>")
            for r_i, row in enumerate(tbl):
                cells = [c.strip() for c in row.strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    continue
                tag = "th" if r_i == 0 else "td"
                parts.append("<tr>" + "".join(
                    "<%s>%s</%s>" % (tag, _esc(c), tag) for c in cells) + "</tr>")
            parts.append("</table>")
            continue
        if line.startswith("#### "):
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            parts.append("<h4>%s</h4>" % _esc(line[5:].strip()))
        elif line.startswith("### "):
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            title = line[4:].strip()
            if title == "概述":
                parts.append('<h3 id="第五十九卷-概述">概述</h3>')
            else:
                parts.append("<h3>%s</h3>" % _esc(title))
        elif line.startswith("## "):
            parts.append('<h2 id="第五十九卷-方言">第五十九卷 方言</h2>')
        elif line.startswith("- "):
            if not in_ul:
                parts.append("<ul>")
                in_ul = True
            parts.append("<li>%s</li>" % _esc(line[2:].strip()))
        elif line.strip():
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            parts.append("<p>%s</p>" % _esc(line.strip()))
        k += 1
    if in_ul:
        parts.append("</ul>")
    return "\n".join(parts)


def main():
    apply = "--apply" in sys.argv
    new_md = build_volume_md()
    new_html = to_html_block(new_md)
    print("新方言卷 MD 长度:", len(new_md), " HTML 片段:", len(new_html))

    # --- body_chapters_v2 替换 ---
    body = BODY.read_text(encoding="utf-8")
    i = body.find("## 第五十九卷方言")
    j = body.find("## 第六十卷", i)
    print("body 段:", i, j)
    body_new = body[:i] + new_md + "\n\n" + body[j:]

    # --- 全书 html 替换 ---
    rd = READER.read_text(encoding="utf-8")
    hi = rd.find('<h2 id="第五十九卷-方言">')
    hj = rd.find('<h2 id="第六十卷-人物">')
    print("html 段:", hi, hj)
    rd_new = rd[:hi] + new_html + "\n" + rd[hj:]

    if apply:
        BK.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BODY, BK / BODY.name)
        shutil.copy2(READER, BK / READER.name)
        BODY.write_text(body_new, encoding="utf-8")
        READER.write_text(rd_new, encoding="utf-8")
        (ST / "第五十九卷方言_双审版.md").write_text(new_md, encoding="utf-8")
        print("已应用。备份在", BK)
    else:
        (ST / "第五十九卷方言_双审版.md").write_text(new_md, encoding="utf-8")
        print("dry-run（未替换）。生成 第五十九卷方言_双审版.md；加 --apply 执行替换")


if __name__ == "__main__":
    main()
