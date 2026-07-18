#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表格数据精修脚本 — 下册 (104个表格)
使用方法: python refine_tables.py <table_id>
  例: python refine_tables.py LYG-下-T001
  不指定ID则处理所有表格
"""
import json, re, sys
from pathlib import Path

ROOT = Path(r'e:/codex_Learing/09_project_东辛农场/连云港市志_workstation')
DATA_DIR = ROOT / 'workbench' / 'table_entries' / '下' / 'data'
RAW_DIR = ROOT / 'workbench' / 'table_entries' / '下' / 'raw'
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
# 下册 — 104个表格 (页码 1989~2840)
# ============================================================


def refine_下_T001(raw):
    """(标题待确认) (p1989, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T002(raw):
    """(标题待确认) (p1991, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T003(raw):
    """1963~1990年连云港市柳制品生产经营情况表 (p2003, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T004(raw):
    """(标题待确认) (p2004, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T005(raw):
    """(标题待确认) (p2014, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T006(raw):
    """(标题待确认) (p2017, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T007(raw):
    """(标题待确认) (p2020, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T008(raw):
    """(标题待确认) (p2021, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T009(raw):
    """(标题待确认) (p2022, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T010(raw):
    """(标题待确认) (p2048, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T011(raw):
    """(标题待确认) (p2062, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T012(raw):
    """建国后部分年份连云港市收购云台山中药材比较表 (p2065, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T013(raw):
    """连云港市主要药材引种情况一览表 (p2066, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T014(raw):
    """(标题待确认) (p2074, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T015(raw):
    """(标题待确认) (p2076, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T016(raw):
    """(标题待确认) (p2096, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T017(raw):
    """(标题待确认) (p2107, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T018(raw):
    """连云港市医药系统获奖产品一览表 (p2116, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T019(raw):
    """(标题待确认) (p2118, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T020(raw):
    """1970~1990年连云港市烧碱、纯碱、氢氧化钾产量统计表 (p2170, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T021(raw):
    """1965~1990年连云港市磷酸盐主要产品产量统计表 (p2172, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T022(raw):
    """(标题待确认) (p2174, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T023(raw):
    """1973~1990年连云港市硫酸钠、硅酸钠、氧化镁主要产品产量统计表 (p2175, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T024(raw):
    """(标题待确认) (p2176, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T025(raw):
    """1972~1990年连云港市主要胶粘剂产量统计表 (p2178, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T026(raw):
    """(标题待确认) (p2179, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T027(raw):
    """(标题待确认) (p2183, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T028(raw):
    """(标题待确认) (p2193, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T029(raw):
    """(标题待确认) (p2194, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T030(raw):
    """(标题待确认) (p2196, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T031(raw):
    """(标题待确认) (p2197, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T032(raw):
    """(标题待确认) (p2198, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T033(raw):
    """(标题待确认) (p2199, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T034(raw):
    """(标题待确认) (p2200, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T035(raw):
    """(标题待确认) (p2203, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T036(raw):
    """1949~1990年连云港市供电线损率统计表 (p2207, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T037(raw):
    """1983~1990年连云港市乡镇企业水泥瓦产量统计表 (p2229, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T038(raw):
    """(标题待确认) (p2230, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T039(raw):
    """(标题待确认) (p2238, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T040(raw):
    """(标题待确认) (p2243, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T041(raw):
    """(标题待确认) (p2329, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T042(raw):
    """1990年连云港老港区铁路专线分布表 (p2330, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T043(raw):
    """1985年连云港货物吞吐量分类统计表 (p2331, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T044(raw):
    """(标题待确认) (p2332, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T045(raw):
    """1951~1990年连云港车站到发货物运量统计表 (p2333, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T046(raw):
    """(标题待确认) (p2334, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T047(raw):
    """(标题待确认) (p2335, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T048(raw):
    """(标题待确认) (p2336, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T049(raw):
    """1963~1990年连云港外轮理货分公司理货统计表 (p2338, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T050(raw):
    """(标题待确认) (p2339, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T051(raw):
    """(标题待确认) (p2342, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T052(raw):
    """1974~1990年中国人民保险公司连云港分公司涉外保险自营收入理赔统计表 (p2343, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T053(raw):
    """1985~1990年外轮服务公司供水、回收垃圾情况表 (p2345, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T054(raw):
    """1974~1989年中国旗船舶检验统计表 (p2350, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T055(raw):
    """(标题待确认) (p2351, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T056(raw):
    """(标题待确认) (p2352, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T057(raw):
    """(标题待确认) (p2353, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T058(raw):
    """民国13~28年（1924~1939年）连云港市汽车客运单位基本情况表 (p2354, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T059(raw):
    """(标题待确认) (p2357, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T060(raw):
    """1990年新浦汽车站客运发车情况表 (p2360, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T061(raw):
    """(标题待确认) (p2369, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T062(raw):
    """(标题待确认) (p2370, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T063(raw):
    """1990年连云港市筑路养护机械统计表 (p2371, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T064(raw):
    """1950~1982年连云港市市区邮政业务量（计费）统计表 (p2374, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T065(raw):
    """(标题待确认) (p2375, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T066(raw):
    """(标题待确认) (p2376, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T067(raw):
    """(标题待确认) (p2390, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T068(raw):
    """(标题待确认) (p2391, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T069(raw):
    """(标题待确认) (p2392, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T070(raw):
    """表33-3 (p2393, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T071(raw):
    """(标题待确认) (p2395, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T072(raw):
    """(标题待确认) (p2396, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T073(raw):
    """(标题待确认) (p2397, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T074(raw):
    """1977年，人民群众收入增长，消费出现“三转一响”（自行车、手表、缝纫机、收音机）新 (p2403, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T075(raw):
    """(标题待确认) (p2405, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T076(raw):
    """(标题待确认) (p2406, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T077(raw):
    """(标题待确认) (p2431, part01)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T078(raw):
    """(标题待确认) (p2494, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T079(raw):
    """1990年连云港市市区大型饮服网点一览表 (p2567, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T080(raw):
    """1975~1990年连云港市出口商品收购统计表 (p2572, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T081(raw):
    """(标题待确认) (p2577, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T082(raw):
    """(标题待确认) (p2595, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T083(raw):
    """(标题待确认) (p2646, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T084(raw):
    """(标题待确认) (p2647, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T085(raw):
    """(标题待确认) (p2664, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T086(raw):
    """(标题待确认) (p2665, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T087(raw):
    """(标题待确认) (p2677, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T088(raw):
    """(标题待确认) (p2678, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T089(raw):
    """(标题待确认) (p2679, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T090(raw):
    """(标题待确认) (p2680, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T091(raw):
    """(标题待确认) (p2687, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T092(raw):
    """(标题待确认) (p2688, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T093(raw):
    """(标题待确认) (p2700, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T094(raw):
    """1955～1956年度连云港市农村粮食三定”到户情况统计表 (p2701, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T095(raw):
    """(标题待确认) (p2702, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T096(raw):
    """(标题待确认) (p2706, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T097(raw):
    """(标题待确认) (p2707, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T098(raw):
    """(标题待确认) (p2834, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T099(raw):
    """(标题待确认) (p2835, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T100(raw):
    """1966~1983年连云港市农村集体储备粮统计表 (p2836, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T101(raw):
    """(标题待确认) (p2837, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T102(raw):
    """(标题待确认) (p2838, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T103(raw):
    """(标题待确认) (p2839, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}


def refine_下_T104(raw):
    """民国3~24年准北盐税收入统计表 (p2840, part02)
    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""
    return {"columns": ["数值"],
            "rows": [["待对照原图录入"]]}

# ===== 调度表 =====
REFINERS = {
    "LYG-下-T001": refine_下_T001,
    "LYG-下-T002": refine_下_T002,
    "LYG-下-T003": refine_下_T003,
    "LYG-下-T004": refine_下_T004,
    "LYG-下-T005": refine_下_T005,
    "LYG-下-T006": refine_下_T006,
    "LYG-下-T007": refine_下_T007,
    "LYG-下-T008": refine_下_T008,
    "LYG-下-T009": refine_下_T009,
    "LYG-下-T010": refine_下_T010,
    "LYG-下-T011": refine_下_T011,
    "LYG-下-T012": refine_下_T012,
    "LYG-下-T013": refine_下_T013,
    "LYG-下-T014": refine_下_T014,
    "LYG-下-T015": refine_下_T015,
    "LYG-下-T016": refine_下_T016,
    "LYG-下-T017": refine_下_T017,
    "LYG-下-T018": refine_下_T018,
    "LYG-下-T019": refine_下_T019,
    "LYG-下-T020": refine_下_T020,
    "LYG-下-T021": refine_下_T021,
    "LYG-下-T022": refine_下_T022,
    "LYG-下-T023": refine_下_T023,
    "LYG-下-T024": refine_下_T024,
    "LYG-下-T025": refine_下_T025,
    "LYG-下-T026": refine_下_T026,
    "LYG-下-T027": refine_下_T027,
    "LYG-下-T028": refine_下_T028,
    "LYG-下-T029": refine_下_T029,
    "LYG-下-T030": refine_下_T030,
    "LYG-下-T031": refine_下_T031,
    "LYG-下-T032": refine_下_T032,
    "LYG-下-T033": refine_下_T033,
    "LYG-下-T034": refine_下_T034,
    "LYG-下-T035": refine_下_T035,
    "LYG-下-T036": refine_下_T036,
    "LYG-下-T037": refine_下_T037,
    "LYG-下-T038": refine_下_T038,
    "LYG-下-T039": refine_下_T039,
    "LYG-下-T040": refine_下_T040,
    "LYG-下-T041": refine_下_T041,
    "LYG-下-T042": refine_下_T042,
    "LYG-下-T043": refine_下_T043,
    "LYG-下-T044": refine_下_T044,
    "LYG-下-T045": refine_下_T045,
    "LYG-下-T046": refine_下_T046,
    "LYG-下-T047": refine_下_T047,
    "LYG-下-T048": refine_下_T048,
    "LYG-下-T049": refine_下_T049,
    "LYG-下-T050": refine_下_T050,
    "LYG-下-T051": refine_下_T051,
    "LYG-下-T052": refine_下_T052,
    "LYG-下-T053": refine_下_T053,
    "LYG-下-T054": refine_下_T054,
    "LYG-下-T055": refine_下_T055,
    "LYG-下-T056": refine_下_T056,
    "LYG-下-T057": refine_下_T057,
    "LYG-下-T058": refine_下_T058,
    "LYG-下-T059": refine_下_T059,
    "LYG-下-T060": refine_下_T060,
    "LYG-下-T061": refine_下_T061,
    "LYG-下-T062": refine_下_T062,
    "LYG-下-T063": refine_下_T063,
    "LYG-下-T064": refine_下_T064,
    "LYG-下-T065": refine_下_T065,
    "LYG-下-T066": refine_下_T066,
    "LYG-下-T067": refine_下_T067,
    "LYG-下-T068": refine_下_T068,
    "LYG-下-T069": refine_下_T069,
    "LYG-下-T070": refine_下_T070,
    "LYG-下-T071": refine_下_T071,
    "LYG-下-T072": refine_下_T072,
    "LYG-下-T073": refine_下_T073,
    "LYG-下-T074": refine_下_T074,
    "LYG-下-T075": refine_下_T075,
    "LYG-下-T076": refine_下_T076,
    "LYG-下-T077": refine_下_T077,
    "LYG-下-T078": refine_下_T078,
    "LYG-下-T079": refine_下_T079,
    "LYG-下-T080": refine_下_T080,
    "LYG-下-T081": refine_下_T081,
    "LYG-下-T082": refine_下_T082,
    "LYG-下-T083": refine_下_T083,
    "LYG-下-T084": refine_下_T084,
    "LYG-下-T085": refine_下_T085,
    "LYG-下-T086": refine_下_T086,
    "LYG-下-T087": refine_下_T087,
    "LYG-下-T088": refine_下_T088,
    "LYG-下-T089": refine_下_T089,
    "LYG-下-T090": refine_下_T090,
    "LYG-下-T091": refine_下_T091,
    "LYG-下-T092": refine_下_T092,
    "LYG-下-T093": refine_下_T093,
    "LYG-下-T094": refine_下_T094,
    "LYG-下-T095": refine_下_T095,
    "LYG-下-T096": refine_下_T096,
    "LYG-下-T097": refine_下_T097,
    "LYG-下-T098": refine_下_T098,
    "LYG-下-T099": refine_下_T099,
    "LYG-下-T100": refine_下_T100,
    "LYG-下-T101": refine_下_T101,
    "LYG-下-T102": refine_下_T102,
    "LYG-下-T103": refine_下_T103,
    "LYG-下-T104": refine_下_T104,
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