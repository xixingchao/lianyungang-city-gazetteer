# -*- coding: utf-8 -*-
"""Repair source-backed dialect grammar heading/list boundaries in volume 59."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_dialect_grammar_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_dialect_grammar_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第五十九卷方言语法边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"

REPAIRS = [
    {
        "label": "四、几个特殊量词",
        "source": f"{SOURCE}:16826-16829",
        "old": "<p>四、几个特殊量词1、新浦话量词“个”使用范围较广。普通话不用“个”而新浦话用“个”作量词的例子如：一个手、一个桥、一个镜子、一个板凳、一个手表、一个褂子、一个羊、一个米粒子2、其他较特殊的常用量词有：</p>",
        "new": "<h5>四、几个特殊量词</h5>\n<p>1、新浦话量词“个”使用范围较广。普通话不用“个”而新浦话用“个”作量词的例子如：一个手、一个桥、一个镜子、一个板凳、一个手表、一个褂子、一个羊、一个米粒子</p>\n<p>2、其他较特殊的常用量词有：</p>",
    },
    {
        "label": "特殊量词例词列表 / 五、自感动词短语",
        "source": f"{SOURCE}:16830-16841",
        "old": "<p>块：一块甘蔗盼子：干了一盼了、坐了一盼子、玩了一盼子行：一行灰把(十个、十双)：一把子鸡蛋、两把子鸡蛋、一把子筷子充：一充扑克帮子：客人来了一帮子，又来了一帮子合：一合门(两扇门)生子(周岁):这小孩两生子了五、自感动词短语新浦话的自感动词短语由两部分组成，前一部分是表示外界刺激人体某一位置而引起不舒服感觉的动词，这种感觉是受动者的自然感受，而不是施动者有意造成的；后一部分是名词“人”或身体的某一位置。例如：</p>",
        "new": "<ul class=\"dialect-example-list\">\n<li>块：一块甘蔗</li>\n<li>盼子：干了一盼了、坐了一盼子、玩了一盼子</li>\n<li>行：一行灰</li>\n<li>把(十个、十双)：一把子鸡蛋、两把子鸡蛋、一把子筷子</li>\n<li>充：一充扑克</li>\n<li>帮子：客人来了一帮子，又来了一帮子</li>\n<li>合：一合门(两扇门)</li>\n<li>生子(周岁):这小孩两生子了</li>\n</ul>\n<h5>五、自感动词短语</h5>\n<p>新浦话的自感动词短语由两部分组成，前一部分是表示外界刺激人体某一位置而引起不舒服感觉的动词，这种感觉是受动者的自然感受，而不是施动者有意造成的；后一部分是名词“人”或身体的某一位置。例如：</p>",
    },
    {
        "label": "自感动词短语例词列表",
        "source": f"{SOURCE}:16842-16847",
        "old": "<p>冰人：睡在地上~垫人：右鞋跟比左鞋跟高，~闷人：一个人在家里，~噎人：饼子太干，~怕人：天乌黑的，好~硌脚：鞋里有沙子，~</p>",
        "new": "<ul class=\"dialect-example-list\">\n<li>冰人：睡在地上~</li>\n<li>垫人：右鞋跟比左鞋跟高，~</li>\n<li>闷人：一个人在家里，~</li>\n<li>噎人：饼子太干，~</li>\n<li>怕人：天乌黑的，好~</li>\n<li>硌脚：鞋里有沙子，~</li>\n</ul>",
    },
    {
        "label": "一、宾语前置",
        "source": f"{SOURCE}:16848-16851",
        "old": "<p>一、宾语前置在新浦话中，宾语可以直接出现在动词谓语前边。如：①他饭吃了，活还没干。②他钢笔买来了。除此之外，动词后缀“行行”有“正在进行”的意思，用在句子里可以使宾语前置于动词谓语前。如：①他饭吃行行的出去了。②电视看行行的停电了。</p>",
        "new": "<h5>一、宾语前置</h5>\n<p>在新浦话中，宾语可以直接出现在动词谓语前边。如：①他饭吃了，活还没干。②他钢笔买来了。除此之外，动词后缀“行行”有“正在进行”的意思，用在句子里可以使宾语前置于动词谓语前。如：①他饭吃行行的出去了。②电视看行行的停电了。</p>",
    },
    {
        "label": "二、可能补语",
        "source": f"{SOURCE}:16852-16855",
        "old": "<p>二、可能补语普通话常用“得”连接补语的形式表示动作的可能，否定式用“不”，如：吃得了，吃不了。新浦话否定式与普通话相同，肯定式则有差异，可以省掉“得”。如①能说清。②能买起了彩电。③吃饱饱的。④雨下大了。</p>",
        "new": "<h5>二、可能补语</h5>\n<p>普通话常用“得”连接补语的形式表示动作的可能，否定式用“不”，如：吃得了，吃不了。新浦话否定式与普通话相同，肯定式则有差异，可以省掉“得”。如①能说清。②能买起了彩电。③吃饱饱的。④雨下大了。</p>",
    },
    {
        "label": "三、被动句",
        "source": f"{SOURCE}:16856-16858",
        "old": "<p>三、被动句在新浦话中，被动句往往不用“被”，而用“叫、给”两个介词表示被动关系。如：①他叫老师吵了。②茶杯叫人打了。③我给他吓一跳。④苹果给儿子吃光了。</p>",
        "new": "<h5>三、被动句</h5>\n<p>在新浦话中，被动句往往不用“被”，而用“叫、给”两个介词表示被动关系。如：①他叫老师吵了。②茶杯叫人打了。③我给他吓一跳。④苹果给儿子吃光了。</p>",
    },
    {
        "label": "四、比较句",
        "source": f"{SOURCE}:16859-16864",
        "old": "<p>四、比较句新浦话比较句的肯定式用“起”作介词引进比较的另一方，介词短语置于形容词之后，语序与普通话不同。如：①打春后，一天长起一天。②日子一天好起一天。③是荤强起素。</p>",
        "new": "<h5>四、比较句</h5>\n<p>新浦话比较句的肯定式用“起”作介词引进比较的另一方，介词短语置于形容词之后，语序与普通话不同。如：①打春后，一天长起一天。②日子一天好起一天。③是荤强起素。</p>",
    },
    {
        "label": "五、反复问句",
        "source": f"{SOURCE}:16865-16866",
        "old": "<p>五、反复问句新浦话的反复问句主要有“vp不vp”、“vp没vp”两种，这两种形式都有省略式。例如：</p>",
        "new": "<h5>五、反复问句</h5>\n<p>新浦话的反复问句主要有“vp不vp”、“vp没vp”两种，这两种形式都有省略式。例如：</p>",
    },
    {
        "label": "反复问句格式行",
        "source": f"{SOURCE}:16867-16870",
        "old": "<p>vp 不/没vpvp 不/没vv不/没 vpvp不/没有①你喝水不喝水？</p>",
        "new": "<ul class=\"dialect-example-list\">\n<li>vp 不/没vp</li>\n<li>vp 不/没v</li>\n<li>v不/没 vp</li>\n<li>vp不/没有</li>\n</ul>\n<p>①你喝水不喝水？</p>",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed: list[dict[str, str]] = []
    for item in REPAIRS:
        count = text.count(item["old"])
        if count != 1:
            raise RuntimeError(f"expected one match for {item['label']}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"label": item["label"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十九卷方言 / 第五章语法特点：词法、句法小标题与例词列表边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["按源文独立行恢复 h5 小标题和例词列表；不改方言词、例句正文。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十九卷方言语法边界补修

- 时间：{now}
- 范围：`第五十九卷方言 / 第五章语法特点`
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['label']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅按源文行界恢复小标题、编号段和例词列表，不改写方言词、例句或解释。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第五十九卷方言语法边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第五十九卷方言第五章语法特点 9 处边界：`四、几个特殊量词`、`五、自感动词短语`、句法特点下 `一、宾语前置` 至 `五、反复问句`，并将源文逐行例词恢复为列表。
- 依据 `{SOURCE}:16826-16870` 的独立标题行和例词行；不改方言词、例句正文。
- 报告：`output/reports/reader_readability_dialect_grammar_boundaries_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
