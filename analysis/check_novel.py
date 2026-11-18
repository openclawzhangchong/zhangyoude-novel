"""第1卷正文自检:字数/段落数/对话占比/疲劳词/日记格言/结尾检查。

用法: python -I analysis/check_novel.py [章数]
对照 SKILL.md 的硬性参数,超标项用 ! 标出。
"""
import re, sys, glob, os

BASE = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/novel'
LIMITS = dict(chars=(1900, 2900), paras=(55, 210), dial=(10, 80), avg_para=32)
FATIGUE = {'顿时': 2, '似乎': 1, '突然': 1, '居然': 1, '仿佛': 1, '瞬间': 2, '霎时间': 1}

files = sorted(glob.glob(f'{BASE}/第*.md'))
n_check = int(sys.argv[1]) if len(sys.argv) > 1 else len(files)
issues = []

for fp in files[:n_check]:
    is_finale = os.path.basename(fp).startswith('第046')
    txt = open(fp, encoding='utf-8').read()
    name = os.path.basename(fp)
    body = re.sub(r'^#.*$', '', txt, flags=re.M)
    chars = len(re.sub(r'\s', '', body))
    paras = [p for p in body.split('\n') if p.strip()]
    n_para = len(paras)
    dial = sum(1 for p in paras if '“' in p or '"' in p or '”' in p)
    dial_pct = round(dial / max(1, n_para) * 100)
    flag = []
    cap_hi = 4200 if is_finale else LIMITS['chars'][1]
    if not (LIMITS['chars'][0] <= chars <= cap_hi):
        flag.append(f"字数{chars}!")
    paras_hi = 300 if is_finale else LIMITS['paras'][1]
    if not (LIMITS['paras'][0] <= n_para <= paras_hi):
        flag.append(f"段数{n_para}!")
    avg_p = round(chars / max(1, n_para), 1)
    if avg_p > LIMITS['avg_para']:
        flag.append(f"均段长{avg_p}!")
    if not (LIMITS['dial'][0] <= dial_pct <= LIMITS['dial'][1]):
        flag.append(f"对话%{dial_pct}!")
    if '教学日记' not in txt:
        flag.append("无日记格言!")
    fatigue = {w: body.count(w) for w in FATIGUE if body.count(w) > FATIGUE[w]}
    if fatigue:
        flag.append(f"疲劳词{fatigue}!")
    tail = [p.strip() for p in paras[-6:] if p.strip()]
    if len(tail) < 4:
        flag.append("结尾太短!")
    status = 'OK ' if not flag else '!! '
    print(f'{status}{name}  字{chars:5d} 段{n_para:3d} 对话{dial_pct:3d}%  {" ".join(flag)}')
    if flag:
        issues.append(name)

print(f'\n{len(files)} chapters checked, {len(issues)} flagged: {issues}')
