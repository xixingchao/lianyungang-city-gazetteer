# -*- coding: utf-8 -*-
"""Repair source-backed short/empty leaf sections in the current reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_short_leaf_sections_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_short_leaf_sections_20260705.json"

OUTER_TITLE = '<h4 id="第二十八卷-第三章政策法规-第一节外商投资优惠政策">第一节外商投资优惠政策</h4>'
INNER_TITLE = '<h4 id="第二十八卷-第三章政策法规-第二节内联企业优惠待遇">第二节内联企业优惠待遇</h4>'
INNER_INTRO = '<p>根据《连云港市人民政府关于连云港经济技术开发区内联企业优惠待遇的暂行规定》，对国内企、事业单位到开发区联合或独立兴办、经营的企业（即内联企业）提供税收、费用和其他方面的优惠。</p>'
GOV_TITLE = '<h4 id="第四十二卷-第六章连云港市人民政府-第三节政务纪要">第三节政务纪要</h4>'
GOV_END = '<h3 id="第四十二卷-第七章区、县人民政府">第七章区、县人民政府</h3>'

GOV_CONTENT = """
<p><strong>一、机构改革</strong></p>
<p>1980年，按照党政分开的原则，组建政府机构，恢复地方行政机关工作和领导，改变“文化大革命”期间党政一元化领导体制。市政府设办公室，恢复建立市计划委员会、市经济委员会、市科学技术委员会等政府工作部门42个。</p>
<p>1983年，实行市管县新体制，将原属徐州地区的赣榆、东海两县，原属淮阴地区的灌云县划归连云港市管辖。按照全省统一部署，精简机构、紧缩编制，充分发挥各级政府职能，组建适应新体制的行政机构，将职能任务相同或相近的部门予以合并或合署办公，精简专业经济管理部门，将化学工业局、机械工业局、纺织工业局、建材工业局、建筑工程局、房地产管理局、医药管理局等改为行业管理工业公司；调整农村经济管理部门，撤销市农业委员会和农林水利局，设农业局、水利局、多种经营管理局、社队工业局（1984年9月改为乡镇企业管理局）；增设税务局、物价局、审计局等经济监督管理部门。市政府进一步简政放权，把应属于区管理范围的城建、工商行政、商业、供销、文化、教育、卫生、市政管理任务和行政权力下放给区，发挥区级政府职能。</p>
<p>1983年，在进行市、县（区）机构改革的同时，农村进行政社分设工作。改革人民公社政社合一体制，组建乡人民政府和经济联合委员会。有条件的集镇改为建置镇。原生产大队改建村民委员会，成为群众自治组织，到1983年9月，撤社建政工作基本结束。</p>
<p>1984年4月，连云港市被国家列为全国第一批14个沿海开放城市之后，为了适应改革开放的新形势，6月成立经济体制改革办公室，7月成立对外开放领导小组办公室，8月成立对外经济委员会，11月，外经委与外贸局合并成立对外经济贸易委员会。1985年2月成立连云港市经济技术联合开发公司、国际技术贸易开发公司、建筑开发公司、旅游开发公司。1985年，市政府设置工作部门58个。至1990年底，除市计划经济委员会分设为计划委员会和经济委员会，市劳动人事局分设为劳动局、人事局，新增设市政府法制局以外，机构没有大的变动。</p>
<p><strong>二、农村经济体制改革</strong></p>
<p>从1981年6月开始，在全市农村农、林、牧、副、渔各业推行专业队、专业组、专业户等多种形式联产计酬责任制，实行定劳力、定面积、定产量、定报酬、定奖赔的“五定”制度。1983年，全市有98%的社队在坚持土地公有制的基础上，将土地按农户人口比例分给农户自主经营、自负盈亏，土地承包期一定15年不变，调动农民生产积极性，农村经济开始由单一粮食生产向农、副、工、建筑、运输多种经营转变。1984年1月成立市商品粮基地领导小组，建设商品粮基地，东海县成为全国60个商品粮基地县之一。</p>
<p>1985年贯彻中共中央[1984]1号文件，深化农村经济体制改革，完善农村双层经营家庭联产承包责任制，改革农副产品统购统销为合同定购，调整产业结构，在稳定粮食生产的同时，发展多种经营和乡镇工业，加大农业投入，实施科技兴农，发展创汇农业，全面搞活农村经济。至1990年底，全市有398.9万亩耕地，13万农村劳动力，生产粮食201.7万吨，棉花1.68万吨，油料12.5万吨，生猪存栏101万头，水产品9.1万吨，农民年人均纯收入814元，农业开始走向贸、工、农一体化，产、供、销一条龙的发展道路。</p>
<p><strong>三、城市经济体制改革</strong></p>
<p>1983年，市政府以企业调整、改组、整顿、放权，实行经济责任制为中心进行工商企业管理制度改革。组织企业专业化经济联合，逐步调整产业结构、产品结构，进行企业“挖潜、革新、改造”。年底，在市麻纺织厂等7个企业扩大经营自主权试点的基础上，在全市逐步推开。扩大企业在生产计划、产品销售、资金分配、使用、机构设置、干部任免等方面的自主权，改善经营管理。为了巩固企业改革成果，1981年，组织全市工商企业整顿，抓好领导班子建设，深化企业经济体制改革。</p>
<p>1984年，中共中央《关于经济体制改革决定》发出后，企业改革逐步发展到所有权和经营权两权分离、政企分开，使企业成为自主经营和自负盈亏的社会主义商品生产经营者，及时进行了税制、物价、金融、物资流通等方面配套改革。1987年开始，中型企业基本实行承包经营责任制，1988年在全市工商企业中全面推开，引入竞争机制，民主选聘承包经营者，改革劳动用工制度。推行招标承包、风险抵押、全员共保、工效挂钩等多种方式，逐步完善、配套措施。1990年下半年，市政府对上一轮承包进行考核、审计、奖惩、总结表彰，平稳开展第二轮承包，为企业转换经营机制，建立现代企业制度奠定了基础。</p>
<p><strong>四、扩大对外开放</strong></p>
<p>1984年4月，连云港市被国家列为全国首批对外开放的14个沿海城市之一以后，市政府抓住机遇，扩大对外开放。7月，成立市对外开放领导小组，制定连云港发展规划，建立连云港经济技术开发区，以此为窗口发展外向型经济。研究制定了《连云港市关于加强直接利用外资工作的暂行规定》、《连云港市关于引进技术设备和进口商品物资的暂行规定》、《连云港市关于鼓励外商投资的若干规定》。特别是新亚欧大陆桥的贯通，连云港市联合内地省区，推进陇海兰新沿线和内地省区横向经济联合，形成外引内联相互促进，相辅相成的双向开放新格局。对外贸易快速增长，利用外资成效明显，外经工作步入自主经营的新阶段，扩大国际间友好往来与交流，连云港市先后与日本市、韩国木浦市、澳大利亚大吉郎市等城市结为友好城市。</p>
<p><strong>五、制定执行“六五”、“七五”计划</strong></p>
<p>1980~1990年，连云港市政府制定和执行国民经济和社会发展两个五年计划，取得显著成效，政治、社会安定，改革开放顺利进行，国民经济和社会事业发展迅速。1990年完成国民生产总值50.14亿元，工农业总产值87.59亿元，财政收入3.67亿元，农业生产连年丰收，连云港港口吞吐量1137万吨，重点工程和基础设施建设投资7.43亿元，出口商品总值6.05亿元，教育、科学、文化、卫生事业有了较大发展，人民生活水平不断提高，1990年城市人民年均生活收入1380元，农民人均年收入814元。</p>
<p><strong>六、加强城市基础设施建设</strong></p>
<p>改革开放以来，市政府加强城市规划、建设和管理，改善交通、通讯、市政等基础设施。扩建连云港机场、建设铁路新海绕行线，新建邮电大楼、广播电视中心、第一人民医院门诊楼等标志建筑，扩建新海发电厂、茅口水厂，提高城市供电、供水能力。建设花果山风景区，改善投资环境，连云港港口成为全国一类口岸，连云港市被评为全国投资环境40优城市之一。</p>
""".strip()


def replace_once(text: str, old: str, new: str, label: str) -> tuple[str, bool]:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1), old != new


def repair_air_governance(html: str) -> tuple[str, bool]:
    before = html
    html = html.replace('<h5>工艺废气治理</h5>\n<p>1979年，市锦屏化工厂', '<p><strong>工艺废气治理</strong> 1979年，市锦屏化工厂', 1)
    html = html.replace('</p>\n\n<h5>建设烟尘控制区</h5>\n<p>连云港市从1974年开始抓消烟除尘工作。', '</p>\n<p><strong>建设烟尘控制区</strong> 连云港市从1974年开始抓消烟除尘工作。', 1)
    return html, html != before


def repair_dev_policy(html: str) -> tuple[str, bool]:
    before = html
    html, _ = replace_once(html, OUTER_TITLE + '\n' + INNER_TITLE, OUTER_TITLE, 'remove premature inner title')
    html, _ = replace_once(html, '<p>5.外商投资企业同时享有国家和江苏省有关法律、法规以及有关规定的各项优惠待遇。</p>\n<p>根据《连云港市人民政府关于连云港经济技术开发区内联企业优惠待遇的暂行规定》', '<p>5.外商投资企业同时享有国家和江苏省有关法律、法规以及有关规定的各项优惠待遇。</p>\n' + INNER_TITLE + '\n<p>根据《连云港市人民政府关于连云港经济技术开发区内联企业优惠待遇的暂行规定》', 'insert inner title before inner policy')
    return html, html != before


def repair_government_memo(html: str) -> tuple[str, bool]:
    old = GOV_TITLE + '\n' + GOV_END
    new = GOV_TITLE + '\n' + GOV_CONTENT + '\n' + GOV_END
    return replace_once(html, old, new, 'government memo empty section')


def main() -> None:
    html = HTML.read_text(encoding='utf-8')
    changes = {}
    html, changes['air_governance_subheads_demoted'] = repair_air_governance(html)
    html, changes['dev_policy_heading_moved'] = repair_dev_policy(html)
    html, changes['government_memo_restored'] = repair_government_memo(html)
    HTML.write_text(html, encoding='utf-8')

    payload = {
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'reader': str(HTML.relative_to(ROOT)).replace('\\', '/'),
        'changes': changes,
        'sources': [
            'workbench/body_chapters/上/第四卷至第十卷（part02）.md:6966-7024',
            'workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:23938-24053',
            'workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32280-32359',
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    REPORT_MD.write_text('\n'.join([
        '# 短叶子章节结构补修',
        '',
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        '',
        '## 修复项',
        '',
        '- 第六卷大气污染治理：将 `二、治理` 下的 `工艺废气治理`、`建设烟尘控制区` 从同级标题降为段内小题，修正空叶子误结构。',
        '- 第二十八卷政策法规：将 `第二节内联企业优惠待遇` 标题移动到外商投资优惠政策正文之后、内联企业优惠正文之前。',
        '- 第四十二卷第六章政务纪要：按源文补回 `机构改革`、`农村经济体制改革`、`城市经济体制改革`、`扩大对外开放`、`制定执行“六五”、“七五”计划`、`加强城市基础设施建设`。',
        '',
        '## 源证据',
        '',
        '- `workbench/body_chapters/上/第四卷至第十卷（part02）.md:6966-7024`',
        '- `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:23938-24053`',
        '- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32280-32359`',
        '',
    ]) + '\n', encoding='utf-8')
    print('changes=' + json.dumps(changes, ensure_ascii=False))
    print(f'report={REPORT_MD}')


if __name__ == '__main__':
    main()
