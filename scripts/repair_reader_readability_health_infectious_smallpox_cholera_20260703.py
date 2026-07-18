# -*- coding: utf-8 -*-
"""Restore Fifth十五卷常见病防治传染病防治天花与霍乱小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_infectious_smallpox_cholera_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_infectious_smallpox_cholera_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷传染病防治天花霍乱回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0173.txt:15-36; page_0174.txt:3-8"
SCOPE_START = '<p><strong>一、天花</strong></p>'
SCOPE_END = '<p><strong>三、伤寒、副伤寒</strong></p>'

NEW_HTML = """<p><strong>一、天花</strong></p>
<p>海州地区民间医生为儿童接种牛痘历史悠久，民国3年（1914年）始用新法为儿童接种牛痘，新旧法为儿童接种牛痘并行，一直延续到20世纪50年代。民国19年，连云发病12例，翌年发病13例。新浦、海州发病300例。民国33年，新浦、海州、连云天花流行，临洪一个150人的自然村发病8例、死亡1例。至民国37年，新浦、海州、连云共接种牛痘2.96万人。民国38年3月，连云发病20例，海州发病1例。1950年春，全市接种牛痘1.41万人，秋季又接种2995人。1951年接种9.52万人。1952年全民普种牛痘，共接种15.13万人，占人口总数的82.6%。1952年，连云发病1例。1953年后，市内无病例发生。</p>
<p>此后每年春秋都免费接种牛痘。1953～1961年，全市累计接种15.68万人。1962年，第二次全民普种牛痘，除不到3个月的婴儿和55岁以上老人共2.52万人外，共应接种20.49万人，实际接种16.8万人，占应种人数的82.2%，占人口总数的71.4%。1983年，开始只对婴儿进行初种，对6岁、12岁儿童、18岁青年复种，平均每年接种1万人。1981年4月，世界卫生组织宣布全世界消灭了天花，根据中华人民共和国卫生部（81）卫防字26号文件精神，全市停止牛痘接种。</p>
<p><strong>二、霍乱、副霍乱</strong></p>
<p>民国9年（1920年），市内流行霍乱始有记载。民国20年夏，新浦、海州、连云等地霍乱流行持续40余天，死人无统计，新浦一家5口死3人。民国30年，市内开始注射霍乱菌苗。民国32年至34年，海州、新坝、南城局部霍乱流行。建国后，每年普遍注射霍乱菌苗，其中以渔民、盐工为主要对象。1963年，成立连云港市防疫指挥部及办公室，市、区、乡各级医院建立肠道门诊，以便及早发现霍乱病人。成立3个机动抢救组，每组有7名医护人员，配备药品、器械。突击接种霍乱菌苗17万人，抽调109人在疫区内开展疫苗检查，清理环境。对居民采取突击性预防服药。1964～1974年，每年夏秋季节都将霍乱、副霍乱作为预防重点，坚持对腹泻病人观察和粪检，经常对居民点周围的水源监测。1975年起，对沿海居民、渔港码头流动船民及进出连云港市汽车乘客监测和服预防性药物。</p>
<p>1978年，发病103例，1人死亡，其余治愈。1981～1988年，全市发生108例，无死亡，其中1986年发病75例。1989～1990年，无病例发生。</p>
"""

EXPECTED_TEXT = [
    "临洪一个150人的自然村发病8例、死亡1例",
    "共应接种20.49万人，实际接种16.8万人",
    "1964～1974年，每年夏秋季节都将霍乱、副霍乱作为预防重点",
    "1981～1988年，全市发生108例，无死亡",
    "1989～1990年，无病例发生",
]
RESIDUALS = [
    "临洪个150人的自然村",
    "20.49方人",
    "1953~1961年",
    "1964~1974年",
    "1981~1988年",
    "1989~1990年,无病例发生",
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
    return changed, {"rewrote_scope": changed, "items_restored": 2, "paragraphs_restored": 4}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治 / 天花、霍乱副霍乱",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建传染病防治开头两个小项，停止在三、伤寒、副伤寒前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷传染病防治天花霍乱回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：修正 `临洪一个150人的自然村`、`20.49万人` 等 OCR 残留，并统一本小段年份连接号。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷传染病防治天花霍乱回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治` 中 `一、天花` 至 `三、伤寒、副伤寒` 前。
- 修复内容：修正 `临洪个150人的自然村`、`20.49方人`、年份连接号和 `1989~1990年,无病例发生` 标点残留。
- 报告：`output/reports/reader_readability_health_infectious_smallpox_cholera_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷传染病防治天花霍乱回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第一节传染病防治` 的 `一、天花`、`二、霍乱、副霍乱` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `三、伤寒、副伤寒` 前。
- 修正 `临洪个150人的自然村`、`20.49方人`、年份连接号和 `1989~1990年,无病例发生` 等残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_infectious_smallpox_cholera_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷传染病防治天花霍乱回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
