# -*- coding: utf-8 -*-
"""
批次3工具 v2：三方共识比对（整卷拼接流对齐版）

相对旧版（逐页比对）的改进：
- v2 页流与引擎页流各自拼接成整卷流后一次对齐，页界错位（上页尾巴进本页）
  不再产生假 FLAG_M/X
- 页眉/页脚模式（·页码·、连云港市志、章名页眉）单独归为 header_noise
- rapid 段用 boundary_map(v2,rapid) 直接截取，不再链式映射

分类：
- FLAG_A  双引擎一致反 v2 → 疑似 v2 错字（高优先）
- FLAG_B  三方全不同 → 需目视图核（中优先）
- FLAG_M  引擎有 v2 无（排除页眉/表格残文后）→ 疑似漏识别
- FLAG_X  v2 有引擎无（同上排除）→ 疑似多识别/错段
- header_noise / table_residue / engine_noise 计数忽略
"""
import argparse
import io
import json
import re
import difflib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2"
OCR_BASE = ROOT / "workbench" / "ocr_v2" / "ocr"
OUT_DIR = ROOT / "output" / "reports" / "batch3"

WS = re.compile(r"\s+")
HAN = re.compile(r"[\u4e00-\u9fff]")
HEADER_PAT = re.compile(r"^(·\d+·|第[一二三四五六七八九十]+卷|第[一二三四五六七八九十]+章.*·\d+·|.*连云港市志.*·\d+·|·\d+·.*|.*连云港市志.*)$")


def norm(s):
    return WS.sub("", s)


def digit_ratio(s):
    return sum(1 for c in s if c.isdigit()) / max(len(s), 1)


def boundary_map(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    m = [0] * (len(a) + 1)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                m[i1 + k] = j1 + k
        m[i1] = j1
        m[i2] = j2
    last = 0
    for i in range(len(a) + 1):
        if m[i] == 0 and i != 0:
            m[i] = last
        else:
            last = m[i]
    return m


def v2_pages(md_path):
    """v2 文件 → [(page_no, norm_text)] 按锚序。"""
    t = io.open(md_path, encoding="utf-8").read()
    pages, cur, buf = [], None, []
    for blk in re.split(r"(<!--\s*page-anchor:\s*[A-Z0-9\-]+\s*-->)", t):
        s = blk.strip()
        m = re.match(r"<!--\s*page-anchor:\s*(?:LYG-S-)?0*(\d+)\s*-->", s)
        if m:
            if cur is not None:
                pages.append((cur, norm("".join(buf))))
            cur, buf = int(m.group(1)), []
            continue
        if s.startswith("<!--") or s.startswith("#"):
            continue
        buf.append(re.sub(r"\{\{[^}]*\}\}", "", s))
    if cur is not None:
        pages.append((cur, norm("".join(buf))))
    return pages


def engine_stream(part, engine, start, end):
    """引擎逐页 JSON → (整卷流, {char_pos: page})"""
    chars = []
    pos2page = {}
    for page in range(start, end + 1):
        p = OCR_BASE / engine / part / f"page_{page:04d}.json"
        if not p.exists():
            continue
        d = json.loads(io.open(p, encoding="utf-8").read())
        base = len(chars)
        txt = norm("".join(l["text"] for l in d["lines"]))
        chars.append(txt)
        for k in range(len(txt)):
            pos2page[base + k] = page
    return "".join(chars), pos2page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True)
    ap.add_argument("--v2md", required=True)
    ap.add_argument("--pages", required=True)
    args = ap.parse_args()
    start, end = (int(x) for x in args.pages.split("-"))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    v2pg = v2_pages(V2 / args.v2md)
    v2pg = [(p, t) for p, t in v2pg if start <= p <= end]
    v2_stream = "".join(t for _, t in v2pg)
    # v2 字符位置 → 页
    v2_pos2page = {}
    off = 0
    for p, t in v2pg:
        for k in range(len(t)):
            v2_pos2page[off + k] = p
        off += len(t)

    pd, _ = engine_stream(args.part, "paddle", start, end)
    rp, _ = engine_stream(args.part, "rapid", start, end)
    map_pd = boundary_map(v2_stream, pd)
    map_rp = boundary_map(v2_stream, rp)

    flags = []
    stats = Counter()
    sm = difflib.SequenceMatcher(None, v2_stream, pd, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        seg_v2 = v2_stream[i1:i2]
        seg_pd = pd[j1:j2]
        seg_rp = rp[map_rp[i1]:map_rp[i2]] if map_rp[i2] >= map_rp[i1] else ""
        seg_all = seg_v2 or seg_pd
        if not seg_all or not HAN.search(seg_all):
            continue
        page = v2_pos2page.get(i1) or v2_pos2page.get(max(i1 - 1, 0), 0)
        if HEADER_PAT.match(seg_pd or "") or HEADER_PAT.match(seg_v2 or ""):
            stats["header_noise"] += 1
            continue
        if digit_ratio(seg_all) > 0.5:
            stats["table_residue"] += 1
            continue
        ctx = (v2_stream[max(0, i1 - 12): i1] + "【" + (seg_v2 or "⟨无⟩") + "】"
               + v2_stream[i2: i2 + 12])
        rec = {"page": page, "v2": seg_v2, "paddle": seg_pd, "rapid": seg_rp, "ctx": ctx}
        if tag == "replace" and seg_v2 and seg_pd:
            if seg_v2 == seg_rp:
                stats["paddle_noise"] += 1
                continue
            if seg_pd == seg_rp:
                rec["type"] = "FLAG_A"
            else:
                rec["type"] = "FLAG_B"
        elif tag == "delete":
            rec["type"] = "FLAG_X"
        elif tag == "insert":
            rec["type"] = "FLAG_M"
            rec["ctx"] = (v2_stream[max(0, i1 - 12): i1] + "⟨漏⟩" + v2_stream[i1: i1 + 12])
        else:
            continue
        flags.append(rec)
        stats[rec["type"]] += 1

    summary = {"part": args.part, "v2md": args.v2md, "pages": f"{start}-{end}",
               "v2_chars": len(v2_stream), "paddle_chars": len(pd), "rapid_chars": len(rp),
               "stats": dict(stats)}
    io.open(OUT_DIR / f"{args.part}_consensus.json", "w", encoding="utf-8").write(
        json.dumps({"summary": summary, "flags": flags}, ensure_ascii=False, indent=1))

    lines = [f"# {args.part} 三方共识比对（{start}-{end}，整卷流对齐）", "",
             f"- v2 流 {len(v2_stream)} 字 | paddle {len(pd)} 字 | rapid {len(rp)} 字",
             f"- FLAG_A 疑似v2错字: {stats.get('FLAG_A', 0)} | FLAG_B 三方不同: {stats.get('FLAG_B', 0)}",
             f"- FLAG_M 疑漏: {stats.get('FLAG_M', 0)} | FLAG_X 疑多: {stats.get('FLAG_X', 0)}",
             f"- 噪声过滤: 页眉 {stats.get('header_noise', 0)} | 表格残文 {stats.get('table_residue', 0)} | paddle单方 {stats.get('paddle_noise', 0)}",
             "", "## FLAG_A 明细", ""]
    for f in flags:
        if f["type"] == "FLAG_A":
            lines.append(f"- p{f['page']} v2「{f['v2']}」×引擎「{f['paddle']}」 …{f['ctx']}…")
    lines += ["", "## FLAG_B 明细", ""]
    for f in flags:
        if f["type"] == "FLAG_B":
            lines.append(f"- p{f['page']} v2「{f['v2']}」 pd「{f['paddle']}」 rp「{f['rapid']}」 …{f['ctx']}…")
    lines += ["", "## FLAG_M 明细（前100）", ""]
    n = 0
    for f in flags:
        if f["type"] == "FLAG_M" and n < 100:
            lines.append(f"- p{f['page']} 漏「{f['paddle'][:40]}」 …{f['ctx'][:70]}…")
            n += 1
    io.open(OUT_DIR / f"{args.part}_consensus.md", "w", encoding="utf-8",
            newline="\n").write("\n".join(lines) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
