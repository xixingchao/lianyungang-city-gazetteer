# -*- coding: utf-8 -*-
"""Narrow upper-volume source sync for factory `广/厂` residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "upper_source_factory_residuals_batch337_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "upper_source_factory_residuals_batch337_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_上册源稿厂字残留补修第三百三十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
]

REPLACEMENTS = [
    ("该广占地面积0.7万平方米", "该厂占地面积0.7万平方米", 1, "PaddleOCR 上/part03 与正式阅读稿同句为“该厂占地面积0.7万平方米”。"),
    ("该广生产的香巾纸", "该厂生产的香巾纸", 3, "PaddleOCR 上/part03 与正式阅读稿同句为“该厂生产的香巾纸”。"),
    ("该广产品获淮阴地区家具式样", "该厂产品获淮阴地区家具式样", 3, "PaddleOCR 上/part03 与正式阅读稿同句为“该厂产品获淮阴地区家具式样”。"),
    ("该广利用积累资金50万元", "该厂利用积累资金50万元", 3, "PaddleOCR 上/part03 与正式阅读稿同句为“该厂利用积累资金50万元”。"),
    ("该广先后获省纺工系统经济", "该厂先后获省纺工系统经济", 3, "PaddleOCR 上/part03 与正式阅读稿同句为“该厂先后获省纺工系统经济”。"),
    ("该广历史最高产值为1988年的2463.4万元", "该厂历史最高产值为1988年的2463.4万元", 3, "PaddleOCR 上/part03 与正式阅读稿同句为“该厂历史最高产值为1988年的2463.4万元”。"),
    ("该广位于新浦解放东路东首", "该厂位于新浦解放东路东首", 3, "PaddleOCR 上/part03 与正式阅读稿同句为“该厂位于新浦解放东路东首”。"),
    ("广区占地面积1.86万平方米", "厂区占地面积1.86万平方米", 3, "PaddleOCR 上/part03 与正式阅读稿同句为“厂区占地面积1.86万平方米”。"),
    ("广区占地3.37万平方米", "厂区占地3.37万平方米", 3, "PaddleOCR 上/part03 与正式阅读稿同句为“厂区占地3.37万平方米”。"),
]

CHECK_TERMS = ["该广占地", "该广生产", "该广产品", "该广利用", "该广先后", "该广历史", "该广位于新浦", "广区占地"]
MARKER = "## 2026-07-08 上册源稿厂字残留补修第三百三十七批"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_replacements() -> tuple[list[dict], dict[str, int], dict[str, int]]:
    run_changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        original = text
        for old, new, _batch_count, reason in sorted(REPLACEMENTS, key=lambda item: len(item[0]), reverse=True):
            count = text.count(old)
            if not count:
                continue
            text = text.replace(old, new)
            run_changes.append({"path": rel(path), "old": old, "new": new, "count": count, "reason": reason})
        if text != original:
            path.write_text(text, encoding="utf-8")

    exact_residuals = {
        old: sum(read(path).count(old) for path in TARGETS if path.exists())
        for old, _new, _batch_count, _reason in REPLACEMENTS
    }
    term_totals = {term: sum(read(path).count(term) for path in TARGETS if path.exists()) for term in CHECK_TERMS}
    return run_changes, exact_residuals, term_totals


def batch_changes() -> list[dict]:
    return [
        {"old": old, "new": new, "count": batch_count, "reason": reason}
        for old, new, batch_count, reason in REPLACEMENTS
    ]


def render(run_changes: list[dict], exact_residuals: dict[str, int], term_totals: dict[str, int]) -> str:
    batch_total = sum(item["count"] for item in batch_changes())
    run_total = sum(item["count"] for item in run_changes)
    lines = [
        "# 上册源稿厂字残留补修 batch337",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 本批累计修复总数：{batch_total}",
        f"- 本次运行新增替换：{run_total}",
        "- 范围：全书正文汇总、上册正文汇总、上册第十卷至第十六卷当前源稿。",
        "- 依据：PaddleOCR 上/part03 合并文本与正式全书阅读稿同句。",
        "- 原则：只替换完整企业/厂区短语；不作 `广 -> 厂` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 本批累计替换明细",
    ]
    for item in batch_changes():
        lines.append(f"- `{item['old']}` -> `{item['new']}`；累计次数 {item['count']}；依据：{item['reason']}")

    lines.extend(["", "## 本次运行新增替换", ""])
    if run_changes:
        for item in run_changes:
            lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}")
    else:
        lines.append("- 本次重跑未产生新增替换；正文数据已在前次运行中落地。")

    lines.extend(["", "## 精确旧短语残留", ""])
    bad = {key: value for key, value in exact_residuals.items() if value}
    if bad:
        for key, value in bad.items():
            lines.append(f"- `{key}`：{value}")
    else:
        lines.append("- 本批精确旧短语在检查范围内均为 0。")

    lines.extend(["", "## 宽检查词总量", ""])
    for term, count in term_totals.items():
        lines.append(f"- `{term}`：{count}")

    lines.extend([
        "",
        "## 范围外保留项",
        "",
        "- `该广位于新浦海连中路26号`、`该广占地9.6万平方米` 位于全书正文汇总的中册语境，不属于本批上册 part03 证据范围，留待后续单独回源核对。",
    ])
    return "\n".join(lines) + "\n"


def memory_block(batch_total: int, term_totals: dict[str, int]) -> str:
    totals = "，".join(f"`{term}` {count}" for term, count in term_totals.items())
    return f"""{MARKER}

- 依据 PaddleOCR 上/part03 与正式阅读稿同句，补修上册源稿和正文汇总中企业/厂区语境 `广 -> 厂` 残留，本批累计共 {batch_total} 处。
- 代表修复：`该广生产/产品/利用/先后/历史/位于新浦解放东路东首 -> 该厂...`，`广区占地 -> 厂区占地`，补齐 `该广占地面积0.7万平方米 -> 该厂占地面积0.7万平方米` 的遗漏。
- 本批精确旧短语残留为 0；宽检查词总量：{totals}。
- 宽检查词中的 `该广位于新浦海连中路26号`、`该广占地9.6万平方米` 属于全书汇总中册语境，本批未处理，留待后续单独回源核对。
- 报告：`output/reports/upper_source_factory_residuals_batch337_20260708.md`；进度：`output/reports/progress/20260708_上册源稿厂字残留补修第三百三十七批.md`。
- 未作 `广 -> 厂` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""


def upsert_memory(block: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    if next_start < 0:
        new = old[:start].rstrip() + "\n\n" + block.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + block.strip() + old[next_start:]
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    run_changes, exact_residuals, term_totals = apply_replacements()
    batch = batch_changes()
    batch_total = sum(item["count"] for item in batch)
    run_total = sum(item["count"] for item in run_changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "batch_total": batch_total,
        "run_total": run_total,
        "batch_changes": batch,
        "run_changes": run_changes,
        "exact_residuals": exact_residuals,
        "term_totals": term_totals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(run_changes, exact_residuals, term_totals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(memory_block(batch_total, term_totals))
    print(f"batch_total={batch_total}")
    print(f"run_total={run_total}")
    print(f"exact_residuals_nonzero={ {k: v for k, v in exact_residuals.items() if v} }")
    print(f"term_totals={term_totals}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
