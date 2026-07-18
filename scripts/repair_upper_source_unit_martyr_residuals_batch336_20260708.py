# -*- coding: utf-8 -*-
"""Narrow upper-volume source residual sync for units and martyrs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "upper_source_unit_martyr_residuals_batch336_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "upper_source_unit_martyr_residuals_batch336_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_上册源稿单位烈士残留补修第三百三十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SUMMARY = ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md"
COUNTY = ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md"
INDUSTRY = ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md"

REPLACEMENTS = [
    (
        SUMMARY,
        "烈土的英名",
        "烈士的英名",
        "正式全书阅读稿同句为“3576位烈士的英名”；烈士陵园固定语境。",
    ),
    (
        SUMMARY,
        "营造陆域100多方平方米",
        "营造陆域100多万平方米",
        "PaddleOCR/正式阅读稿同句为“营造陆域100多万平方米”。",
    ),
    (
        SUMMARY,
        "10人为革命烈土",
        "10人为革命烈士",
        "PaddleOCR/正式阅读稿同句为“10人为革命烈士”。",
    ),
    (
        SUMMARY,
        "追认朱爱周为革命烈土",
        "追认朱爱周为革命烈士",
        "PaddleOCR/正式阅读稿同句为“追认朱爱周为革命烈士”。",
    ),
    (
        COUNTY,
        "校园占地29.5方平方米",
        "校园占地29.5万平方米",
        "PaddleOCR/正式阅读稿同句为“校园占地29.5万平方米”。",
    ),
    (
        INDUSTRY,
        "彩色玻璃马赛克15方平方米、工艺玻璃器血50方只（件）",
        "彩色玻璃马赛克15万平方米、工艺玻璃器皿50万只（件）",
        "PaddleOCR 上/part03/page_0197 与正式阅读稿同句为“彩色玻璃马赛克15万平方米、工艺玻璃器皿50万只（件）”。",
    ),
    (
        INDUSTRY,
        "该企业区占地面积0.5方平方米",
        "该企业厂区占地面积0.5万平方米",
        "PaddleOCR 上/part03/page_0293 与正式阅读稿同句为“该企业厂区占地面积0.5万平方米”。",
    ),
    (
        INDUSTRY,
        "新建、扩建厂房14.5方平方米",
        "新建、扩建厂房14.5万平方米",
        "PaddleOCR/正式阅读稿同句为“新建、扩建厂房14.5万平方米”。",
    ),
    (
        INDUSTRY,
        "该广占地面积0.7方平方米",
        "该厂占地面积0.7万平方米",
        "PaddleOCR/正式阅读稿同句为“该厂占地面积0.7万平方米”。",
    ),
    (
        INDUSTRY,
        "年印能力增至30方色令",
        "年印能力增至30万色令",
        "PaddleOCR/正式阅读稿同句为“年印能力增至30万色令”。",
    ),
    (
        INDUSTRY,
        "建筑面积0.81方平方米",
        "建筑面积0.81万平方米",
        "PaddleOCR/正式阅读稿同句为“建筑面积0.81万平方米”。",
    ),
    (
        INDUSTRY,
        "存栏羊达8.11方只",
        "存栏羊达8.11万只",
        "PaddleOCR/正式阅读稿同句为“存栏羊达8.11万只”。",
    ),
    (
        INDUSTRY,
        "建筑面积0.2方平方米",
        "建筑面积0.2万平方米",
        "PaddleOCR/正式阅读稿同类企业简介语境为“建筑面积0.2万平方米”。",
    ),
    (
        INDUSTRY,
        "占地面积11.4方平方米",
        "占地面积11.4万平方米",
        "PaddleOCR/正式阅读稿同句为“占地面积11.4万平方米”。",
    ),
    (
        INDUSTRY,
        "占地面积0.8方平方米",
        "占地面积0.8万平方米",
        "PaddleOCR/正式阅读稿同句为“占地面积0.8万平方米”。",
    ),
    (
        INDUSTRY,
        "厂区占地面积0.6方平方米",
        "厂区占地面积0.6万平方米",
        "PaddleOCR/正式阅读稿同句为“厂区占地面积0.6万平方米”。",
    ),
    (
        INDUSTRY,
        "生产人造革2方平方米",
        "生产人造革2万平方米",
        "PaddleOCR/正式阅读稿同句为“生产人造革2万平方米”。",
    ),
    (
        INDUSTRY,
        "年均产中空瓶24方只",
        "年均产中空瓶24万只",
        "PaddleOCR/正式阅读稿同句为“年均产中空瓶24万只”。",
    ),
]

CHECK_TERMS = [
    "方平方米",
    "方色令",
    "方只",
    "烈土",
    "器血",
    "该企业区",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_replacements() -> tuple[list[dict], dict[str, int], dict[str, int]]:
    changes: list[dict] = []
    by_path: dict[Path, list[tuple[str, str, str]]] = {}
    for path, old, new, reason in REPLACEMENTS:
        by_path.setdefault(path, []).append((old, new, reason))

    for path, replacements in by_path.items():
        if not path.exists():
            continue
        text = read(path)
        original = text
        for old, new, reason in sorted(replacements, key=lambda item: len(item[0]), reverse=True):
            count = text.count(old)
            if not count:
                continue
            text = text.replace(old, new)
            changes.append({
                "path": rel(path),
                "old": old,
                "new": new,
                "count": count,
                "reason": reason,
            })
        if text != original:
            path.write_text(text, encoding="utf-8")

    exact_residuals: dict[str, int] = {}
    for path, old, _new, _reason in REPLACEMENTS:
        key = f"{rel(path)} :: {old}"
        exact_residuals[key] = read(path).count(old) if path.exists() else -1

    paths = sorted({path for path, _old, _new, _reason in REPLACEMENTS})
    term_totals: dict[str, int] = {}
    for term in CHECK_TERMS:
        term_totals[term] = sum(read(path).count(term) for path in paths if path.exists())
    return changes, exact_residuals, term_totals


def render(changes: list[dict], exact_residuals: dict[str, int], term_totals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 上册源稿单位烈士残留补修 batch336",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：仅三份上册当前源稿：总述与大事记、第三卷区县概况、第十卷至第十六卷（part03）。",
        "- 依据：PaddleOCR 页级文本、正式全书阅读稿同句，以及已核定的单位/烈士固定语境。",
        "- 原则：只替换完整短语；不作 `方/万`、`烈土/烈士`、`广/厂`、`人/入` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            lines.append(
                f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['reason']}"
            )
    else:
        lines.append("- 本批没有新增替换。")

    lines.extend(["", "## 精确旧短语残留", ""])
    nonzero = {key: value for key, value in exact_residuals.items() if value}
    if nonzero:
        for key, value in nonzero.items():
            lines.append(f"- `{key}`：{value}")
    else:
        lines.append("- 本批旧短语在检查范围内均为 0。")

    lines.extend(["", "## 检查词总量", ""])
    for term, count in term_totals.items():
        lines.append(f"- `{term}`：{count}")
    return "\n".join(lines) + "\n"


def append_memory(total: int, term_totals: dict[str, int]) -> None:
    marker = "## 2026-07-08 上册源稿单位烈士残留补修第三百三十六批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    totals = "，".join(f"`{term}` {count}" for term, count in term_totals.items())
    block = f"""
{marker}

- 限定三份上册当前源稿，按 PaddleOCR 页级文本和正式阅读稿同句证据补修单位、烈士及少量固定企业语境残留，共 {total} 处。
- 代表修复：`方平方米 -> 万平方米`、`30方色令 -> 30万色令`、`8.11/24方只 -> 万只`、`烈土 -> 烈士`、`工艺玻璃器血 -> 工艺玻璃器皿`、固定句 `该广占地 -> 该厂占地`。
- 本批检查范围剩余：{totals}。
- 报告：`output/reports/upper_source_unit_martyr_residuals_batch336_20260708.md`；进度：`output/reports/progress/20260708_上册源稿单位烈士残留补修第三百三十六批.md`。
- 未作 `方/万`、`烈土/烈士`、`广/厂`、`人/入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, exact_residuals, term_totals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "exact_residuals": exact_residuals,
        "term_totals": term_totals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, exact_residuals, term_totals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    append_memory(total, term_totals)
    print(f"total={total}")
    print(f"exact_residuals_nonzero={ {k: v for k, v in exact_residuals.items() if v} }")
    print(f"term_totals={term_totals}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
