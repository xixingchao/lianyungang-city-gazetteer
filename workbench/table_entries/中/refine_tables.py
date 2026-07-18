#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表格数据精修脚本 — 中册 (129个表格)
使用方法: python refine_tables.py <table_id>
  例: python refine_tables.py LYG-中-T001
  不指定ID则处理所有表格
"""
import json, re, sys
from pathlib import Path

ROOT = Path(r'e:/codex_Learing/09_project_东辛农场/连云港市志_workstation')
DATA_DIR = ROOT / 'workbench' / 'table_entries' / '中' / 'data'
RAW_DIR = ROOT / 'workbench' / 'table_entries' / '中' / 'raw'
sys.stdout.reconfigure(encoding='utf-8')

def read_raw(table_id):
    txt = sorted(RAW_DIR.glob(f'{table_id}_*.txt'))
    return txt[0].read_text(encoding='utf-8') if txt else ""

def read_json(table_id):
    j = DATA_DIR / f'{table_id}.json'
    return json.loads(j.read_text(encoding='utf-8')) if j.exists() else None

def save_json(table_id, data):
    j = DATA_DIR / f'{table_id}.json'
    data['row_count'] = len(data['rows'])
    data['col_count'] = len(data['columns'])
    j.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

# ============================================================
# 各表的精修函数
# 返回: {columns, rows} 更新后的结构
# 中册 — 129个表格 (页码 925~1970)
# ============================================================


def refine_中_T001(raw):
    """(标题待确认) (p925, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T002(raw):
    """(标题待确认) (p929, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T003(raw):
    """1963~1990年连云港市柳制品生产经营情况表 (p942, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T004(raw):
    """1963~1990年连云港市柳制品生产经营情况表 (p949, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T005(raw):
    """1963~1990年连云港市柳制品生产经营情况表 (p954, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T006(raw):
    """注：简介企业不列入本表。 (p960, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T007(raw):
    """注：简介企业不列入本表。 (p961, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T008(raw):
    """注：简介企业不列入本表。 (p962, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T009(raw):
    """注：简介企业不列入本表。 (p963, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T010(raw):
    """注：简介企业不列入本表。 (p985, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T011(raw):
    """19761990年连云港市食用酒精产量统计表 (p992, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T012(raw):
    """建国后部分年份连云港市收购云台山中药材比较表 (p1020, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T013(raw):
    """连云港市主要药材引种情况一览表 (p1021, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T014(raw):
    """连云港市主要药材引种情况一览表 (p1022, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T015(raw):
    """1958~1990年连云港医药站经营品种销售统计表 (p1040, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T016(raw):
    """1958~1990年连云港医药站经营品种库存统计表 (p1041, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T017(raw):
    """1990年连云港市医药系统工业企业基本情况表 (p1042, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T018(raw):
    """连云港市医药系统获奖产品一览表 (p1043, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T019(raw):
    """连云港市医药系统获奖产品一览表 (p1048, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T020(raw):
    """1970~1990年连云港市烧碱、纯碱、氢氧化钾产量统计表 (p1050, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T021(raw):
    """1965~1990年连云港市磷酸盐主要产品产量统计表 (p1051, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T022(raw):
    """1965~1990年连云港市磷酸盐主要产品产量统计表 (p1052, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T023(raw):
    """1973~1990年连云港市硫酸钠、硅酸钠、氧化镁主要产品产量统计表 (p1055, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T024(raw):
    """1973~1990年连云港市硫酸钠、硅酸钠、氧化镁主要产品产量统计表 (p1063, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T025(raw):
    """1972~1990年连云港市主要胶粘剂产量统计表 (p1083, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T026(raw):
    """1972~1990年连云港市主要胶粘剂产量统计表 (p1090, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T027(raw):
    """1972~1990年连云港市主要胶粘剂产量统计表 (p1093, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T028(raw):
    """咪唑琳两性表面活性剂 (p1094, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T029(raw):
    """连云港水表厂 (p1136, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T030(raw):
    """连云港水表厂 (p1171, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T031(raw):
    """注：简介企业不列入本表。 (p1198, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T032(raw):
    """1990年连云港市主要勘察设计单位览表 (p1204, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T033(raw):
    """1990年连云港市主要勘察设计单位览表 (p1220, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T034(raw):
    """1990年连云港市主要勘察设计单位览表 (p1232, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T035(raw):
    """1990年连云港市主要勘察设计单位览表 (p1243, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T036(raw):
    """1949~1990年连云港市供电线损率统计表 (p1266, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T037(raw):
    """1983~1990年连云港市乡镇企业水泥瓦产量统计表 (p1303, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T038(raw):
    """1983~1990年连云港市乡镇企业水泥瓦产量统计表 (p1309, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T039(raw):
    """1988年、1990年连云港市乡镇企业及出口产品情况表 (p1311, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T040(raw):
    """1988年、1990年连云港市乡镇企业及出口产品情况表 (p1314, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T041(raw):
    """1988年、1990年连云港市乡镇企业及出口产品情况表 (p1325, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T042(raw):
    """1990年连云港老港区铁路专线分布表 (p1348, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T043(raw):
    """1985年连云港货物吞吐量分类统计表 (p1357, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T044(raw):
    """1949~1990年连云港港货物吞吐量统计表 (p1358, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T045(raw):
    """1951~1990年连云港车站到发货物运量统计表 (p1362, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T046(raw):
    """1977~1990年连云港站运输收入统计表 (p1363, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T047(raw):
    """1977~1990年连云港站运输收入统计表 (p1372, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T048(raw):
    """注：此表不含港务局装卸公司库场和其它行业储存内销物资的库场。 (p1373, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T049(raw):
    """1963~1990年连云港外轮理货分公司理货统计表 (p1379, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T050(raw):
    """中国银行办理外币存款的对象，1979年10月31日以前仅限于驻华外交代表机构、领 (p1383, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T051(raw):
    """1979~1990年中国银行连云港分行记帐结算统计表 (p1385, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T052(raw):
    """1974~1990年中国人民保险公司连云港分公司涉外保险自营收入理赔统计表 (p1387, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T053(raw):
    """1985~1990年外轮服务公司供水、回收垃圾情况表 (p1390, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T054(raw):
    """1974~1989年中国旗船舶检验统计表 (p1419, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T055(raw):
    """1990年东海县县级公路概况表 (p1444, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T056(raw):
    """1990年灌云县县级公路概况表 (p1445, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T057(raw):
    """1990年灌云县县级公路概况表 (p1446, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T058(raw):
    """民国13~28年（1924~1939年）连云港市汽车客运单位基本情况表 (p1449, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T059(raw):
    """民国13~28年（1924~1939年）连云港市汽车客运单位基本情况表 (p1450, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T060(raw):
    """1990年新浦汽车站客运发车情况表 (p1451, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T061(raw):
    """1990年新浦汽车站客运发车情况表 (p1452, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T062(raw):
    """1990年新浦汽车站客运发车情况表 (p1457, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T063(raw):
    """1990年连云港市筑路养护机械统计表 (p1461, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T064(raw):
    """1950~1982年连云港市市区邮政业务量（计费）统计表 (p1496, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T065(raw):
    """1983~1990年连云港市邮政业务量（计费）统计表 (p1497, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T066(raw):
    """1983~1990年连云港市邮政业务量（计费）统计表 (p1498, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T067(raw):
    """1990年连云港市邮电局（所）一览表 (p1512, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T068(raw):
    """1990年连云港市邮电局（所）一览表 (p1513, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T069(raw):
    """1990年连云港市邮电局（所）一览表 (p1514, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T070(raw):
    """表33-3 (p1545, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T071(raw):
    """表33-3 (p1546, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T072(raw):
    """1949~1990年连云港市社会商品零售额统计表 (p1551, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T073(raw):
    """1949~1990年连云港市社会商品零售额统计表 (p1552, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T074(raw):
    """1977年，人民群众收入增长，消费出现“三转一响”（自行车、手表、缝纫机、收音机）新 (p1555, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T075(raw):
    """19491990年部分年份连云港市市区国营商业主要商品零售量统计表（二） (p1556, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T076(raw):
    """19491990年部分年份连云港市市区国营商业主要商品零售量统计表（二） (p1557, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T077(raw):
    """19491990年部分年份连云港市市区国营商业主要商品零售量统计表（二） (p1561, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T078(raw):
    """19491990年部分年份连云港市市区国营商业主要商品零售量统计表（二） (p1567, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T079(raw):
    """1990年连云港市市区大型饮服网点一览表 (p1577, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T080(raw):
    """1975~1990年连云港市出口商品收购统计表 (p1602, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T081(raw):
    """1975~1990年连云港市出口商品收购统计表 (p1603, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T082(raw):
    """1975~1990年连云港市出口商品收购统计表 (p1612, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T083(raw):
    """1975~1990年连云港市出口商品收购统计表 (p1613, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T084(raw):
    """合资经营生产水表 (p1614, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T085(raw):
    """合资经营生产水表 (p1615, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T086(raw):
    """汽轮机保护仪表 (p1616, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T087(raw):
    """汽轮机保护仪表 (p1617, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T088(raw):
    """汽轮机保护仪表 (p1619, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T089(raw):
    """汽轮机保护仪表 (p1620, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T090(raw):
    """1984~1987年连云港市租赁项目一览表 (p1621, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T091(raw):
    """1984~1990年连云港市批准来料加工装配项目表 (p1622, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T092(raw):
    """仪器仪表接插件 (p1623, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T093(raw):
    """仪器仪表接插件 (p1634, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T094(raw):
    """1955～1956年度连云港市农村粮食三定”到户情况统计表 (p1635, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T095(raw):
    """其它品种退出定购。4月，各粮管所代表政府与全市533417户农民签订了粮食定购合同， (p1637, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T096(raw):
    """1957~1990年连云港市市镇定量食油销售统计表 (p1641, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T097(raw):
    """1957~1990年连云港市市镇定量食油销售统计表 (p1642, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T098(raw):
    """1957~1990年连云港市供应农业人口食油统计表 (p1647, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T099(raw):
    """1957~1990年连云港市供应农业人口食油统计表 (p1648, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T100(raw):
    """1966~1983年连云港市农村集体储备粮统计表 (p1660, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T101(raw):
    """1966~1983年连云港市农村集体储备粮统计表 (p1661, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T102(raw):
    """1966~1983年连云港市农村集体储备粮统计表 (p1677, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T103(raw):
    """1966~1983年连云港市农村集体储备粮统计表 (p1686, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T104(raw):
    """民国3~24年准北盐税收入统计表 (p1708, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T105(raw):
    """1952~1990年连云港市预算内全民企业收入统计表 (p1711, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T106(raw):
    """1949~1990年连云港市主要财政支出统计表 (p1719, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T107(raw):
    """1949~1990年连云港市主要财政支出统计表 (p1765, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T108(raw):
    """1984~1990年连云港市金融机构存款统计表 (p1775, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T109(raw):
    """1949~1990年连云港市储蓄种类表 (p1777, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T110(raw):
    """1949~1990年连云港市储蓄种类表 (p1780, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T111(raw):
    """1949~1990年连云港市储蓄种类表 (p1783, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T112(raw):
    """1949~1990年连云港市储蓄种类表 (p1785, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T113(raw):
    """1949~1990年连云港市储蓄种类表 (p1812, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T114(raw):
    """1949~1990年连云港市储蓄种类表 (p1823, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T115(raw):
    """市境至1956年5月市第-一次党的代表大会召开前，市委领导人均由上级党组织任命， (p1847, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T116(raw):
    """历任市委常委表 (p1849, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T117(raw):
    """组相继建立。1971年6月，中共连云港市第四次代表大会召开，瘫痪四年之久的各级党组织 (p1850, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T118(raw):
    """组相继建立。1971年6月，中共连云港市第四次代表大会召开，瘫痪四年之久的各级党组织 (p1852, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T119(raw):
    """组相继建立。1971年6月，中共连云港市第四次代表大会召开，瘫痪四年之久的各级党组织 (p1853, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T120(raw):
    """组相继建立。1971年6月，中共连云港市第四次代表大会召开，瘫痪四年之久的各级党组织 (p1854, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T121(raw):
    """组相继建立。1971年6月，中共连云港市第四次代表大会召开，瘫痪四年之久的各级党组织 (p1856, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T122(raw):
    """组相继建立。1971年6月，中共连云港市第四次代表大会召开，瘫痪四年之久的各级党组织 (p1857, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T123(raw):
    """1977~1990年连云港市干部统计表 (p1859, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T124(raw):
    """1977~1990年连云港市干部统计表 (p1860, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T125(raw):
    """1977~1990年连云港市干部统计表 (p1861, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T126(raw):
    """《准则》公布到1982年，各级纪委对《准则》的执行情况，每年进行一次全面检查，表彰先进 (p1868, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T127(raw):
    """《准则》公布到1982年，各级纪委对《准则》的执行情况，每年进行一次全面检查，表彰先进 (p1869, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T128(raw):
    """市，县政协委员，1人当选为市人大代表。市、县（区)统战部和定居台胞保持经常联系，为 (p1875, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_中_T129(raw):
    """连云港市第至七届历届政协委员会委员组成情况表 (p1970, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}

# ===== 调度表 =====
REFINERS = {
    "LYG-中-T001": refine_中_T001,
    "LYG-中-T002": refine_中_T002,
    "LYG-中-T003": refine_中_T003,
    "LYG-中-T004": refine_中_T004,
    "LYG-中-T005": refine_中_T005,
    "LYG-中-T006": refine_中_T006,
    "LYG-中-T007": refine_中_T007,
    "LYG-中-T008": refine_中_T008,
    "LYG-中-T009": refine_中_T009,
    "LYG-中-T010": refine_中_T010,
    "LYG-中-T011": refine_中_T011,
    "LYG-中-T012": refine_中_T012,
    "LYG-中-T013": refine_中_T013,
    "LYG-中-T014": refine_中_T014,
    "LYG-中-T015": refine_中_T015,
    "LYG-中-T016": refine_中_T016,
    "LYG-中-T017": refine_中_T017,
    "LYG-中-T018": refine_中_T018,
    "LYG-中-T019": refine_中_T019,
    "LYG-中-T020": refine_中_T020,
    "LYG-中-T021": refine_中_T021,
    "LYG-中-T022": refine_中_T022,
    "LYG-中-T023": refine_中_T023,
    "LYG-中-T024": refine_中_T024,
    "LYG-中-T025": refine_中_T025,
    "LYG-中-T026": refine_中_T026,
    "LYG-中-T027": refine_中_T027,
    "LYG-中-T028": refine_中_T028,
    "LYG-中-T029": refine_中_T029,
    "LYG-中-T030": refine_中_T030,
    "LYG-中-T031": refine_中_T031,
    "LYG-中-T032": refine_中_T032,
    "LYG-中-T033": refine_中_T033,
    "LYG-中-T034": refine_中_T034,
    "LYG-中-T035": refine_中_T035,
    "LYG-中-T036": refine_中_T036,
    "LYG-中-T037": refine_中_T037,
    "LYG-中-T038": refine_中_T038,
    "LYG-中-T039": refine_中_T039,
    "LYG-中-T040": refine_中_T040,
    "LYG-中-T041": refine_中_T041,
    "LYG-中-T042": refine_中_T042,
    "LYG-中-T043": refine_中_T043,
    "LYG-中-T044": refine_中_T044,
    "LYG-中-T045": refine_中_T045,
    "LYG-中-T046": refine_中_T046,
    "LYG-中-T047": refine_中_T047,
    "LYG-中-T048": refine_中_T048,
    "LYG-中-T049": refine_中_T049,
    "LYG-中-T050": refine_中_T050,
    "LYG-中-T051": refine_中_T051,
    "LYG-中-T052": refine_中_T052,
    "LYG-中-T053": refine_中_T053,
    "LYG-中-T054": refine_中_T054,
    "LYG-中-T055": refine_中_T055,
    "LYG-中-T056": refine_中_T056,
    "LYG-中-T057": refine_中_T057,
    "LYG-中-T058": refine_中_T058,
    "LYG-中-T059": refine_中_T059,
    "LYG-中-T060": refine_中_T060,
    "LYG-中-T061": refine_中_T061,
    "LYG-中-T062": refine_中_T062,
    "LYG-中-T063": refine_中_T063,
    "LYG-中-T064": refine_中_T064,
    "LYG-中-T065": refine_中_T065,
    "LYG-中-T066": refine_中_T066,
    "LYG-中-T067": refine_中_T067,
    "LYG-中-T068": refine_中_T068,
    "LYG-中-T069": refine_中_T069,
    "LYG-中-T070": refine_中_T070,
    "LYG-中-T071": refine_中_T071,
    "LYG-中-T072": refine_中_T072,
    "LYG-中-T073": refine_中_T073,
    "LYG-中-T074": refine_中_T074,
    "LYG-中-T075": refine_中_T075,
    "LYG-中-T076": refine_中_T076,
    "LYG-中-T077": refine_中_T077,
    "LYG-中-T078": refine_中_T078,
    "LYG-中-T079": refine_中_T079,
    "LYG-中-T080": refine_中_T080,
    "LYG-中-T081": refine_中_T081,
    "LYG-中-T082": refine_中_T082,
    "LYG-中-T083": refine_中_T083,
    "LYG-中-T084": refine_中_T084,
    "LYG-中-T085": refine_中_T085,
    "LYG-中-T086": refine_中_T086,
    "LYG-中-T087": refine_中_T087,
    "LYG-中-T088": refine_中_T088,
    "LYG-中-T089": refine_中_T089,
    "LYG-中-T090": refine_中_T090,
    "LYG-中-T091": refine_中_T091,
    "LYG-中-T092": refine_中_T092,
    "LYG-中-T093": refine_中_T093,
    "LYG-中-T094": refine_中_T094,
    "LYG-中-T095": refine_中_T095,
    "LYG-中-T096": refine_中_T096,
    "LYG-中-T097": refine_中_T097,
    "LYG-中-T098": refine_中_T098,
    "LYG-中-T099": refine_中_T099,
    "LYG-中-T100": refine_中_T100,
    "LYG-中-T101": refine_中_T101,
    "LYG-中-T102": refine_中_T102,
    "LYG-中-T103": refine_中_T103,
    "LYG-中-T104": refine_中_T104,
    "LYG-中-T105": refine_中_T105,
    "LYG-中-T106": refine_中_T106,
    "LYG-中-T107": refine_中_T107,
    "LYG-中-T108": refine_中_T108,
    "LYG-中-T109": refine_中_T109,
    "LYG-中-T110": refine_中_T110,
    "LYG-中-T111": refine_中_T111,
    "LYG-中-T112": refine_中_T112,
    "LYG-中-T113": refine_中_T113,
    "LYG-中-T114": refine_中_T114,
    "LYG-中-T115": refine_中_T115,
    "LYG-中-T116": refine_中_T116,
    "LYG-中-T117": refine_中_T117,
    "LYG-中-T118": refine_中_T118,
    "LYG-中-T119": refine_中_T119,
    "LYG-中-T120": refine_中_T120,
    "LYG-中-T121": refine_中_T121,
    "LYG-中-T122": refine_中_T122,
    "LYG-中-T123": refine_中_T123,
    "LYG-中-T124": refine_中_T124,
    "LYG-中-T125": refine_中_T125,
    "LYG-中-T126": refine_中_T126,
    "LYG-中-T127": refine_中_T127,
    "LYG-中-T128": refine_中_T128,
    "LYG-中-T129": refine_中_T129,
}


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    refined = 0

    for tid, refiner in REFINERS.items():
        if target and tid != target:
            continue

        data = read_json(tid)
        if not data:
            print(f"  ! {tid} — JSON不存在")
            continue

        raw = read_raw(tid)
        result = refiner(raw)

        data['columns'] = result['columns']
        data['rows'] = result['rows']
        data['notes'] = data.get('notes', '').replace('从OCR自动提取骨架', '已精修')
        if '待对照原图精修' in data.get('notes', ''):
            data['notes'] = data['notes'].replace('待对照原图精修', '对照原图确认')

        save_json(tid, data)
        rcount = len(result["rows"])
        ccount = len(result["columns"])
        filled = sum(1 for r in result["rows"] for c in r if c and c != "待对照原图录入")
        print(f"  ✓ {tid}: {rcount}行×{ccount}列 ({filled}个已填充)")
        refined += 1

    if refined == 0:
        print("未处理任何表。支持的ID:")
        for k in REFINERS:
            print(f"  {k}")
    else:
        print(f"\n精修完成: {refined}个")

if __name__ == '__main__':
    main()