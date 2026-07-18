# -*- coding: utf-8 -*-
"""Thirty-sixth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch36_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch36_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十六批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "徐智入党", "old": "徐智（1921~）浙江省杭州市人。民国28年（1939年）参加革命、加人中国共产党。", "new": "徐智（1921~）浙江省杭州市人。民国28年（1939年）参加革命、加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0390.txt:6-7"},
    {"label": "车秀民入党", "old": "车秀民（1921～）山东省日照市人。民国33年（1944年）3月参加革命，民国29年5月加人中国共产党。", "new": "车秀民（1921～）山东省日照市人。民国33年（1944年）3月参加革命，民国29年5月加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0390.txt:16-17"},
    {"label": "许耀林入党", "old": "许耀林（1922～）山东省日照市人。民国27年（1938年）参加革命，民国29年加人中国共产党。", "new": "许耀林（1922～）山东省日照市人。民国27年（1938年）参加革命，民国29年加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0390.txt:36-37"},
    {"label": "耿杰民入党", "old": "耿杰民（1922~）山东省邹平县人。民国27年（1938年）参加革命，同年加人中国共产党。", "new": "耿杰民（1922~）山东省邹平县人。民国27年（1938年）参加革命，同年加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0390.txt:40-41"},
    {"label": "杨鸿儒入党", "old": "杨鸿儒（1922～）山东省莱州人，民国33年（1944年）加人中国共产党，", "new": "杨鸿儒（1922～）山东省莱州人，民国33年（1944年）加入中国共产党，", "source": "workbench/ocr/paddle_ocr/下/part02/page_0391.txt:9"},
    {"label": "王儒现入党", "old": "王儒现（1922～）山东省平邑县人。民国28年（1939年）参加革命，民国30年加人中国共产党。", "new": "王儒现（1922～）山东省平邑县人。民国28年（1939年）参加革命，民国30年加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0391.txt:13-14"},
    {"label": "林永入党", "old": "林永（1923～）山东省文登县人。民国31年（1942年）4月参加革命，民国35年1月加人中国共产党。", "new": "林永（1923～）山东省文登县人。民国31年（1942年）4月参加革命，民国35年1月加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0391.txt:39-40"},
    {"label": "曹良友入党", "old": "曹良友（1924~）河北省宁晋县人。民国33年（1944年）9月参加革命，民国37年加人中国共产党。", "new": "曹良友（1924~）河北省宁晋县人。民国33年（1944年）9月参加革命，民国37年加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0392.txt:14-15"},
    {"label": "何仁华入党", "old": "何仁华（1925～）兴化市人。民国33年（1944年）参加工作并加人中国共产党。", "new": "何仁华（1925～）兴化市人。民国33年（1944年）参加工作并加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0392.txt:24"},
    {"label": "吴学志入党", "old": "吴学志（1925～）沭阳县人。民国33年（1944年）5月参加革命，同年加人中国共产党。", "new": "吴学志（1925～）沭阳县人。民国33年（1944年）5月参加革命，同年加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0392.txt:40-41"},
    {"label": "高心意入党", "old": "高心意（1926～）山东省海阳县人。民国32年（1943年)参加革命，次年加人中国共产党。", "new": "高心意（1926～）山东省海阳县人。民国32年（1943年)参加革命，次年加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0393.txt:8-9"},
    {"label": "王寿明入党", "old": "1973年加人中国共产党，1977年出席江苏省工业学大庆会议，", "new": "1973年加入中国共产党，1977年出席江苏省工业学大庆会议，", "source": "workbench/ocr/paddle_ocr/下/part02/page_0393.txt:39-40"},
    {"label": "鲁少时入党", "old": "鲁少时（1927～）东台县人。民国33年（1944年)7月参加工作；同年10月加人中国共产党。", "new": "鲁少时（1927～）东台县人。民国33年（1944年)7月参加工作；同年10月加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0393.txt:41-42"},
    {"label": "王隆香入党", "old": "王隆香（1933～）湖南省资兴县人。1951年参加工作。1956年毕业于中国人民解放军第四军医大学。1965年6月加人中国共产党。", "new": "王隆香（1933～）湖南省资兴县人。1951年参加工作。1956年毕业于中国人民解放军第四军医大学。1965年6月加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0396.txt:15-16"},
    {"label": "刘步生入党", "old": "刘步生(1936~）铜山县人。1960年加人中国共产党。", "new": "刘步生(1936~）铜山县人。1960年加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0397.txt:9"},
    {"label": "周维先入党", "old": "周维先（1937～）宜兴市人。1958年毕业于东北师范大学，分配至内蒙古伊克昭盟千部业余大学工作。1973年加人中国共产党。", "new": "周维先（1937～）宜兴市人。1958年毕业于东北师范大学，分配至内蒙古伊克昭盟千部业余大学工作。1973年加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0397.txt:16-17"},
    {"label": "郑申雄入党", "old": "郑申雄（1940～）广东省南海县人。1961年9月参加工作，1978年9月加人中国共产党。", "new": "郑申雄（1940～）广东省南海县人。1961年9月参加工作，1978年9月加入中国共产党。", "source": "workbench/ocr/paddle_ocr/下/part02/page_0398.txt:19-20"},
]


def append_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(target["changed"] for target in targets)
    payload = {"time": now, "scope": "第三十六批正文残留回源修复", "targets": targets, "total_replacements": total, "verified_items": len(REPLACEMENTS), "principle": "只修下册人物简介页级 OCR 明确写作加入中国共产党的条目。"}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# 第三十六批正文残留回源修复", "", f"- 时间：{now}", "- 原则：只修下册人物简介页级 OCR 明确写作加入中国共产党的条目。", f"- 核验项：{len(REPLACEMENTS)} 项。", f"- 本次替换：{total} 处。", "- 暂缓：源页仍写作 `加人` 的徐进德、毛庚年等条目，以及更早烈士传大段。", "", "## 文件"]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                lines.append(f"- {item['label']}：依据 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。")
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 第三十六批正文残留回源修复"
    memory = f"""
{marker}
- 修复下册人物简介页级 OCR 明确证明的 `加人中国共产党` 残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/下/part02/page_0390.txt`、`page_0391.txt`、`page_0392.txt`、`page_0393.txt`、`page_0396.txt`、`page_0397.txt`、`page_0398.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓源页仍写作 `加人` 的徐进德、毛庚年等条目，以及更早烈士传大段。
- 报告：`output/reports/reader_readability_source_backed_batch36_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
