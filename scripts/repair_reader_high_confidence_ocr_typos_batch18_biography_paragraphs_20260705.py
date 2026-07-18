# -*- coding: utf-8 -*-
"""Eighteenth batch: PaddleOCR-backed biography paragraph repairs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch18_biography_paragraphs_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch18_biography_paragraphs_20260705.json"

CHANGES = [
    {
        "section": "李赓三传",
        "old": "<p>李魔三（1894～1940）海州李村人。民国28年（1939年）3月，日军侵占海州后，烧杀抢掠的罪行激起季三的民族仇恨，多次孤身一一人夜袭新浦西口日军岗哨，杀死日军2人、汉奸1人，获得日式三八枪2支。日军得知系李三所为，多次偷袭小李庄，李三之妻不幸落入日军魔掌并惨遭杀害。民国28年秋，日本人小野和朝鲜人李云龙在海州洪门果园被季三抓捕，小野因反抗被李三击毙，李云龙被解至东海县政府。李三在东海县组织抗日铁血锄奸大队，集中300余人，以东海县平明乡为根据地开展游击战争，以少数零星日伪军为袭击目标，打击其器张气焰。抗日铁血锄奸大队被东海县政府编入东海县常备大队，县长庞寿峰兼任大队长，季三任中队长。民国29年1月2日，由于汉奸告密，日军围剿小季庄，日军用刺刀驱赶村民集合，强迫村民交出季三，否则，将血洗小李庄。在危急关头，李三为使村民免遭杀戮，挺身而出献出了自己的生命。解放后，东海县人民政府追认李三为抗日革命烈士。</p>",
        "new": "<p>李赓三（1894～1940）海州李村人。民国28年（1939年）3月，日军侵占海州后，烧杀抢掠的罪行激起李赓三的民族仇恨，多次孤身一人夜袭新浦西筋口日军岗哨，杀死日军2人、汉奸1人，获得日式三八枪2支。日军得知系李赓三所为，多次偷袭小李庄，李赓三之妻不幸落入日军魔掌并惨遭杀害。民国28年秋，日本人小野和朝鲜人李云龙在海州洪门果园被李赓三抓捕，小野因反抗被李赓三击毙，李云龙被解至东海县政府。李赓三在东海县组织抗日铁血锄奸大队，集中300余人，以东海县平明乡为根据地开展游击战争，以少数零星日伪军为袭击目标，打击其嚣张气焰。抗日铁血锄奸大队被东海县政府编入东海县常备大队，县长庞寿峰兼任大队长，李赓三任中队长。民国29年1月2日，由于汉奸告密，日军围剿小李庄，日军用刺刀驱赶村民集合，强迫村民交出李赓三，否则，将血洗小李庄。在危急关头，李赓三为使村民免遭杀戮，挺身而出献出了自己的生命。解放后，东海县人民政府追认李赓三为抗日革命烈士。</p>",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0355.txt:9-19 PaddleOCR 给出完整李赓三传段落",
            "workbench/ocr/raw/下/part02/page_0355.txt 原 OCR 可见人名与地名误识残留",
        ],
    },
    {
        "section": "吴辟初传",
        "old": "<p>吴辟初（1897～1943）灌云县南岗潘洼人。自幼习武，枪法很好，防匪保家，闻名乡里。民国28年（1939年）3月，日军从灌河口登陆，灌云县政府弃城逃跑，吴辟初非常愤慨，对中国共产党坚持抗战的立场深表敬意，成为党的忠实朋友。7月，国民党顽固派制造“汤沟事件”，杀害八路军三团团长汤曙红。该团北撤后留下五六十人坚持斗争，得到吴辟初的掩护。中共灌云县委地下联络点设在吴家。8月，吴辟初被国民党东海县长庞寿峰委任为东海县常备队第二大队长。民国29年秋，灌云县抗日民主政权成立，吴辟初应邀担任抗日民主政权县参议员、县土绅委员会主任、边区联防主任和淮海区参议员。民国30年，伪军大队长杨九洲多次企图在南岗以南建立据点，在吴辟初领导的地方武装抵抗下，未能得逞。民国32年3月，伪军三四百人进犯潘家洼，被吴辟初打退。4月中旬，日军平墩等地。22日凌晨，灌云县党政机关和一个警卫队从李恒庄向潘家洼转移，不幸与敌人遭遇，双方发生激战。县委负责人钱天素立即带领机关人员向叮当河东撤退，并要求昊辟初一起转移，但吴辟初坚持待县机关安全撤出后，自己才撤离阵地。撤退中吴辟初胸部中弹，部下要架着他走，他命令大家：“快跑，不要管我。”不幸再次中弹，壮烈牺牲。</p>",
        "new": "<p>吴辟初（1897～1943）灌云县南岗潘洼人。自幼习武，枪法很好，防匪保家，闻名乡里。民国28年（1939年）3月，日军从灌河口登陆，灌云县政府弃城逃跑，吴辟初非常愤慨，对中国共产党坚持抗战的立场深表敬意，成为党的忠实朋友。7月，国民党顽固派制造“汤沟事件”，杀害八路军三团团长汤曙红。该团北撤后留下五六十人坚持斗争，得到吴辟初的掩护。中共灌云县委地下联络点设在吴家。8月，吴辟初被国民党东海县长庞寿峰委任为东海县常备队第二大队长。民国29年秋，灌云县抗日民主政权成立，吴辟初应邀担任抗日民主政权县参议员、县士绅委员会主任、边区联防主任和淮海区参议员。民国30年，伪军大队长杨九洲多次企图在南岗以南建立据点，在吴辟初领导的地方武装抵抗下，未能得逞。民国32年3月，伪军三四百人进犯潘家洼，被吴辟初打退。4月中旬，日军从徐州调来加强大队和伪军四五百人，于4月21日扫荡灌云县境内抗日根据地李恒庄、平墩等地。22日凌晨，灌云县党政机关和一个警卫队从李恒庄向潘家洼转移，不幸与敌人遭遇，双方发生激战。县委负责人钱天素立即带领机关人员向叮当河东撤退，并要求吴辟初一起转移，但吴辟初坚持待县机关安全撤出后，自己才撤离阵地。撤退中吴辟初胸部中弹，部下要架着他走，他命令大家：“快跑，不要管我。”不幸再次中弹，壮烈牺牲。民国33年1月，淮海区各界人士在叮当河滩为吴辟初立碑公祭。</p>",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0356.txt:11-25 PaddleOCR 给出吴辟初传完整后半段",
            "workbench/ocr/raw/下/part02/page_0356.txt 原 OCR 可见县土绅、日军平墩等地、昊辟初等误识",
        ],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修两个人物传略中已由页级 PaddleOCR 明确支持的整段缺损与错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十八批：人物传略整段对照",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- {item['section']}：整段替换 1 处，恢复页级 PaddleOCR 支持的人名、地名、事由和缺失句。")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版；不改中间 OCR 原文。",
        "- 不展示、未嵌入页图；证据来自本地 OCR 文本路径。",
        "- 不扩大到其它人物传略或 `器张/嚣张` 全局替换。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
