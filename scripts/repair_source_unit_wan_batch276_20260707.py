from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "workbench/body_chapters/上/总述与大事记.md",
    "workbench/body_chapters/上/第四卷至第十卷（part02）.md",
    "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md",
    "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
    "workbench/body_chapters/连云港市志_上册_正文汇总.md",
    "workbench/body_chapters/连云港市志_中册_正文汇总.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
]

REPLACEMENTS = [
    {
        "old": "方立方米",
        "new": "万立方米",
        "evidence": "上下文均为库容、供水量、工程土石方、构件产能或仓库容积等量纲，OCR 漏识“万”。",
    },
    {
        "old": "方亩",
        "new": "万亩",
        "evidence": "上下文均为灌溉面积、养鱼面积、土地面积等，OCR 将“万”误作“方”。",
    },
    {
        "old": "立方来",
        "new": "立方米",
        "evidence": "工程量单位中“米”误识作“来”。",
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


def residuals():
    found = {}
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD_PATTERNS if text.count(bad)}
        if hits:
            found[rel] = hits
    return found


def write_report(changes, left):
    total = sum(row["count"] for row in changes)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = {
        "batch": 276,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "Source-layer unit typo cleanup only; current final-reader HTML had no target hits.",
            "No backup or obsolete files were changed intentionally.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/source_unit_wan_batch276_20260707.md"
    js = ROOT / "output/reports/source_unit_wan_batch276_20260707.json"
    lines = [
        "# 源层工程量单位万字残留补修 batch276",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：上册大事记/城乡建设水利相关源稿、中册建材/交通源稿、上册/中册/全书正文汇总。当前正式 HTML 未命中本批坏短语，本批主要防止源层回流。",
        "- 原则：只处理完整单位残留 `方立方米`、`方亩`、`立方来`；不做单字泛替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        if row["count"]:
            lines.append(f"- `{row['path']}`：`{row['old']}` -> `{row['new']}`；次数 {row['count']}；依据：{row['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    if left:
        for rel, hits in left.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标源稿/汇总中均为 0。")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, total


def append_progress(report_md):
    progress = ROOT / "output/reports/progress/20260707_源层工程量单位万字残留补修第二百七十六批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 源层工程量单位万字残留补修第二百七十六批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据源稿/正文汇总上下文，定点修复工程量、库容、供水量、灌溉面积、构件产能等单位残留：`方立方米 -> 万立方米`、`方亩 -> 万亩`、`立方来 -> 立方米`。
- 同步范围：上册大事记/城乡建设水利相关源稿、中册建材/交通源稿、上册/中册/全书正文汇总；当前正式 HTML 未命中本批坏短语，本批主要防止源层回流。
- 报告：`output/reports/source_unit_wan_batch276_20260707.md`；进度：`output/reports/progress/20260707_源层工程量单位万字残留补修第二百七十六批.md`；未处理 backup/obsolete，未打开、展示或嵌入图片。
"""
        memory.write_text(old.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


def main():
    changes = apply_changes()
    left = residuals()
    md, total = write_report(changes, left)
    append_progress(md)
    print(f"total={total}")
    print(f"residuals={json.dumps(left, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
