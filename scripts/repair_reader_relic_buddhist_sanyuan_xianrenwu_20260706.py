# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed Xianrenwu and Sanyuan Palace reader text."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_relic_buddhist_sanyuan_xianrenwu_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_relic_buddhist_sanyuan_xianrenwu_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十八批_仙人屋三元宫.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("仙人屋原名瓢崖", "仙人屋石刻位于连云区宿城乡万寿山南坡。原名“崖”。有“关然门窗，洞内宽广", "仙人屋石刻位于连云区宿城乡万寿山南坡。原名“瓢崖”。有“天然门窗，洞内宽广", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("仙人屋陶澍至此", "如屋，清两江总督陶廚至此”，更名“仙人屋”。", "如屋，清两江总督陶澍至此”，更名“仙人屋”。", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("仙人屋陶澍手笔", "皆清道光二年（1835年）陶廚手笔。", "皆清道光二年（1835年）陶澍手笔。", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("水帘洞道光括号", "清宣宗道光十五年（1835年赐给陶澍的御书", "清宣宗道光十五年（1835年）赐给陶澍的御书", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("水帘洞凹龛", "刻在一长方形凹中，洞门上还有", "刻在一长方形凹龛中，洞门上还有", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("三元宫废圮", "清顺治十八年（1661年）裁海后，三元宫废妃。", "清顺治十八年（1661年）裁海后，三元宫废圮。", "workbench/ocr/paddle_ocr/下/part02/page_0261.txt"),
    ("三元宫倾颓修葺", "此后庙宇不断倾。乾隆三十七年（1772年）前后，漕运总督崔应阶等相继修茸，", "此后庙宇不断倾颓。乾隆三十七年（1772年）前后，漕运总督崔应阶等相继修葺，", "workbench/ocr/paddle_ocr/下/part02/page_0261.txt"),
    ("三元宫捐俸修葺", "逐渐恢复旧观。嘉庆八年（1803年）知州唐仲冕继而捐俸修茸，", "逐渐恢复旧观。嘉庆八年（1803年）知州唐仲冕继而捐俸修葺，", "workbench/ocr/paddle_ocr/下/part02/page_0261.txt"),
    ("三元宫陶澍", "光十四年（1834年）八月至年底，两江总督陶廚大修", "光十四年（1834年）八月至年底，两江总督陶澍大修", "workbench/ocr/paddle_ocr/下/part02/page_0261.txt"),
    ("三元宫葺此斋堂", "门楼3间、二山门3间、东西配楼12间、茸此斋堂3间、碑亭2座、库炉2座。", "门楼3间、二山门3间、东西配楼12间、葺此斋堂3间、碑亭2座、库炉2座。", "workbench/ocr/paddle_ocr/下/part02/page_0261.txt"),
    ("三元宫磴道", "像31尊，二山门内塑灵宫1尊、功曹8尊。另加宽道，由53级（）拓展为74级。", "像31尊，二山门内塑灵宫1尊、功曹8尊。另加宽磴道，由53级(磴)拓展为74级。", "workbench/ocr/paddle_ocr/下/part02/page_0261.txt"),
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
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "PaddleOCR-backed Xianrenwu stone inscriptions and Sanyuan Palace Buddhist section repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by the cited PaddleOCR page are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七十八批：仙人屋、三元宫",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、下册 part02 源稿、全书正文汇总中的仙人屋石刻、水帘洞石刻和三元宫佛教段。",
        "- 只处理 PaddleOCR 同页明确支撑的长上下文短语，不做全局替换。",
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
## 2026-07-06 高置信 OCR 错字补修第七十八批：仙人屋、三元宫

- 依据下册 part02 PaddleOCR 页 `page_0105` 与 `page_0261`，修复主阅读版、下册源稿、全书正文汇总中的仙人屋石刻、水帘洞石刻和三元宫佛教段残留 OCR 错字。
- 典型修复：`原名“崖”/关然门窗/陶廚/凹中` 改为 `原名“瓢崖”/天然门窗/陶澍/凹龛中`；三元宫段 `废妃/倾/修茸/茸此斋堂/加宽道，由53级（）` 改为 `废圮/倾颓/修葺/葺此斋堂/加宽磴道，由53级(磴)`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_relic_buddhist_sanyuan_xianrenwu_20260706.md`。
- 边界：`修茸`、`陶廚` 在全书其他位置仍需逐页闭合证据，本批不做全局替换。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第七十八批：仙人屋、三元宫", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
