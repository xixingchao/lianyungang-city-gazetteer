# -*- coding: utf-8 -*-
"""Batch 46: verified culture painting residue OCR fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch46_culture_painting_residue_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch46_culture_painting_residue_20260706.json"

CHANGES = [
    {
        "old": "1982年举办了曹仲苓、黄荔岑、钱彤夫、王寿暖书法遗作展览。",
        "new": "1982年举办了曹仲苓、黄荔岑、钱彤夫、王寿谖书法遗作展览。",
        "section": "文化书法遗作展览段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0021.txt:33 作王寿谖书法遗作展览"],
    },
    {
        "old": "建国后，在张镐楼、陈少林、张理、潘雪岑等教师的精心教育下，一一批美术新苗苗壮成长。有专于连环画的王寿暖，专于国画的张一平、王宏喜、金大雪、周明亮、吴海浪、程民粉画的唐俊德、杨谷昌、马元庭、李家华等，专于版画的倪传诗、周兴等，专于漫画的葛玉琦、史红路等。",
        "new": "建国后，在张霭楼、陈少林、张理、潘雪岑等教师的精心教育下，一批美术新苗茁壮成长。有专于连环画的王寿谖，专于国画的张一平、王宏喜、金大雪、周明亮、吴海浪、程民义、陈学慈、花千红、石仁勇等，专于油画的邹本务、吴宜恩、杨炳昌、孙传宾等，专于水彩水粉画的唐俊德、杨谷昌、马元庭、李家华等，专于版画的倪传诗、周兴等，专于漫画的葛玉琦、史红路等。",
        "section": "文化绘画人才段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0022.txt:22-26 作张霭楼、一批美术新苗茁壮成长、王寿谖、程民义、陈学慈、花千红、石仁勇、油画、水彩水粉画等完整文本"],
    },
    {
        "old": "陈学慈的《港城黄昏》、邹本务的《收海带首次参展。",
        "new": "陈学慈的《港城黄昏》、邹本务的《收海带》首次参展。",
        "section": "文化绘画参展段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0022.txt:27-28 作邹本务的《收海带》首次参展"],
    },
    {
        "old": "杨炳昌的《作》参展。",
        "new": "杨炳昌的《习作》参展。",
        "section": "文化水彩水粉画展段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0022.txt:32-33 作杨炳昌的《习作》参展"],
    },
    {
        "old": "此后他创作的历史题材《先驱者》、李白》等雕塑作品",
        "new": "此后他创作的历史题材《先驱者》、《李白》等雕塑作品",
        "section": "文化雕塑历史题材段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0023.txt:13-14 作《先驱者》、《李白》等雕塑作品"],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}: {change['old'][:80]}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修页级 PaddleOCR 闭合且旧串唯一命中的文化卷书法、绘画、雕塑残留短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四十六批：文化绘画残留短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- {item['section']}：`{item['old']}` -> `{item['new']}`（命中 {item['count']} 处）")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版，不改 OCR 原文。",
        "- 每项旧串均要求唯一命中。",
        "- 只处理下册文化卷书法、绘画、雕塑小节 `page_0021` 至 `page_0023` 已闭合短片段。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
