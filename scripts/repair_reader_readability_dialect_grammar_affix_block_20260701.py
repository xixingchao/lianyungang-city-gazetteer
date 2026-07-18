# -*- coding: utf-8 -*-
"""Repair flattened dialect grammar affix examples in volume 59."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_dialect_grammar_affix_block_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_dialect_grammar_affix_block_20260701.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第五十九卷方言语法词缀例词残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = """<p>一、词缀1、前缀。新浦话的形容词有比较丰富的前缀，常用的有：透、怪、多、精、稀、宿、死、恶、瘟、烂、血、挺、焦、苦。这些形容词的前缀一般表示“很、非常”的意义，加深了形容词性质、状态的程度。例如：</p>
<p>透：~俊、~新、~熟、~肥精：~枵、~细、~稀、~轻、~窄怪：~高、~好、~老实、~神气稀：~累、~松、~碎、~薄、~贱缩：~绿、~蓝、~紫、~青、~尖死：~热、~沉、~重、~笨、~慢挺：~硬、~湿、~新、~快恶：~俊、~酸、~苦焦：~干、~酸、~粘瘟：~腥、~臊、~臭苦：~辣、~咸烂：~酸、~腥多：~高、~厚、~重、~肥的血：~好、~调皮、~对头、~不讲理2、后缀。新浦话的许多动词、名词、形容词都可以带后缀。新浦话的动词后缀主要有：巴、行行、头、查、悠、乎。它们具有使动词原义轻化、小化、动作随便、漫不经心的意思。</p>
<p>例如：</p>
<p>巴：捏~、拉~、搓~、晃~、粘~查：扒~、抠~行行：干~、吃~、看~、睡~、玩~头：有干~、有吃~、没玩~、没看~乎：摆~、炸~、热~、软~悠：转~、晃~新浦话名词后缀“子”很有特点。除了与普通话共有的“子”缀词外，新浦话还有普通话没有的“子”缀词。例如：</p>
<p>手掌~、小腿~、牛犊~、鸡冠~、树枝~、蒜苗~、柿饼~、虾皮~、油果~、奶~饭盒~、手套~、牙刷~、针鼻~、鸡屋~、拐角~、雨点~、香炉~、木鱼~、乌~闺女~、侄女~、街滑~、土包~、斜眼~、豁嘴~、疯汉~、姑姑~、瘸腿~、媳~新浦话形容词的后缀主要有：乎、淫、濠、兮兮、不拉几、的慌。例如：</p>
<p>悬乎、熟乎、热乎、苦淫、酸淫、热濠、粘兮兮、脏兮兮、神经兮兮、甜不拉几、酸不拉几、热的慌、冷的慌、闷的慌、喜的慌3、中缀。新浦话常用的中缀有：溜、不、把、乎。例如：</p>
<p>溜：嗲~嘴子、滴~打挂、稀~歪拽把：百~块、千~块、万~个不:左~拉子、黑~拢通、憨~拉几乎：血~流淋二、形容词的生动形式新浦话的形容词一般都有程度差别的细微变化，这种变化是通过形容词前边或后边加上词缀构成的。单音形容词加上词缀后，其含义和用法基本上没有变化，只是表示程度的不同，有的含义弱化了，有的含义强化了。把这种不同程度的变化叫做形容词的原级、弱化级、强化级、最高级。不是所有的形容词都可以构成完整的四级形式。形容词的弱化级、强化级、最高级不能再加上程度副词，如“苦”，可以构成“苦、苦淫的、恶苦、恶苦恶苦的”四级，但不能说“很苦淫的、非常恶苦、特别恶苦恶苦”。举例如下：</p>"""

NEW = """<p>一、词缀</p>
<p>1、前缀。新浦话的形容词有比较丰富的前缀，常用的有：透、怪、多、精、稀、宿、死、恶、瘟、烂、血、挺、焦、苦。这些形容词的前缀一般表示“很、非常”的意义，加深了形容词性质、状态的程度。例如：</p>
<ul class="dialect-example-list">
<li>透：~俊、~新、~熟、~肥</li>
<li>精：~枵、~细、~稀、~轻、~窄</li>
<li>怪：~高、~好、~老实、~神气</li>
<li>稀：~累、~松、~碎、~薄、~贱</li>
<li>缩：~绿、~蓝、~紫、~青、~尖</li>
<li>死：~热、~沉、~重、~笨、~慢</li>
<li>挺：~硬、~湿、~新、~快</li>
<li>恶：~俊、~酸、~苦</li>
<li>焦：~干、~酸、~粘</li>
<li>瘟：~腥、~臊、~臭</li>
<li>苦：~辣、~咸</li>
<li>烂：~酸、~腥</li>
<li>多：~高、~厚、~重、~肥的</li>
<li>血：~好、~调皮、~对头、~不讲理</li>
</ul>
<p>2、后缀。新浦话的许多动词、名词、形容词都可以带后缀。新浦话的动词后缀主要有：巴、行行、头、查、悠、乎。它们具有使动词原义轻化、小化、动作随便、漫不经心的意思。例如：</p>
<ul class="dialect-example-list">
<li>巴：捏~、拉~、搓~、晃~、粘~</li>
<li>查：扒~、抠~</li>
<li>行行：干~、吃~、看~、睡~、玩~</li>
<li>头：有干~、有吃~、没玩~、没看~</li>
<li>乎：摆~、炸~、热~、软~</li>
<li>悠：转~、晃~</li>
</ul>
<p>新浦话名词后缀“子”很有特点。除了与普通话共有的“子”缀词外，新浦话还有普通话没有的“子”缀词。例如：</p>
<p>手掌~、小腿~、牛犊~、鸡冠~、树枝~、蒜苗~、柿饼~、虾皮~、油果~、奶~、饭盒~、手套~、牙刷~、针鼻~、鸡屋~、拐角~、雨点~、香炉~、木鱼~、乌~、闺女~、侄女~、街滑~、土包~、斜眼~、豁嘴~、疯汉~、姑姑~、瘸腿~、媳~。</p>
<p>新浦话形容词的后缀主要有：乎、淫、濠、兮兮、不拉几、的慌。例如：</p>
<p>悬乎、熟乎、热乎、苦淫、酸淫、热濠、粘兮兮、脏兮兮、神经兮兮、甜不拉几、酸不拉几、热的慌、冷的慌、闷的慌、喜的慌。</p>
<p>3、中缀。新浦话常用的中缀有：溜、不、把、乎。例如：</p>
<ul class="dialect-example-list">
<li>溜：嗲~嘴子、滴~打挂、稀~歪拽</li>
<li>把：百~块、千~块、万~个</li>
<li>不：左~拉子、黑~拢通、憨~拉几</li>
<li>乎：血~流淋</li>
</ul>
<p>二、形容词的生动形式</p>
<p>新浦话的形容词一般都有程度差别的细微变化，这种变化是通过形容词前边或后边加上词缀构成的。单音形容词加上词缀后，其含义和用法基本上没有变化，只是表示程度的不同，有的含义弱化了，有的含义强化了。把这种不同程度的变化叫做形容词的原级、弱化级、强化级、最高级。不是所有的形容词都可以构成完整的四级形式。形容词的弱化级、强化级、最高级不能再加上程度副词，如“苦”，可以构成“苦、苦淫的、恶苦、恶苦恶苦的”四级，但不能说“很苦淫的、非常恶苦、特别恶苦恶苦”。举例如下：</p>"""


def write_reports(replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十九卷方言 / 第五章语法特点 / 第一节词法特点",
        "source": "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:16703",
        "reader_path": str(HTML),
        "flattened_blocks_replaced": replaced,
        "principle": "按源文行界拆分词缀例词，不改写方言词条内容。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第五十九卷方言语法词缀例词残文修复

- 时间：{now}
- 范围：`第五十九卷方言 / 第五章语法特点 / 第一节词法特点`
- 源文依据：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:16703`

## 修复动作

- 将 `透：~俊...血：~好...2、后缀...` 的粘连段按源文行界拆开。
- 前缀、动词后缀、中缀例词改为列表；名词后缀、形容词后缀和“形容词的生动形式”恢复为独立段落。
- 替换阅读版压平残文：{replaced} 组。

## 核对说明

- 本轮只调整段落和列表结构，不重写方言词、例词和解释。
- 该段源文在工作台正文汇总中已有明确换行，可直接用于恢复阅读边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(replaced: int) -> None:
    marker = "## 2026-07-01 第五十九卷方言语法词缀例词残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计剩余的 `音标/字汇密集段落`：第五十九卷方言第五章语法特点 `透：~俊...血：~好...2、后缀...` 粘连段进行回源修复。
- 源文依据：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:16703` 附近的明确换行。
- 阅读版中前缀、动词后缀、中缀例词已拆为列表，名词后缀、形容词后缀及“形容词的生动形式”恢复独立段落；替换压平残文 {replaced} 组。
- 报告：`output/reports/reader_readability_dialect_grammar_affix_block_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected one flattened dialect affix block, found {count}")
    text = text.replace(OLD, NEW, 1)
    HTML.write_text(text, encoding="utf-8")
    write_reports(1)
    update_memory(1)
    print("dialect affix block repaired")
    print("flattened_blocks_replaced=1")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
