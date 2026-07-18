# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern residues, batch 111."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch111_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch111_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_海关与对虾弧菌残留回源补修第一百一十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "海关现场查私隐匿不报",
        "old": "他们曾多次查获港澳和中远船员隐不报、伪造发票、进口物品和走私外汇出口以及夹带禁止进口的黄色、淫移、反动印刷品等案件。",
        "new": "他们曾多次查获港澳和中远船员隐匿不报、伪造发票、进口物品和走私外汇出口以及夹带禁止进口的黄色、淫秽、反动印刷品等案件。",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0502.txt:4-5；raw 同页误作隐不报/淫移",
    },
    {
        "label": "海关黄色淫秽录音录像带",
        "old": "1986~1987年，多次发现船员将黄色、淫移的录音、录像带伪装成空白带或改换片名等蒙混进口的走私案件。",
        "new": "1986~1987年，多次发现船员将黄色、淫秽的录音、录像带伪装成空白带或改换片名等蒙混进口的走私案件。",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0502.txt:9-10；raw 同页误作淫移",
    },
    {
        "label": "海关顾某走私案件补漏",
        "old": "1985年4月，码头值勤关员查获了河北省远洋公司“新东”轮服务员吕某藏于食品箱中的黄色画报和黄色录像带。1986和录像机一台的走私案件，处当事人罚款3000元，追回物品。1987年1月28日（除岁）",
        "new": "1985年4月，码头值勤关员查获了河北省远洋公司“新东”轮服务员吕某藏于食品箱中的黄色画报和黄色录像带。1986年5月，查获外运连云港分公司顾某于夜间11时登利比里亚籍“银杉”轮购买外烟78条和录像机一台的走私案件，处当事人罚款3000元，追回物品。1987年1月28日（除夕）",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0502.txt:12-14；raw 同页漏顾某案件并误作除岁",
    },
    {
        "label": "海关顾某走私案件源稿断行补漏",
        "old": "了河北省远洋公司“新东”轮服务员吕某藏于食品箱中的黄色画报和黄色录像带。1986\n和录像机一台的走私案件，处当事人罚款3000元，追回物品。1987年1月28日（除岁）",
        "new": "了河北省远洋公司“新东”轮服务员吕某藏于食品箱中的黄色画报和黄色录像带。1986\n年5月，查获外运连云港分公司顾某于夜间11时登利比里亚籍“银杉”轮购买外烟78条\n和录像机一台的走私案件，处当事人罚款3000元，追回物品。1987年1月28日（除夕）",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0502.txt:12-14；源稿断行残留",
    },
    {
        "label": "海关拖轮与淫秽刊物",
        "old": "晚，上海航道局一瘦去香港施工后的拖轮靠港。根据有关情况，船管科对其实行重点抽查，结果发现有船员带录像机一台、录像带11盘、电动打字机1台、外烟52条、旧服装60余件、淫移刊物6份未向海关申报，企图利用节日闯关。",
        "new": "晚，上海航道局一艘去香港施工后的拖轮靠港。根据有关情况，船管科对其实行重点抽查，结果发现有船员带录像机一台、录像带11盘、电动打字机1台、外烟52条、旧服装60余件、淫秽刊物6份未向海关申报，企图利用节日闯关。",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0502.txt:15-17；raw 同页误作一瘦/淫移",
    },
    {
        "label": "海关拖轮源稿断行",
        "old": "晚，上海航道局一瘦去香港施工后的拖轮靠港。根据有关情况，船管科对其实行重点抽",
        "new": "晚，上海航道局一艘去香港施工后的拖轮靠港。根据有关情况，船管科对其实行重点抽",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0502.txt:15；源稿断行残留",
    },
    {
        "label": "海关现场查私源稿断行",
        "old": "禁止进口的黄色、淫移、反动印刷品等",
        "new": "禁止进口的黄色、淫秽、反动印刷品等",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0502.txt:5；源稿断行残留",
    },
    {
        "label": "海关黄色淫秽录音录像带源稿断行",
        "old": "船员将黄色、淫移的录音、录像带伪装成空白带",
        "new": "船员将黄色、淫秽的录音、录像带伪装成空白带",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0502.txt:10；源稿断行残留",
    },
    {
        "label": "海关拖轮淫秽刊物源稿断行",
        "old": "余件、淫移刊物6份未向海关申报",
        "new": "余件、淫秽刊物6份未向海关申报",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0502.txt:17；源稿断行残留",
    },
    {
        "label": "东方对虾弧菌发病临界值",
        "old": "确定每毫升含量10万个是孤菌发病的临界值",
        "new": "确定每毫升含量10万个是弧菌发病的临界值",
        "source": "workbench/ocr/paddle_ocr/上/part03/page_0113.txt:17；raw 同页误作孤菌，邻句多处弧菌互证",
    },
]

LEFT_UNTOUCHED = [
    "公路管理段 `防碍交通安全运行` raw/Paddle 同页均作 `防碍`，暂不凭现代规范改为 `妨碍`。",
    "下册科技段 `中国对虾孤菌病防治研究` raw/Paddle 同页均作 `孤菌`，虽与上册 `东方对虾弧菌病` 类似，本批仍不猜改。",
    "税务/饮食业 `链席` 尚未取得同页 Paddle 正形，继续保留。",
    "本批未使用或展示页图。",
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
        for item in items:
            item["verified"] = verify.count(item["new"])
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Source-backed modern residue repair for customs and shrimp vibrio sections",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with page-level raw/Paddle evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 海关与对虾弧菌残留补修第一百一十一批：回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的海关现场查私段和上册对虾疾病防治段 OCR 残留。",
        "- 仅处理 raw/Paddle 页级文本可闭合的精确短语或同页漏句。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次运行新增替换：{payload['changed_this_run']} 处",
        f"- 当前核验覆盖：{payload['verified_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百一十一批：海关与对虾弧菌残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 raw/Paddle 页级回源，修复海关现场查私段 `淫移 -> 淫秽`、`隐不报 -> 隐匿不报`、`一瘦 -> 一艘`、`除岁 -> 除夕`，并补回 `1986年5月...顾某...` 漏句；同步修复上册对虾疾病防治段 `孤菌发病 -> 弧菌发病`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch111_20260706.md`。
- 边界：`防碍交通安全运行`、下册科技段 `中国对虾孤菌病防治研究`、税务/饮食业 `链席` 继续等待更强证据；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
