# -*- coding: utf-8 -*-
"""Repair source-backed factory/unit residues in middle volume, batch 225."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "middle_food_medicine_factory_units_batch225_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_food_medicine_factory_units_batch225_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册食品医药厂字单位残留补修第二百二十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("市罐头食品广", "市罐头食品厂", "workbench/ocr/paddle_ocr/中/part01/page_0076.txt"),
    ("年产能力为1.5方吨", "年产能力为1.5万吨", "workbench/ocr/paddle_ocr/中/part01/page_0076.txt"),
    ("洪门酒广", "洪门酒厂", "workbench/ocr/paddle_ocr/中/part01/page_0083.txt"),
    ("酒广4名", "酒厂4名", "workbench/ocr/paddle_ocr/中/part01/page_0083.txt"),
    ("市洪门酒广", "市洪门酒厂", "workbench/ocr/paddle_ocr/中/part01/page_0084.txt"),
    ("市葡萄酒广以", "市葡萄酒厂以", "workbench/ocr/paddle_ocr/中/part01/page_0086.txt"),
    ("该广位于新浦区幸福路9号", "该厂位于新浦区幸福路9号", "workbench/ocr/paddle_ocr/中/part01/page_0093.txt"),
    ("连云港市酶制剂广", "连云港市酶制剂厂", "workbench/ocr/paddle_ocr/中/part01/page_0103.txt"),
    ("襄河乳品广", "襄河乳品厂", "workbench/ocr/paddle_ocr/中/part01/page_0107.txt"),
    ("新浦淀粉广", "新浦淀粉厂", "workbench/ocr/paddle_ocr/中/part01/page_0107.txt"),
    ("市海州酿化广", "市海州酿化厂", "workbench/ocr/paddle_ocr/中/part01/page_0111.txt"),
    ("连云港向阳制药广", "连云港向阳制药厂", "workbench/ocr/paddle_ocr/中/part01/page_0124.txt"),
    ("东北制药总广", "东北制药总厂", "workbench/ocr/paddle_ocr/中/part01/page_0128.txt"),
    ("上海化工广", "上海化工厂", "workbench/ocr/paddle_ocr/中/part01/page_0129.txt"),
    ("新浦五金工具广", "新浦五金工具厂", "workbench/ocr/paddle_ocr/中/part01/page_0129.txt"),
    ("原市眼镜广", "原市眼镜厂", "workbench/ocr/paddle_ocr/中/part01/page_0129.txt"),
    ("该广充分利用", "该厂充分利用", "workbench/ocr/paddle_ocr/中/part01/page_0132.txt"),
]

EVIDENCE = {
    "workbench/ocr/paddle_ocr/中/part01/page_0076.txt": ["市罐头食品厂", "年产能力提高到1.5万吨以上"],
    "workbench/ocr/paddle_ocr/中/part01/page_0083.txt": ["洪门酒厂由4锅蒸馏操作改为5锅蒸馏操作", "酒厂4名酿酒师傅"],
    "workbench/ocr/paddle_ocr/中/part01/page_0084.txt": ["1982年，市洪门酒厂投资30万元"],
    "workbench/ocr/paddle_ocr/中/part01/page_0086.txt": ["市葡萄酒厂以", "先进设备为投资资本"],
    "workbench/ocr/paddle_ocr/中/part01/page_0093.txt": ["该厂位于新浦区幸福路9号"],
    "workbench/ocr/paddle_ocr/中/part01/page_0103.txt": ["企业改称为连云港市酶制剂厂"],
    "workbench/ocr/paddle_ocr/中/part01/page_0107.txt": ["襄河乳品厂因奶源严重缺乏", "新浦淀粉厂并入新浦制冰"],
    "workbench/ocr/paddle_ocr/中/part01/page_0111.txt": ["市海州酿化厂脱水蔬菜生产线建成投产"],
    "workbench/ocr/paddle_ocr/中/part01/page_0124.txt": ["连云港向阳制药厂在剂型上逐步增加"],
    "workbench/ocr/paddle_ocr/中/part01/page_0128.txt": ["东北制药总厂"],
    "workbench/ocr/paddle_ocr/中/part01/page_0129.txt": ["上海化工厂", "新浦五金工具厂", "原市眼镜厂"],
    "workbench/ocr/paddle_ocr/中/part01/page_0132.txt": ["该厂充分利用先进的检测工具"],
}

RESIDUE_PATTERNS = [old for old, _, _ in REPLACEMENTS]


def ensure_evidence() -> None:
    missing = []
    for rel, snippets in EVIDENCE.items():
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        for snippet in snippets:
            if snippet not in text:
                missing.append(f"{rel}: {snippet}")
    if missing:
        raise SystemExit("missing evidence: " + "; ".join(missing))


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()

    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        file_changes = []
        for old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_changes.append({"old": old, "new": new, "count": count, "source": source})
        if text != original:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "changes": file_changes})

    residuals = {}
    for pattern in RESIDUE_PATTERNS:
        residuals[pattern] = {}
        for path in TARGETS:
            text = path.read_text(encoding="utf-8", errors="ignore")
            residuals[pattern][str(path.relative_to(ROOT))] = text.count(pattern)

    payload = {"time": now, "changes": changes, "residuals": residuals, "evidence": EVIDENCE}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册食品医药厂字单位残留补修第二百二十五批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿、全书阅读稿、中册正文源稿、全书正文汇总。",
        "- 依据 PaddleOCR 页级文字证据，补修食品工业和医药段厂字、万吨单位残留。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["changes"]:
            lines.append(
                f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['source']}` |"
            )
    lines.extend(["", "## 残留计数", ""])
    for pattern, files in residuals.items():
        lines.append(f"- `{pattern}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 中册食品医药厂字单位残留补修第二百二十五批\n\n"
    memory += "- 依据中册 PaddleOCR 页级文字，补修食品工业和医药段 `广 -> 厂`、罐头厂 `1.5方吨 -> 1.5万吨` 等源稿/阅读稿残留。\n"
    memory += "- 覆盖市罐头食品厂、洪门酒厂、市葡萄酒厂、酶制剂厂、襄河乳品厂、新浦淀粉厂、市海州酿化厂、连云港向阳制药厂、东北制药总厂、上海化工厂、新浦五金工具厂、原市眼镜厂、药用包装材料厂等明确回源点。\n"
    memory += "- 同步范围：中册/全书阅读稿、中册正文源稿、全书正文汇总；报告：`output/reports/middle_food_medicine_factory_units_batch225_20260707.md`。\n"
    memory += "- 未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for c in changes if c["changes"]),
        "report": str(REPORT_MD),
        "residual_total": sum(sum(v.values()) for v in residuals.values()),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
