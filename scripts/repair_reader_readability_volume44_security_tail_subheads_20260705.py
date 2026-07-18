# -*- coding: utf-8 -*-
"""Repair source-backed volume 44 public security tail boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume44_security_tail_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume44_security_tail_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十四卷治安尾部标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

REPAIRS = [
    {
        "label": "九、交通管理",
        "source": f"{SOURCE}:4364",
        "old": "<p>九、交通管理订商营汽车管理办法，规定“载客汽车不得装货，载货汽车不得搭客。",
        "new": "<h5>九、交通管理</h5>\n<p>订商营汽车管理办法，规定“载客汽车不得装货，载货汽车不得搭客。",
    },
    {
        "label": "十、消防机构",
        "source": f"{SOURCE}:4588-4589",
        "old": "<p>十、消防机构民国20年至民国28年（1931～1939年），东海县公安局所设有消防队组织。</p>",
        "new": "<h5>十、消防机构</h5>\n<p>民国20年至民国28年（1931～1939年），东海县公安局所设有消防队组织。</p>",
    },
    {
        "label": "十一、边防管理",
        "source": f"{SOURCE}:4856-4878",
        "old": "<p>各边防派出所共查船2.02万条次，对违章的给予批评教育、行政处分、罚款、吊扣证件等处理。赣榆县三洋港边防派出所查处一个12人盗窃团伙。",
        "new": "<h5>十一、边防管理</h5>\n<p>1959年，连云港市公安局清理市区水上船只。1963年，沿海各分局、派出所与市区参加春汛生产渔船订立安全公约，对出海船只安全情况逐船检查，在每船设治安员1人；协同有关部门，划定外来船只停泊地段，统一联络信号，统一规定安全制度。1976年上半年，市公安局各边防派出所把港口船只检查管理纳入渔汛保卫工作，执行进出港申报、定点停泊、船只看管、查岗查船、验滩等制度。1977年，市公安局边防科会同港务监督部门精神，制订港口管理规则并公布实施。1980年，市人民边防武装警察支队共办理进出港签证11025船次，查船300余次、1500条船，打击水上违法分子，整顿港口治安秩序。1982年，市人民边防警察支队共查船59244条，对查出有违章现象的1016条船只作处理。1983年9月15日至11月底，市边防分局完成出海船舶、出海船民簿证换发工作。1984年，全市边防出动2953人次，查船1.37万条次，发现违章船舶623条，均按规定处理。1985年，各边防派出所共查船2.02万条次，对违章的给予批评教育、行政处分、罚款、吊扣证件等处理。赣榆县三洋港边防派出所查处一个12人盗窃团伙。",
    },
    {
        "label": "十二、反走私、安全检查",
        "source": f"{SOURCE}:4879",
        "old": "<p>十二、反走私、安全检查1982年，市边防分局破获走私案3起。",
        "new": "<h5>十二、反走私、安全检查</h5>\n<p>1982年，市边防分局破获走私案3起。",
    },
    {
        "label": "一、预审",
        "source": f"{SOURCE}:4956",
        "old": "<p>一、预审民国30年（1941年），海陵县（路北东海县）公安局设审讯股。",
        "new": "<h5>一、预审</h5>\n<p>民国30年（1941年），海陵县（路北东海县）公安局设审讯股。",
    },
    {
        "label": "二、监所",
        "source": f"{SOURCE}:5000",
        "old": "<p>二、监所民国3年（1914年），东海县公署设看守所。",
        "new": "<h5>二、监所</h5>\n<p>民国3年（1914年），东海县公署设看守所。",
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
        "scope": "第四十四卷治安：第一章尾部和第六节预审监所小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": [
            "恢复源文独立行可证明的小标题边界。",
            "补回十一、边防管理分页前半段；不重建表44-5、44-7等表格数字。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十四卷治安尾部标题边界补修

- 时间：{now}
- 范围：第四十四卷治安，第一章尾部与第六节预审监所。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['label']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的小标题边界，并补回 `十一、边防管理` 分页前半段。\n- 不重建交通事故、安全检查等统计表。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十四卷治安尾部标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十四卷治安尾部 6 处标题边界：`九、交通管理`、`十、消防机构`、`十一、边防管理`、`十二、反走私、安全检查`、第六节 `一、预审`、`二、监所`。
- 依据 `{SOURCE}:4364-5000`；补回 `十一、边防管理` 分页前半段，不重建表 44-5、44-7 等表格数字。
- 报告：`output/reports/reader_readability_volume44_security_tail_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
