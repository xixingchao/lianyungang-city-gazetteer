# -*- coding: utf-8 -*-
"""Repair high-confidence 干部 OCR residues written as 于部."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_ganbu_batch187_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ganbu_batch187_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_干部残字补修第一百八十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("工商管理于部", "工商管理干部"),
    ("税务于部", "税务干部"),
    ("选拔一批于部", "选拔一批干部"),
    ("提拔于部中", "提拔干部中"),
    ("机关于部文化学校", "机关干部文化学校"),
    ("要求于部系统地", "要求干部系统地"),
    ("各级于部写出", "各级干部写出"),
    ("轮训于部", "轮训干部"),
    ("名于部参加", "名干部参加"),
    ("党员于部", "党员干部"),
    ("老于部局", "老干部局"),
    ("基层于部分批", "基层干部分批"),
    ("部队于部和战士", "部队干部和战士"),
    ("社团管理于部", "社团管理干部"),
    ("县处级于部", "县处级干部"),
    ("主管于部", "主管干部"),
    ("专职宣传于部", "专职宣传干部"),
    ("调解于部", "调解干部"),
    ("领导于部", "领导干部"),
    ("组成的于部队", "组成的干部队"),
    ("抽调于部参加", "抽调干部参加"),
    ("一般于部", "一般干部"),
    ("于部文化补习学校", "干部文化补习学校"),
    ("专业技术于部", "专业技术干部"),
    ("于部缺额", "干部缺额"),
    ("提拨于部", "提拨干部"),
    ("后备于部", "后备干部"),
    ("转业于部", "转业干部"),
    ("部分于部南下", "部分干部南下"),
    ("调进于部", "调进干部"),
    ("抽调100名于部", "抽调100名干部"),
    ("两地于部", "两地干部"),
    ("调出于部", "调出干部"),
    ("学习的于部", "学习的干部"),
    ("成立于部保健委员会", "成立干部保健委员会"),
    ("名于部调整工资", "名干部调整工资"),
    ("名于部增加副食品供应", "名干部增加副食品供应"),
    ("患病于部减少", "患病干部减少"),
    ("于部考察工作", "干部考察工作"),
    ("城市于部和职工家属", "城市干部和职工家属"),
    ("基层工会于部", "基层工会干部"),
    ("离退休老于部", "离退休老干部"),
    ("采取于部联系", "采取干部联系"),
    ("优秀妇女于部", "优秀妇女干部"),
    ("于部中专", "干部中专"),
    ("科技于部进修学院", "科技干部进修学院"),
    ("文艺于部", "文艺干部"),
    ("文化于部培训班", "文化干部培训班"),
    ("基层宣传于部", "基层宣传干部"),
    ("新闻于部", "新闻干部"),
    ("药政管理专职于部", "药政管理专职干部"),
    ("市于部疗养院", "市干部疗养院"),
    ("51名于部乘海船", "51名干部乘海船"),
    ("三十名专业于部", "三十名专业干部"),
]

SKIPPED_BOUNDARIES = [
    "由于部分",
    "属于部管",
    "便于部队",
    "低于部颁",
    "由于部分泊位",
    "对于部调配",
    "剧自近于部",
    "机电排粮，于部每夜补助",
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(text: str, term: str) -> list[str]:
    return [text[max(0, m.start() - 50):m.start() + 100].replace("\n", " ") for m in re.finditer(re.escape(term), text)]


def upsert_memory(total: int, remaining: dict[str, int]) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百八十七批：干部候选"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    rem = ", ".join(f"{k}:{v}" for k, v in remaining.items())
    block = f"""
{marker}

- 核对当前阅读稿 `于部` 残留，按干部职务、培训、调配、宣传、药政、文艺、科技等明确语境定点修复为 `干部`。
- 本批仅使用完整短语白名单，修复 {total} 处；报告：`output/reports/reader_ganbu_batch187_20260707.md`。
- 保留 `由于部分/属于部管/便于部队/低于部颁/对于部调配/剧自近于部/机电排粮，于部每夜补助` 等边界；未打开、展示或嵌入图片。
- 修后当前 reader 纯文本 `于部` 剩余：{rem}。
""".strip()
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + block + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + block + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    totals = Counter()
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain(before)
        after = before
        per_file = []
        for old, new in REPLACEMENTS:
            count = after.count(old)
            if count:
                after = after.replace(old, new)
                per_file.append({"old": old, "new": new, "changed": count})
                totals[f"{old} -> {new}"] += count
        target.write_text(after, encoding="utf-8")
        after_plain = plain(after)
        results.append({
            "target": str(target),
            "changed": sum(item["changed"] for item in per_file),
            "before_plain_yubu": before_plain.count("于部"),
            "after_plain_yubu": after_plain.count("于部"),
            "remaining_contexts": contexts(after_plain, "于部"),
            "replacements": per_file,
        })
    total = sum(item["changed"] for item in results)
    remaining = {Path(item["target"]).name: item["after_plain_yubu"] for item in results}
    payload = {
        "time": now,
        "scope": "current reader high-confidence 干部 OCR repair",
        "changed": total,
        "replacements": dict(totals),
        "targets": results,
        "skipped_boundaries": SKIPPED_BOUNDARIES,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 干部残字补修第一百八十七批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 仅修复干部语境中 `于部` 对 `干部` 的 OCR 误识。",
        "- 使用完整短语白名单；未做 `于部 -> 干部` 全局替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处；剩余 `于部` {item['after_plain_yubu']} 处")
    lines.extend(["", "## 保留边界", ""])
    for term in SKIPPED_BOUNDARIES:
        lines.append(f"- `{term}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, remaining)
    print(json.dumps({"changed": total, "remaining": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
