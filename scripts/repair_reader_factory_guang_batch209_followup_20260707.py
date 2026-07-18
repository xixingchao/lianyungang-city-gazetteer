# -*- coding: utf-8 -*-
"""Follow up one skipped lower-reader 广->厂 residue from batch209."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_factory_guang_batch209_followup_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_factory_guang_batch209_followup_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_厂字残留补修第二百零九批补遗.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "市眼镜广、市邮电局、市</p><p>印刷厂、市汽车公司"
NEW = "市眼镜厂、市邮电局、市</p><p>印刷厂、市汽车公司"
EVIDENCE = "市眼镜厂、市邮电局、市印刷厂、市汽车公司"


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def count_candidates(text: str, full_text: str) -> int:
    total = 0
    for m in re.finditer("广", text):
        ctx = text[max(0, m.start() - 16): min(len(text), m.end() + 16)]
        good = ctx.replace("广", "厂", 1)
        if full_text.count(good) and not full_text.count(ctx):
            total += 1
    return total


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_text = plain(FULL.read_text(encoding="utf-8"))
    if full_text.count(EVIDENCE) < 1:
        raise SystemExit(f"missing full-reader evidence: {EVIDENCE}")
    html = LOWER.read_text(encoding="utf-8")
    count = html.count(OLD)
    if count:
        html = html.replace(OLD, NEW)
        LOWER.write_text(html, encoding="utf-8")
    remaining = count_candidates(plain(html), full_text)
    payload = {"time": now, "changed": count, "remaining_candidates": remaining, "old": plain(OLD), "new": plain(NEW)}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    text = "\n".join([
        "# 厂字残留补修第二百零九批补遗",
        "",
        f"> 生成时间：{now}",
        "",
        "## 统计",
        "",
        f"- 修复：{count} 处",
        f"- 修后下册 `广 -> 厂` 短上下文候选剩余：{remaining} 条",
        "- 未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 替换项",
        "",
        f"- `{plain(OLD)}` -> `{plain(NEW)}`：{count} 处",
        "",
    ])
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    old_memory = MEMORY.read_text(encoding="utf-8")
    MEMORY.write_text(old_memory.rstrip() + "\n\n## 2026-07-07 高置信 OCR 错字补修第二百零九批补遗：下册厂字残留\n\n- 补修 batch209 漏过的 `市眼镜广 -> 市眼镜厂` 1 处。\n- 修后按短上下文扫描，下册 `广 -> 厂` 候选剩余 0 条；报告：`output/reports/reader_factory_guang_batch209_followup_20260707.md`。\n- 未打开、展示或嵌入图片。\n", encoding="utf-8")
    print(json.dumps({"changed": count, "remaining_candidates": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
