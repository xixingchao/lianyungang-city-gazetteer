# -*- coding: utf-8 -*-
"""Restore the English 'General Summary' section (附录五) into reader + v2.

Source: the pre-reflow body_chapters copy of 第五十二卷至第六十卷及附录（下part02）.md
at commit 73153e8, which preserves the original line breaks of the OCR.

Cleaning rules:
- drop running heads / page numbers ('General Summary·2733', 'Histroy of LianYunGang', '2735' etc.)
- de-hyphenate line-final hyphens, join other lines with a space
- blank lines delimit paragraphs
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEAD_RE = re.compile(r"^(General\s+Summary|GENERAL\s*SUMMARY|Histroy of LianYunGang|GENERAL|SUMMARY|·\s*\d{4}|\d{3,4})\s*[:：.]?\s*$", re.I)
PAGENO_RE = re.compile(r"^[:：.]?\s*\d{4}\s*[:：.]?$")


def load_old() -> str:
    out = subprocess.run(
        ["git", "show", "73153e8:workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"],
        cwd=ROOT, capture_output=True)
    return out.stdout.decode("utf-8")


def build_paragraphs() -> list[str]:
    t = load_old()
    k = t.find("GENERAL")
    tail = t.find("\n跋", k)
    region = t[k : tail if tail > k else len(t)]
    cut = region.find("SUMMARY")
    region = region[cut + len("SUMMARY"):] if cut >= 0 else region

    paras: list[str] = []
    cur: list[str] = []
    for raw in region.split("\n"):
        line = raw.strip()
        if not line:
            if cur:
                paras.append(" ".join(cur)); cur = []
            continue
        if HEAD_RE.match(line) or PAGENO_RE.match(line):
            continue
        if re.match(r"^<!--", line):
            continue
        if re.match(r"^[（(][一二三四五六七八九十][）)]$", line):
            if cur:
                paras.append(" ".join(cur)); cur = []
            paras.append(line)
            continue
        # 去掉行首的残余页码/冒号
        line = re.sub(r"^[:：.]\s*\d{4}\s*[:：.]?\s*", "", line)
        line = re.sub(r"^(GENERAL|SUMMARY)\s*", "", line) if line.isupper() else line
        if not line:
            continue
        if cur and cur[-1].endswith("-"):
            cur[-1] = cur[-1][:-1] + line  # 行末连字符 → 直接拼接
        else:
            cur.append(line)
    if cur:
        paras.append(" ".join(cur))
    # 段落内页眉/页码残片清理 + 空格规范化
    CLEAN = [
        (r"Histroy of LianYunGang(?: City)?\s*[·:.]?\s*General Summary\s*[·:.]?\s*", " "),
        (r"General Summary\s*[·:.]?\s*\d{3,4}\s*[:：.]?\s*", " "),
        (r"\b\d{3,4}\s*[:：.]?\s*Histroy of LianYunGang(?: City)?\b\s*[:：.]?\s*", " "),
        (r"GENERAL\s*SUMMARY\s*", " "),
        (r"\bHistroy of LianYunGang\b\s*[·:.]?\s*", " "),
        (r"\b·\s*\d{3,4}\b", " "),
    ]
    out: list[str] = []
    for p in paras:
        for _ in range(2):
            for pat, rep in CLEAN:
                p = re.sub(pat, rep, p)
        p = re.sub(r"\s+", " ", p)
        p = re.sub(r"\s+([,.;:])", r"\1", p)
        p = re.sub(r"^\d{3,4}\s*[:：.]?\s*", "", p)  # 段首残留页码
        p = p.strip()
        if not p:
            continue
        # 跨页拼接：上一段未以句末标点结束 → 与当前段合并
        if out and not re.search(r"[.!?\"'\u2019\u201d)\]]$", out[-1]):
            if out[-1].endswith("-"):
                out[-1] = out[-1][:-1] + p
            else:
                out[-1] = out[-1] + " " + p
            continue
        out.append(p)
    # 段内嵌着的部分标题（OCR 把标题并进了正文）也要拆出
    final: list[str] = []
    for p in out:
        parts = re.split(r"([（(][一二三四五六七八九十]+[）)])", p)
        buf = []
        for seg in parts:
            seg = seg.strip()
            if not seg:
                continue
            if re.fullmatch(r"[（(][一二三四五六七八九十]+[）)]", seg):
                if buf:
                    final.append(" ".join(buf)); buf = []
                final.append(seg)
            else:
                buf.append(seg)
        if buf:
            final.append(" ".join(buf))
    return final


def main() -> None:
    paras = build_paragraphs()
    letters = sum(len(re.findall(r"[A-Za-z]", p)) for p in paras)
    print("段落数:", len(paras), "| 英文字母:", letters)
    print("首段:", paras[0][:150])
    print("末段:", paras[-1][:150])
    heads = [p for p in paras if len(p) <= 4]
    print("短标题段:", heads)
    Path(r"C:\Users\52744\_scratch\english_summary_paras.txt").write_text("\n\n".join(paras), encoding="utf-8")
    print("已写出临时文件")


if __name__ == "__main__":
    main()
