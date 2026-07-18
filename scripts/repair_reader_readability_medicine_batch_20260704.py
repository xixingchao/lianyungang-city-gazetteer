# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in Volume 19 medicine."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_medicine_batch_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_medicine_batch_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十九卷医药高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第十九卷-医药">第十九卷医药</h2>'
SCOPE_END = '<h2 id="第二十卷-化学工业">第二十卷化学工业</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0114.txt:12-28; page_0115.txt:8-27; page_0116.txt:3-16; page_0117.txt:15-25; page_0118.txt:11-27; page_0119.txt:59-83; page_0120.txt:20-37; page_0121.txt:21-31; page_0123.txt:10-36; page_0124.txt:3-41; page_0125.txt:10-31; page_0126.txt:29-40; page_0128.txt:37-40; page_0129.txt:6-20; page_0130.txt:31-37; page_0131.txt:25-38; page_0132.txt:13-35; page_0134.txt:15-32; page_0135.txt:3-38"
REPLACEMENTS = [
    ("酊水剂", "一一些新开设的西药房，也偶尔配制一一些水剂", "一些新开设的西药房，也偶尔配制一些酊水剂"),
    ("医药支公司缺句", "1954年成立徐州医药分公司新海连药1958年", "1954年成立徐州医药分公司新海连药房，1956年改为新海连医药支公司，统一管理中西药、医疗器械的经营。1958年"),
    ("亏损", "多年号损", "多年亏损"),
    ("罂粟碱", "人工合成罂栗碱", "人工合成罂粟碱"),
    ("足叶乙甙概述", "抗癌新药一一足叶乙武", "抗癌新药——足叶乙甙"),
    ("强力灵破折号", "抗肝炎良药一一强力灵", "抗肝炎良药——强力灵"),
    ("药品管理法引号", "《中华人民共和国药品管理法，对药品生产", "《中华人民共和国药品管理法》，对药品生产"),
    ("证类本草段", "梁代的《本草经《本草纲目拾遗》中多处记载海州的药物", "梁代的《本草经集注》，唐代的《新修本草》，宋代的《图经本草》、《重修政和经史证类备用本草》（简称《证类本草》），明代的《本草品汇精要》、《本草蒙荃》、《本草纲目》、《本草乘雅半偈》以及清代的《本草纲目拾遗》中多处记载海州的药物"),
    ("证类本草标点", "《证类本，草》", "《证类本草》"),
    ("山踯躅", "海州山蹈、海州山茱英", "海州山踯躅、海州山茱萸"),
    ("菝葜", "海州樊、海州石韦", "海州菝葜、海州石韦"),
    ("菝葜考辨", "华东蓝刺头、、有柄石韦", "华东蓝刺头、菝葜、有柄石韦"),
    ("芫花蒺藜", "旋覆花、芜花、蒲黄、鹤虱、蛇床子、白葵藜", "旋覆花、芫花、蒲黄、鹤虱、蛇床子、白蒺藜"),
    ("辛荑栀子", "辛、子、凌霄", "辛荑、栀子、凌霄"),
    ("葶苈子", "苏败酱、掌劳子、半枝莲", "苏败酱、葶苈子、半枝莲"),
    ("海螵蛸", "艾叶、海螺等", "艾叶、海螵蛸等"),
    ("十至五十吨", "香需；1050吨", "香需；10~50吨"),
    ("菟丝子桑螵蛸", "菀丝子、老鹳草、桑骠", "菟丝子、老鹳草、桑螵蛸"),
    ("平原葶苈子", "扁蓄、掌劳子、小蓟", "扁蓄、葶苈子、小蓟"),
    ("山茱萸种植场", "主要种植山茱黄、薏苡", "主要种植山茱萸、薏苡"),
    ("十一届三中全会缺句", "<p>均由连云港医药采购供应站", "<p>中共十一届三中全会以后，按市场需求和指导性计划安排药材种植，种植面积和品种均由连云港医药采购供应站"),
    ("五十年代末", "20世纪50年代未", "20世纪50年代末"),
    ("牛蒡子栝楼", "牛劳子、金银花、楼等50多种", "牛蒡子、金银花、栝楼等50多种"),
    ("山茱萸科研", "山茱黄、黄连科研项目", "山茱萸、黄连科研项目"),
    ("山茱萸获奖", "天麻和山茱黄", "天麻和山茱萸"),
    ("家种药材山茱萸", "凌霄花、山茱黄、金银花", "凌霄花、山茱萸、金银花"),
    ("草药资源资料", "《云台山中草药资源档案的空白", "《云台山中草药简志》、《云台山中草药资源普查与研究》、《中草药彩照图集》等资料，填补了连云港市中药资源档案的空白"),
    ("炒煅", "炒缎、蒸制", "炒煅、蒸制"),
    ("饮片技改缺句", "1987年，对中药饮片生产进行技术改造，150多吨", "1987年，对中药饮片生产进行技术改造，更新加工设备并添置检测仪器，实现了机械化、科学化生产，生产品种达600个，年产能力150多吨"),
    ("泛叠菊花心", "泛查、合煎、摊药等过程。摊膏药要成为花心", "泛叠、合煎、摊药等过程。摊膏药要成为菊花心"),
    ("秃虺蛇", "俗称“秃蛇”", "俗称“秃虺蛇”"),
    ("板蓝根干糖浆", "板蓝根于糖浆", "板蓝根干糖浆"),
    ("酊水剂剂型", "后又进一步扩大到水、口服液", "后又进一步扩大到酊水、口服液"),
    ("藿香正气片", "蕾香正气片", "藿香正气片"),
    ("酊水剂去重", "口服液剂、酊酊水剂", "口服液剂、酊水剂"),
    ("酊水剂品种", "口服液剂、水剂、胶囊剂等10种剂型", "口服液剂、酊水剂、胶囊剂等10种剂型"),
    ("减脂茶投入", "减脂茶为连云港中药厂1978年自行研制，1979年初投人批量生产", "减脂茶为连云港中药厂1978年自行研制，1979年初投入批量生产"),
    ("酊水剂生产", "生产原料药、水剂、片剂", "生产原料药、酊水剂、片剂"),
    ("新海油厂", "新海油广生产", "新海油厂生产"),
    ("曙光化工厂", "曙光化工广生产", "曙光化工厂生产"),
    ("红旗制药厂破折号", "正式药厂一红旗制药厂", "正式药厂——红旗制药厂"),
    ("陈皮酊", "陈皮酐", "陈皮酊"),
    ("逐年增长", "遂年增长", "逐年增长"),
    ("抗菌痢胶囊", "试制抗菌胶囊", "试制抗菌痢胶囊"),
    ("投入小批量", "投人小批量生产", "投入小批量生产"),
    ("向阳制药厂", "连云港向阳制药广", "连云港向阳制药厂"),
    ("东风制药厂", "一师制药广改名", "一师制药厂改名"),
    ("酊水剂线", "改造水剂生产线", "改造酊水剂生产线"),
    ("酊水剂品", "酐水剂品", "酊水剂品"),
    ("进入八十年代", "进人20世纪80年代", "进入20世纪80年代"),
    ("异博定投入", "产品当年通过验收并投人生产", "产品当年通过验收并投入生产"),
    ("上海医药工业研究院缺句", "该厂在上海级鉴定，并投入批量生产", "该厂在上海医药工业研究院帮助下，用Ⅱ树脂取代CAP作肠溶隔离层试验成功，填补了国内空白。1984年，生物化学制药厂与蜂疗专家房柱共同研制的抗血脂新药——蜂胶片通过省级鉴定，并投入批量生产"),
    ("足叶乙甙技术", "足叶乙武生产技术", "足叶乙甙生产技术"),
    ("足叶乙甙原料", "足叶乙武。", "足叶乙甙。"),
    ("654-2", "654一2", "654-2"),
    ("布洛芬", "布落芬", "布洛芬"),
    ("荼普生", "茶普生", "荼普生"),
    ("足叶乙甙针剂", "针剂罂粟碱、足叶乙武", "针剂罂粟碱、足叶乙甙"),
    ("抗菌痢胶囊名录", "大蒜素、抗菌痫", "大蒜素、抗菌痢"),
    ("甘露醇工艺缺句", "150吨温除盐", "150吨左右。1988年又将水浸泡改为多级多次酸水套泡，将高电耗的电渗析器除盐工艺改为高温除盐"),
    ("大蒜素", "大薪素", "大蒜素"),
    ("进入城市医院", "进人城市医院", "进入城市医院"),
    ("进入市场", "进人市场", "进入市场"),
    ("进入临床", "进人临床验证", "进入临床验证"),
    ("足叶乙甙标题", "足叶乙武国内", "足叶乙甙 国内"),
    ("足叶投入", "1987年正式投人生产", "1987年正式投入生产"),
    ("进入美国", "在国际上进人了美国", "在国际上进入了美国"),
    ("足叶乙甙产能", "足叶乙武20公斤", "足叶乙甙20公斤"),
    ("异博定粉", "昇博定粉800公斤", "异博定粉800公斤"),
    ("罂粟碱产能", "罄粟碱160公斤", "罂粟碱160公斤"),
    ("东北制药总厂", "东北制药总广", "东北制药总厂"),
    ("上海化工厂", "上海化工广", "上海化工厂"),
    ("足叶乙甙获奖", "原料药足叶乙武于1987年", "原料药足叶乙甙于1987年"),
    ("五金工具厂", "新浦五金工具广", "新浦五金工具厂"),
    ("眼镜厂", "原市眼镜广", "原市眼镜厂"),
    ("医疗材料坯", "漂白毛巾坏", "漂白毛巾坯"),
    ("坯布", "坏布、脱脂纱布", "坯布、脱脂纱布"),
    ("LYG-75型", "LYG一75型", "LYG-75型"),
    ("金牛引号", "优秀新产品金牛”奖", "优秀新产品“金牛”奖"),
    ("朝阳卫生材料厂开头", "一、连云港市朝阳卫生材料厂体企业", "一、连云港市朝阳卫生材料厂该厂为1980年由原市朝阳毛巾厂改建的市内第一家卫生材料厂。该厂为朝阳乡集体企业"),
    ("药包材该厂", "该广充分利用先进", "该厂充分利用先进"),
    ("药包材金牛", "第二届新产品金牛”奖", "第二届新产品“金牛”奖"),
    ("又有西药房", "以后文有多家西药房", "以后又有多家西药房"),
    ("兵燹", "屡遭兵，尤其日本", "屡遭兵燹，尤其日本"),
    ("省优质服务单位", "省优质服务单省级企业管理优秀单位", "省优质服务单位、省级“四好”仓库、省中药饮片质量先进单位等荣誉称号，1990年被评为省先进企业、省级企业管理优秀单位"),
    ("跌入低谷", "跌人低谷", "跌入低谷"),
    ("列入计划", "列人省医药公司", "列入省医药公司"),
    ("萎缩", "随之菱缩", "随之萎缩"),
    ("卫生材料厂", "朝阳卫生材料广的纱布", "朝阳卫生材料厂的纱布"),
    ("纳入主渠道", "医药纳人国营", "医药纳入国营"),
    ("膏丸剂", "离丸剂、水剂", "膏丸剂、酊水剂"),
    ("疟疾", "症疾、甲状腺", "疟疾、甲状腺"),
    ("斯锑黑克", "斯黑克、酒古酸锑钾", "斯锑黑克、酒古酸锑钾"),
    ("乙胺嘧啶", "乙胺啶、海群生、驱灵", "乙胺嘧啶、海群生、驱蛔灵"),
    ("淮北", "向准北盐务局", "向淮北盐务局"),
    ("流弊", "严防流彝", "严防流弊"),
    ("麻醉药品办法缺句", "1987年11月国务院重新发布卡、按量供应", "1987年11月国务院重新发布《麻醉药品管理办法》。各医药商业部门在麻醉药品保管、销售等各环节严格把关，坚持按卡、按量供应"),
    ("天津史克", "大津史克", "天津史克"),
]

RESIDUE_PARAGRAPHS = [
    "<p>产量(公斤)年份太子参1957山东临沭139268赣榆、东海1969玄参山东郊城赣榆19582053851976北沙参1959山东莱阳赣榆1313131969杭州1959466844赣榆、东海、灌云1975淮阴佩兰19657508101984徐州薏苡1968163410赣榆、东海、灌云1977</p>\n",
    "<p>年份产量（公斤）</p>\n",
    "<p>地黄19682184351979赣榆、东海、灌云徐州牡丹62019791971310赣榆、东海、灌云南通1441978延胡索1972赣榆、东海、灌云190安徽东海、灌云：</p>\n",
    "<p>1511861978板蓝根197319732611701979黄芪赣榆、东海、灌云黑龙江依兰县赣榆、东海、灌云1202521982桔梗1979山东临沭连云港市正常年景家种主要药材有30多个品种，2500亩，年总产量为500吨。其中年产量在50~100吨的有太子参、薏苡、玄参、北沙参；10~50吨的有白芍、地黄、丹参、桔梗、佩兰、板蓝根、芡实等；10吨以下的有延胡索、瓜萎、紫苏、白苏、丹皮、枫茄花、凌霄花、山茱萸、金银花等。</p>",
]
RESIDUE_REPLACEMENT = "<p>连云港市正常年景家种主要药材有30多个品种，2500亩，年总产量为500吨。其中年产量在50~100吨的有太子参、薏苡、玄参、北沙参；10~50吨的有白芍、地黄、丹参、桔梗、佩兰、板蓝根、芡实等；10吨以下的有延胡索、瓜萎、紫苏、白苏、丹皮、枫茄花、凌霄花、山茱萸、金银花等。</p>"


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    original = text[start:end]
    segment = original
    counts: dict[str, int] = {}
    for label, old, new in REPLACEMENTS:
        count = segment.count(old)
        if count:
            segment = segment.replace(old, new)
        elif new not in segment:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    residue_count = 0
    for residue in RESIDUE_PARAGRAPHS[:-1]:
        if residue.strip() in segment:
            segment = segment.replace(residue.strip(), "", 1)
            residue_count = 1
        elif RESIDUE_REPLACEMENT not in segment:
            raise RuntimeError("table 19-3 residue paragraph not found")
    final_residue = RESIDUE_PARAGRAPHS[-1]
    if final_residue in segment:
        segment = segment.replace(final_residue, RESIDUE_REPLACEMENT, 1)
        residue_count = 1
    elif RESIDUE_REPLACEMENT not in segment:
        raise RuntimeError("table 19-3 final residue paragraph not found")
    counts["表19-3压平残文"] = residue_count
    if segment != original:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [new for _label, _old, new in REPLACEMENTS if new not in segment]
    residuals = [old for _label, old, new in REPLACEMENTS if old in segment and old not in new]
    residue_residuals = [p for p in RESIDUE_PARAGRAPHS if p.strip() in segment]
    if missing or residuals or residue_residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}, residue_residuals={len(residue_residuals)}")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_changes = sum(counts.values())
    verified_items = len(REPLACEMENTS) + 1
    payload = {
        "time": now,
        "scope": "第十九卷医药",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": verified_items,
        "current_run_replacements": current_changes,
        "counts": counts,
        "principle": "仅修复页级 OCR 清楚给出正确写法的第十九卷错识；未由结构化表承接的表格残文不删除。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第十九卷医药高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复/收束：{verified_items} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 重点：修正概述、中药材、化学制药、医疗器械材料、医药购销中的药名、厂名、投入/列入、缺句和错字。",
        "- 表格：删除已由 `LYG-中-T013/T014` 承接的表19-3压平残文；表19-4尚未结构化承接，残留单位段未删。",
        "- 保留：源 OCR 自身不能确认的药品名和表格数字不凭猜测改。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第十九卷医药高置信错识回源修复

- 对第十九卷医药进行小批回源修复，范围限定在 `第十九卷-医药` 到 `第二十卷-化学工业` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`多年号损`→`多年亏损`，`足叶乙武`→`足叶乙甙`，`山茱黄`→`山茱萸`，`投人/列人/进人`→`投入/列入/进入`，并补回中药资源普查资料、饮片技改、医药商业荣誉等缺句。
- 本批核验修复/收束 {verified_items} 项；已删除表19-3压平残文 1 组，因该表已由 `LYG-中-T013/T014` verified 表承接；未核定疑点保留。
- 报告：`output/reports/reader_readability_medicine_batch_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第十九卷医药高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
