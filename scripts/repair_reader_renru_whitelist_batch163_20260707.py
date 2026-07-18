# -*- coding: utf-8 -*-
"""Repair high-confidence 人/入 OCR residues by phrase whitelist."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_renru_whitelist_batch163_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_renru_whitelist_batch163_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人入残字白名单补修第一百六十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["人社", "人会", "人库", "人选", "人厂", "人伍", "加人", "人驻"]

REPLACEMENTS = [
    ("人社农户", "入社农户"),
    ("人社股金", "入社股金"),
    ("全部人社", "全部入社"),
    ("规划人社", "规划入社"),
    ("在人社以后", "在入社以后"),
    ("没有人社以前", "没有入社以前"),
    ("自从人社以后", "自从入社以后"),
    ("人会工人", "入会工人"),
    ("前人会的会员", "前入会的会员"),
    ("攻人会稽", "攻入会稽"),
    ("瓶酒人库", "瓶酒入库"),
    ("人库公粮", "入库公粮"),
    ("人库时", "入库时"),
    ("一步人库", "一步入库"),
    ("征购人库", "征购入库"),
    ("人库粮质", "入库粮质"),
    ("人库合同", "入库合同"),
    ("实际人库", "实际入库"),
    ("人市库", "入市库"),
    ("实际人库数", "实际入库数"),
    ("利润人库", "利润入库"),
    ("征实人库", "征实入库"),
    ("并征人库", "并征入库"),
    ("增加了人库额", "增加了入库额"),
    ("及时人库", "及时入库"),
    ("盐税人库", "盐税入库"),
    ("组织人库", "组织入库"),
    ("实物人库", "实物入库"),
    ("当年人库", "当年入库"),
    ("税年人库", "税款入库"),
    ("编自、人库", "编目、入库"),
    ("清理人库", "清理入库"),
    ("出人库登记", "出入库登记"),
    ("直接人库", "直接入库"),
    ("穿房人库", "穿房入库"),
    ("作品人选", "作品入选"),
    ("人选参展", "入选参展"),
    ("人选江苏", "入选江苏"),
    ("人选全国", "入选全国"),
    ("人选省商业", "入选省商业"),
    ("人选山东", "入选山东"),
    ("人选国家", "入选国家"),
    ("人厂社员", "入厂社员"),
    ("前人伍", "前入伍"),
    ("农村人伍", "农村入伍"),
    ("城镇人伍", "城镇入伍"),
    ("义务兵人伍", "义务兵入伍"),
    ("批准人伍", "批准入伍"),
    ("的人伍条件", "的入伍条件"),
    ("青年人伍当兵", "青年入伍当兵"),
    ("加人中国共产党", "加入中国共产党"),
    ("加人共产党", "加入共产党"),
]

LEFT_UNTOUCHED = [
    "`人驻` 当前为 `留人驻船`、`专人驻场所`、`若干人驻扎/驻守` 等合法相邻字，未处理。",
    "`人选` 中 `人选名单`、`代表人选`、`组成人员的人选` 等合法候选人语义保留。",
    "`人会` 中 `负责人会议`、`老人会`、`穷人会`、`派人会同`、`人人会买彩签` 等合法相邻字保留。",
    "未做任何裸 `人 -> 入` 或裸词全局替换。",
    "未打开、展示或嵌入图片。",
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 60):m.start() + 90].replace("\n", " ") for m in re.finditer(term, plain)]


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    pattern_counts = {old: 0 for old, _ in REPLACEMENTS}
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after = before
        file_patterns = []
        for old, new in REPLACEMENTS:
            count = after.count(old)
            if count:
                after = after.replace(old, new)
                pattern_counts[old] += count
                file_patterns.append({"old": old, "new": new, "count": count})
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "changed": sum(item["count"] for item in file_patterns),
            "before_terms": {term: before_plain.count(term) for term in TERMS},
            "after_terms": {term: after_plain.count(term) for term in TERMS},
            "patterns": file_patterns,
            "remaining_contexts": {term: contexts(after_plain, term) for term in TERMS if after_plain.count(term)},
        })

    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader high-confidence 人/入 OCR residue whitelist repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人入残字白名单补修第一百六十三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 按短语白名单修复 `入社/入会/入库/入选/入厂/入伍/加入` 语境。",
        "- 未做裸 `人 -> 入` 或裸词全局替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 替换项",
        "",
    ]
    for old, count in sorted(((k, v) for k, v in pattern_counts.items() if v), key=lambda x: x[0]):
        lines.append(f"- `{old}` -> `{dict(REPLACEMENTS)[old]}`：{count} 处")
    lines.extend(["", "## 文件", ""])
    for item in results:
        after_bits = ", ".join(f"{k}:{v}" for k, v in item["after_terms"].items() if v)
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处；剩余 {after_bits or '无'}")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百六十三批：人入白名单"
    upsert_memory(marker, f"""
{marker}

- 核对当前阅读稿 `人社/人会/人库/人选/人厂/人伍/加人/人驻` 上下文，按短语白名单修复 `入社/入会/入库/入选/入厂/入伍/加入` 高置信残字。
- 本批修复 {total} 处；报告：`output/reports/reader_renru_whitelist_batch163_20260707.md`。
- 保留 `负责人会议`、`老人会`、`穷人会`、`代表人选/人选名单`、`留人驻船/人驻扎` 等合法相邻字；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
