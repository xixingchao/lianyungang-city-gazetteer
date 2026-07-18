#!/usr/bin/env python3
"""
删除 part02/part03 中重复的总目录和章节目录区块。
使用精确行号定位，保留正文中的所有内容。
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

BODY_DIR = os.path.join(os.path.dirname(__file__), '..', 'workbench', 'body_chapters', '上')

# 精确行号范围（0-indexed）
# part02: L1193 "总篇目·" 到 L2642 空行（正文前的最后一行）
# part03: L1193 "总篇目·" 到 L5500 空行（正文前的最后一行）
FIXES = {
    # part02: L1193 "总篇目·" ~ L2644 空行前, 保留 L2645 "第四章"
    '第四卷至第十卷（part02）.md': (1193 - 1, 2644),  # [start, end)
    # part03: L1193 "总篇目·" ~ L5499 尾注，保留 L5501 "第十一卷"
    '第十卷至第十六卷（part03）.md': (1193 - 1, 5500),
}


def main():
    dry_run = '--dry-run' in sys.argv
    mode = "预览" if dry_run else "执行"

    print(f"{'='*60}")
    print(f"[{mode}] 删除 part02/part03 重复目录区块")
    print(f"{'='*60}")

    for fname, (start_idx, end_idx) in FIXES.items():
        fpath = os.path.join(BODY_DIR, fname)
        if not os.path.exists(fpath):
            print(f"[WARN] 文件不存在: {fname}")
            continue

        with open(fpath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 验证起始行
        actual_start = lines[start_idx].strip()
        actual_end_prev = lines[end_idx - 1].strip() if end_idx > 0 else ''
        actual_end_next = lines[end_idx].strip() if end_idx < len(lines) else ''

        print(f"\n=== {fname} ===")
        print(f"  删除 L{start_idx+1} ~ L{end_idx}（{end_idx - start_idx} 行）")
        print(f"  起始行: [{actual_start}]")
        print(f"  删除末行: [{actual_end_prev}]")
        print(f"  保留首行: [{actual_end_next}]")

        # 验证
        assert actual_start == '总篇目·', f"起始行不匹配: '{actual_start}'"
        if fname.startswith('第四卷'):
            # part02: 保留 L2645 "第四章"
            assert actual_end_next == '第四章', \
                f"保留行不正确: '{actual_end_next}'"
        elif fname.startswith('第十卷'):
            assert actual_end_next == '第十一卷', \
                f"保留行不正确: '{actual_end_next}'"

        if not dry_run:
            backup_path = fpath + '.dup_backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            new_lines = lines[:start_idx] + lines[end_idx:]
            with open(fpath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            print(f"  已执行，备份: {os.path.basename(backup_path)}")

    print(f"\n{'='*60}")
    print("预览模式，未实际修改" if dry_run else "删除完成")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
