# -*- coding: utf-8 -*-
"""Repair source-backed industry and storage unit residues, batch 236."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "上" / "第一卷_自然环境.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "body_source_industry_storage_units_batch236_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "body_source_industry_storage_units_batch236_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_工矿粮食单位残留补修第二百三十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
ITEMS = [
    ("累计开采量已达10方吨以上", "累计开采量已达10万吨以上", "上/part01/page_0204.txt", "累计开采量已达10万吨以上"),
    ("D级储量为130方吨", "D级储量为130万吨", "上/part01/page_0204.txt", "D级储量为130万吨"),
    ("连云港出口淮盐114.660方吨", "连云港出口淮盐114.660万吨", "上/part03/page_0164.txt", "连云港出口淮盐114.660万吨"),
    ("生产玻璃瓶1.07方吨", "生产玻璃瓶1.07万吨", "上/part03/page_0197.txt", "生产玻璃瓶1.07万吨"),
    ("塑料制品2.5方吨", "塑料制品2.5万吨", "上/part03/page_0275.txt", "塑料制品2.5万吨"),
    ("年均产泡沫板13方吨", "年均产泡沫板13万吨", "上/part03/page_0287.txt", "年均产泡沫板13万吨"),
    ("年出口豆（生）油2方吨", "年出口豆（生）油2万吨", "中/part02/page_0231.txt", "年出口豆(生)油2万吨、油饼4万吨"),
    ("基本解决了1.5~2方吨大米", "基本解决了1.5~2万吨大米", "中/part02/page_0244.txt", "基本解决了1.5~2万吨大米"),
    ("保粮数量达到19.8方吨", "保粮数量达到19.8万吨", "中/part02/page_0244.txt", "保粮数量达到19.8万吨"),
    ("设备主要有露天锥形发酵罐、方吨", "设备主要有露天锥形发酵罐、万吨", "中/part01/page_0092.txt", "设备主要有露天锥形发酵罐、万吨"),
    ("合成氨年产能力达到7.10方吨", "合成氨年产能力达到7.10万吨", "中/part01/page_0165.txt", "合成氨年产能力达到7.10万吨"),
    ("当年产量1.6方吨", "当年产量1.6万吨", "中/part01/page_0166.txt", "当年产量1.6万吨"),
    ("实产合成氨6.98方吨", "实产合成氨6.98万吨", "中/part01/page_0167.txt", "实产合成氨6.98万吨"),
    ("合成氨年生产能力达3.6方吨", "合成氨年生产能力达3.6万吨", "中/part01/page_0167.txt", "合成氨年生产能力达3.6万吨"),
    ("碳铵14.70方吨", "碳铵14.70万吨", "中/part01/page_0167.txt", "碳铵14.70万吨"),
    ("年生产能力达5.6方吨", "年生产能力达5.6万吨", "中/part01/page_0167.txt", "年生产能力达5.6万吨"),
    ("能力达到3方吨", "能力达到3万吨", "中/part01/page_0167.txt", "能力达到3万吨"),
    ("实产1.06方吨", "实产1.06万吨", "中/part01/page_0168.txt", "实产1.06万吨"),
]


def evidence_path(rel: str) -> Path:
    volume, part, page = rel.split("/")
    return ROOT / "workbench" / "ocr" / "paddle_ocr" / volume / part / page


def ensure_evidence() -> None:
    for _, _, rel, snippet in ITEMS:
        path = evidence_path(rel)
        text = path.read_text(encoding="utf-8", errors="ignore")
        if snippet not in text:
            raise SystemExit(f"missing evidence: {path.relative_to(ROOT)}: {snippet}")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        file_items = []
        for old, new, rel, _ in ITEMS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_items.append({"old": old, "new": new, "count": count, "evidence": str(evidence_path(rel).relative_to(ROOT))})
        if file_items:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "items": file_items})

    residuals = {
        old: {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(old) for path in TARGETS}
        for old, _, _, _ in ITEMS
    }
    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 工矿粮食单位残留补修第二百三十六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复自然矿产、淮盐出口、轻工塑料、粮食储藏、酒厂设备和合成氨段中已由页级 PaddleOCR 证实的单位残留。",
        "- 同步正常命名正文源稿和全书正文汇总；未处理旧交付包、obsolete 或乱码副本。",
        "- 未处理 OCR 仍不支持的 `一项自动控制多`、`对项自进行解除`；未做全局替换，未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["items"]:
            lines.append(f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['evidence']}` |")
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 工矿粮食单位残留补修第二百三十六批\n\n"
    memory += "- 依据页级 PaddleOCR，修复自然矿产、淮盐出口、轻工塑料、粮食储藏、酒厂设备和合成氨段多处 `方吨 -> 万吨` 残留。\n"
    memory += "- 同步范围：正常命名正文源稿及全书正文汇总；报告：`output/reports/body_source_industry_storage_units_batch236_20260707.md`。\n"
    memory += "- `一项自动控制多`、`对项自进行解除` 仍缺强证据，本批未猜改；未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
