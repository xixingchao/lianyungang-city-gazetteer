from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第三十卷至第四十二卷（中part02）.md"),
        "replacements": [
            ("联谊联络，促进祖国统，为引进外资", "联谊联络，促进祖国统一，为引进外资", "workbench/ocr/paddle_ocr/中/part02/page_0477.txt:37"),
            ("六、祖国统一一联谊、对外联络委员会", "六、祖国统一联谊、对外联络委员会", "workbench/ocr/paddle_ocr/下/part01/page_0230.txt:18"),
            ("成立祖国统工作委员会", "成立祖国统一工作委员会", "workbench/ocr/paddle_ocr/中/part02/page_0467.txt:11;下/part01/page_0230.txt:18"),
            ("加强联联谊工作", "加强联谊工作", "workbench/ocr/paddle_ocr/中/part02/page_0471.txt:12-13;page_0472.txt:27-28"),
            ("在抗日战争中牺性。1985年在其殉国", "在抗日战争中牺牲。1985年在其殉国", "workbench/ocr/paddle_ocr/下/part01/page_0025.txt:29-32"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"),
        "replacements": [
            ("英勇牺性，有的在艰苦工作中", "英勇牺牲，有的在艰苦工作中", "workbench/ocr/paddle_ocr/下/part02/page_0094.txt:18"),
            ("不幸再次中弹，壮烈牺性。民国", "不幸再次中弹，壮烈牺牲。民国", "workbench/ocr/paddle_ocr/下/part02/page_0356.txt:25"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("联谊联络，促进祖国统，为引进外资", "联谊联络，促进祖国统一，为引进外资", "workbench/ocr/paddle_ocr/中/part02/page_0477.txt:37"),
            ("六、祖国统一一联谊、对外联络委员会", "六、祖国统一联谊、对外联络委员会", "workbench/ocr/paddle_ocr/下/part01/page_0230.txt:18"),
            ("成立祖国统工作委员会", "成立祖国统一工作委员会", "workbench/ocr/paddle_ocr/中/part02/page_0467.txt:11;下/part01/page_0230.txt:18"),
            ("加强联联谊工作", "加强联谊工作", "workbench/ocr/paddle_ocr/中/part02/page_0471.txt:12-13;page_0472.txt:27-28"),
            ("在抗日战争中牺性。1985年在其殉国", "在抗日战争中牺牲。1985年在其殉国", "workbench/ocr/paddle_ocr/下/part01/page_0025.txt:29-32"),
            ("英勇牺性，有的在艰苦工作中", "英勇牺牲，有的在艰苦工作中", "workbench/ocr/paddle_ocr/下/part02/page_0094.txt:18"),
            ("不幸再次中弹，壮烈牺性。民国", "不幸再次中弹，壮烈牺牲。民国", "workbench/ocr/paddle_ocr/下/part02/page_0356.txt:25"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_中册.html"),
        "replacements": [
            ("联谊联络，促进祖国统，为引进外资", "联谊联络，促进祖国统一，为引进外资", "workbench/ocr/paddle_ocr/中/part02/page_0477.txt:37"),
            ("六、祖国统一一联谊、对外联络委员会", "六、祖国统一联谊、对外联络委员会", "workbench/ocr/paddle_ocr/下/part01/page_0230.txt:18"),
            ("成立祖国统工作委员会", "成立祖国统一工作委员会", "workbench/ocr/paddle_ocr/中/part02/page_0467.txt:11;下/part01/page_0230.txt:18"),
            ("加强联联谊工作", "加强联谊工作", "workbench/ocr/paddle_ocr/中/part02/page_0471.txt:12-13;page_0472.txt:27-28"),
            ("在抗日战争中牺性。1985年在其殉国", "在抗日战争中牺牲。1985年在其殉国", "workbench/ocr/paddle_ocr/下/part01/page_0025.txt:29-32"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_下册.html"),
        "replacements": [
            ("祭扫海烈士纪念塔", "祭扫淮海烈士纪念塔", "workbench/ocr/paddle_ocr/下/part01/page_0323.txt:4"),
            ("英勇牺性，有的在艰苦工作中", "英勇牺牲，有的在艰苦工作中", "workbench/ocr/paddle_ocr/下/part02/page_0094.txt:18"),
            ("不幸再次中弹，壮烈牺性。民国", "不幸再次中弹，壮烈牺牲。民国", "workbench/ocr/paddle_ocr/下/part02/page_0356.txt:25"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_全书.html"),
        "replacements": [
            ("成立祖国统工作委员会", "成立祖国统一工作委员会", "workbench/ocr/paddle_ocr/中/part02/page_0467.txt:11;下/part01/page_0230.txt:18"),
        ],
    },
]

BAD_PATTERNS = [
    "联谊联络，促进祖国统，为引进外资",
    "六、祖国统一一联谊、对外联络委员会",
    "成立祖国统工作委员会",
    "加强联联谊工作",
    "在抗日战争中牺性。1985年在其殉国",
    "祭扫海烈士纪念塔",
    "英勇牺性，有的在艰苦工作中",
    "不幸再次中弹，壮烈牺性。民国",
]


def main():
    changes = []
    for task in TASKS:
        path = ROOT / task["path"]
        text = path.read_text(encoding="utf-8")
        file_changes = []
        for old, new, evidence in task["replacements"]:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            file_changes.append({"old": old, "new": new, "count": count, "evidence": evidence})
        path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": str(task["path"]), "changes": file_changes})

    total = sum(item["count"] for file in changes for item in file["changes"])
    residuals = {}
    target_paths = sorted({str(task["path"]) for task in TASKS})
    for rel in target_paths:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {pat: text.count(pat) for pat in BAD_PATTERNS if text.count(pat)}
        if hits:
            residuals[rel] = hits

    report_md = ROOT / "output/reports/reader_source_confirmed_typos_batch253_20260707.md"
    report_json = ROOT / "output/reports/reader_source_confirmed_typos_batch253_20260707.json"
    lines = [
        "# 正文源稿阅读稿明确 OCR 错字修复 batch253",
        "",
        f"- 修复总数：{total}",
        "- 范围：中册政协段、下册社团/文物人物段、全书正文汇总及当前阅读稿。",
        "- 原则：只修页级 PaddleOCR 或相邻权威页明确支持的短语；未批量处理 `牺性`。",
        "",
        "## 替换明细",
    ]
    for file in changes:
        lines.append(f"\n### {file['path']}")
        for item in file["changes"]:
            lines.append(f"- `{item['old']}` -> `{item['new']}`；次数 {item['count']}；证据 `{item['evidence']}`")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for rel, hits in residuals.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标文件中均为 0。")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps({"total": total, "changes": changes, "residuals": residuals}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
