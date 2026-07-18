# -*- coding: utf-8 -*-
"""Narrow 人学/人园/人托 repairs in education contexts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "ruxue_source_residuals_batch334_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "ruxue_source_residuals_batch334_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_入学残留补修第三百三十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷_人口（part01_部分）.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("青年人学。学校", "青年入学。学校", "PaddleOCR 上/part01 合并稿为“青年入学”。"),
    ("人学10630\n人，人学率18.8", "入学10630\n人，入学率18.8", "PaddleOCR 上/part01 合并稿为“入学10630人，入学率18.8%”。"),
    ("人学10630\n人，入学率18.8", "入学10630\n人，入学率18.8", "PaddleOCR 上/part01 合并稿为“入学10630人，入学率18.8%”。"),
    ("初中人学率", "初中入学率", "PaddleOCR 上/part01 合并稿为“初中入学率”。"),
    ("高中人\n学率", "高中入\n学率", "PaddleOCR 上/part01 合并稿为“高中入学率”。"),
    ("人学率不足15%", "入学率不足15%", "PaddleOCR 上/part01 合并稿为“入学率不足15%”。"),
    ("学龄儿童人学率", "学龄儿童入学率", "PaddleOCR 上/part01 合并稿多处为“学龄儿童入学率”。"),
    ("适龄儿童人学率", "适龄儿童入学率", "PaddleOCR 上/part01 合并稿为“适龄儿童入学率99.3%”。"),
    ("以优先人托、人学，招工", "以优先入托、入学、招工", "PaddleOCR 上/part01 合并稿为“优先入托、入学、招工”。"),
    ("以优先入托、人学，招工", "以优先入托、入学、招工", "PaddleOCR 上/part01 合并稿为“优先入托、入学、招工”。"),
    ("盐工适龄子女全部人学读", "盐工适龄子女全部入学读", "PaddleOCR 上/part03 合并稿为“全部入学读书”。"),
    ("小孩人学等", "小孩入学等", "上下文为军队干部家庭小孩入学困难。"),
    ("子女人学入托", "子女入学入托", "上下文为优抚对象子女入学入托优惠政策。"),
    ("全县应人学聋儿童", "全县应入学聋儿童", "上下文为应入学聋儿童统计。"),
    ("对人学学生", "对入学学生", "上下文为技工学校入学学生文化程度要求。"),
    ("人学职工8649人", "入学职工8649人", "上下文为职工业余学校入学职工人数。"),
    ("人学前班", "入学前班", "同段全书汇总已为“入学前班”。"),
    ("幼儿人学，学制", "幼儿入学，学制", "上下文为学前班招收幼儿入学。"),
    ("残疾儿童人学", "残疾儿童入学", "上下文为安排残疾儿童入学。"),
    ("儿童6岁人学", "儿童6岁入学", "上下文为小学学制与儿童入学年龄。"),
    ("人学年龄市区", "入学年龄市区", "上下文为小学入学年龄规定。"),
    ("进行人学教育", "进行入学教育", "上下文为每届学生入学教育。"),
    ("师范生人学", "师范生入学", "上下文为师范生入学即开展专业思想教育。"),
    ("中小学人学\n新生", "中小学入学\n新生", "上下文为中小学入学新生过多。"),
    ("平民子女人学", "平民子女入学", "上下文为学校招收平民子女入学。"),
    ("学生人学年龄", "学生入学年龄", "上下文为放宽学生入学年龄。"),
    ("人园幼儿", "入园幼儿", "PaddleOCR 上/part01 合并稿为“入园幼儿”。"),
    ("人园儿童", "入园儿童", "PaddleOCR 上/part01 合并稿为“入园儿童”。"),
    ("人园率", "入园率", "PaddleOCR 上/part01 合并稿为“入园率”。"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def collect_residuals() -> dict[str, dict[str, int]]:
    terms = ["人学", "人园", "人托"]
    residuals: dict[str, dict[str, int]] = {}
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        counts = {term: text.count(term) for term in terms if text.count(term)}
        if counts:
            residuals[str(path.relative_to(ROOT)).replace("\\", "/")] = counts
    return residuals


def apply_replacements() -> tuple[list[dict], dict[str, dict[str, int]]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        original = text
        for old, new, evidence in sorted(REPLACEMENTS, key=lambda item: len(item[0]), reverse=True):
            count = text.count(old)
            if not count:
                continue
            text = text.replace(old, new)
            changes.append({
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "old": old,
                "new": new,
                "count": count,
                "evidence": evidence,
            })
        if text != original:
            path.write_text(text, encoding="utf-8")
    return changes, collect_residuals()


def render(changes: list[dict], residuals: dict[str, dict[str, int]]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 入学残留补修 batch334",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正文汇总、上册正文汇总、相关上/下分册源稿。",
        "- 原则：只处理教育/入园入托语境中 OCR 或上下文明示的 `人学 -> 入学`、`人园 -> 入园`、`人托 -> 入托`；保留 `聋哑人学校`、`艺人学习`、`有人学拳术`、`郡人学博`、`万人学习/学完` 等正常命中。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for path, counts in residuals.items():
            pairs = "，".join(f"`{term}` {count}" for term, count in counts.items())
            lines.append(f"- `{path}`：{pairs}；已人工筛除为正常词或暂不凭常识处理的疑点。")
    else:
        lines.append("- `人学/人园/人托`：0")
    return "\n".join(lines) + "\n"


def append_memory(total: int, residuals: dict[str, dict[str, int]]) -> None:
    marker = "## 2026-07-08 入学残留补修第三百三十四批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    residual_total = sum(sum(counts.values()) for counts in residuals.values())
    block = f"""
{marker}

- 依据 PaddleOCR 与教育语境，补修 `人学/人园/人托` 残留，共 {total} 处。
- 代表修复：`青年入学`、`入学10630人/入学率`、`优先入托、入学、招工`、`盐工适龄子女全部入学读书`、`子女入学入托`、`入学教育`、`入园幼儿/入园率`。
- 本批后目标文件仍有相关残留 {residual_total} 处，主要为 `聋哑人学校`、`艺人学习`、`有人学拳术`、`郡人学博`、`万人学习/学完` 等正常词或暂不凭常识处理项；报告：`output/reports/ruxue_source_residuals_batch334_20260708.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "residuals": residuals, "changes": changes}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    content = render(changes, residuals)
    REPORT.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")
    append_memory(total, residuals)
    print(f"total={total}")
    print(f"residual={sum(sum(counts.values()) for counts in residuals.values())}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
