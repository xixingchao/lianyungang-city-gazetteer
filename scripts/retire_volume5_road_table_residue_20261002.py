# -*- coding: utf-8 -*-
"""撤出阅读版/v2 中「表5-3、表5-4」的表格残文，改为结构化表占位/嵌入（2026-10-02）。

背景：第五卷市政建设章的表5-3（县城干道）、表5-4（市区一般道路·巷）在阅读版里被压成
整行正文（表头碎片 + 787/354/461 字残文），且表5-4 续表（p347）内容整段丢失。
本次回源核录为 LYG-上-T056 / LYG-上-T057 两张结构化表后，撤出残文。

- v2：残文区替换为 {{STRUCTURED_TABLE:表ID}} 占位（与全库体例一致）
- 阅读版：撤出残文（表由 scripts/embed_verified_tables_into_reader.py 嵌入本卷「已核结构化表格」节）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2" / "第四卷至第十卷（part02）.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

V2_PATTERNS = [
    # 表5-3 残文（表头碎片 + 787 字残文）
    (re.compile(r"人行道面积（平方米）\n\n长度宽度最后修城区道路名称起讫地点其中其中（米）\n\n（米）\n\n（米）\n\n环城北路[^\n]*"),
     "{{STRUCTURED_TABLE:LYG-上-T056}}", "表5-3"),
    # 表5-4 残文：B 段（新浦，354 字）在锚 LYG-S-0346 之前、C 段（云台/连云，461 字）在其后；
    # 撤 B 段残文、保留页锚，C 段残文处落占位
    (re.compile(r"人行道面积（平方米）\n\n长度宽度起讫地点其中其中最后修城区道路名称（米）\n\n（米）\n\n合计水泥[^\n]*\n\n"),
     "", "表5-4(前段)"),
    (re.compile(r"人行道面积（平方米）\n\n长度宽度其中其中最后修城区道路名称起讫地点（米）\n\n（米）\n\n合计水泥[^\n]*"),
     "{{STRUCTURED_TABLE:LYG-上-T057}}", "表5-4(后段)"),
]

READER_PATTERNS = [
    (re.compile(r"\n<p>人行道面积（平方米）</p>\n<p>长度宽度最后修城区道路名称起讫地点其中其中（米）</p>\n<p>（米）</p>\n+"
                r"<p>（米）</p>\n<p>环城北路[^<]*</p>"), "\n", "表5-3"),
    (re.compile(r"\n<p>人行道面积（平方米）</p>\n<p>长度宽度起讫地点其中其中最后修城区道路名称（米）</p>\n<p>（米）</p>\n"
                r"<p>合计水泥[^<]*</p>\n+"
                r"<p>人行道面积（平方米）</p>\n<p>长度宽度其中其中最后修城区道路名称起讫地点（米）</p>\n<p>（米）</p>\n"
                r"<p>合计水泥[^<]*</p>"), "\n", "表5-4"),
]


def apply(path: Path, patterns, label: str) -> int:
    text = path.read_text(encoding="utf-8")
    n = 0
    for pat, repl, which in patterns:
        text, k = pat.subn(repl, text, count=1)
        print(f"  {label} {which}: 替换 {k} 处")
        n += k
    path.write_text(text, encoding="utf-8")
    return n


def main() -> None:
    print("v2:")
    n1 = apply(V2, V2_PATTERNS, "v2")
    print("reader:")
    n2 = apply(READER, READER_PATTERNS, "reader")
    if n1 + n2 == 0:
        print("没有可替换的残文（可能已处理）")
    # 复核
    v2t = V2.read_text(encoding="utf-8")
    rt = READER.read_text(encoding="utf-8")
    print("v2 占位:", v2t.count("{{STRUCTURED_TABLE:LYG-上-T056}}"), v2t.count("{{STRUCTURED_TABLE:LYG-上-T057}}"))
    print("v2 残文残留:", v2t.count("环城北路环城西路"), v2t.count("合计水泥合计建时间"))
    print("reader 残文残留:", rt.count("环城北路环城西路"), rt.count("合计水泥合计建时间"), rt.count("长度宽度最后修城区道路名称"))


if __name__ == "__main__":
    main()
