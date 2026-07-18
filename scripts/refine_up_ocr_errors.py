# -*- coding: utf-8 -*-
"""
连云港市志 上册 OCR 系统性错误修正脚本

基于阶段E精修产物，修正已知OCR系统性错误：
1. 沭/述混淆（新述河→新沭河、述阳→沭阳等）
2. 沐/沭混淆（新沐河→新沭河、临沐县→临沭县等）
3. 经纬度/数字符号缺失（3507'→35°07'、11824°→118°24'等）
4. 形近字修正（参考连云港市地方志特定地名/人名）
5. 大事记格式规范化

用法:
  python refine_up_ocr_errors.py --dry-run     # 预览修正
  python refine_up_ocr_errors.py                # 执行修正
  python refine_up_ocr_errors.py --file <path>  # 单文件修正
"""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "workbench" / "body_chapters" / "上"
BACKUP_DIR = ROOT / "workbench" / "body_chapters" / "上_backup_before_ocr_fix"

# ============================================================
# 修正规则：每项 (pattern, replacement, description)
# 注意：只修正地名/专名中的错误，不碰普通叙述中的"述"
# ============================================================

CORRECTIONS = [
    # ---- 沭/述 混淆（地名专名）----
    # 新述河 → 新沭河（山东/江苏界河，贯穿全志高频出现）
    (r"新述河", "新沭河", "新述河→新沭河"),
    # 述阳 → 沭阳（沭阳县，连云港邻县，高频出现）
    (r"述阳", "沭阳", "述阳→沭阳"),
    # 述北河 → 沭北河
    (r"述北河", "沭北河", "述北河→沭北河"),
    # 述城镇 → 沭城镇
    (r"述城镇", "沭城镇", "述城镇→沭城镇"),
    # 述河 → 沭河（需小心，可能误改"描述河流"——但志书中极少这种表述）
    (r"(\u53bf|\u5883|\u81f3|\u5165|\u53e3|\u4e0e|\u3001)(\s*)述河", r"\1\2沭河", "X述河→X沭河"),
    # 古述水 → 古沭水
    (r"古述水", "古沭水", "古述水→古沭水"),
    # 淮述新河 → 淮沭新河
    (r"淮述新河", "淮沭新河", "淮述新河→淮沭新河"),
    # 述新河 → 沭新河（沭阳至新浦/新沂的河道）
    (r"述新河", "沭新河", "述新河→沭新河"),
    # 述新渠 → 沭新渠
    (r"述新渠", "沭新渠", "述新渠→沭新渠"),
    # 述新分干渠 → 沭新分干渠
    (r"述新分干渠", "沭新分干渠", "述新分干渠→沭新分干渠"),
    # 述水 → 沭水（在"江淮述水"等语境）
    (r"(\u6c5f\u6dee|\u8c03\u5f15)(\s*)述水", r"\1\2沭水", "江淮述水→江淮沭水"),
    # 述北 → 沭北（灌云县引述阳县→引沭阳县，但需排除"上述北方"之类）
    (r"引述阳", "引沭阳", "引述阳→引沭阳"),
    # 准述新河 → 淮沭新河
    (r"准述新河", "淮沭新河", "准述新河→淮沭新河"),

    # ---- 沐/沭 混淆（地名专名）----
    # 新沐河 → 新沭河
    (r"新沐河", "新沭河", "新沐河→新沭河"),
    # 沐新河 → 沭新河
    (r"沐新河", "沭新河", "沐新河→沭新河"),
    # 沐新渠 → 沭新渠
    (r"沐新渠", "沭新渠", "沐新渠→沭新渠"),
    # 临沐县 → 临沭县
    (r"临沐县", "临沭县", "临沐县→临沭县"),
    # 沂沐泗 → 沂沭泗
    (r"沂沐泗", "沂沭泗", "沂沐泗→沂沭泗"),
    # 沂、沐、泗 → 沂、沭、泗
    (r"沂、沐、泗", "沂、沭、泗", "沂、沐、泗→沂、沭、泗"),
    # 古沐河 → 古沭河
    (r"古沐河", "古沭河", "古沐河→古沭河"),
    # 淮沐新河 → 淮沭新河
    (r"淮沐新河", "淮沭新河", "淮沐新河→淮沭新河"),
    # 沐河 → 沭河（需小心上下文，但志书中"沐河"几乎都是"沭河"之误）
    (r"(\u5c71\u4e1c|\u6c82|\u6c8c|\u65b0|\u53e4|\u4e34)(\s*)沐河", r"\1\2沭河", "X沐河→X沭河"),
    # 沐北 → 沭北
    (r"沐北(\u6cb3|\u5730)", r"沭北\1", "沐北X→沭北X"),

    # ---- 经纬度符号修正 ----
    # 11824°119°48° → 118°24'~119°48'
    (r"11824°119°48°", "118°24'~119°48'", "经度格式修正"),
    # 3507 → 35°07'（在经纬度上下文）
    (r"～3507之间", "～35°07'之间", "纬度3507→35°07'"),
    (r"~3507'", "~35°07'", "纬度3507'→35°07'"),
    # 119°48(?!['°\d]) → 119°48'
    (r"119°48(?!['\'\°\d])", "119°48'", "119°48→119°48'"),
    # 34°12~ → 34°12'~
    (r"(\d+)°(\d{2})~(\d+)", r"\1°\2'~\3", "度分格式补撇号"),
    # 3507' 单独出现在经纬度语境
    (r"(\d+)°(\d{2})[′\']?(\s*[～~]\s*)3507", r"\1°\2'\335°07'", "复合纬度修正"),
]

# ============================================================
# 大事记格式修正规则
# ============================================================

# 大事记年份条目应统一为 "XXXX年" 开头
# 修复断行导致年份与内容分离的情况
EVENT_YEAR_PATTERN = re.compile(r"(?<!\d)(\d{4})年\s*\n(?=[^\n]{2,60}\n)")

# ============================================================
# 形近字修正（志书特定地名/术语）
# ============================================================
TYPO_FIXES = [
    # 常见OCR形近字（只修正高置信度错误）
    ("吡咤", "叱咤", "吡咤→叱咤"),
    ("进一一步", "进一步", "进一一步→进一步"),
    ("编繁", "编纂", "编繁→编纂"),
    ("凤俗", "风俗", "凤俗→风俗"),
    ("披沙栋金", "披沙拣金", "披沙栋金→披沙拣金"),
    ("达捻山", "达山", "达捻山→达山"),  # 前三岛之一
    ("达翰尔", "达斡尔", "达翰尔→达斡尔"),
    ("胸山", "朐山", "胸山→朐山"),  # 海州古地名（极高频）
    ("郊子国", "郯子国", "郊子国→郯子国"),
    ("隶准安府", "隶淮安府", "隶准安府→隶淮安府"),
    ("治准指挥部", "治淮指挥部", "治准→治淮"),
    ("黄准海平原", "黄淮海平原", "黄准海→黄淮海"),
    ("准北盐场", "淮北盐场", "准北盐场→淮北盐场"),
    ("蔬浚", "疏浚", "蔬浚→疏浚"),
    ("潼失", "湮失", "潼失→湮失"),
    ("海浸", "海侵", "海浸→海侵"),  # 地质术语
    ("侵人", "侵入", "侵人→侵入"),  # 地质术语
    ("溶岩", "熔岩", "溶岩→熔岩"),  # 地质术语
    ("卷性浩繁", "卷帙浩繁", "卷性浩繁→卷帙浩繁"),
    # 注：瞻程非邈、总而成、大伴 等存疑，保留原文待人工确认
]


def apply_corrections(text: str, dry_run: bool = False) -> tuple[str, list[str]]:
    """应用修正规则，返回(修正后文本, 修正日志列表)"""
    log = []
    result = text

    for pattern, replacement, desc in CORRECTIONS:
        matches = re.findall(pattern, result)
        if matches:
            count = len(matches)
            result = re.sub(pattern, replacement, result)
            log.append(f"  [{desc}] ×{count}")

    for old, new, desc in TYPO_FIXES:
        count = result.count(old)
        if count > 0:
            result = result.replace(old, new)
            log.append(f"  [{desc}] ×{count}")

    return result, log


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    """处理单个精修MD文件"""
    text = filepath.read_text(encoding="utf-8")
    fixed, log = apply_corrections(text, dry_run)

    stats = {
        "file": filepath.name,
        "size_before": len(text),
        "size_after": len(fixed),
        "changes": len(log),
        "log": log,
    }

    if not dry_run and fixed != text:
        # 备份原文件
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup_path = BACKUP_DIR / filepath.name
        backup_path.write_text(text, encoding="utf-8")
        # 写入修正后
        filepath.write_text(fixed, encoding="utf-8")

    return stats


def main():
    parser = argparse.ArgumentParser(description="上册OCR系统性错误修正")
    parser.add_argument("--dry-run", action="store_true", help="预览修正，不实际写入")
    parser.add_argument("--file", help="单文件修正（文件名，如 第一卷_自然环境.md）")
    args = parser.parse_args()

    if args.file:
        fpath = CHAPTER_DIR / args.file
        if not fpath.exists():
            print(f"[ERROR] 文件不存在: {fpath}")
            return
        files = [fpath]
    else:
        files = sorted(CHAPTER_DIR.glob("*.md"))

    total_stats = {"files": 0, "total_changes": 0, "total_log_entries": 0}
    all_logs = []

    for fpath in files:
        if fpath.name.startswith("连云港市志_上册_正文汇总"):
            continue  # 跳过汇总文件，只修正分章
        stats = process_file(fpath, dry_run=args.dry_run)
        total_stats["files"] += 1
        total_stats["total_changes"] += stats["changes"]
        total_stats["total_log_entries"] += len(stats["log"])

        if stats["changes"] > 0:
            print(f"\n[FILE] {stats['file']} ({stats['size_before']}→{stats['size_after']} bytes, {stats['changes']} 项修正)")
            for entry in stats["log"]:
                print(entry)
            all_logs.extend(stats["log"])
        else:
            print(f"   {stats['file']} — 无修正")

    print(f"\n{'='*50}")
    print(f"总计：{total_stats['files']} 文件，{total_stats['total_changes']} 处修正")
    if args.dry_run:
        print("【预览模式】未实际写入文件。去掉 --dry-run 执行修正。")
    else:
        print(f"备份目录：{BACKUP_DIR}")
        print("修正已完成。请运行 merge_up_body.py 重新汇总。")

    # 写入修正日志
    log_path = ROOT / "workbench" / "qa" / "上册OCR错误修正日志.md"
    log_lines = [
        "# 上册 OCR 系统性错误修正日志",
        "",
        f"模式：{'预览' if args.dry_run else '执行'}",
        f"文件数：{total_stats['files']}",
        f"修正项数：{total_stats['total_log_entries']}",
        "",
        "## 修正详情",
        "",
    ]
    log_lines.extend(all_logs)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(log_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
