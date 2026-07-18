# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed tourism, military, and technology residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch86_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch86_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十六批_旅游驻防科技.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "三元宫自在天",
        "old": "紧靠三元宫下方的是“自在失”小院",
        "new": "紧靠三元宫下方的是“自在天”小院",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0099.txt",
    },
    {
        "label": "三元宫古银杏",
        "old": "三元宫一带有好多株古银否，树龄均在500年以上",
        "new": "三元宫一带有好多株古银杏，树龄均在500年以上",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0099.txt",
    },
    {
        "label": "三元宫古银杏断行源稿",
        "old": "三元宫一带有好多株古银否，树龄均在500年以\n上",
        "new": "三元宫一带有好多株古银杏，树龄均在500年以\n上",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0099.txt",
    },
    {
        "label": "团圆宫古银杏",
        "old": "院内有水池一方，古银否一株。",
        "new": "院内有水池一方，古银杏一株。",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上_part02_PaddleOCR汇总.md:6529",
    },
    {
        "label": "东磊六色一曰红",
        "old": "可概括为六色：日红。“东磊朱樱”",
        "new": "可概括为六色：一曰红。“东磊朱樱”",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0102.txt",
    },
    {
        "label": "东磊二曰黄银杏",
        "old": "二日黄。东磊多银否杏树，秋后树叶变为否黄色",
        "new": "二曰黄。东磊多银杏树，秋后树叶变为杏黄色",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0102.txt",
    },
    {
        "label": "东磊三曰蓝",
        "old": "三日蓝。云台山的大涧多集中于山的东侧",
        "new": "三曰蓝。云台山的大涧多集中于山的东侧",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0102.txt",
    },
    {
        "label": "驻防桑格淮安",
        "old": "康熙三十九年，漕运总督案格题设淮安城守营时撤销",
        "new": "康熙三十九年，漕运总督桑格题设淮安城守营时撤销",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0166.txt",
    },
    {
        "label": "科技粳型水稻",
        "old": "夏代，云台山区已种植梗型水稻。西汉时，境内漆器、铁器、石器、纺织品等制作精美。",
        "new": "夏代，云台山区已种植粳型水稻。西汉时，境内漆器、铁器、石器、纺织品等制作精美。",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0414.txt",
    },
    {
        "label": "科技粳型水稻总述异文",
        "old": "夏朝初，境内已种植梗型水稽，为世界上最早种植梗型水稻的地区之一。",
        "new": "夏朝初，境内已种植粳型水稻，为世界上最早种植粳型水稻的地区之一。",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:36466",
    },
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "PaddleOCR-backed tourism, military, and technology residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by cited OCR evidence are changed.",
        "skipped": "Ancient-text residues and single-source raw-only readings remain pending.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十六批：旅游、驻防、科技",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应中册/下册源稿、全书正文汇总中的少量 OCR 残留。",
        "- 仅处理 PaddleOCR 或已精修 OCR 明确支撑的 `自在天/银杏/曰/桑格/粳型水稻`。",
        "- 古籍诗文、旧志序文、raw 单源未闭合片段继续保留。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次实际替换：{payload['changed_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源：`{item['source']}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第八十六批：旅游、驻防、科技

- 依据 OCR 页 `中/part02/page_0099`、`中/part02/page_0102`、`下/part01/page_0166`、`下/part01/page_0414` 及上册 Paddle 汇总证据，修复主阅读版及对应源稿/汇总中的 8 个精确短片段。
- 典型修复：`自在失` -> `自在天`，`古银否/银否杏树/否黄色` -> `古银杏/银杏树/杏黄色`，`日红/二日黄/三日蓝` -> `一曰红/二曰黄/三曰蓝`，`案格题设` -> `桑格题设`，`梗型水稻/梗型水稽` -> `粳型水稻`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_paddle_backed_residues_batch86_20260706.md`。
- 边界：乡土文存古籍诗文与 raw 单源残留仍需逐页闭合证据，未做全局替换；未展示、未嵌入图片。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十六批：旅游、驻防、科技", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
