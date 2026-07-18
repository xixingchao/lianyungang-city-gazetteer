from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "output" / "reports" / "dialect_volume59_audit_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_proofread_ledger_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "volume59_proofread_ledger_20260709.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言逐页精校台账.md"


def stage_for(book_page: int | None, markers: str) -> tuple[str, str]:
    if not book_page:
        return "目录/卷界", "低"
    if 2580 <= book_page <= 2586:
        return "第一章/第二章：声韵调与方言差别", "高"
    if 2587 <= book_page <= 2596:
        return "第三章：同音字汇", "最高"
    if 2597 <= book_page <= 2622:
        return "第四章：方言词汇", "高"
    if 2623 <= book_page <= 2625:
        return "第五章：语法特点", "中"
    return markers or "待判定", "中"


def main() -> None:
    audit = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))
    ocr_hits = audit.get("ocr", {}).get("hits", [])
    rows = []
    for hit in ocr_hits:
        book_page = hit.get("book_page") or hit.get("书页")
        try:
            book_page = int(book_page) if book_page not in (None, "") else None
        except ValueError:
            book_page = None
        markers = "、".join(hit.get("markers", []) or hit.get("标志", []) or [])
        stage, priority = stage_for(book_page, markers)
        path = hit.get("file") or hit.get("path") or hit.get("ocr_path") or hit.get("命中文件")
        image = hit.get("image") or hit.get("image_path") or hit.get("本地页图")
        rows.append({
            "ocr_page": hit.get("ocr_page") or hit.get("OCR页"),
            "book_page": book_page,
            "stage": stage,
            "priority": priority,
            "ocr_path": path,
            "image_path": image,
            "markers": markers,
            "status": "待逐页精校",
        })

    rows.sort(key=lambda r: (r["book_page"] is None, r["book_page"] or 0, r["ocr_page"] or 0))
    payload = {"generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"), "rows": rows}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 第五十九卷方言逐页精校台账",
        "",
        f"- 时间：{payload['generated_at']}",
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
    for r in rows:
        if not r["book_page"]:
            continue
        lines.append(
            f"| {r['book_page']} | {r['ocr_page']} | {r['stage']} | {r['priority']} | "
            f"`{r['ocr_path']}` | `{r['image_path']}` | {r['status']} |"
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"rows={len(rows)} report={REPORT_MD}")


if __name__ == "__main__":
    main()
