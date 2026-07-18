# -*- coding: utf-8 -*-
"""Repair source-backed Shuyang/Shu water leftovers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_shuyang_water_batch363_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_shuyang_water_batch363_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总沭阳沭新水利残留补修第三百六十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总沭阳沭新水利残留补修第三百六十三批"

FULL = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
UP_PART02 = ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md"

CHECK_FILES = [
    FULL,
    UP_PART02,
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
]
CHECK_TERMS = ["新述河", "新沐河", "述南", "述北", "沐南", "沐北", "临沐县", "沂述", "沂沐", "人海口", "沐阳县", "准述", "沐新", "述城", "蕃北地涵", "蕃薇河"]


@dataclass(frozen=True)
class Replacement:
    path: Path
    old: str
    new: str
    evidence: str


REPLACEMENTS = [
    Replacement(FULL, "至沭阳县述城镇一线", "至沭阳县沭城镇一线", "上 part01 merged OCR line 6991 明确为“沭城镇一线”。"),
    Replacement(FULL, "开挖了石梁河水库、准述新\n河", "开挖了石梁河水库、淮沭新\n河", "上 part02 merged OCR line 16358 明确为“淮沭新河”。"),
    Replacement(FULL, "自沭阳县沐新闸至海州洪", "自沭阳县沭新闸至海州洪", "上 part03 merged OCR line 4874 明确为“沭新闸”。"),
    Replacement(FULL, "沭新渠又称蔷北干渠，自吴场村蕃北地涵调", "沭新渠又称蔷北干渠，自吴场村蔷北地涵调", "上 part03 merged OCR line 4876 明确为“蔷北地涵”。"),
    Replacement(FULL, "全长28公里。沐新\n河又称蕃北截水沟", "全长28公里。沭新\n河又称蔷北截水沟", "上 part03 merged OCR lines 4877-4878 明确为“沭新河又称蔷北截水沟”。"),
    Replacement(FULL, "自薇河顺场通航阐引江淮水", "自蔷薇河顺场通航阐引江淮水", "上 part03 merged OCR line 4878 明确为“自蔷薇河顺场通航阐引江淮水”。"),
    Replacement(FULL, "蕃北地涵又称沭新地涵。位于沐阳县、东海县交界的吴场村蕃薇河底", "蔷北地涵又称沭新地涵。位于沭阳县、东海县交界的吴场村蔷薇河底", "上 part03 merged OCR line 4908 明确为“蔷北地涵”“沭阳县”“蔷薇河底”。"),
    Replacement(FULL, "1972～1985年，蕃北地涵年均引江淮水", "1972～1985年，蔷北地涵年均引江淮水", "上 part03 merged OCR line 4914 明确为“蔷北地涵年均引江淮水”。"),
    Replacement(FULL, "输水渠6.8公里、述北\n第截洪沟10.1公里", "输水渠6.8公里、沭北\n第一截洪沟10.1公里", "上 part03 merged OCR line 5105 及同段正确稿明确为“沭北第一截洪沟”。"),
    Replacement(FULL, "小吴场入沐阳县境，在沭阳县境内", "小吴场入沭阳县境，在沭阳县境内", "中册 source 第三十卷至第四十二卷（中part02） line 146 为“入沭阳县境”。"),
    Replacement(FULL, "三棵树至述城", "三棵树至沭城", "中册 source 第三十卷至第四十二卷（中part02） line 147 为“至沭城”。"),
    Replacement(FULL, "古泊善后河西起沐阳县境", "古泊善后河西起沭阳县境", "中册 source 第三十卷至第四十二卷（中part02） line 1997 为“西起沭阳县境”。"),
    Replacement(FULL, "自沭阳县城与准述河连接", "自沭阳县城与淮沭河连接", "中册 source 第三十卷至第四十二卷（中part02） line 2002 为“与淮沭河连接”。"),
    Replacement(FULL, "中共沐阳县城", "中共沭阳县城", "下册 source 第五十二卷至第六十卷及附录（下part02） line 19961 为“中共沭阳县城”。"),
    Replacement(FULL, "赣榆县、沐阳县案件", "赣榆县、沭阳县案件", "下册 source 第四十三卷至第五十一卷（下part01） line 2894 为“赣榆县、沭阳县案件”。"),
    Replacement(FULL, "榆园山农民军攻打沐阳县城", "榆园山农民军攻打沭阳县城", "下册 source 第四十三卷至第五十一卷（下part01） line 8900 为“攻打沭阳县城”。"),
    Replacement(FULL, "海州沐阳县主薄沈括", "海州沭阳县主薄沈括", "下册 source 第四十三卷至第五十一卷（下part01） line 22762 为“海州沭阳县主薄沈括”。"),
    Replacement(UP_PART02, "开挖了石梁河水库、准述新\n河", "开挖了石梁河水库、淮沭新\n河", "上 part02 merged OCR line 16358 明确为“淮沭新河”。"),
    Replacement(UP_PART02, "始兴办沂沐尾间工\n程", "始兴办沂沭尾间工\n程", "上 part02 merged OCR lines 18822-18823 明确为“沂沭尾间工程”。"),
    Replacement(UP_PART02, "进行沂沐尾间\n工程", "进行沂沭尾间\n工程", "上 part02 merged OCR line 18847 明确为“沂沭尾间工程”。"),
    Replacement(UP_PART02, "沂沐下游河道尽遭淤塞，沂沐洪水", "沂沭下游河道尽遭淤塞，沂沭洪水", "上 part02 merged OCR lines 21603-21607 明确为“沂沭下游”“沂沭河洪水”。"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[list[dict], dict[str, dict[str, int]]]:
    changes: list[dict] = []
    by_path: dict[Path, list[Replacement]] = {}
    for item in REPLACEMENTS:
        by_path.setdefault(item.path, []).append(item)

    for path, replacements in by_path.items():
        if not path.exists():
            continue
        text = read(path)
        updated = text
        for item in replacements:
            count = updated.count(item.old)
            if count:
                updated = updated.replace(item.old, item.new)
                changes.append({"path": rel(path), "old": item.old, "new": item.new, "count": count, "evidence": item.evidence})
        if updated != text:
            path.write_text(updated, encoding="utf-8")

    residuals: dict[str, dict[str, int]] = {}
    for path in CHECK_FILES:
        if not path.exists():
            continue
        text = read(path)
        hits = {term: text.count(term) for term in CHECK_TERMS if text.count(term)}
        if hits:
            residuals[rel(path)] = hits
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, dict[str, int]]) -> str:
    total = sum(c["count"] for c in changes)
    lines = [
        "# 全书汇总沭阳沭新水利残留补修 batch363",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总及上册水利直接源稿中已由 OCR/source 正文确认的完整短语。",
        "- 依据：上册 part01/part02/part03 merged OCR，中册交通 source，下册治安/军事/科技 source。",
        "- 原则：只修完整短语；不作 `沐 -> 沭`、`述 -> 沭`、`准 -> 淮` 全局替换；题名/书名和未证实 `沐北航道` 暂不处理。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            old = item["old"].replace("\n", "\\n")
            new = item["new"].replace("\n", "\\n")
            lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['evidence']}")
    else:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 残留检查", ""])
    if residuals:
        for path, hits in residuals.items():
            compact = "，".join(f"`{term}` {count}" for term, count in hits.items())
            lines.append(f"- `{path}`：{compact}")
    else:
        lines.append("- 检查范围未见目标残留词。")
    lines.extend([
        "",
        "## 保留边界",
        "",
        "- `沂沐偏重筹泄...` 位于书名/题名语境，本批保留。",
        "- 正式 reader 的 `沐北航道` 未找到页级 OCR 证据，本批继续保留。",
        "- `蕃薇` 在历史河名、校名等语境中大量存在，本批只修 OCR 明确为 `蔷薇` 的沭新河段完整短语。",
        "- 未处理 OCR 源文件、backup、obsolete、历史交付包。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, dict[str, int]]) -> None:
    full_hits = residuals.get(rel(FULL), {})
    up_hits = residuals.get(rel(UP_PART02), {})
    block = f"""{MARKER}

- 依据上册 part01/part02/part03 merged OCR，中册交通 source，下册治安/军事/科技 source，补修全书正文汇总及上册水利直接源稿中 `沭阳/沭城/沭新/淮沭/沭北/沂沭` 可证残留，共 {total} 处。
- 代表修复：`沭阳县述城镇 -> 沭阳县沭城镇`、`准述新河 -> 淮沭新河`、`沭阳县沐新闸 -> 沭阳县沭新闸`、`沐阳县境 -> 沭阳县境`、`述北第截洪沟 -> 沭北第一截洪沟`、`沂沐尾间工程 -> 沂沭尾间工程`。
- 本批后全书汇总保留检查范围：`沐北` {full_hits.get('沐北', 0)}，`沂沐` {full_hits.get('沂沐', 0)}，`人海口` {full_hits.get('人海口', 0)}，`沐阳县` {full_hits.get('沐阳县', 0)}，`准述` {full_hits.get('准述', 0)}，`沐新` {full_hits.get('沐新', 0)}，`述城` {full_hits.get('述城', 0)}。
- 本批后上册水利源稿保留检查范围：`沂沐` {up_hits.get('沂沐', 0)}，`沐北` {up_hits.get('沐北', 0)}。
- `沂沐偏重筹泄...` 位于书名/题名语境，本批保留；正式 reader 的 `沐北航道` 未找到页级 OCR 证据，本批继续保留；未作 `沐 -> 沭`、`述 -> 沭`、`准 -> 淮` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_shuyang_water_batch363_20260708.md`；进度：`output/reports/progress/20260708_全书汇总沭阳沭新水利残留补修第三百六十三批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:])
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    changes, residuals = apply_fix()
    total = sum(c["count"] for c in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals, "check_files": [rel(p) for p in CHECK_FILES if p.exists()]}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total, residuals)
    print(f"total={total}")
    print(json.dumps(residuals, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
