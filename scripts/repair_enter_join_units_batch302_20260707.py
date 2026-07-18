# -*- coding: utf-8 -*-
"""Narrow page-OCR-backed repairs for 进入/并入/加入 and unit residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "enter_join_units_batch302_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "enter_join_units_batch302_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_进入并入加入与单位残字补修第三百零二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_上册.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
]

REPLACEMENTS = [
    ("生产于事改生产助理", "生产干事改生产助理", "PaddleOCR 中/part02/page_0496 为“生产干事改生产助理”。"),
    ("全市大炼钢铁运动进人高潮", "全市大炼钢铁运动进入高潮", "PaddleOCR 上/part01/page_0081 为“进入高潮”。"),
    ("对私改造进人高潮", "对私改造进入高潮", "PaddleOCR 上/part02/page_0196 为“对私改造进入高潮”。"),
    ("反内战斗争进人高潮", "反内战”斗争进入高潮", "PaddleOCR 下/part01/page_0306 为“反饥饿、反内战”斗争进入高潮”。"),
    ("率领进人山东", "率领进入山东", "PaddleOCR 下/part01/page_0171 为“率领进入山东”。"),
    ("率领进人滨海地区", "率领进入滨海地区", "PaddleOCR 下/part01/page_0171 为“率领进入滨海地区”。"),
    ("二纵再度进人东海县境", "二纵再度进入东海县境", "PaddleOCR 下/part01/page_0171 为“二纵再度进入东海县境”。"),
    ("为进人花果山的要道", "为进入花果山的要道", "PaddleOCR 中/part02/page_0097 同章同景区用“进入花果山”。"),
    ("并人沭阳县和灌云县", "并入沭阳县和灌云县", "PaddleOCR 上/part01/page_0071 为“并入沭阳县和灌云县”。"),
    ("并人徐海公路运输管理局", "并入徐海公路运输管理局", "PaddleOCR 上/part01/page_0076 为“并入徐海公路运输管理局”。"),
    ("并人徐州汽车运输公司", "并入徐州汽车运输公司", "PaddleOCR 中/part02/page_0032 为“并入徐州汽车运输公司”。"),
    ("并人民主区", "并入民主区", "PaddleOCR 中/part02/page_0496 与上/part01/page_0233 均为“并入民主区”。"),
    ("率部加人八路军东进支队", "率部加入八路军东进支队", "PaddleOCR 上/part01/page_0063 为“率部加入八路军东进支队”。"),
    ("1357方公斤", "1357万公斤", "PaddleOCR 中/part02/page_0149 为“1357万公斤”。"),
    ("11.12方公斤", "11.12万公斤", "PaddleOCR 中/part02/page_0286 为“11.12万公斤”。"),
    ("78.84方公斤", "78.84万公斤", "PaddleOCR 中/part02/page_0286 为“78.84万公斤”。"),
    ("粮食788方公斤", "粮食788万公斤", "PaddleOCR 中/part02/page_0286 为“粮食788万公斤”。"),
    ("长1177.2公单", "长1177.2公里", "PaddleOCR 上/part03/page_0031 为“长1177.2公里”。"),
    ("凭借自已的身份", "凭借自己的身份", "PaddleOCR 上/part02/page_0131 为“凭借自己的身份”。"),
    ("发表自已的意见", "发表自己的意见", "固定语境，应为“自己的意见”。"),
    ("发了自已的愤世", "发了自己的愤世", "人物文学语境，应为“自己的愤世激情”。"),
    ("形成自已的体育", "形成自己的体育", "学校体育传统项目语境，应为“自己的体育传统项目”。"),
]

CHECK_TERMS = [old for old, _new, _reason in REPLACEMENTS]


def apply_replacements() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new, reason in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                changes.append({
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "old": old,
                    "new": new,
                    "count": count,
                    "reason": reason,
                })
        if text != original:
            path.write_text(text, encoding="utf-8")
    residuals: dict[str, int] = {}
    for term in CHECK_TERMS:
        residuals[term] = 0
        for path in TARGETS:
            if path.exists():
                residuals[term] += path.read_text(encoding="utf-8", errors="ignore").count(term)
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 进入并入加入与单位残字补修 batch302",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/分册 HTML、正式正文汇总及对应分册正文源稿。",
        "- 依据：PaddleOCR 上册 part01/page_0063/page_0071/page_0076/page_0081、上册 part02/page_0131/page_0196、上册 part03/page_0031、中册 part02/page_0032/page_0097/page_0149/page_0286/page_0496、下册 part01/page_0171/page_0306。",
        "- 原则：只处理页级 OCR、同章同文或固定语境明确支持的窄短语；不处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 未处理：`动员工9.7万人` 因页级 OCR 同样保留该字形，未作推断替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['reason']}")
    lines.extend(["", "## 残留计数", ""])
    bad = {key: value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-07 进入并入加入与单位残字补修第三百零二批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据页级 OCR、同章同文与固定语境，窄语境补修 `进人 -> 进入`、`并人 -> 并入`、`加人 -> 加入`、`方公斤 -> 万公斤`、`公单 -> 公里`、`自已 -> 自己`、`生产于事 -> 生产干事` 等残字，共 {total} 处。
- 报告：`output/reports/enter_join_units_batch302_20260707.md`；进度：`output/reports/progress/20260707_进入并入加入与单位残字补修第三百零二批.md`。
- `动员工9.7万人` 因页级 OCR 同样保留该字形，未作推断替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    append_memory(total)
    print(f"total={total}")
    print(f"residuals_nonzero={ {k: v for k, v in residuals.items() if v} }")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
