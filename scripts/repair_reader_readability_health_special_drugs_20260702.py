# -*- coding: utf-8 -*-
"""Restore special-drug management subsection from OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_special_drugs_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_special_drugs_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷特殊药品管理回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101255-101294; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7951-7990; "
    "workbench/ocr/paddle_ocr/下/part02/page_0199.txt:19-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0200.txt:3-22"
)
SCOPE_START_OPTIONS = ("<p>五、特殊药品管理", "<p><strong>五、特殊药品管理</strong></p>")
SCOPE_END = '<h4 id="第五十五卷-第四章医政 药政-第五节药品检验">第五节药品检验</h4>'

NEW_HTML = """<p><strong>五、特殊药品管理</strong></p>
<p><strong>麻醉药品管理</strong></p>
<p>1950年，根据中央人民政府政务院《关于麻醉药品临时登记处理办法的通知》和中央人民政府卫生部《管理麻醉药品暂行条例》，各医疗卫生单位及药店对麻醉药品进行清理、登记和处理。1951年4月，市卫生科、税务局、工商科、公安局及市医师联合会联合组建麻醉药品清理登记小组，对各医、药单位抽查。1953年初，市卫生科规定除公立医疗机构的正式医师按《管理麻醉药品暂行条例》享有麻醉药品处方权外，其他各类私立医疗机构未经政府批准一律不准使用麻醉药品。但根据需要，市卫生科批准11名无正式医师资格的医生享有麻醉药品处方权。</p>
<p>1954年，对麻醉药品使用量修订，规定一般注射剂每次可开一次使用量，片剂每次可开一日量；特殊病人如需超量，注射剂可每次开一日量，片剂每次可开三日量。1959年8月，市卫生局对20家医疗单位的麻醉药品使用情况检查。1963年，根据国家卫生部颁发《关于加强麻醉药品管理、严防流弊的联合通知》，市卫生局组织一次麻醉药品管理的全面检查，对批准使用麻醉药品的医疗单位的资格和权限重新审查。江苏省卫生厅批准连云港市新浦人民医院等市内7家医院为使用麻醉药品的医疗单位。麻醉药品实行专人保管，专用处方，专柜加锁保存，专册登记，专帐管理。</p>
<p>1965年，麻醉药品使用权由省卫生厅下放至市卫生局，麻醉药品使用权扩大到部分基层医疗单位。1979年10月，根据省卫生厅《关于贯彻〈麻醉药品管理条例细则〉的补充规定》，公社卫生院使用麻醉药品必须具备一定条件，特殊病人需用麻醉药品，凭医院诊断证明及所在单位或生产大队介绍信，持病人户口簿至市卫生局申请，由市卫生局核定麻醉药品特殊使用卡后，方可到指定医疗单位开具处方取药，病人死亡后立即交还使用卡。</p>
<p>1984年2月，市卫生局制订《晚期癌症病人使用麻醉药品的暂行规定》，确定市第一人民医院、市第二人民医院、市第三人民医院、市第四人民医院、连云港港务局职工医院、省淮北盐务局医院、解放军149医院及赣榆、东海、灌云三县人民医院享有癌症病人诊断权，可出具“晚期癌症病人诊断证明书”，病人可凭此证诊断证明书及户口簿到市、县卫生局办理“麻醉药品特殊使用卡”。1988年12月，市卫生局制订《连云港市麻醉药品使用管理规定》、《关于麻醉药品档案管理的暂行规定》。</p>
<p><strong>毒限制药品管理</strong></p>
<p>1954年10月，市政府卫生科转发省卫生厅颁发的《毒剧药品剂量表》。1956年7月，市人民委员会颁发《管理麻黄素暂行实施办法》，规定个人购买麻黄素时，必须持有医生处方和单位证明信，限购20片。1960年，根据《江苏省毒药及限制性剧药管理办法》，停止部分商店销售去氧麻黄素和复方樟脑酊的权限。1963年，市卫生局规定医疗用中西药品的毒、限制性药品一律由市医药公司经营销售，其他商店不得经营。各医疗单位需使用该类药品时，可凭单位介绍信到市医药公司购买。</p>
<p>1979年，执行国家卫生部、医药管理局颁发的《医疗用毒药、限制性剧药管理规定》，按规定第一类毒、限剧药品只限于供应医疗单位使用，药品经营部门不得在门市部零售，第二类毒、限剧药可由药品经营部门零售，但必须经有关部门批准和必须按医生处方限量出售。1981年4月，将复方甘草片（含阿片）及复方樟脑酊纳入第二类毒、限制药管理。</p>
<p>1983年1月，省卫生厅颁布《关于将强痛定、盐酸哌甲酯列入医用毒、限剧药品管理的通知》，将上述两种药品列入第一类毒、限制药品范围管理，只限供应医疗单位，且须在医生指导下使用。1986年，将强痛定列入精神药品类管理。1989年12月，市卫生局转发国家卫生部《医疗用毒性药品管理办法》，强调医疗用毒性中药作非医疗性使用时，应由使用单位主管部门严格审查，并报医药主管部门审核后方可在指定的药品经营单位购买，使用单位应按有关规定严格管理，每日盘点、记录，做到帐册相符。</p>"""

EXPECTED_TEXT = [
    "<p><strong>五、特殊药品管理</strong></p>",
    "<p><strong>麻醉药品管理</strong></p>",
    "每次可开一次使用量",
    "《关于加强麻醉药品管理、严防流弊的联合通知》，市卫生局组织一次",
    "必须具备一定条件",
    "<p><strong>毒限制药品管理</strong></p>",
    "《毒剧药品剂量表》",
    "复方樟脑酊",
    "列入第一类毒、限制药品范围管理",
]
RESIDUALS = [
    "五、特殊药品管理麻醉药品管理",
    "每次可开次使用量",
    "联合通知》市卫生局组织一次",
    "一一定条件",
    "每限制药品管理",
    "<毒剧药品剂量表》",
    "复方樟脑的权限",
    "列人第一类毒",
]


def find_scope(text: str) -> tuple[int, int]:
    starts = [text.find(marker) for marker in SCOPE_START_OPTIONS]
    valid_starts = [start for start in starts if start != -1]
    if not valid_starts:
        raise RuntimeError("special drugs scope start not found")
    start = min(valid_starts)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        text = text[:start] + new_segment + text[end:]
        HTML.write_text(text, encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"special drugs expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"special drugs residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第四节药政管理 / 五、特殊药品管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本整体复原特殊药品管理小节；未处理第五节药品检验。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷特殊药品管理回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第四节药政管理 / 五、特殊药品管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `五、特殊药品管理` 小节标题。
- 拆分 `麻醉药品管理`、`毒限制药品管理` 分项标题。
- 修正 `一次使用量`、通知后标点、`一定条件`、`《毒剧药品剂量表》`、`复方樟脑酊`、`列入` 等 OCR 错误。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第五节药品检验`。

## 核对说明

- PaddleOCR `page_0199.txt` 确认 `五、特殊药品管理`、`麻醉药品管理` 及麻醉药品管理主体文字。
- PaddleOCR `page_0200.txt` 确认跨页尾段、`毒限制药品管理` 及 `第五节药品检验` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷特殊药品管理回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第四节 `药政管理` 的 `五、特殊药品管理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分小节与分项标题，并按 OCR 复原麻醉药品、毒限制药品管理文字。
- 本轮新增整段替换 {changed} 处；`第五节药品检验` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_special_drugs_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("special drugs section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
