# -*- coding: utf-8 -*-
"""批次5-结构化：vol59 48页转录 → 词典模式 JSON/CSV

输出（workbench/volume59/structured/）:
  vocab_entries.json   词汇章词条（页19-45，约1600条）
  vocab_entries.csv    同上（词典模式表）
  char_rows.json       同音字汇行（页9-19）
  volume59_all.json    全卷结构（章节+页+块）
用法: python structure_volume59_20261002.py
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TR = ROOT / "workbench" / "volume59" / "transcripts"
OUT = ROOT / "workbench" / "volume59" / "structured"
OUT.mkdir(parents=True, exist_ok=True)

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹˥˦˧˨˩"
TONE_NUM = str.maketrans(SUP, "012345678955432")


def norm_ipa(s: str) -> str:
    return s.translate(TONE_NUM)


def parse_frontmatter(text: str):
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


IPA_RE = re.compile(r"[a-zA-Zɑ-ʯɐ-ʯʰ-˿]+[⁰¹²³⁴⁵⁶⁷⁸⁹˥˦˧˨˩\d]*")


def split_entry(line: str):
    """'- 词头　IPA　释义' → (word, ipa, gloss) 或 None"""
    body = line[2:].strip()
    parts = re.split(r"[\s\u3000]+", body, maxsplit=2)
    if len(parts) < 2:
        return None
    word = parts[0]
    # 找 IPA：含音标字符或声调上标
    ipa = parts[1] if len(parts) > 1 else ""
    gloss = parts[2] if len(parts) > 2 else ""
    if not any(ch in ipa for ch in SUP) and not any("\u0250" <= ch <= "\u02ff" for ch in ipa):
        # 第二段不是 IPA：把 word 后的内容整体当 word 的扩展
        return None
    return word, ipa, gloss


def is_ipa_token(tok: str) -> bool:
    if not tok:
        return False
    if any("\u4e00" <= ch <= "\u9fff" for ch in tok):
        return False
    if any(ch in SUP for ch in tok):
        return True
    return any(ord(ch) > 127 for ch in tok)


def main():
    vocab = []
    char_rows = []
    pages_meta = []
    for pno in range(1, 49):
        fp = TR / f"page_{pno:03d}.md"
        if not fp.exists():
            continue
        text = fp.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        section = None
        has_ch4 = "# 第四章" in text
        mode = "other"  # other / vocab / grammar
        for line in text.splitlines():
            if line.startswith("# 第四章"):
                mode = "vocab"
                continue
            if line.startswith("# 第五章"):
                mode = "grammar"
                continue
            if line.startswith("## "):
                section = line[3:].strip()
                continue
            if not line.startswith("- "):
                continue
            if section and section.startswith("页面注记"):
                continue
            body = line[2:].strip()
            if not body or body.startswith("**") or body.startswith("台账") or body.startswith("□ 字新增"):
                continue
            if mode == "other" and 20 <= pno <= 45 and not has_ch4:
                mode = "vocab"
            if mode == "vocab" and 19 <= pno <= 45:
                # 词汇章词条：优先按全角空格分字段（注解内的半角空格不切断）
                parts = re.split(r"\u3000+", body)
                if len(parts) < 2:
                    parts = re.split(r"[\s\u3000]+", body)
                if len(parts) >= 2:
                    word = parts[0]
                    rest = body[len(word):].strip()
                    # 词头后连续收集 IPA token（可多音节）
                    ipa_toks = []
                    while True:
                        m = re.match(r"([^\s\u3000]+)", rest)
                        if not m:
                            break
                        tok = m.group(1)
                        if is_ipa_token(tok) and not ipa_toks or (is_ipa_token(tok) and ipa_toks):
                            if is_ipa_token(tok):
                                ipa_toks.append(tok)
                                rest = rest[len(tok):].strip()
                                continue
                        break
                    ipa = " ".join(ipa_toks)
                    gloss = rest
                    if not ipa_toks:
                        ipa, gloss = "", body[len(word):].strip()
                    # 词头中的〔…〕注解拆出
                    notes = " ".join(re.findall(r"〔[^〕]*〕", word))
                    word_clean = re.sub(r"〔[^〕]*〕", "", word).strip()
                    if word_clean.startswith("（"):
                        continue  # 跨页 tail 标记行
                    vocab.append({
                        "page": pno,
                        "section": section or "",
                        "word": word_clean,
                        "word_raw": word,
                        "notes": notes,
                        "ipa": ipa,
                        "ipa_norm": norm_ipa(ipa),
                        "gloss": gloss,
                        "flags": {
                            "bai": "〔白" in body,
                            "wen": "〔文" in body,
                            "wenhao": "〔?" in body,
                            "kong": "□" in word_clean,
                        },
                        "raw": body,
                    })
            elif 9 <= pno <= 19:
                # 同音字汇行：'- 声母　①…②…'
                m = re.match(r"^([^\s\u3000]+)[\s\u3000]+(.+)$", body)
                if m:
                    char_rows.append({
                        "page": pno,
                        "initial": m.group(1),
                        "content": m.group(2),
                        "raw": body,
                    })
        pages_meta.append({"page": pno, "frontmatter": fm})

    (OUT / "vocab_entries.json").write_text(
        json.dumps(vocab, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(OUT / "vocab_entries.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["page", "section", "word", "ipa", "ipa_norm", "gloss",
                    "flag_bai", "flag_wen", "flag_uncertain", "flag_kong", "notes", "raw"])
        for e in vocab:
            fl = e["flags"]
            w.writerow([e["page"], e["section"], e["word"], e["ipa"], e["ipa_norm"],
                        e["gloss"], int(fl["bai"]), int(fl["wen"]),
                        int(fl["wenhao"]), int(fl["kong"]), e["notes"], e["raw"]])
    (OUT / "char_rows.json").write_text(
        json.dumps(char_rows, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "volume59_pages_meta.json").write_text(
        json.dumps(pages_meta, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"vocab entries: {len(vocab)}")
    print(f"char rows: {len(char_rows)}")
    from collections import Counter
    print("vocab by page:", dict(sorted(Counter(e['page'] for e in vocab).items())))
    noipa = [e for e in vocab if not e["ipa"]]
    print("无IPA行:", len(noipa))
    for e in noipa[:5]:
        print("  ", e["page"], e["raw"][:60])


if __name__ == "__main__":
    main()
