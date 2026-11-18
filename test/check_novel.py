"""正文规格自检（仓库通用版）。

用法（在仓库根目录执行）:
    python -I test/check_novel.py            # 检查全部章节
    python -I test/check_novel.py 10         # 只检查前 10 章

对照 SKILL.md 的硬性参数，超标项用 ! 标出。
参数是《弱鸡的我却被正道人士奉为无上圣魔》40 章定量拆解的实测值
（见 docs/02_拆书方法论.md），换题材请按新样本重校。
"""
import re, sys, glob, os

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novel')
LIMITS = dict(chars=(1900, 2900), paras=(55, 210), dial=(10, 80), avg_para=32)
FATIGUE = {'顿时': 2, '似乎': 1, '突然': 1, '居然': 1, '仿佛': 1, '瞬间': 2, '霎时间': 1}
FINALE_NO = '第046'   # 卷末章允许加长（终章规格）
FINALE_CHARS = 4200
FINALE_PARAS = 300

def check(fp):
    txt = open(fp, encoding='utf-8').read()
    name = os.path.basename(fp)
    is_finale = name.startswith(FINALE_NO)
    body = re.sub(r'^#.*$', '', txt, flags=re.M)
    chars = len(re.sub(r'\s', '', body))
    paras = [p for p in body.split('\n') if p.strip()]
    n_para = len(paras)
    dial = sum(1 for p in paras if '“' in p or '"' in p or '”' in p)
    dial_pct = round(dial / max(1, n_para) * 100)
    flag = []
    cap_chars = FINALE_CHARS if is_finale else LIMITS['chars'][1]
    cap_paras = FINALE_PARAS if is_finale else LIMITS['paras'][1]
    if not (LIMITS['chars'][0] <= chars <= cap_chars):
        flag.append(f"字数{chars}!")
    if not (LIMITS['paras'][0] <= n_para <= cap_paras):
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
    return not flag

def main():
    files = sorted(glob.glob(os.path.join(BASE, '第*.md')))
    n = int(sys.argv[1]) if len(sys.argv) > 1 else len(files)
    ok = [check(fp) for fp in files[:n]]
    print(f'\n{len(files)} chapters checked, {len(files[:n]) - sum(ok)} flagged')
    sys.exit(0 if all(ok) else 1)

if __name__ == '__main__':
    main()
