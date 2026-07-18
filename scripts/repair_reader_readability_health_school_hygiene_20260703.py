# -*- coding: utf-8 -*-
"""Restore Fifth十五卷公共卫生第四节学校卫生 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_school_hygiene_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_school_hygiene_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷公共卫生学校卫生回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0170.txt:11-36; page_0171.txt:3-40"
SCOPE_START = '<h4 id="第五十五卷-第一章公共卫生-第四节学校卫生">第四节学校卫生</h4>'
SCOPE_END = '<h4 id="第五十五卷-第一章公共卫生-第五节环境卫生">第五节环境卫生</h4>'

NEW_HTML = """<h4 id="第五十五卷-第一章公共卫生-第四节学校卫生">第四节学校卫生</h4>
<p><strong>一、医务室</strong></p>
<p>民国20年（1931年），东海师范学校始建医务室。1950年，江苏省新海中学建医务室。1954～1966年，市区重点中学和中专以上院校建医务室，配备1～2名专职校医。</p>
<p>1980年，开始贯彻国家教育部、卫生部颁发的《中小学卫生工作暂行规定（草案）》，市区大、中学校全部建立医务室。赣榆、灌云、东海三县重点中学和解放路小学建立医务室。其他中小学多数配备兼职保健教师。至1990年底，全市设立医务室的大中小学43所，共有专职医务人员71人，其中市区学校有医务室23个，医务人员47人。共培训保健教师1100人次。</p>
<p><strong>二、体质调查</strong></p>
<p>1950～1966年，全市中学每年对学生进行一次体格检查，1971年后恢复每年对学生的体格检查。1978年，按国家卫生部《关于进行中国青少年及儿童身体形态机能素质研究的通知》精神，市组织人力对沿海渔业、农业区内5～15岁儿童4414人体格进行检查。检查结果表明，渔区儿童各年龄组的身高体重等的平均值均大于农区儿童。1985年1～6月，市教育局、卫生局、体育运动委员会，根据国家教育部、卫生部、体育运动委员会、民族事务委员会颁发的《中国学生体制健康调研要求》，抽调41人对城乡29所中小学7～18岁学生共13991人，进行形态、机能、素质、健康4类28项内容的检查。检查结果表明，中小学生的发育正常，其中11～13岁学生的发育快速。1987年，市教育局、卫生局颁发《关于连云港市学生体检的若干规定》，各校在每年一次学生体检中按形态、机能、健康三部分进行。1988年各校建立学生健康卡片，全市有177所学校建立卫生档案。</p>
<p><strong>三、卫生监测</strong></p>
<p>1956年，市卫生部门对16所中小学教室采光及照明情况调查。市卫生防疫站于1976年、1978年对各校教学环境卫生状况进行监测和调查。1980年秋，市卫生防疫站对连云港市延安中学和公园小学学生进行乙型肝炎表面抗原携带检测。延安中学检测460人，HBsAg（乙型肝炎表面抗原）阳性30人，HBS（乙型肝炎表面抗体）阳性18人，乙型肝炎病毒感染率为10.5%。公园小学检测526人，HBsAg阳性24人，抗HBS阳性47人，乙型肝炎病毒感染率为13.49%。两校中小学生抗HBS阳性率有显著差异。各学龄组的乙型肝炎病毒感染率以小学四年级（11岁左右）组最高，表明该年龄组学生对乙型肝炎病毒较敏感。对HBSAg阳性学生进行随访和体检，均未发现有肝炎体征，对部分学生进行肝功能检查，亦未发现异常。1984年，对全市54所大中小学校教学环境监测和调查，结果显示，中小学教学环境存在问题较多。如东海县有些学校采光面积较小，自然采光系数太低，有的低至1：16（卫生标准为1：4～1：6），室内光线不均匀，最大的720Lux，最低的20Lux，自然照度系数仅有0.26%～3%（卫生标准为不小于1%～1.5%）；桌间距太小，前排距黑板太近，人工照明较差。对以上各种不符合卫生标准的问题，立即向有关部门提出建议。1985年，继续对各校教学环境卫生状况监测和调查。1985年，灌云县卫生防疫站对灌云县中学和灌云县实验小学958名10～18岁男生和698名9～17岁女生进行青春期发育情况调查。女生月经初潮期年龄最小为9岁，最大的为17岁。男生首次遗精最小为11岁，最大为18岁。在第二性征的发育方面，发现女生乳房发育的最小年龄为9岁，10～11岁时大多为Ⅰ度，15岁后已有51.29%发育成熟，呈Ⅲ度；男生喉节突出、变音、胡须长出的平均年龄为15.8岁。</p>
<p><strong>四、疾病防治</strong></p>
<p>1950年，市卫生部门对学生中头虱和疥疮防治。1951年，新海中学对509名学生体检，其中视力不良占2%，查出沙眼患者123人，占24.17%。1955年，市卫生防疫站对学生沙眼病情调查，解放路小学六年级42人全部患有沙眼；市立海州中学检查544人，患沙眼505人，阳性率92.85%；东海师范学校检查683人，患沙眼498人，阳性率72.91%。对此，除对患者治疗外，各校加强对学生个人卫生教育，使沙眼患者逐年减少。1955年，对市立中学544名学生进行视力检查，视力不良者77人，占14.15%，东海师范学校检查683名学生的视力，视力不良者125人，占18.3%。1955年，对部分中小学进行肠道寄生病调查，1958年开始全面防治，但感染率多年未见明显下降。市内学生结核病防治工作始于1959年，新海中学对高中毕业班180人进行结核病检查，查出5人患病，患病率为2.78%；1960年又对高中毕业班186人检查，查出患病者2人。1961年，国家教育部、卫生部发出《关于防治肺结核肝炎等传染病的通知》，引起各校重视，市内有14所中等学校对7282名学生检查传染病，共查出患者69人，患病率为0.91%。1970年后，学生结核病患病率有所下降。1977年后，学生视力不良率呈逐步提高趋势，据新海中学医务室监测，该校学生视力不良率，1979年为51.4%，1982年为59.6%，1983年为64.6%，1984年为71.3%。为防止视力减退，各校采取多种措施防治，到1989年视力不良率下降为66.8%，仍继续防治。1982年抽查11所小学学生肠道寄生虫病，共查9285名7～15岁学生，阳性1770人，感染率为53.9%，其中城区学生感染率为42.6%，郊区感染率为67.2%。1982年，学生中患结核病率为0.4%，对历年查出的结核病学生患者都进行了治疗。1987年，对14所小学6852名学生检查，查出1606名学生有头虱，感染率为23.4%，均采用菊脂类药物“灭虱露”灭虱。1987～1989年，全市对中小学生疥疮普查23.72万人次，查出患者929人，用硫磺软膏对其中的659人治疗，治愈率为100%。1990年，对全市中小学生18.83万人进行龋齿病检查，患者1.3万人，龋患率为6.9%。对其中4290人治疗，治愈率为32.9%。</p>
"""

EXPECTED_TEXT = [
    "《中小学卫生工作暂行规定（草案）》",
    "1950～1966年，全市中学每年对学生进行一次体格检查",
    "延安中学检测460人，HBsAg（乙型肝炎表面抗原）阳性30人",
    "公园小学检测526人，HBsAg阳性24人，抗HBS阳性47人",
    "10～11岁时大多为Ⅰ度",
    "解放路小学六年级42人全部患有沙眼",
    "用硫磺软膏对其中的659人治疗",
]
RESIDUALS = [
    "一、医务室民国20年",
    "颁发的中小学卫生工作暂行规定（草案）》",
    "二、体质调查的体格检查",
    "延安中学检测460病毒感染率",
    "10～11岁时大多为1度",
    "全部惠有沙眼",
    "硫磺软离",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    changed = int(text[start:end] != NEW_HTML)
    if changed:
        HTML.write_text(text[:start] + NEW_HTML + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return changed, {"rewrote_scope": changed, "subheads_restored": 4, "paragraphs_restored": 8}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第一章公共卫生 / 第四节学校卫生",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建学校卫生节，停止在第五节环境卫生前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷公共卫生学校卫生回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：恢复四个小标题，补回医务室、体质调查、卫生监测段漏文，修正乙肝检测数字、Ⅰ度、患有沙眼、硫磺软膏等 OCR 残留。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷公共卫生学校卫生回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第一章公共卫生 / 第四节学校卫生` 至 `第五节环境卫生` 前。
- 修复内容：恢复 `一、医务室`、`二、体质调查`、`三、卫生监测`、`四、疾病防治` 小标题；补回 `1950～1966年`、乙肝检测阳性人数等漏文；修正 `惠有沙眼`、`硫磺软离` 等残留。
- 报告：`output/reports/reader_readability_health_school_hygiene_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷公共卫生学校卫生回源修复

- 对第五十五卷卫生 `第一章公共卫生 / 第四节学校卫生` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第五节环境卫生` 前。
- 恢复四个小标题，补回医务室、体质调查、卫生监测段漏文，修正乙肝检测数字、`Ⅰ度`、`患有沙眼`、`硫磺软膏` 等 OCR 残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_school_hygiene_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷公共卫生学校卫生回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
