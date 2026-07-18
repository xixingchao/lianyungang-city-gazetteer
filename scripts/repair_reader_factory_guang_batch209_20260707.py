# -*- coding: utf-8 -*-
"""Repair evidence-backed lower-reader 广->厂 residues, batch209."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_factory_guang_batch209_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_factory_guang_batch209_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_厂字残留补修第二百零九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("监所附设工广或</p><p>作坊", "监所附设工厂或</p><p>作坊", "监所附设工厂或作坊"),
    ("市绝缘材料</p><p>广采用风水相结合", "市绝缘材料</p><p>厂采用风水相结合", "市绝缘材料厂采用风水相结合"),
    ("市电线广在编织车间", "市电线厂在编织车间", "市电线厂在编织车间"),
    ("神户面包广、高岛屋界店", "神户面包厂、高岛屋界店", "神户面包厂、高岛屋界店"),
    ("南牛奶广、中林公司", "南牛奶厂、中林公司", "南牛奶厂"),
    ("市棉织广建立职</p><p>工代表大会制度", "市棉织厂建立职</p><p>工代表大会制度", "市棉织厂建立职工代表大会制度"),
    ("东海硅微粉广开发活性</p><p>硅微粉系列产品", "东海硅微粉厂开发活性</p><p>硅微粉系列产品", "东海硅微粉厂开发活性硅微粉"),
    ("屹立在工广、医院、海岛", "屹立在工厂、医院、海岛", "屹立在工厂、医院、海岛"),
    ("在街头、工广、街道建立", "在街头、工厂、街道建立", "在街头、工厂、街道建立"),
    ("《60万吨碱广工地见闻》", "《60万吨碱厂工地见闻》", "《60万吨碱厂工地见闻》"),
    ("在市塑料广152名", "在市塑料厂152名", "在市塑料厂152名"),
    ("查治对象以工广女工", "查治对象以工厂女工", "查治对象以工厂女工"),
    ("市眼镜广、市</p><p>印刷厂", "市眼镜厂、市</p><p>印刷厂", "市眼镜厂、市邮电局"),
    ("河南洛阳玻璃广足球队", "河南洛阳玻璃厂足球队", "河南洛阳玻璃厂足球队"),
    ("新海连市华兴铁工广副经</p><p>理", "新海连市华兴铁工厂副经</p><p>理", "新海连市华兴铁工厂副经理"),
    ("新海油厂分广厂</p><p>长", "新海油厂分厂厂</p><p>长", "新海油厂分厂厂长"),
    ("分配至灌云县农机广。1968", "分配至灌云县农机厂。1968", "分配至灌云县农机厂"),
    ("进行广长（经理）负责制", "进行厂长（经理）负责制", "厂长（经理）负责制"),
]


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


def upsert_memory(total: int, remaining_candidates: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第二百零九批：下册厂字残留"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复下册 `广 -> 厂` 高置信残留 {total} 处。
- 本批仅替换完整 HTML 片段，不做单字 `广 -> 厂`；报告：`output/reports/reader_factory_guang_batch209_20260707.md`。
- 修后按短上下文扫描，下册仍有 {remaining_candidates} 条 `广 -> 厂` 候选；未打开、展示或嵌入图片。
""".strip()
    MEMORY.write_text(old.rstrip() + "\n\n" + block + "\n", encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_text = plain(FULL.read_text(encoding="utf-8"))
    evidence = {evidence_text: full_text.count(evidence_text) for _old, _new, evidence_text in REPLACEMENTS}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    html = LOWER.read_text(encoding="utf-8")
    changed_items = []
    for old, new, _evidence_text in REPLACEMENTS:
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            changed_items.append({"old": plain(old), "new": plain(new), "changed": count})
    LOWER.write_text(html, encoding="utf-8")
    after_plain = plain(html)
    total = sum(item["changed"] for item in changed_items)
    remaining_candidates = count_candidates(after_plain, full_text)

    payload = {
        "time": now,
        "changed": total,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
        "lower_remaining_factory_candidates": remaining_candidates,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 厂字残留补修第二百零九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前下册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `广 -> 厂` 的固定短语错识。",
        "- 未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后下册 `广 -> 厂` 短上下文候选剩余：{remaining_candidates} 条",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, remaining_candidates)
    print(json.dumps({"changed": total, "remaining_candidates": remaining_candidates, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
