import re, glob, os

BASE = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/lewen'
files = sorted(glob.glob(f'{BASE}/0*.txt'))

def clean(txt):
    # 去掉页眉标题泄漏（章节标题在正文中重复出现）
    lines = txt.split('\n')
    title = lines[0].strip()
    out = []
    for l in lines[1:]:
        s = l.strip()
        if s == title or s == title + ' ':
            continue
        out.append(l)
    return '\n'.join(out)

rows = []
all_text = []
for fp in files:
    txt = clean(open(fp, encoding='utf-8').read())
    all_text.append(txt)
    paras = [p.strip() for p in txt.split('\n') if p.strip()]
    n_chars = len(re.sub(r'\s', '', txt))
    n_dial = sum(1 for p in paras if '“' in p or '"' in p)
    sents = [s for s in re.split(r'[。！？；…]', txt) if s.strip()]
    lens = [len(re.sub(r'\s', '', s)) for s in sents]
    avg_s = sum(lens) / max(1, len(lens))
    short = sum(1 for L in lens if L <= 15) / max(1, len(lens))
    rows.append((os.path.basename(fp), n_chars, len(paras), round(n_dial/max(1,len(paras))*100), round(avg_s,1), round(short*100)))

print('file    chars  paras  dial%  avgSent  <=15字%')
for r in rows:
    print(f'{r[0]}  {r[1]:5d}  {r[2]:4d}  {r[3]:4d}  {r[4]:6.1f}  {r[5]:5.0f}')

full = '\n'.join(all_text)
total_c = len(re.sub(r'\s', '', full))
print(f'\nTOTAL chars: {total_c}, avg/chapter: {total_c//40}')

# 疲劳词与风格特征词频
print('\n== 风格特征词频(全书40章) ==')
for w in ['突然', '忽然', '竟然', '居然', '仿佛', '似乎', '瞬间', '霎时间', '顿时', '随即', '紧接着']:
    print(f'  {w}: {full.count(w)}')
print('\n== 吐槽/口头禅特征 ==')
for w in ['呃', '啧', '唉', '等等', '不对', '呵呵', '脑袋', '脑子', '心累', '无语', '懵', '憋', '什么鬼', '搞什么']:
    print(f'  {w}: {full.count(w)}')
print('\n== 迪化机制词 ==')
for w in ['深不可测', '高人', '大魔头', '魔神', '神机妙算', '成竹在胸', '不动声色', '面不改色', '装', '日记']:
    print(f'  {w}: {full.count(w)}')
print('\n== 日记体引言数 ==')
print('  取自天地无上圣魔:', full.count('取自天地无上圣魔'))
