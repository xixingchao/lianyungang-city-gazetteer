# -*- coding: utf-8 -*-
"""Repair second verified 进人/进入 residual group."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_enter_residues_batch381_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_enter_residues_batch381_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_进入残留补修第三百八十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 进入残留补修第三百八十一批"

PATHS = [
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]

EVIDENCE = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
EVIDENCE_TERMS = [
    "城市供水进入了",
    "进入集市交易",
    "已进入国内",
    "进入国际市场",
    "进入试产阶段",
    "进入附近城乡市场",
    "进入机械化阶段",
    "进入批量生产阶段",
    "进入省4家联营厂",
    "一进入山谷",
    "青口港、大浦港进入",
    "农民进入市场",
    "供应进入连云港港口",
    "进入支出基数",
    "进入了法制轨道",
    "进入货物",
    "进入崩溃",
    "进入新的建设与发展时期",
    "进入各级工会",
    "进入中共连云港市第四届委员会",
    "进入新的历史时期",
    "进入普通家庭",
    "进入系统、规范",
    "肉鸡加工进入",
    "蛋制品进入",
    "中草药进入",
    "进入20世纪80年代",
    "进入临床验证",
    "进入了美国",
    "进入全面发展的新时期",
    "进入80年代",
    "进入恢复、发展时期",
    "进入安装阶段",
    "进入我国内水域",
    "进入县处级",
    "进入就业年龄",
    "进入60年代",
]

PHRASES = [
    ("供水", "城市供水进人了一", "城市供水进入了一"),
    ("市场", "进人集市交易", "进入集市交易"),
    ("水产", "已进人国内", "已进入国内"),
    ("水产", "进人国际市场", "进入国际市场"),
    ("试产", "进人试产阶段", "进入试产阶段"),
    ("家具", "进人附近城乡市场", "进入附近城乡市场"),
    ("机械化", "进人机械化阶段", "进入机械化阶段"),
    ("量产", "进人批量生产阶段", "进入批量生产阶段"),
    ("服装", "进人省4家联营厂", "进入省4家联营厂"),
    ("景区", "一进人山谷", "一进入山谷"),
    ("商业", "青口港、大浦港进人", "青口港、大浦港进入"),
    ("粮食", "农民进人市场", "农民进入市场"),
    ("外轮", "供应进人连云港港口", "供应进入连云港港口"),
    ("财政", "应进人支出基数", "应进入支出基数"),
    ("税务", "进人了法制轨道", "进入了法制轨道"),
    ("税务", "进人货物", "进入货物"),
    ("金融", "进人崩溃", "进入崩溃"),
    ("党史", "进人新的建设与发展时期", "进入新的建设与发展时期"),
    ("党史", "进人各级工会", "进入各级工会"),
    ("党史", "人进人中共连云港市第四届委员会", "人进入中共连云港市第四届委员会"),
    ("政协", "进人新的历", "进入新的历"),
    ("广电", "进人普通家庭", "进入普通家庭"),
    ("体育", "进人系统、规范", "进入系统、规范"),
    ("食品", "肉鸡加工进人", "肉鸡加工进入"),
    ("食品", "蛋制品进人", "蛋制品进入"),
    ("医药", "中草药进人", "中草药进入"),
    ("医药", "进人20世纪80年代", "进入20世纪80年代"),
    ("医药", "并进人临床验证", "并进入临床验证"),
    ("医药", "进人了美国", "进入了美国"),
    ("化工", "进人全面发展的新时期", "进入全面发展的新时期"),
    ("工业", "进人80年代", "进入80年代"),
    ("工业", "进人恢复、发展时期", "进入恢复、发展时期"),
    ("电力", "进人安装阶段", "进入安装阶段"),
    ("港监", "进人我国内水域", "进入我国内水域"),
    ("干部", "进人县处级", "进入县处级"),
    ("就业", "进人就业年龄", "进入就业年龄"),
    ("教育", "进人60年代", "进入60年代"),
]

@dataclass(frozen=True)
class Replacement:
    label: str
    path: Path
    old: str
    new: str

REPLACEMENTS = [Replacement(label, path, old, new) for path in PATHS for label, old, new in PHRASES]
OLD_TERMS = [old for _, old, _ in PHRASES]
NEW_TERMS = [new for _, _, new in PHRASES]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def apply_replacements() -> list[dict[str, object]]:
    results = []
    for item in REPLACEMENTS:
        text = read(item.path)
        count = text.count(item.old)
        if count:
            item.path.write_text(text.replace(item.old, item.new), encoding="utf-8")
        after = read(item.path)
        results.append({"label": item.label, "path": rel(item.path), "old": item.old, "new": item.new, "old_count": count, "new_count_after": after.count(item.new)})
    return results


def collect_counts(paths: list[Path], terms: list[str]) -> dict[str, dict[str, int]]:
    counts = {}
    for path in paths:
        text = read(path)
        hits = {term: text.count(term) for term in terms if text.count(term)}
        if hits:
            counts[rel(path)] = hits
    return counts


def render(results, evidence, old_counts, new_counts) -> str:
    total = sum(int(item["old_count"]) for item in results)
    by_label = defaultdict(int)
    for item in results:
        by_label[item["label"]] += int(item["old_count"])
    lines = [
        "# 进入残留补修 batch381",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行正文源稿、上册/全书汇总中由正式 reader 对证的第二组 `进人 -> 进入` 完整短语。",
        "- 原则：只修完整语境；保留 `引进人才`、`先进人物`、`新进人员` 等合法词；暂不处理断句不明的 `进人设...`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 分项统计",
    ]
    for label in sorted(by_label):
        lines.append(f"- {label}：{by_label[label]} 处。")
    lines.extend(["", "## 证据位置"])
    for term, hits in evidence.items():
        compact = "，".join(str(i) for i in hits) or "未命中"
        lines.append(f"- `output/final_reader/连云港市志_全书.html` 行 {compact}：`{term}`")
    lines.extend(["", "## 旧词残留检查"])
    if old_counts:
        for path, hits in old_counts.items():
            compact = "，".join(f"`{term}` {count}" for term, count in hits.items())
            lines.append(f"- `{path}`：{compact}")
    else:
        lines.append("- 检查范围未见本批旧词残留。")
    lines.extend(["", "## 新词命中"])
    for path, hits in new_counts.items():
        compact = "，".join(f"`{term}` {count}" for term, count in hits.items())
        lines.append(f"- `{path}`：{compact}")
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, old_counts: dict[str, dict[str, int]]) -> None:
    summary_old = old_counts.get("workbench/body_chapters/连云港市志_全书_正文汇总.md", {})
    block = f"""{MARKER}

- 依据正式 reader 证据，补修市场、产业阶段、财政税务、金融、党史、医药、工业、电力、干部就业、教育等语境中的第二组 `进人 -> 进入` 完整短语，共 {total} 处。
- 代表修复：`进人集市交易 -> 进入集市交易`、`进人试产阶段 -> 进入试产阶段`、`进人机械化阶段 -> 进入机械化阶段`、`进人崩溃 -> 进入崩溃`、`进人新的建设与发展时期 -> 进入新的建设与发展时期`、`进人安装阶段 -> 进入安装阶段`。
- 本批后全书正文汇总旧词检查剩余：`进人集市交易` {summary_old.get('进人集市交易', 0)}，`进人试产阶段` {summary_old.get('进人试产阶段', 0)}，`进人安装阶段` {summary_old.get('进人安装阶段', 0)}，`进人就业年龄` {summary_old.get('进人就业年龄', 0)}。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作 `人 -> 入` 全局替换；合法 `引进人才`、`先进人物`、`新进人员` 等继续保留；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_enter_residues_batch381_20260708.md`；进度：`output/reports/progress/20260708_进入残留补修第三百八十一批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:]), encoding="utf-8")


def main() -> None:
    results = apply_replacements()
    evidence = {term: line_hits(EVIDENCE, term) for term in EVIDENCE_TERMS}
    old_counts = collect_counts(PATHS, OLD_TERMS)
    new_counts = collect_counts(PATHS, NEW_TERMS)
    total = sum(int(item["old_count"]) for item in results)
    report = render(results, evidence, old_counts, new_counts)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "results": results, "evidence": evidence, "old_counts": old_counts, "new_counts": new_counts}
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total, old_counts)
    print(f"total={total}")
    print(json.dumps(old_counts, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
