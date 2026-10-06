# -*- coding: utf-8 -*-
"""Fix 附录五(英文总述) + 跋 in reader and v2, sourced from the pre-reflow body_chapters copy.

- 英文总述: 3 个畸形嵌套 section（各带空「(七）」标题）+ 只剩末段 → 用原件重建全篇（二~九）。
- 跋: 缺失「高有为」与首段，且「连云港市，古称海州…」段游离在标题前（带杂散「（八）」）→ 按原件重建。
"""
from __future__ import annotations

import html as H
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "73153e8:workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
V2 = ROOT / "workbench" / "body_chapters_v2" / "第五十二卷至第六十卷及附录（下part02）.md"

HEAD_RE = re.compile(r"^(General\s+Summary|GENERAL\s*SUMMARY|Histroy of LianYunGang|GENERAL|SUMMARY|·\s*\d{4}|\d{3,4})\s*[:：.]?\s*$", re.I)
PAGENO_RE = re.compile(r"^[:：.]?\s*\d{4}\s*[:：.]?$")
CLEAN = [
    (r"Histroy of LianYunGang(?: City)?\s*[·:.]?\s*General Summary\s*[·:.]?\s*", " "),
    (r"General Summary\s*[·:.]?\s*\d{3,4}\s*[:：.]?\s*", " "),
    (r"\b\d{3,4}\s*[:：.]?\s*Histroy of LianYunGang(?: City)?\b\s*[:：.]?\s*", " "),
    (r"GENERAL\s*SUMMARY\s*", " "),
    (r"\bHistroy of LianYunGang\b\s*[·:.]?\s*", " "),
    (r"\b·\s*\d{3,4}\b", " "),
]
END_RE = re.compile(r"[.!?。！？…\"'\u2019\u201d)\]]$")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_old() -> str:
    return subprocess.run(["git", "show", OLD], cwd=ROOT, capture_output=True).stdout.decode("utf-8")


def clean_paras(lines: list[str], break_on_cn_end: bool = False) -> list[str]:
    paras: list[str] = []
    cur: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            if cur:
                paras.append(" ".join(cur)); cur = []
            continue
        if HEAD_RE.match(line) or PAGENO_RE.match(line) or line.startswith("<!--"):
            continue
        line = re.sub(r"^[:：.]\s*\d{4}\s*[:：.]?\s*", "", line)
        if cur and cur[-1].endswith("-"):
            cur[-1] = cur[-1][:-1] + line
        elif break_on_cn_end and cur and re.search(r"[。！？”》]$", cur[-1]):
            paras.append(" ".join(cur)); cur = [line]
        else:
            cur.append(line)
    if cur:
        paras.append(" ".join(cur))
    out: list[str] = []
    for p in paras:
        for _ in range(2):
            for pat, rep in CLEAN:
                p = re.sub(pat, rep, p)
        p = re.sub(r"\s+", " ", p)
        p = re.sub(r"\s+([,.;:])", r"\1", p)
        p = re.sub(r"^\d{3,4}\s*[:：]\s*", "", p)
        p = p.strip()
        if not p:
            continue
        if len(p) <= 12 and not re.search(r"[，。！？、：;,.]", p):
            if out:
                out[-1] = out[-1]  # keep previous
            out.append(p)
            continue
        if out and len(out[-1]) > 12 and not END_RE.search(out[-1]):
            out[-1] = (out[-1][:-1] if out[-1].endswith("-") else out[-1] + " ") + p
            continue
        out.append(p)
    # 部分标题拆段
    final: list[str] = []
    for p in out:
        for seg in re.split(r"([（(][一二三四五六七八九十]+[）)])", p):
            seg = seg.strip()
            if not seg:
                continue
            final.append(seg)
    return [p for p in final if p]


def english_paras(t: str) -> list[str]:
    k = t.find("GENERAL")
    tail = t.find("\n跋", k)
    region = t[k : tail if tail > k else len(t)]
    cut = region.find("SUMMARY")
    if cut >= 0:
        region = region[cut + len("SUMMARY"):]
    return clean_paras(region.split("\n"))


def ba_paras(t: str) -> list[str]:
    k = t.find("\n跋\n", t.find("LYG-2907"))
    k2 = t.find("\n编纂始末", k)
    region = t[k:k2]
    lines = [ln for ln in region.split("\n")]
    # 跳过标题行「跋」（含前置空行）
    while lines and lines[0].strip() in ("", "跋"):
        lines = lines[1:]
    return clean_paras(lines, break_on_cn_end=True)


def main() -> None:
    t = load_old()
    en = english_paras(t)
    ba = ba_paras(t)
    print("英文段落:", len(en), "| 字母:", sum(len(re.findall(r"[A-Za-z]", p)) for p in en))
    print("跋段落:", len(ba), "| 字:", sum(len(re.findall(r"[\u4e00-\u9fff]", p)) for p in ba))
    print("跋首段:", ba[0][:40], "| 跋末段:", ba[-1][:40])

    # ---- reader ----
    h = READER.read_text(encoding="utf-8")
    # 1) 英文块：从第一个 english-summary-section 到它所属的 </section>
    k = h.find('<section class="english-summary-section"')
    e = h.find("</section>", k) + len("</section>")
    en_html = "\n".join(
        ("<p><strong>%s</strong></p>" % esc(p)) if len(p) <= 4 else ("<p>%s</p>" % esc(p)) for p in en
    )
    h = h[:k] + en_html + h[e:]
    # 2) 跋：删掉游离的（八）段，重建跋节内容
    stray = "<p>（八）</p>"
    assert stray in h
    h = h.replace(stray, "", 1)
    kba = h.find('<h2 id="跋">跋</h2>')
    kend = h.find('<h2 id="编纂始末">', kba)
    seg = h[kba:kend]
    # 取出原有跋正文（保留其中的块：标题之后到下一个 h2）
    body_start = kba + len('<h2 id="跋">跋</h2>')
    old_body = h[body_start:kend]
    # 原正文里“连云港市，古称海州…”段（已在前面被移到标题前）在 old_body 中就是第一段之后的内容
    # 直接整体替换为原件重排版
    ba_html = "\n".join("<p>%s</p>" % esc(p) for p in ba)
    h = h[:body_start] + "\n" + ba_html + "\n" + h[kend:]
    READER.write_text(h, encoding="utf-8")
    print("reader 已更新")

    # ---- v2 ----
    v = V2.read_text(encoding="utf-8")
    k = v.find("### 五、总述(英文)")
    k2 = v.find("## 跋", k)
    en_md = "\n\n".join(en)
    v = v[: k + len("### 五、总述(英文)")] + "\n\n" + en_md + "\n\n" + v[k2:]
    # 跋
    kb = v.find("## 跋")
    kb2 = v.find("## 编纂始末", kb)
    v = v[: kb + len("## 跋")] + "\n\n" + "\n\n".join(ba) + "\n\n" + v[kb2:]
    V2.write_text(v, encoding="utf-8")
    print("v2 已更新")

    # 校验
    h2 = READER.read_text(encoding="utf-8")
    print("reader 校验: Yellow Sea:", h2.count("Yellow Sea"), "| 高有为:", h2.count("高有为"),
          "| (七）重复:", h2.count("<p><strong>(七）</strong></p>"), "| english-summary-section:", h2.count("english-summary-section"))


if __name__ == "__main__":
    main()
