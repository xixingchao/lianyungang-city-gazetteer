# -*- coding: utf-8 -*-
"""Repair a second PaddleOCR-backed batch in the relic stone-inscription section."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_relic_stone_inscriptions_batch2_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_relic_stone_inscriptions_batch2_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十七批_文物石刻续补.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("王谟癸卯", "开皇三年岁次葵卯四", "开皇三年岁次癸卯四", "workbench/ocr/paddle_ocr/下/part02/page_0103.txt"),
    ("孔望山铭颜渊喟然", "春秋成史。颜渊然，曾子日唯", "春秋成史。颜渊喟然，曾子日唯", "workbench/ocr/paddle_ocr/下/part02/page_0103.txt"),
    ("归云洞擘窠", "云洞作擎书，深没石2厘米", "云洞作擘窠书，深没石2厘米", "workbench/ocr/paddle_ocr/下/part02/page_0103.txt"),
    ("安钝陶昺", "偕知州陶莴因古圣贤遗像", "偕知州陶昺因古圣贤遗像", "workbench/ocr/paddle_ocr/下/part02/page_0103.txt"),
    ("安钝书吏", "海州书更钱铸老人刘宣", "海州书吏钱铸老人刘宣", "workbench/ocr/paddle_ocr/下/part02/page_0103.txt"),
    ("张叔夜钤辖1", "前兵马铃辖赵子庄", "前兵马钤辖赵子庄", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("张叔夜钤辖2", "兵马铃辖赵令", "兵马钤辖赵令", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("张叔夜朐山", "前胸山令阎质", "前朐山令阎质", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("张叔夜王冶", "司刑曹王治", "司刑曹王冶", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("张叔夜蒋仝", "怀仁主簿蒋全", "怀仁主簿蒋仝", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("张叔夜王大猷", "权朐山尉王大献", "权朐山尉王大猷", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("鳌头山巨鍪", "山应载巨整", "山应载巨鍪", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("王梦龄金鳌", "白虎变金整", "白虎变金鳌", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("驺虞", "师亮采“骑虞”篆书题勒", "师亮采“驺虞”篆书题勒", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("黄窝丰腴", "书法工整丰。张思沛诗", "书法工整丰腴。张思沛诗", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("乌龙潭", "鸟龙潭崖壁上又刻", "乌龙潭崖壁上又刻", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("万寿山殷忧", "大字“般忧启圣，多难兴邦”", "大字“殷忧启圣，多难兴邦”", "workbench/ocr/paddle_ocr/下/part02/page_0107.txt"),
    ("万寿山无逊色焉", "无逊色為！国家兴亡", "无逊色焉！国家兴亡", "workbench/ocr/paddle_ocr/下/part02/page_0107.txt"),
    ("万寿山爰镌", "追往思来，壮怀无已，爱镌八字于石", "追往思来，壮怀无已，爰镌八字于石", "workbench/ocr/paddle_ocr/下/part02/page_0107.txt"),
    ("万寿山二十七", "民国八年五月，倭寇大举进犯连云港", "民国二十七年五月，倭寇大举进犯连云港", "workbench/ocr/paddle_ocr/下/part02/page_0107.txt"),
    ("万寿山爰题", "爱题数字，共相奋勉", "爰题数字，共相奋勉", "workbench/ocr/paddle_ocr/下/part02/page_0107.txt"),
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:5]}")
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "PaddleOCR-backed relic stone-inscription follow-up repair",
        "targets": applied,
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "principle": "Only exact long-context replacements backed by the cited PaddleOCR page are changed.",
        "skipped": "Names or readings that remain potentially edition-sensitive, such as 宋蟠/朱蟠, are not changed in this batch.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七十七批：文物石刻续补",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、下册 part02 源稿、全书正文汇总中的文物卷石刻短片段。",
        "- 只处理 PaddleOCR 同页明确支撑的官名、刻文、题名和形近字。",
        "- 不处理仍可能涉及版本差异的人名读法。",
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
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第七十七批：文物石刻续补

- 依据下册 part02 文物卷 PaddleOCR 页 `page_0103`、`page_0104`、`page_0106`、`page_0107`，继续修复主阅读版、下册源稿、全书正文汇总中的石刻段残留。
- 典型修复：`葵卯/颜渊然/擎书/陶莴/书更` 改为 `癸卯/颜渊喟然/擘窠书/陶昺/书吏`；张叔夜题名段 `铃辖/王治/蒋全/王大献` 改为 `钤辖/王冶/蒋仝/王大猷`；鳌头山和万寿山段修为 `巨鍪/金鳌/驺虞/丰腴/殷忧/无逊色焉/爰镌/民国二十七年`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_relic_stone_inscriptions_batch2_20260706.md`。
- 暂缓：`宋蟠/朱蟠` 等仍可能涉及版本差异的人名读法，继续按页核对，不做顺手替换。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第七十七批：文物石刻续补", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
