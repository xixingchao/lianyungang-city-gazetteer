# -*- coding: utf-8 -*-
"""
重启批次2：以 7-06 阅读版正文为底回填重建 body_chapters_v2/

背景（docs/项目重启计划_20261001.md）：阅读版含约25万字修复内容不在任何源文件，
源里另有68万字残文已被阅读版清除。因此 v2 = 阅读版文本 + 旧源页锚回贴。

做法：
1. 阅读版按 h1-h4/p/表格占位 切成有序块，规范化为连续字符流（记录每块区间）。
2. 旧源（body_chapters_reflowed，12文件按书序）按页锚分块，每锚取多个规范化特征片段。
3. 前向滑窗对齐：reader_stream.find(特征, rp, rp+WINDOW)，锚定每个页锚在阅读版中的位置。
   未匹配的锚（残文清除页/整段改写页）由前后已匹配锚的区间插值覆盖。
4. 按锚区间把阅读版块分配到锚，输出 v2 章节文件：
   - h2/h3/h4 → ##/###/####，表格 → {{STRUCTURED_TABLE:表ID}}，正文段原样
   - 首个匹配锚之前的阅读版块（书名/目录等）写 00_卷首杂项.md
   - 未获块的锚保留锚行 + 未回贴标记（锚不丢）

验收口径：锚匹配率、未回贴锚数、v2规范文本对阅读版覆盖率(应≥99%)。
"""
import io
import re
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "workbench" / "body_chapters_reflowed"
DST = ROOT / "workbench" / "body_chapters_v2"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_DIR = ROOT / "output" / "reports" / "progress"

K = 40          # 特征片段长度（规范化后）
WINDOW = 250000  # 前向搜索窗口

BOOK_ORDER = [
    "序与凡例.md",
    "总述与大事记.md",
    "第一卷_自然环境.md",
    "第二卷_建置区划.md",
    "第三卷_区县概况.md",
    "第四卷_人口（part01_部分）.md",
    "第四卷至第十卷（part02）.md",
    "第十卷至第十六卷（part03）.md",
    "第十七卷至第二十九卷（中part01）.md",
    "第三十卷至第四十二卷（中part02）.md",
    "第四十三卷至第五十一卷（下part01）.md",
    "第五十二卷至第六十卷及附录（下part02）.md",
]

NORM_RE = re.compile(r"[\s，。、；：！？“”‘’（）《》〈〉…·\-~～%‰]")
TABLE_ID_RE = re.compile(r"表ID[:：]\s*([^\s；;，,]+)")


def norm(s):
    return NORM_RE.sub("", s)


# ---------- 阅读版切块 ----------
def load_reader_blocks():
    t = io.open(READER, encoding="utf-8", errors="ignore").read()
    body = re.search(r"<body.*?>(.*)</body>", t, re.S).group(1)
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", body, flags=re.S)

    blocks = []  # (kind, plain_text)
    pos = 0
    pattern = re.compile(
        r"<h([1-5])[^>]*>(.*?)</h\1>|<p[^>]*>(.*?)</p>|<table[^>]*>.*?</table>", re.S)
    last_p_text = ""
    for m in pattern.finditer(body):
        if m.group(1):       # heading
            txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            blocks.append(("h" + m.group(1), txt))
        elif m.group(3) is not None:  # p
            txt = re.sub(r"<[^>]+>", "", m.group(3)).strip()
            txt = re.sub(r"\s+", " ", txt)
            last_p_text = txt
            if txt:
                blocks.append(("p", txt))
        else:                # table
            tid_m = TABLE_ID_RE.search(last_p_text)
            tid = tid_m.group(1) if tid_m else f"未编号-{len(blocks):04d}"
            blocks.append(("table", tid))
    # 去掉目录导航等无关块由后续 front-matter 截断处理
    return blocks


# ---------- 源锚块 ----------
def load_source_anchors():
    """返回 [(file, anchor_id, [para_text...], norm_text)] 按书序。"""
    anchors = []
    for rel in BOOK_ORDER:
        p = SRC / rel
        t = io.open(p, encoding="utf-8").read()
        t = re.sub(r"^#.*$", "", t, flags=re.M)
        t = re.sub(r"<!--\s*精修说明[^>]*-->", "", t)
        cur_id, cur_paras = None, []
        def flush():
            if cur_id is not None:
                anchors.append((rel, cur_id, list(cur_paras), norm("".join(cur_paras))))
        # 简单顺序扫描
        out = []
        for blk in re.split(r"(<!--\s*page-anchor:\s*[^>]*-->)", t):
            s = blk.strip()
            if s.startswith("<!--") and "page-anchor" in s:
                flush()
                cur_id = re.search(r"page-anchor:\s*([A-Z0-9\-]+)", s).group(1)
                cur_paras = []
                continue
            for para in s.split("\n\n"):
                ps = para.strip()
                if not ps or ps.startswith("<!--") or ps.startswith("#"):
                    continue
                cur_paras.append(ps)
        flush()
    return anchors


def candidates_for(ntext):
    """一个锚的规范化文本 → 特征片段候选（长优先）。"""
    cands = []
    if len(ntext) >= K + 5:
        cands = [ntext[:K], ntext[len(ntext)//2 - K//2: len(ntext)//2 + K//2], ntext[-K:]]
    elif len(ntext) >= 20:
        cands = [ntext]
    else:
        cands = [ntext] if ntext else []
    # 去重保序
    seen, out = set(), []
    for c in cands:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def main():
    DST.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    blocks = load_reader_blocks()
    # 阅读版字符流与块区间
    rd_stream_parts = []
    rd_spans = []  # (start, end, idx)
    off = 0
    for i, (kind, txt) in enumerate(blocks):
        nt = norm(txt)
        rd_stream_parts.append(nt)
        rd_spans.append((off, off + len(nt), i))
        off += len(nt)
    rd_stream = "".join(rd_stream_parts)

    anchors = load_source_anchors()
    print("reader blocks:", len(blocks), "stream chars:", len(rd_stream))
    print("source anchors:", len(anchors))

    # 前向对齐
    rp = 0
    anchor_pos = []          # (rel, id, pos or None)
    last_pos = -1
    for rel, aid, paras, ntext in anchors:
        cands = candidates_for(ntext)
        found = None
        for c in cands:
            pos = rd_stream.find(c, rp, rp + WINDOW)
            if pos != -1:
                if pos == last_pos and len(cands) > 1:
                    continue  # 与上一锚同位，换候选
                found = pos
                break
        if found is None:
            anchor_pos.append((rel, aid, None))
        else:
            anchor_pos.append((rel, aid, found))
            last_pos = found
            rp = found

    matched = [(rel, aid, pos) for rel, aid, pos in anchor_pos if pos is not None]
    print(f"anchors matched: {len(matched)}/{len(anchor_pos)}")

    # 分配阅读版块到锚：块 start ∈ [pos_k, pos_{k+1}) → anchor_k
    assign = {i: [] for i in range(len(anchor_pos))}   # anchor_idx -> block idx list
    front_matter = []
    a = 0
    for start, end, bi in rd_spans:
        # 找到最后一个 pos <= start 的已匹配锚
        while a + 1 < len(anchor_pos):
            nxt = None
            j = a + 1
            while j < len(anchor_pos):
                if anchor_pos[j][2] is not None:
                    nxt = j
                    break
                j += 1
            if nxt is not None and start >= anchor_pos[nxt][2]:
                a = nxt
            else:
                break
        if anchor_pos[a][2] is None or start < anchor_pos[a][2]:
            front_matter.append(bi)
        else:
            assign[a].append(bi)

    assigned_blocks = sum(len(v) for v in assign.values())
    print("blocks assigned:", assigned_blocks, "front matter:", len(front_matter))

    # 输出 v2
    per_file = Counter()
    unmatched_report = []
    fhs = {}
    for idx, (rel, aid, pos) in enumerate(anchor_pos):
        if rel not in fhs:
            fhs[rel] = io.open(DST / Path(rel).name, "w", encoding="utf-8", newline="\n")
            fhs[rel].write(f"# {Path(rel).stem}\n\n")
        fh = fhs[rel]
        fh.write(f"<!-- page-anchor: {aid} -->\n\n")
        blks = assign.get(idx, [])
        if not blks:
            fh.write("<!-- 未回贴：阅读版无对应文本（残文清除或整段改写） -->\n\n")
            unmatched_report.append((rel, aid))
        for bi in blks:
            kind, txt = blocks[bi]
            if kind == "h2":
                fh.write(f"## {txt}\n\n")
            elif kind == "h3":
                fh.write(f"### {txt}\n\n")
            elif kind == "h4":
                fh.write(f"#### {txt}\n\n")
            elif kind == "h5":
                fh.write(f"##### {txt}\n\n")
            elif kind == "table":
                fh.write(f"{{{{STRUCTURED_TABLE:{txt}}}}}\n\n")
            else:
                fh.write(f"{txt}\n\n")
        per_file[rel] += len(blks)
    for fh in fhs.values():
        fh.close()

    if front_matter:
        fm = io.open(DST / "00_卷首杂项.md", "w", encoding="utf-8", newline="\n")
        fm.write("# 卷首杂项（首个页锚前的阅读版块，多为书名/生成说明/目录，批次6决定取舍）\n\n")
        for bi in front_matter:
            kind, txt = blocks[bi]
            fm.write(f"{txt}\n\n")
        fm.close()

    # 覆盖率：已分配块的规范字符数 / 阅读版字符流
    assigned_chars = sum(rd_spans[bi][1] - rd_spans[bi][0]
                         for v in assign.values() for bi in v)
    fm_chars = sum(rd_spans[bi][1] - rd_spans[bi][0] for bi in front_matter)
    coverage = 100 * assigned_chars / max(len(rd_stream) - fm_chars, 1)

    rpt = [
        "# 2026-10-01 批次2：body_chapters_v2 回填重建",
        "",
        f"- 阅读版块：{len(blocks)}（front matter {len(front_matter)}）",
        f"- 源页锚：{len(anchor_pos)}，匹配 {len(matched)}（{100*len(matched)/len(anchor_pos):.1f}%），未回贴 {len(unmatched_report)}",
        f"- 分配到锚的块字符覆盖率（除卷首）：{coverage:.2f}%",
        "",
        "| 文件 | 分配块数 |", "|---|---:|",
    ]
    for rel, n in per_file.items():
        rpt.append(f"| {rel} | {n} |")
    rpt += ["", "## 未回贴锚清单", ""]
    for rel, aid in unmatched_report:
        rpt.append(f"- {rel} :: {aid}")
    io.open(REPORT_DIR / "20261001_批次2_v2回填重建.md", "w", encoding="utf-8",
            newline="\n").write("\n".join(rpt) + "\n")

    print(json.dumps({
        "anchors": len(anchor_pos), "matched": len(matched),
        "unmatched": len(unmatched_report),
        "blocks": len(blocks), "front_matter": len(front_matter),
        "coverage_pct": round(coverage, 2),
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
