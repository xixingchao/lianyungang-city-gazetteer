from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_JSON = ROOT / "output" / "reports" / "volume59_proofread_ledger_20260709.json"
LEDGER_MD = ROOT / "output" / "reports" / "volume59_proofread_ledger_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言逐页精校台账.md"

BOUNDARY_CHECKED = {
    2580, 2581, 2583, 2585,
    2587, 2589, 2591, 2593, 2595,
    2597, 2599, 2601, 2603, 2605,
    2607, 2609, 2611, 2613,
    2615, 2617, 2619, 2621,
    2623, 2625,
}


def main() -> None:
    data = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))
    for row in data["rows"]:
        if row.get("book_page") in BOUNDARY_CHECKED:
            row["status"] = "边界已核，待逐字页图精校"
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    LEDGER_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 第五十九卷方言逐页精校台账",
        "",
        f"- 更新时间：{data['updated_at']}",
        "- 范围：第五十九卷方言，以下册 part02 页级 OCR 为主索引。",
        "- 原则：优先核对音标、同音字、方言词条；本地页图只作核验依据，不在聊天中展示。",
        "",
        "## 批次顺序",
        "",
        "1. 2587-2596：第三章同音字汇，优先级最高。",
        "2. 2580-2586：第一章/第二章声韵调，优先级高。",
        "3. 2597-2622：第四章方言词汇，优先级高，按 2-3 页一批。",
        "4. 2623-2625：第五章语法特点，优先级中。",
        "",
        "## 页级台账",
        "",
        "| 书页 | OCR页 | 阶段 | 优先级 | OCR文本 | 本地页图 | 状态 |",
        "|---:|---:|---|---|---|---|---|",
    ]
    for r in data["rows"]:
        if not r.get("book_page"):
            continue
        lines.append(
            f"| {r['book_page']} | {r['ocr_page']} | {r['stage']} | {r['priority']} | "
            f"`{r['ocr_path']}` | `{r['image_path']}` | {r['status']} |"
        )
    text = "\n".join(lines) + "\n"
    LEDGER_MD.write_text(text, encoding="utf-8")
    PROGRESS_MD.write_text(text, encoding="utf-8")
    print("updated boundary statuses")


if __name__ == "__main__":
    main()
