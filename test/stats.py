"""全书统计与完整性检查（仓库通用版）。

用法（在仓库根目录执行）:
    python -I test/stats.py

输出：总章数、总字数、章均字数、章节编号连续性、日记编号连续性。
"""
import re, glob, os, sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novel')

def main():
    files = sorted(glob.glob(os.path.join(BASE, '第*.md')))
    if not files:
        print('novel/ 下没有章节文件')
        sys.exit(1)

    total = 0
    nos = []
    diary = []
    for fp in files:
        txt = open(fp, encoding='utf-8').read()
        body = re.sub(r'^#.*$', '', txt, flags=re.M)
        total += len(re.sub(r'\s', '', body))
        m = re.search(r'第(\d+)章', os.path.basename(fp))
        if m:
            nos.append(int(m.group(1)))
        d = re.search(r'第(\d+)篇', txt)
        if d:
            diary.append(int(d.group(1)))

    print(f'章节数:   {len(files)}')
    print(f'总字数:   {total}')
    print(f'章均字数: {total // max(1, len(files))}')
    print(f'章节编号: {nos[0]} - {nos[-1]}', end=' ')
    gaps = [n for n in range(nos[0], nos[-1] + 1) if n not in set(nos)]
    print('（连续）' if not gaps else f'（缺章: {gaps}）')
    if diary:
        dupes = len(diary) != len(set(diary))
        print(f'日记编号: {min(diary)} - {max(diary)}' + ('（有重复!）' if dupes else '（连续唯一）'))

if __name__ == '__main__':
    main()
