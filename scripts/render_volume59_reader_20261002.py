# -*- coding: utf-8 -*-
"""批次5-结构化：vol59 双审版阅读器 HTML 渲染

输入: workbench/volume59/transcripts/*.md + structured/vocab_entries.json
输出: workbench/volume59/structured/连云港市志_第五十九卷方言_双审版.html
用法: python render_volume59_reader_20261002.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TR = ROOT / "workbench" / "volume59" / "transcripts"
ST = ROOT / "workbench" / "volume59" / "structured"
OUT = ST / "连云港市志_第五十九卷方言_双审版.html"

CSS = """
body{font-family:"Source Han Serif SC","Noto Serif CJK SC",SimSun,serif;max-width:980px;margin:0 auto;
padding:24px 20px 80px;line-height:1.85;color:#222;background:#faf8f4}
h1{font-size:1.7em;text-align:center;border-bottom:3px double #8a6d3b;padding-bottom:14px}
h2{font-size:1.35em;border-left:6px solid #8a6d3b;padding-left:12px;margin-top:2em;background:#f3ede2}
h3{font-size:1.12em;color:#6b4f1d;margin-top:1.6em}
.meta{color:#666;font-size:.92em;background:#f3ede2;padding:10px 14px;border-radius:6px}
.entry{display:grid;grid-template-columns:8.5em 12em 1fr;gap:2px 10px;padding:3px 6px;border-bottom:1px dashed #e2dccf}
.entry:nth-child(even){background:#fbf9f5}
.word{font-weight:600;font-size:1.08em}
.ipa{font-family:"Charis SIL","Doulos SIL","DejaVu Sans",serif;color:#7a4a1d;white-space:nowrap;font-size:.98em}
.gloss{color:#333}
.flag{color:#a33;font-size:.8em;vertical-align:super}
.flag-bai{color:#1a6b3c}
.note{color:#8a6d3b;font-size:.82em;display:block}
.sec-head{position:sticky;top:0;background:#efe7d8;padding:4px 8px;font-weight:700;border-bottom:2px solid #c9b78e;z-index:5}
ul{padding-left:1.4em}
li{margin:2px 0}
table{border-collapse:collapse;width:100%;font-size:.92em;margin:8px 0}
td,th{border:1px solid #cfc5b0;padding:4px 8px;text-align:left}
th{background:#efe7d8}
.searchbar{position:sticky;top:0;background:#faf8f4;padding:8px 0;z-index:10;border-bottom:2px solid #8a6d3b}
.searchbar input{width:100%;font-size:1.05em;padding:8px 12px;border:2px solid #c9b78e;border-radius:6px;background:#fff}
.hidden{display:none}
.toc a{display:block;padding:2px 0;color:#6b4f1d}
.pg{color:#b09b6d;font-size:.78em;margin-left:6px}
footer{margin-top:3em;border-top:1px solid #cfc5b0;padding-top:12px;color:#777;font-size:.88em}
"""

JS = """
function doSearch(){
  var q=document.getElementById('q').value.trim().toLowerCase();
  var ents=document.querySelectorAll('.entry');
  var shown=0;
  for(var i=0;i<ents.length;i++){
    var e=ents[i];
    if(!q){e.classList.remove('hidden');shown++;continue}
    var t=e.textContent.toLowerCase();
    if(t.indexOf(q)>=0){e.classList.remove('hidden');shown++}else{e.classList.add('hidden')}
  }
  document.getElementById('cnt').textContent=q?('匹配 '+shown+' 条'):'';
}
"""


def md_inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def render_md_page(text: str) -> str:
    """把转录 MD 渲染成 HTML（标题/列表/表格/段落）"""
    out = []
    lines = text.splitlines()
    i = 0
    in_ul = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("---") and i == 0:
            # frontmatter
            i += 1
            while i < len(lines) and not lines[i].startswith("---"):
                i += 1
            i += 1
            continue
        if line.startswith("# "):
            out.append(f"<h3>{md_inline(line[2:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h4>{md_inline(line[3:])}</h4>")
        elif line.startswith("| "):
            # 表格
            tbl = []
            while i < len(lines) and lines[i].startswith("|"):
                tbl.append(lines[i])
                i += 1
            out.append("<table>")
            for r_i, row in enumerate(tbl):
                cells = [c.strip() for c in row.strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    continue
                tag = "th" if r_i == 0 else "td"
                out.append("<tr>" + "".join(f"<{tag}>{md_inline(c)}</{tag}>" for c in cells) + "</tr>")
            out.append("</table>")
            continue
        elif line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{md_inline(line[2:])}</li>")
        else:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if line.strip():
                out.append(f"<p>{md_inline(line)}</p>")
        i += 1
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)


def entry_html(e: dict) -> str:
    word = html.escape(e["word"])
    flags = []
    if e["flags"]["kong"]:
        flags.append('<span class="flag">□</span>')
    if e["flags"]["bai"]:
        flags.append('<span class="flag flag-bai">白</span>')
    if e["flags"]["wenhao"]:
        flags.append('<span class="flag">?</span>')
    note = f'<span class="note">{html.escape(e["notes"])}</span>' if e.get("notes") else ""
    return (f'<div class="entry" data-pg="{e["page"]}">'
            f'<div class="word">{word}{"".join(flags)}{note}</div>'
            f'<div class="ipa">{html.escape(e["ipa"])}</div>'
            f'<div class="gloss">{html.escape(e["gloss"])}</div></div>')


def main():
    vocab = json.loads((ST / "vocab_entries.json").read_text(encoding="utf-8"))
    # 按韵部聚合（保持页序）
    sec_order = []
    by_sec = {}
    for e in vocab:
        key = e["section"] or "未分韵"
        if key not in by_sec:
            by_sec[key] = []
            sec_order.append(key)
        by_sec[key].append(e)

    parts = []
    parts.append("<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>")
    parts.append("<meta name='viewport' content='width=device-width,initial-scale=1'>")
    parts.append("<title>连云港市志·第五十九卷 方言（双审版）</title>")
    parts.append(f"<style>{CSS}</style></head><body>")
    parts.append("<h1>连云港市志 · 第五十九卷《方言》<br><span style='font-size:.6em'>双审版 · 2026-10-02</span></h1>")
    parts.append("<div class='meta'>本阅读器由 48 页人工转录（六区2.7倍 + 高倍复核）与全卷双审结果生成。"
                 "词汇章 1395 条已全部经过字形双审（字汇互证 / 8-16x 放大裁定）；"
                 "〔白〕=白读、□=原书有音无字或空框、?=原书字形存疑照录。"
                 "结构化数据：vocab_entries.json / vocab_entries.csv。</div>")

    # 目录
    parts.append("<h2 id='toc'>目录</h2><div class='toc'>")
    parts.append("<a href='#ch1'>第一章 方言差别（页1-4）</a>")
    parts.append("<a href='#ch2'>第二章 语音系统（页5-8）</a>")
    parts.append("<a href='#ch3'>第三章 同音字汇（页9-19）</a>")
    parts.append("<a href='#ch4'>第四章 方言词汇（页19-45，1395条）</a>")
    parts.append("<a href='#ch5'>第五章 语法（页45-48）</a>")
    parts.append("</div>")

    def add_pages(title, aid, rng):
        parts.append(f"<h2 id='{aid}'>{title}</h2>")
        for pno in rng:
            fp = TR / f"page_{pno:03d}.md"
            if not fp.exists():
                continue
            parts.append(f"<h3>卷内第 {pno:03d} 页 <span class='pg'>(书页对照见转录 frontmatter)</span></h3>")
            parts.append(render_md_page(fp.read_text(encoding="utf-8", errors="replace")))

    add_pages("第一章　方言差别", "ch1", range(1, 5))
    add_pages("第二章　语音系统", "ch2", range(5, 9))
    add_pages("第三章　同音字汇", "ch3", range(9, 19))

    parts.append("<h2 id='ch4'>第四章　方言词汇（结构化 · 1395条）</h2>")
    parts.append("<div class='searchbar'><input id='q' placeholder='搜索词条 / 释义 / 音标…（如：老鼠、tʂ、下雨）' oninput='doSearch()'>"
                 "<span id='cnt' style='color:#8a6d3b;font-size:.9em'></span></div>")
    for sec in sec_order:
        ents = by_sec[sec]
        pages = sorted({e["page"] for e in ents})
        pr = f"{pages[0]}-{pages[-1]}" if len(pages) > 1 else str(pages[0])
        parts.append(f"<div class='sec-head'>{html.escape(sec)}　<span class='pg'>{len(ents)}条 · 页{pr}</span></div>")
        for e in ents:
            parts.append(entry_html(e))
    parts.append("<h3>第四章 各页原始转录（含页面注记与互证）</h3>")
    for pno in range(19, 46):
        fp = TR / f"page_{pno:03d}.md"
        if fp.exists():
            parts.append(f"<details><summary>卷内第 {pno:03d} 页 原始转录</summary>")
            parts.append(render_md_page(fp.read_text(encoding="utf-8", errors="replace")))
            parts.append("</details>")

    add_pages("第五章　语法", "ch5", range(45, 49))

    parts.append("<footer>生成脚本：scripts/render_volume59_reader_20261002.py ｜ "
                 "数据源：workbench/volume59/transcripts/page_001-048.md ｜ "
                 "台账：workbench/volume59/uncertain_ledger.csv（词汇章126条全结案）</footer>")
    parts.append(f"<script>{JS}</script></body></html>")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print("written", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
