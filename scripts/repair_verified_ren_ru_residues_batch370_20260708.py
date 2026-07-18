# -*- coding: utf-8 -*-
"""Repair PaddleOCR-proven 人/入 residual phrases in current sources."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_ren_ru_residues_batch370_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_ren_ru_residues_batch370_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_可证人入残留补修第三百七十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 可证人入残留补修第三百七十批"

SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
UPPER_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
UPPER_EVENTS = ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md"
UPPER_PART03 = ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md"
LOWER_PART02 = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
READER_ALL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
READER_LOW = ROOT / "output" / "final_reader" / "连云港市志_下册.html"

EVIDENCE_FILES = [
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0056.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0078.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0079.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0111.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0121.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0151.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0153.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0154.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part02" / "page_0183.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0209.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0225.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0022.txt",
]

EVIDENCE_TERMS = {
    "workbench/ocr/paddle_ocr/上/part01/page_0056.txt": ["何锋钰率兵进入海州城维持秩序"],
    "workbench/ocr/paddle_ocr/上/part01/page_0078.txt": ["加入高级农业社的农户占总数的98%", "加入渔业合作"],
    "workbench/ocr/paddle_ocr/上/part01/page_0079.txt": ["全市进入全民整风阶段"],
    "workbench/ocr/paddle_ocr/上/part01/page_0111.txt": ["刘小斌入选“江苏省1984年十佳新闻人物”"],
    "workbench/ocr/paddle_ocr/上/part01/page_0121.txt": ["市话进入全国自动网"],
    "workbench/ocr/paddle_ocr/上/part01/page_0151.txt": ["进入我国东海", "一支进入黄海北部"],
    "workbench/ocr/paddle_ocr/上/part01/page_0153.txt": ["进入5月份气温才能稳定上升"],
    "workbench/ocr/paddle_ocr/上/part01/page_0154.txt": ["全市进入雨季"],
    "workbench/ocr/paddle_ocr/上/part02/page_0183.txt": ["加入沿海14个开放城市创立的“沿海"],
    "workbench/ocr/paddle_ocr/上/part03/page_0209.txt": ["该产品入选北京全国新产品展示信"],
    "workbench/ocr/paddle_ocr/上/part03/page_0225.txt": ["企业加入了常州白雪制冷集团"],
    "workbench/ocr/paddle_ocr/下/part02/page_0022.txt": ["4幅篆刻作品入选江苏省职工国画", "9幅作品入选江苏省名胜古迹篆刻展览"],
}


@dataclass(frozen=True)
class Replacement:
    label: str
    path: Path
    old: str
    new: str


REPLACEMENTS = [
    Replacement("进入海州城", SUMMARY, "何锋钰率兵进人海州城维持秩序", "何锋钰率兵进入海州城维持秩序"),
    Replacement("加入合作社", SUMMARY, "加人高级农业社的农户占总数的98%；加人渔业合作", "加入高级农业社的农户占总数的98%；加入渔业合作"),
    Replacement("进入整风阶段", SUMMARY, "全市进人全民整风阶段", "全市进入全民整风阶段"),
    Replacement("刘小斌入选", SUMMARY, "刘小斌人选江苏省1984年十佳新闻人物”。", "刘小斌入选“江苏省1984年十佳新闻人物”。"),
    Replacement("刘小斌入选", UPPER_SUMMARY, "刘小斌人选江苏省1984年十佳新闻人物”。", "刘小斌入选“江苏省1984年十佳新闻人物”。"),
    Replacement("刘小斌入选", UPPER_EVENTS, "刘小斌人选江苏省1984年十佳新闻人物”。", "刘小斌入选“江苏省1984年十佳新闻人物”。"),
    Replacement("进入全国自动网", SUMMARY, "市话进人全国自动网", "市话进入全国自动网"),
    Replacement("进入东海黄海", SUMMARY, "进人我国东海后，拐折向黄海，一支进人黄海北部", "进入我国东海后，拐折向黄海，一支进入黄海北部"),
    Replacement("进入5月份", SUMMARY, "进人5月份气温才能稳定上升", "进入5月份气温才能稳定上升"),
    Replacement("进入雨季", SUMMARY, "全市进人雨季", "全市进入雨季"),
    Replacement("加入沿海城市组织", SUMMARY, "加人沿海14个开放城市创立的“沿海", "加入沿海14个开放城市创立的“沿海"),
    Replacement("产品入选", SUMMARY, "该产品人选北京全国新产品展示信", "该产品入选北京全国新产品展示信"),
    Replacement("产品入选", UPPER_SUMMARY, "该产品人选北京全国新产品展示信", "该产品入选北京全国新产品展示信"),
    Replacement("产品入选", UPPER_PART03, "该产品人选北京全国新产品展示信", "该产品入选北京全国新产品展示信"),
    Replacement("加入制冷集团", SUMMARY, "企业加人了常州白雪制冷集团", "企业加入了常州白雪制冷集团"),
    Replacement("篆刻作品", LOWER_PART02, "4幅蒙刻作品入选江苏省职工国画", "4幅篆刻作品入选江苏省职工国画"),
    Replacement("篆刻作品", SUMMARY, "4幅蒙刻作品入选江苏省职工国画", "4幅篆刻作品入选江苏省职工国画"),
    Replacement("篆刻作品", READER_ALL, "4幅蒙刻作品入选江苏省职工国画", "4幅篆刻作品入选江苏省职工国画"),
    Replacement("篆刻作品", READER_LOW, "4幅蒙刻作品入选江苏省职工国画", "4幅篆刻作品入选江苏省职工国画"),
    Replacement("篆刻入选", LOWER_PART02, "9蝠作品人选江苏省名胜古迹篆刻展览", "9幅作品入选江苏省名胜古迹篆刻展览"),
    Replacement("篆刻入选", SUMMARY, "9蝠作品人选江苏省名胜古迹篆刻展览", "9幅作品入选江苏省名胜古迹篆刻展览"),
    Replacement("篆刻入选", READER_ALL, "9蝠作品入选江苏省名胜古迹篆刻展览", "9幅作品入选江苏省名胜古迹篆刻展览"),
    Replacement("篆刻入选", READER_LOW, "9蝠作品入选江苏省名胜古迹篆刻展览", "9幅作品入选江苏省名胜古迹篆刻展览"),
]

OLD_TERMS = [
    "何锋钰率兵进人",
    "加人高级农业社",
    "加人渔业合作",
    "全市进人全民整风阶段",
    "刘小斌人选",
    "市话进人全国自动网",
    "进人我国东海",
    "进人黄海北部",
    "进人5月份",
    "全市进人雨季",
    "加人沿海14个开放城市",
    "该产品人选北京全国新产品展示信",
    "企业加人了常州白雪制冷集团",
    "4幅蒙刻作品",
    "9蝠作品",
    "作品人选江苏省名胜古迹篆刻展览",
]

NEW_TERMS = [
    "何锋钰率兵进入",
    "加入高级农业社",
    "加入渔业合作",
    "全市进入全民整风阶段",
    "刘小斌入选",
    "市话进入全国自动网",
    "进入我国东海",
    "进入黄海北部",
    "进入5月份",
    "全市进入雨季",
    "加入沿海14个开放城市",
    "该产品入选北京全国新产品展示信",
    "企业加入了常州白雪制冷集团",
    "4幅篆刻作品",
    "9幅作品入选江苏省名胜古迹篆刻展览",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def apply_replacements() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for item in REPLACEMENTS:
        text = read(item.path)
        before = text.count(item.old)
        if before:
            item.path.write_text(text.replace(item.old, item.new), encoding="utf-8")
        results.append({
            "label": item.label,
            "path": rel(item.path),
            "old_count": before,
            "new_count_after": read(item.path).count(item.new),
            "old": item.old,
            "new": item.new,
        })
    return results


def collect_evidence() -> dict[str, dict[str, list[int]]]:
    evidence: dict[str, dict[str, list[int]]] = {}
    for path in EVIDENCE_FILES:
        key = rel(path)
        evidence[key] = {}
        for term in EVIDENCE_TERMS.get(key, []):
            evidence[key][term] = line_hits(path, term)
    return evidence


def collect_counts(paths: list[Path], terms: list[str]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for path in paths:
        text = read(path)
        hits = {term: text.count(term) for term in terms if text.count(term)}
        if hits:
            counts[rel(path)] = hits
    return counts


def render(results: list[dict[str, object]], evidence: dict[str, dict[str, list[int]]], old_counts: dict[str, dict[str, int]], new_counts: dict[str, dict[str, int]]) -> str:
    by_label: dict[str, int] = defaultdict(int)
    for item in results:
        by_label[str(item["label"])] += int(item["old_count"])
    total = sum(int(item["old_count"]) for item in results)

    lines = [
        "# 可证人入残留补修 batch370",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行正文汇总、少数上/下册源稿和正式 reader 中已由 PaddleOCR 证实的完整短语。",
        "- 原则：只修完整短语；不作 `人 -> 入`、`蒙 -> 篆`、`蝠 -> 幅` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 分项统计",
    ]
    for label in sorted(by_label):
        lines.append(f"- {label}：{by_label[label]} 处。")

    lines.extend(["", "## 证据位置"])
    for path, terms in evidence.items():
        lines.append(f"- `{path}`")
        for term, hits in terms.items():
            compact = "，".join(str(i) for i in hits) or "未命中"
            lines.append(f"  - 行 {compact}：`{term}`")

    lines.extend(["", "## 替换明细"])
    for item in results:
        if int(item["old_count"]):
            lines.append(f"- `{item['path']}`：{item['label']}，替换 {item['old_count']} 处；`{item['old']}` -> `{item['new']}`。")

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


def upsert_memory(results: list[dict[str, object]], old_counts: dict[str, dict[str, int]]) -> None:
    total = sum(int(item["old_count"]) for item in results)
    summary_old = old_counts.get("workbench/body_chapters/连云港市志_全书_正文汇总.md", {})
    reader_old = old_counts.get("output/final_reader/连云港市志_全书.html", {})
    block = f"""{MARKER}

- 依据上册 part01/page_0056、0078、0079、0111、0121、0151、0153、0154，part02/page_0183，part03/page_0209、0225，以及下册 part02/page_0022 页级 PaddleOCR 成句证据，补修现行正文汇总、少数分册源稿和正式 reader 中可证 `人/入` 与篆刻短语残留，共 {total} 处。
- 代表修复：`进人海州城 -> 进入海州城`、`加人高级农业社/渔业合作 -> 加入高级农业社/渔业合作`、`全市进人全民整风阶段 -> 全市进入全民整风阶段`、`刘小斌人选 -> 刘小斌入选`、`市话进人全国自动网 -> 市话进入全国自动网`、`进人我国东海/黄海北部 -> 进入我国东海/黄海北部`、`进人5月份/进人雨季 -> 进入5月份/进入雨季`、`加人沿海14个开放城市 -> 加入沿海14个开放城市`、`产品人选北京全国新产品展示信 -> 产品入选北京全国新产品展示信`、`企业加人了常州白雪制冷集团 -> 企业加入了常州白雪制冷集团`、`4幅蒙刻作品/9蝠作品人选 -> 4幅篆刻作品/9幅作品入选`。
- 本批后全书正文汇总旧词检查剩余：`进人海州城` {summary_old.get('何锋钰率兵进人', 0)}，`加人高级农业社` {summary_old.get('加人高级农业社', 0)}，`全市进人全民整风阶段` {summary_old.get('全市进人全民整风阶段', 0)}，`刘小斌人选` {summary_old.get('刘小斌人选', 0)}，`4幅蒙刻作品` {summary_old.get('4幅蒙刻作品', 0)}，`9蝠作品` {summary_old.get('9蝠作品', 0)}。
- 本批后全书 reader 旧词检查剩余：`4幅蒙刻作品` {reader_old.get('4幅蒙刻作品', 0)}，`9蝠作品` {reader_old.get('9蝠作品', 0)}。
- 未作危险全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_ren_ru_residues_batch370_20260708.md`；进度：`output/reports/progress/20260708_可证人入残留补修第三百七十批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    new_text = old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:])
    MEMORY.write_text(new_text, encoding="utf-8")


def main() -> None:
    results = apply_replacements()
    touched = sorted({item.path for item in REPLACEMENTS})
    evidence = collect_evidence()
    old_counts = collect_counts(touched, OLD_TERMS)
    new_counts = collect_counts(touched, NEW_TERMS)
    report = render(results, evidence, old_counts, new_counts)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": sum(int(item["old_count"]) for item in results),
        "results": results,
        "evidence": evidence,
        "old_counts": old_counts,
        "new_counts": new_counts,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(results, old_counts)
    print(f"total={data['total']}")
    print(json.dumps(old_counts, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
