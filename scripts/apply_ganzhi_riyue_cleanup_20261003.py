# -*- coding: utf-8 -*-
"""收尾轮：干支（己/已、壬/王）与「日/曰」误识批量规范化。"""
import argparse
import glob
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2_GLOB = os.path.join(ROOT, "workbench", "body_chapters_v2", "*.md")
READER = os.path.join(ROOT, "output", "final_reader", "连云港市志_全书.html")

FIXES = [
    # 干支
    ("岁在已未", "岁在己未", 1),
    ("嘉靖乙已三月", "嘉靖乙巳三月", 1),
    ("明隆庆王申秋日", "明隆庆壬申秋日", 1),
    ("岁次王申孟冬", "岁次壬申孟冬", 1),
    ("岁次王辰季冬", "岁次壬辰季冬", 1),
    # 日/曰
    ("唐·崔逸纪日：", "唐·崔逸纪曰：", 1),
    ("诗日", "诗曰", 37),
    ("名日十八盘", "名曰十八盘", 1),
    ("名日灵泉", "名曰灵泉", 1),
    ("名日“照海亭”", "名曰“照海亭”", 1),
    ("名日永安堤", "名曰永安堤", 1),
    ("铭日：“玉女窗”", "铭曰：“玉女窗”", 1),
    ("语日：“乞火不若取燧", "语曰：“乞火不若取燧", 1),
    ("后代其诗日因巡来至", "后代其诗曰因巡来至", 1),
]

PROBES = ["壬戍", "甲戍", "丙戍", "庚戍", "戊戍", "戍子", "戍午", "戍辰", "戍申", "戍戌", "癸亥", "诗日"]


def counts(text, s):
    return text.count(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    v2_files = sorted(glob.glob(V2_GLOB))
    v2_text = {f: io.open(f, encoding="utf-8").read() for f in v2_files}
    html = io.open(READER, encoding="utf-8").read()

    ok = 0
    for old, new, exp in FIXES:
        n_v2 = sum(counts(t, old) for t in v2_text.values())
        if n_v2 == exp:
            ok += 1
        else:
            files_hit = [os.path.basename(f) for f, t in v2_text.items() if old in t]
            print(f"!! v2={n_v2} html={counts(html, old)} exp={exp} | {old} | {files_hit}")
    print(f"可应用: {ok} / {len(FIXES)}")
    if args.dry:
        for s in PROBES:
            n = 0
            for f, t in v2_text.items():
                i = t.find(s)
                while i >= 0 and n < 3:
                    ln = t.count("\n", 0, i) + 1
                    print(f"  [{s}] {os.path.basename(f)[:16]} L{ln}: ...{t[max(0,i-40):i+len(s)+40]}...".replace(chr(10), '⏎'))
                    n += 1
                    i = t.find(s, i + 1)
        print("(dry)")
        return

    n = 0
    for old, new, exp in FIXES:
        if sum(counts(t, old) for t in v2_text.values()) != exp:
            print(f"SKIP {old}")
            continue
        for f in v2_files:
            if old in v2_text[f]:
                v2_text[f] = v2_text[f].replace(old, new)
        if old in html:
            html = html.replace(old, new)
        n += 1
    for f in v2_files:
        io.open(f, "w", encoding="utf-8", newline="").write(v2_text[f])
    io.open(READER, "w", encoding="utf-8", newline="").write(html)
    print(f"已写入 {n} 组修正")


if __name__ == "__main__":
    main()
