# -*- coding: utf-8 -*-
"""
重启批次1：源章节断行重排 + 机械错字修复

把 workbench/body_chapters 下 12 个源章节 MD（含 paddle_上 子目录）重排成自然段落，
输出到 workbench/body_chapters_reflowed/，不改动源文件。

规则沿用 reformat_full.py 已在 7-06 阅读版上验证过的口径：
- 空行 = 段落边界；连续非空行合并为一段
- 卷/章/节/篇标题、大事记年份条目、序号列表项独立成段
- 页锚注释 <!-- page-anchor: ... --> 与表格注释 <!-- TABLE: ... --> 原位保留
- 跨页段落回接：上页末段无句末标点且下页首段非标题/年份/列表 → 合并
- 行首闭合标点（，。、；：等）并入上一段（OCR 把标点挤到下一行行首的情况）

机械错字修复（只做高置信、全部留痕）：
- 数字一数字 → ～（OCR 把范围号 ～ 误识为 一），如 1949一1957
- 汉字链 一X一Y（≥2 处相连）→ 不改，输出待核清单（如 大别山一东海一胶东）

输出：
- workbench/body_chapters_reflowed/*.md
- output/reports/progress/20261001_批次1_源章节断行重排与机械修复.md
"""
import io
import os
import re
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "workbench" / "body_chapters"
DST = ROOT / "workbench" / "body_chapters_reflowed"
REPORT_DIR = ROOT / "output" / "reports" / "progress"

TITLE_PATTERNS = [
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+卷\s"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+卷$"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+章\s"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+节\s*"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+节$"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+篇\s"),
    re.compile(r"^附\d+-\d+"),
    re.compile(r"^(序|凡例|总述|大事记|总篇目|附录|跋|编纂始末)$"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+卷[\s\u4e00-\u9fff]"),
]

SENTENCE_END_CHARS = set("。！？；：」』）)\"'\"'}》…")

YEAR_PATTERN = re.compile(r"^(春秋|秦|汉|三国|晋|南北朝|隋|唐|宋|元|明|清|民国|共和国|周)[^\n]{0,15}年[）)]")
AD_YEAR_PATTERN = re.compile(r"^\d{4}年")

LIST_ITEM_PATTERN = re.compile(r"^([一二三四五六七八九十]+、|\d+[.、])")

# 行首闭合标点：上一行末尾被 OCR 挤过来的标点（行首即标点即并入，无论行多长）
LEADING_CLOSE_PUNCT = re.compile(r"^[，。、；：）》」』”’]")

DIGIT_DASH = re.compile(r"(?<=\d)一(?=\d)")
DASH_CHAIN = re.compile(r"[\u4e00-\u9fff]一[\u4e00-\u9fff]{1,}一[\u4e00-\u9fff]")


def is_title(s):
    if not s or len(s) > 30:
        return False
    return any(p.match(s) for p in TITLE_PATTERNS)


def is_year_entry(s):
    return len(s) <= 30 and bool(YEAR_PATTERN.match(s) or AD_YEAR_PATTERN.match(s))


def is_list_item(s):
    return len(s) <= 40 and bool(LIST_ITEM_PATTERN.match(s))


def is_comment(s):
    return s.startswith("<!--") and s.endswith("-->")


def is_placeholder(s):
    return s.startswith("{{") and "}}" in s


def reflow_text(md_text, fname, stats):
    """按页锚分块重排；返回新文本。"""
    # 按行扫描，注释行与标题行原样独立保留
    out_lines = []          # 输出行（段落 = 多行合并成单行）
    cur = []                # 当前段落累积
    anchors = re.split(r"(<!-- page-anchor: [^>]*-->)", md_text)

    def flush():
        if cur:
            para = "".join(cur)
            out_lines.append(para)
            cur.clear()

    # 处理顺序：逐块（锚前导言 / 锚+正文）
    for chunk in anchors:
        if chunk.startswith("<!-- page-anchor:"):
            flush()
            out_lines.append("")
            out_lines.append(chunk)
            out_lines.append("")
            continue
        raw_lines = chunk.splitlines()
        i = 0
        n = len(raw_lines)
        while i < n:
            s = raw_lines[i].strip()
            if not s:
                flush()
                i += 1
                continue
            if is_comment(s) or is_placeholder(s):
                flush()
                out_lines.append(s)
                i += 1
                continue
            # 行首闭合标点 → 并入上一段
            if LEADING_CLOSE_PUNCT.match(s) and out_lines and out_lines[-1] and not is_comment(out_lines[-1]):
                out_lines[-1] = out_lines[-1] + s
                stats["punct_start_joined"] += 1
                i += 1
                continue
            if is_title(s):
                flush()
                out_lines.append(s)
                i += 1
                continue
            if is_year_entry(s):
                flush()
                out_lines.append(s)
                i += 1
                continue
            if is_list_item(s):
                flush()
                cur.append(s)   # 列表项可带续行（下一轮普通行会并入）
                i += 1
                continue
            cur.append(s)
            i += 1
        flush()

    # 段落间统一为单空行（页锚前后已加）
    return "\n\n".join(l for l in out_lines)


def cross_page_join(text, stats):
    """页锚跨页段落回接：上页末段无句末标点且下页首段非特殊段 → 合并。

    合并跨越的页锚以内联注释保留在合并段内部（锚不丢）。
    """
    parts = text.split("\n\n")
    merged = []
    i = 0
    while i < len(parts):
        p = parts[i]
        if p.strip().startswith("<!-- page-anchor:") or p.strip() == "":
            merged.append(p)
            i += 1
            continue
        # 找下一个正文段（沿途收集跨过的页锚）
        j = i + 1
        skipped_anchors = []
        next_body = None
        while j < len(parts):
            s = parts[j].strip()
            if s.startswith("<!-- page-anchor:"):
                skipped_anchors.append(s)
                j += 1
                continue
            if s == "":
                j += 1
                continue
            next_body = parts[j]
            break
        last = p.strip()
        can_join = (next_body is not None and last
                    and not is_title(last)
                    and not last.endswith(tuple(SENTENCE_END_CHARS))
                    and not is_year_entry(next_body.strip())
                    and not is_title(next_body.strip())
                    and not is_list_item(next_body.strip())
                    and not is_comment(next_body.strip()))
        if can_join:
            merged.append(p + "".join(skipped_anchors) + next_body.strip())
            stats["cross_page_joined"] += 1
            i = j + 1
            continue
        # 不合并：跨过的页锚也要原样保留
        if skipped_anchors:
            merged.append(p)
            merged.extend(skipped_anchors)
            i = j
            continue
        merged.append(p)
        i += 1
    return "\n\n".join(merged)


def main():
    DST.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    files = []
    for name in sorted(os.listdir(SRC)):
        p = SRC / name
        if p.is_file() and name.endswith(".md") and ".bak" not in name and "backup" not in name \
                and "汇总" not in name:
            files.append(p)
    sub = SRC / "paddle_上"
    if sub.is_dir():
        for name in sorted(os.listdir(sub)):
            p = sub / name
            if p.is_file() and name.endswith(".md") and ".bak" not in name and "backup" not in name \
                    and "汇总" not in name:
                files.append(p)

    stats = Counter()
    dash_fixes = []
    dash_chain_cases = []
    summary = []

    for p in files:
        rel = p.relative_to(SRC)
        t = io.open(p, encoding="utf-8").read()
        before_lines = sum(1 for l in t.splitlines() if l.strip() and not l.strip().startswith("<!--")
                           and not l.startswith("#"))
        before_chars = len(re.sub(r"\s", "", re.sub(r"<!--.*?-->", "", t, flags=re.S)))

        # 机械修复（重排前做，作用于整篇正文；注释内不动）
        def fix_dash(m):
            ctx = t[max(0, m.start() - 12): m.end() + 12].replace("\n", " ")
            dash_fixes.append(f"{rel}: …{ctx}…")
            return "～"
        body_fixed = DIGIT_DASH.sub(fix_dash, t)
        stats["dash_fixed"] += len(DIGIT_DASH.findall(t))
        for m in DASH_CHAIN.finditer(body_fixed):
            ctx = body_fixed[max(0, m.start() - 15): m.end() + 15].replace("\n", " ")
            dash_chain_cases.append(f"{rel}: …{ctx}…")

        st = Counter()
        reflowed = reflow_text(body_fixed, rel.name, st)
        reflowed = cross_page_join(reflowed, st)
        for k, v in st.items():
            stats[k] += v

        after_lines = sum(1 for l in reflowed.splitlines() if l.strip() and not l.strip().startswith("<!--")
                          and not l.startswith("#"))
        after_chars = len(re.sub(r"\s", "", re.sub(r"<!--.*?-->", "", reflowed, flags=re.S)))
        dst = DST / rel.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        io.open(dst, "w", encoding="utf-8", newline="\n").write(reflowed + "\n")
        summary.append((str(rel), before_lines, after_lines, before_chars, after_chars))

    # 汇总报告
    lines = [
        "# 2026-10-01 批次1：源章节断行重排与机械修复",
        "",
        "源 → workbench/body_chapters_reflowed/，源文件未动。",
        "",
        "| 文件 | 重排前行数 | 重排后行数 | 重排前字数 | 重排后字数 |",
        "|---|---:|---:|---:|---:|",
    ]
    for rel, bl, al, bc, ac in summary:
        lines.append(f"| {rel} | {bl} | {al} | {bc} | {ac} |")
    lines += [
        "",
        "## 全局统计",
        "",
        f"- 数字位一→～ 修复：{stats['dash_fixed']} 处（全部留痕于 dash_fixes）",
        f"- 行首标点并入上一段：{stats['punct_start_joined']} 处",
        f"- 跨页段落回接：{stats['cross_page_joined']} 处",
        f"- 汉字链 一X一Y 待核：{len(dash_chain_cases)} 处",
        "",
        "## 数字位一→～ 修复明细",
        "",
    ]
    lines += [f"- {x}" for x in dash_fixes[:400]] or ["（无）"]
    if len(dash_fixes) > 400:
        lines.append(f"- …（其余 {len(dash_fixes) - 400} 条见 dash_fixes.json）")
    lines += ["", "## 汉字链 一X一Y 待核清单", ""]
    lines += [f"- {x}" for x in dash_chain_cases[:300]] or ["（无）"]
    if len(dash_chain_cases) > 300:
        lines.append(f"- …（其余 {len(dash_chain_cases) - 300} 条见 dash_chain.json）")

    rpt = REPORT_DIR / "20261001_批次1_源章节断行重排与机械修复.md"
    io.open(rpt, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

    io.open(ROOT / "output" / "reports" / "dash_fixes.json", "w", encoding="utf-8").write(
        json.dumps(dash_fixes, ensure_ascii=False, indent=1))
    io.open(ROOT / "output" / "reports" / "dash_chain.json", "w", encoding="utf-8").write(
        json.dumps(dash_chain_cases, ensure_ascii=False, indent=1))

    print(json.dumps({
        "files": len(files),
        "dash_fixed": stats["dash_fixed"],
        "punct_start_joined": stats["punct_start_joined"],
        "cross_page_joined": stats["cross_page_joined"],
        "dash_chain_cases": len(dash_chain_cases),
    }, ensure_ascii=False, indent=1))
    for rel, bl, al, bc, ac in summary:
        print(f"{rel}: {bl} -> {al} 行, {bc} -> {ac} 字")


if __name__ == "__main__":
    main()
