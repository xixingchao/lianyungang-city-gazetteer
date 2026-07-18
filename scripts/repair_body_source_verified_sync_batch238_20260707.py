# -*- coding: utf-8 -*-
"""Sync already verified unit repairs into remaining body source files, batch 238."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "body_source_verified_sync_batch238_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "body_source_verified_sync_batch238_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_已证实正文源稿同步回填第二百三十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
ITEMS = [
    ("港口货物吞吐量11方吨", "港口货物吞吐量11万吨", "上/part01/page_0073.txt", "港口货物吞吐量11万吨"),
    ("港口吞吐量256方吨", "港口吞吐量256万吨", "上/part01/page_0087.txt", "港口吞吐量256万吨"),
    ("年通过能力390方吨设计", "年通过能力390万吨设计", "上/part01/page_0090.txt", "年通过能力390万吨设计"),
    ("港口货物吞吐量335方吨，其中外贸59方吨", "港口货物吞吐量335万吨，其中外贸59万吨", "上/part01/page_0094.txt", "港口货物吞吐量335万吨，其中外贸59万吨"),
    ("港口货物吞吐量242万吨，其中外贸65方吨", "港口货物吞吐量242万吨，其中外贸65万吨", "上/part01/page_0096.txt", "港口货物吞吐量242万吨，其中外贸65万吨"),
    ("港口货物吞吐量303方吨", "港口货物吞吐量303万吨", "上/part01/page_0098.txt", "港口货物吞吐量303万吨"),
    ("港口货物吞吐量594方吨", "港口货物吞吐量594万吨", "上/part01/page_0100.txt", "港口货物吞吐量594万吨"),
    ("港口货物吞吐量858方吨", "港口货物吞吐量858万吨", "上/part01/page_0109.txt", "港口货物吞吐量858万吨"),
    ("累计开采量已达10方吨以上", "累计开采量已达10万吨以上", "上/part01/page_0204.txt", "累计开采量已达10万吨以上"),
    ("D级储量为130方吨", "D级储量为130万吨", "上/part01/page_0204.txt", "D级储量为130万吨"),
    ("蓄水量762方吨", "蓄水量762万吨", "上/part02/page_0060.txt", "蓄水量762万吨"),
    ("容量20方吨蓄水坝", "容量20万吨蓄水坝", "上/part02/page_0061.txt", "容量20万吨蓄水坝"),
    ("蓄水量35方吨", "蓄水量35万吨", "上/part02/page_0061.txt", "蓄水量35万吨"),
    ("生活用水60方吨", "生活用水60万吨", "上/part02/page_0062.txt", "生活用水60万吨"),
    ("新建1方吨滤池1座", "新建1万吨滤池1座", "上/part02/page_0062.txt", "新建1万吨滤池1座"),
    ("设计能力10方吨/日", "设计能力10万吨/日", "上/part02/page_0062.txt", "设计能力10万吨/日"),
    ("生猪饲养量降至186.16方头", "生猪饲养量降至186.16万头", "上/part03/page_0074.txt", "生猪饲养量降至186.16万头"),
    ("连云港出口淮盐114.660方吨", "连云港出口淮盐114.660万吨", "上/part03/page_0164.txt", "连云港出口淮盐114.660万吨"),
    ("生产玻璃瓶1.07方吨", "生产玻璃瓶1.07万吨", "上/part03/page_0197.txt", "生产玻璃瓶1.07万吨"),
    ("塑料制品2.5方吨", "塑料制品2.5万吨", "上/part03/page_0275.txt", "塑料制品2.5万吨"),
    ("年均产泡沫板13方吨", "年均产泡沫板13万吨", "上/part03/page_0287.txt", "年均产泡沫板13万吨"),
    ("加工白条肉1.74方吨", "加工白条肉1.74万吨", "中/part01/page_0071.txt", "加工白条肉1.74万吨"),
    ("当年宰杀22方头", "当年宰杀22万头", "中/part01/page_0073.txt", "当年宰杀22万头"),
    ("年宰量36方头生猪", "年宰量36万头生猪", "中/part01/page_0073.txt", "年宰量36万头生猪"),
    ("全市白酒生产能力3.5方吨", "全市白酒生产能力3.5万吨", "中/part01/page_0085.txt", "全市白酒生产能力3.5万吨"),
    ("年增1方吨啤酒能力", "年增1万吨啤酒能力", "中/part01/page_0086.txt", "年增1万吨啤酒能力"),
    ("年产能力增到1.5方吨", "年产能力增到1.5万吨", "中/part01/page_0087.txt", "年产能力增到1.5万吨"),
    ("年产能力4.5方吨", "年产能力4.5万吨", "中/part01/page_0087.txt", "年产能力4.5万吨"),
    ("设备主要有露天锥形发酵罐、方吨", "设备主要有露天锥形发酵罐、万吨", "中/part01/page_0092.txt", "设备主要有露天锥形发酵罐、万吨"),
    ("加工水产冻品2.95方吨", "加工水产冻品2.95万吨", "中/part01/page_0109.txt", "加工水产冻品2.95万吨"),
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
    missing = []
    for _, _, rel, snippet in ITEMS:
        path = evidence_path(rel)
        text = path.read_text(encoding="utf-8", errors="ignore")
        if snippet not in text:
            missing.append(f"{path.relative_to(ROOT)}: {snippet}")
    if missing:
        raise SystemExit("missing evidence:\n" + "\n".join(missing))


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
        "# 已证实正文源稿同步回填第二百三十八批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 将前序已由页级 PaddleOCR 证实的单位修复，同步回填到遗漏的上册正文汇总和中册正文源稿。",
        "- 未处理旧交付包、obsolete 或乱码副本；未做全局替换，未打开、展示或嵌入图片。",
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
    memory += "\n\n## 2026-07-07 已证实正文源稿同步回填第二百三十八批\n\n"
    memory += "- 将前序已证实的 `方吨/方头 -> 万吨/万头` 修复同步回填到 `连云港市志_上册_正文汇总.md` 和 `第十七卷至第二十九卷（中part01）.md`。\n"
    memory += "- 报告：`output/reports/body_source_verified_sync_batch238_20260707.md`；未处理旧交付包、obsolete 或乱码副本，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
