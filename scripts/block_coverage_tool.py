# -*- coding: utf-8 -*-
"""结构去重/错位分析工具：给 文件+行区间，报告该区间句子的「独有/重复」归属。

用法: py -3 scripts/block_coverage_tool.py <文件> <起行> <止行>
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"E:\codex_Learing\project_连云港市志\repo"


def norm(s):
    return re.sub(r"\s", "", s)


def main():
    fname, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    P = os.path.join(ROOT, "workbench", "body_chapters_v2", fname)
    lines = io.open(P, encoding="utf-8").read().split("\n")
    block = lines[a - 1:b]
    B = norm("".join(block))
    rest = norm("".join(lines[:a - 1]) + "".join(lines[b:]))
    sents = [s for s in re.split(r"(?<=[。！？])", B) if len(s) >= 8]
    missing = [s for s in sents if s not in rest]
    print(f"块 L{a}-L{b}: 归一 {len(B)} 字, {len(sents)} 句; 独有 {len(missing)} 句")
    for s in missing[:60]:
        print("  独有:", s[:130])
    # 反向：块内是否存在“块外也有的整句占比”
    dup = len(sents) - len(missing)
    print(f"重复句 {dup} / {len(sents)}")


if __name__ == "__main__":
    main()
