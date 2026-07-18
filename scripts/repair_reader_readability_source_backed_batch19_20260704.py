# -*- coding: utf-8 -*-
"""Repair a nineteenth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch19_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch19_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十九批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "小沙东海战干部队",
        "51名干部组成的于部队",
        "51名干部组成的干部队",
        "workbench/ocr/paddle_ocr/下/part01/page_0162.txt:24",
    ),
    (
        "人防抽调干部",
        "市人民武装部抽调于部参加人民防空工作",
        "市人民武装部抽调干部参加人民防空工作",
        "workbench/ocr/paddle_ocr/下/part01/page_0187.txt:13",
    ),
    (
        "工会棉织厂",
        "在市棉织广建立职工代表大会制度",
        "在市棉织厂建立职工代表大会制度",
        "workbench/ocr/paddle_ocr/下/part01/page_0314.txt:5",
    ),
    (
        "基层工会干部",
        "300多名基层工会于部进行企业民主管理知识培训",
        "300多名基层工会干部进行企业民主管理知识培训",
        "workbench/ocr/paddle_ocr/下/part01/page_0314.txt:6",
    ),
    (
        "工会干部学校",
        "市总工会千部学校和中国工运学院联合办学",
        "市总工会干部学校和中国工运学院联合办学",
        "workbench/ocr/paddle_ocr/下/part01/page_0317.txt:9",
    ),
    (
        "妇联干部联系户",
        "采取于部联系一般农户、专业户和科技示范户",
        "采取干部联系一般农户、专业户和科技示范户",
        "workbench/ocr/paddle_ocr/下/part01/page_0333.txt:26",
    ),
    (
        "庭院生产超过千元",
        "庭院生产超过于元",
        "庭院生产超过千元",
        "workbench/ocr/paddle_ocr/下/part01/page_0333.txt:30",
    ),
    (
        "优秀妇女干部",
        "优秀妇女于部和妇女工作者554名",
        "优秀妇女干部和妇女工作者554名",
        "workbench/ocr/paddle_ocr/下/part01/page_0335.txt:22",
    ),
    (
        "入园入托儿童",
        "入园人托儿童6420人",
        "入园入托儿童6420人",
        "workbench/ocr/paddle_ocr/下/part01/page_0336.txt:6",
    ),
    (
        "东海入园幼儿",
        "东海县办起1034个幼儿班，人园幼儿30971人",
        "东海县办起1034个幼儿班，入园幼儿30971人",
        "workbench/ocr/paddle_ocr/下/part01/page_0336.txt:6",
    ),
    (
        "赣榆入园幼儿",
        "赣榆县办起402所幼儿园，共869个班，人园幼儿27397人",
        "赣榆县办起402所幼儿园，共869个班，入园幼儿27397人",
        "workbench/ocr/paddle_ocr/下/part01/page_0336.txt:7",
    ),
    (
        "儿童入园入托",
        "全市3～7岁儿童75%入园人托",
        "全市3～7岁儿童75%入园入托",
        "workbench/ocr/paddle_ocr/下/part01/page_0336.txt:7",
    ),
    (
        "1977入园幼儿",
        "市区有托幼组织113个，人园幼儿1.5万余人，人园率43%",
        "市区有托幼组织113个，入园幼儿1.5万余人，入园率43%",
        "workbench/ocr/paddle_ocr/下/part01/page_0336.txt:12",
    ),
    (
        "1988入园幼儿",
        "全市幼儿园1670所，3095个班，人园幼儿116800人",
        "全市幼儿园1670所，3095个班，入园幼儿116800人",
        "workbench/ocr/paddle_ocr/下/part01/page_0336.txt:24",
    ),
    (
        "教育概况入园幼儿",
        "全市幼儿园1933所，人园幼儿134587人，加上人学前班的幼儿，人园率80.78%",
        "全市幼儿园1933所，入园幼儿134587人，加上入学前班的幼儿，入园率80.78%",
        "workbench/ocr/paddle_ocr/下/part01/page_0348.txt:14-15",
    ),
    (
        "教育概况入学率",
        "全市小学1597所，小学生339968人，人学率98.94%",
        "全市小学1597所，小学生339968人，入学率98.94%",
        "workbench/ocr/paddle_ocr/下/part01/page_0348.txt:15-16",
    ),
    (
        "干部中专",
        "成人中等教育有职工中专、于部中专、职工技术培训学校",
        "成人中等教育有职工中专、干部中专、职工技术培训学校",
        "workbench/ocr/paddle_ocr/下/part01/page_0348.txt:21",
    ),
    (
        "小学入学率3%",
        "赣榆县有小学生3109人。人学率3%",
        "赣榆县有小学生3109人。入学率3%",
        "workbench/ocr/paddle_ocr/下/part01/page_0355.txt:4",
    ),
    (
        "小学入学率9%",
        "灌云县有小学生9612人，人学率9%",
        "灌云县有小学生9612人，入学率9%",
        "workbench/ocr/paddle_ocr/下/part01/page_0355.txt:5",
    ),
    (
        "小学学龄儿童入学率",
        "学龄儿童人学率98.94%",
        "学龄儿童入学率98.94%",
        "workbench/ocr/paddle_ocr/下/part01/page_0355.txt:15",
    ),
    (
        "彭雄51名干部",
        "彭雄率新四军三师51名于部乘海船赴延安学习",
        "彭雄率新四军三师51名干部乘海船赴延安学习",
        "workbench/ocr/paddle_ocr/下/part02/page_0371.txt:13-14",
    ),
]

SKIPPED = [
    "未核源页的 `老于部`、检察信访 `于部违法乱纪`、水利补助 `于部每夜` 继续暂缓。",
    "未做全书 OCR 重修，只按已定位页级证据做短上下文替换。",
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
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["changed"] for item in targets)
    payload = {
        "time": now,
        "scope": "第十九批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 或同页上下文明确支撑的短字符串问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十九批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 PaddleOCR 或同页上下文明确支撑的短字符串问题。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for item in targets[0]["items"]:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`；依据 `{item['source']}`；命中 {item['count']} 处/文件。")
    lines += ["", "## 暂缓", *[f"- {item}" for item in SKIPPED], ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-04 第十九批正文残留回源修复"
    memory = f"""
{marker}
- 对 `output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 同步执行第十九批短上下文 OCR 残留修复。
- 本批覆盖小沙东海战、人防、工会、妇联庭院生产、托幼、教育概况/小学、彭雄传略等 21 项，依据页级 OCR 路径记录在 `output/reports/reader_readability_source_backed_batch19_20260704.md`。
- 仍暂缓未核源页的 `老于部`、检察信访 `于部违法乱纪`、水利补助 `于部每夜` 等残留；不做全书重抽或猜测性替换。
"""
    upsert_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
