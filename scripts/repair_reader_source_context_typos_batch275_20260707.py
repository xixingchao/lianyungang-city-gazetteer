from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "workbench/body_chapters/上/第一卷_自然环境.md",
    "workbench/body_chapters/上/第四卷至第十卷（part02）.md",
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
    "workbench/body_chapters/连云港市志_上册_正文汇总.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
    "output/final_reader/连云港市志_全书.html",
    "output/final_reader/连云港市志_下册.html",
]

REPLACEMENTS = [
    {
        "old": "另一一方面库存积压过多",
        "new": "另一方面库存积压过多",
        "evidence": "同句前文为“一方面市场供应紧张”，后文应为“另一方面”。",
    },
    {
        "old": "分两个阶段。第阶段从1953年12月",
        "new": "分两个阶段。第一阶段从1953年12月",
        "evidence": "后文已有“第二阶段”，此处为“第一阶段”漏字。",
    },
    {
        "old": "比成绩、比责献",
        "new": "比成绩、比贡献",
        "evidence": "“双学双比”固定表述为学文化、学技术，比成绩、比贡献。",
    },
    {
        "old": "投人民工100万工日",
        "new": "投入民工100万工日",
        "evidence": "工程投入民工工日，属“投入”误作“投人”。",
    },
]

BAD_PATTERNS = [item["old"] for item in REPLACEMENTS]


def apply_changes():
    changes = []
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            changes.append({
                "path": rel,
                "old": item["old"],
                "new": item["new"],
                "count": count,
                "evidence": item["evidence"],
            })
        if text != original:
            path.write_text(text, encoding="utf-8", newline="")
    return changes


def count_residuals():
    residuals = {}
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD_PATTERNS if text.count(bad)}
        if hits:
            residuals[rel] = hits
    return residuals


def write_report(changes, residuals):
    total = sum(row["count"] for row in changes)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = {
        "batch": 275,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "notes": [
            "Only context-closed typo repairs were applied.",
            "方立方米 and broader 收人/进人/投人 candidates require page-specific verification and were not changed.",
            "No backup or obsolete files were changed intentionally.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/reader_source_context_typos_batch275_20260707.md"
    js = ROOT / "output/reports/reader_source_context_typos_batch275_20260707.json"
    lines = [
        "# 上下册正文高置信上下文错字补修 batch275",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：上册第一卷/经济综情相关源稿、下册民政源稿、上册/全书正文汇总及当前全书/下册 HTML。",
        "- 原则：只修上下文闭合的漏字、重字、误字；不做 `收人 -> 收入`、`进人 -> 进入` 等泛替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        if row["count"]:
            lines.append(f"- `{row['path']}`：`{row['old']}` -> `{row['new']}`；次数 {row['count']}；依据：{row['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for rel, hits in residuals.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标正式文件中均为 0。")
    lines.extend([
        "",
        "## 暂不处理",
        "",
        "- `方立方米` 涉及 `万立方米/立方米` 等多种上下文，需按页专项核对，本批不改。",
        "- `收人`、`进人`、`投人`、`编人` 等候选数量多且有专名/正常词夹杂，本批只处理完整高置信短语。",
    ])
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, total


def append_progress(report_md):
    progress = ROOT / "output/reports/progress/20260707_上下册正文高置信上下文错字补修第二百七十五批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 上下册正文高置信上下文错字补修第二百七十五批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据当前正式阅读稿和全书正文汇总的上下文，定点修复 4 组高置信 OCR 残留：`另一一方面库存积压过多 -> 另一方面库存积压过多`、`第阶段从1953年12月 -> 第一阶段从1953年12月`、`比责献 -> 比贡献`、`投人民工100万工日 -> 投入民工100万工日`。
- 同步范围：上册第一卷/经济综情相关源稿、下册民政源稿、上册/全书正文汇总及当前全书/下册 HTML；不处理 backup/obsolete。
- `方立方米`、泛 `收人/进人/投人/编人` 等候选需按页专项核对，本批不扩大替换；报告：`output/reports/reader_source_context_typos_batch275_20260707.md`；未打开、展示或嵌入图片。
"""
        memory.write_text(old.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


def main():
    changes = apply_changes()
    residuals = count_residuals()
    md, total = write_report(changes, residuals)
    append_progress(md)
    print(f"total={total}")
    print(f"residuals={json.dumps(residuals, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
