# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern residues, batch 110."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch110_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch110_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_治安税务蔬菜残留回源补修第一百一十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "芥菜品种雪里蕻",
        "old": "芥菜品种有板叶芥、板叶雪里麒。",
        "new": "芥菜品种有板叶芥、板叶雪里蕻。",
        "source": "workbench/ocr/paddle_ocr/上/part02/page_0251.txt:12；raw 同页误作雪里麒",
    },
    {
        "label": "蔬菜公司采购雪里蕻",
        "old": "派员到外地采购干菜5万公斤，雪里麒150缸，作冬缺之用。",
        "new": "派员到外地采购干菜5万公斤，雪里蕻150缸，作冬缺之用。",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0148.txt:11；raw 同页误作雪里麒",
    },
    {
        "label": "路政通告谩骂殴打",
        "old": "更不能围攻、漫骂、殿打路政管理人员",
        "new": "更不能围攻、谩骂、殴打路政管理人员",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0038.txt:41；raw 同页误作漫骂、殿打",
    },
    {
        "label": "小型技术措施贷款额度",
        "old": "1979年，单项贷款的最高额度般在10万元以内",
        "new": "1979年，单项贷款的最高额度一般在10万元以内",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0301.txt:31；raw 同页漏一",
    },
    {
        "label": "小型技术措施贷款额度源稿断行",
        "old": "高额度般在10万元以内",
        "new": "高额度一般在10万元以内",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0301.txt:31；源稿断行残留",
    },
    {
        "label": "良种场包干办法",
        "old": "超亏不补、限期扭亏”的包于办法。",
        "new": "超亏不补、限期扭亏”的包干办法。",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0305.txt:23；raw 同页误作包于",
    },
    {
        "label": "事业单位奖金税免征限额",
        "old": "上述四种类型免征限额为不人均基本工资不足80元的按80元计税",
        "new": "上述四种类型免征限额为不超过1个月。1988年底，免征限额分别调整为3个半月、2个半月、2个月和1个半月；月人均基本工资不足80元的按80元计税",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0326.txt:19-21；raw 同页漏整句",
    },
    {
        "label": "大专院校保卫淫秽书刊",
        "old": "开展对淫移书刊的查禁和收缴工作。",
        "new": "开展对淫秽书刊的查禁和收缴工作。",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0071.txt:39；raw 同页误作淫移",
    },
    {
        "label": "淮海大学学生被殴打事件",
        "old": "连云港淮海大学发生一起学生被校外不法分子殿打事件",
        "new": "连云港淮海大学发生一起学生被校外不法分子殴打事件",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0072.txt:9-10；raw 同页误作准海/殿打",
    },
    {
        "label": "淮海大学学生被殴打事件源稿准海残留",
        "old": "连云港准海大学发生一起学生被校外不法分\n子殿打事件",
        "new": "连云港淮海大学发生一起学生被校外不法分\n子殴打事件",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0072.txt:9-10；源稿断行残留",
    },
    {
        "label": "学生被殴打事件源稿断行",
        "old": "子殿打事件",
        "new": "子殴打事件",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0072.txt:10；源稿断行残留",
    },
    {
        "label": "流氓案件侮辱调戏",
        "old": "下流语言肆意悔厚、调戏。",
        "new": "下流语言肆意侮辱、调戏。",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0074.txt:31；raw 同页误作悔厚",
    },
    {
        "label": "流氓案件陈某被殴打",
        "old": "致使陈弟肝部受伤，陈某也被殿打致伤。",
        "new": "致使陈弟肝部受伤，陈某也被殴打致伤。",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0074.txt:32；raw 同页误作殿打",
    },
    {
        "label": "流氓案件淫秽读物",
        "old": "从其身上搜出秽读物手抄本2种4本。",
        "new": "从其身上搜出淫秽读物手抄本2种4本。",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0074.txt:34；raw 同页漏淫",
    },
    {
        "label": "流氓案件淫秽读物源稿断行",
        "old": "从其身上搜出秽读物手抄本",
        "new": "从其身上搜出淫秽读物手抄本",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0074.txt:34；源稿断行残留",
    },
    {
        "label": "流氓案件猥亵妇女",
        "old": "人群密集处狠亵妇女10余次。",
        "new": "人群密集处猥亵妇女10余次。",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0074.txt:35；raw 同页误作狠亵",
    },
    {
        "label": "胜利村猥亵仓惶逃窜",
        "old": "猛然觉得有人对她狠亵，她大喊“抓流氓”，犯罪分子仓煌逃窜。",
        "new": "猛然觉得有人对她猥亵，她大喊“抓流氓”，犯罪分子仓惶逃窜。",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0074.txt:37；raw 同页误作狠亵/仓煌",
    },
    {
        "label": "查获淫秽物品段补漏",
        "old": "查获淫物品1977年，市公安局在打击青少年犯罪活动中，共收缴黄色淫秽书刊484本。1982~1983年，市公安局查处制作、销售、贩卖反动淫书刊案2起，治安处罚2书刊168本。1985年，市委宣传部、市公安局发布《关于加强严禁淫秽物品宣传教育的意见》，市公安局查禁淫移物品办公室共破获利用淫秒物品犯罪案3起，抓获犯罪分子4人，令停止放映。1987年，市公安局查处制作、传播、贩卖淫移物品案9起，治安处罚17人，查封3个个体录音制作、复制经销点，查获非法出版物21160份、迷信印刷品44761张、各类有害图片772张、录音带1147盘、录像带98盘。9月10日，市政府发布《关于收缴淫移物品的布告》。1988年，市公安局查处制作、贩卖、传播淫移物品案14起，治安处罚26人，收缴淫移录像带81盘、录音带37盘、淫移画报图片挂历115份、裸体扑克57副、非法印刷品3方余件。1989年，市公安局共查处制作、贩卖、传播秽物品案29起，治安处罚93人。",
        "new": "查获淫秽物品1977年，市公安局在打击青少年犯罪活动中，共收缴黄色淫秽书刊484本。1982~1983年，市公安局查处制作、销售、贩卖反动淫秽书刊案2起，治安处罚2人，收缴淫秽书刊77本、裸体画片301份、黄色录音带25盘。1984年，市公安局收缴淫秽书刊168本。1985年，市委宣传部、市公安局发布《关于加强严禁淫秽物品宣传教育的意见》，市公安局查禁淫秽物品办公室共破获利用淫秽物品犯罪案3起，抓获犯罪分子4人，收缴淫秽书刊10本、图片照片103张、录像带33盘，对47处未经批准私自放映录像的责令停止放映。1987年，市公安局查处制作、传播、贩卖淫秽物品案9起，治安处罚17人，查封3个个体录音制作、复制经销点，查获非法出版物21160份、迷信印刷品44761张、各类有害图片772张、录音带1147盘、录像带98盘。9月10日，市政府发布《关于收缴淫秽物品的布告》。1988年，市公安局查处制作、贩卖、传播淫秽物品案14起，治安处罚26人，收缴淫秽录像带81盘、录音带37盘、淫秽画报图片挂历115份、裸体扑克57副、非法印刷品3万余件。1989年，市公安局共查处制作、贩卖、传播淫秽物品案29起，治安处罚93人。",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0085.txt:25-36；raw 同页多处漏字/误字/漏句",
    },
    {
        "label": "查获淫秽物品段源稿零散残留",
        "old": "查获淫物品",
        "new": "查获淫秽物品",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0085.txt:25；源稿断行残留",
    },
    {
        "label": "查禁淫秽物品办公室源稿残留",
        "old": "查禁淫移物品办公室共破获利用淫秒物品犯罪案",
        "new": "查禁淫秽物品办公室共破获利用淫秽物品犯罪案",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0085.txt:29；源稿断行残留",
    },
    {
        "label": "淫秽录像带源稿残留",
        "old": "缴淫移录像带81盘、录音带37盘、淫移画报图片挂历115份",
        "new": "缴淫秽录像带81盘、录音带37盘、淫秽画报图片挂历115份",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0085.txt:35；源稿断行残留",
    },
    {
        "label": "非法印刷品三万余件源稿残留",
        "old": "非法印刷品\n3方余件",
        "new": "非法印刷品\n3万余件",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0085.txt:35-36；源稿断行残留",
    },
]

LEFT_UNTOUCHED = [
    "海关段 `黄色、淫移` 仍只见 raw 页级错形，暂未找到 Paddle 页级正形，不在本批处理。",
    "税务/饮食业 `链席` 尚未取得同页 Paddle 正形，暂不按常识改为 `筵席`。",
    "`中西合壁` 与 `并人徐州第四监狱` 继续保留，等待更强证据。",
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
        "scope": "Source-backed modern residue repair for public security, tax, loan, and vegetable sections",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with page-level raw/Paddle evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 治安税务蔬菜残留补修第一百一十批：回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的治安、税务、信贷、蔬菜段 OCR 残留。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百一十批：治安税务蔬菜残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 raw/Paddle 页级回源，修复蔬菜 `雪里麒 -> 雪里蕻`、交通路政 `漫骂/殿打 -> 谩骂/殴打`、信贷 `高额度般 -> 高额度一般`、财政 `包于办法 -> 包干办法`、税务奖金税漏句，以及下册治安段 `淫移/淫秒/狠亵/悔厚/仓煌` 等残留。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch110_20260706.md`。
- 边界：海关段 `黄色、淫移`、税务/饮食业 `链席`、`中西合壁`、`并人徐州第四监狱` 未取得更强证据，继续保留；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
