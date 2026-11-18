"""把碎叙述段合并:遍历段落(跳过空行),连续非对话段,合并后总长<=70字则并成一段。"""
import re, sys

for fp in sys.argv[1:]:
    lines = open(fp, encoding='utf-8').read().split('\n')
    paras = []
    for l in lines:
        s = l.strip()
        if s:
            paras.append(s)
    out = []
    buf = ''
    for s in paras:
        is_dial = s.startswith('“') or s.startswith('—') or s.startswith('>') or s.startswith('#')
        if is_dial:
            if buf:
                out.append(buf)
                buf = ''
            out.append(s)
            continue
        if buf and len(buf) + len(s) <= 70:
            buf = buf + s
        else:
            if buf:
                out.append(buf)
            buf = s
    if buf:
        out.append(buf)
    txt = '# ' + (paras[0] if paras and paras[0].startswith('第') else '') + '\n\n'
    body = '\n\n'.join(out if not out[0].startswith('第') else out[1:])
    if not out[0].startswith('第'):
        body = '\n\n'.join(out)
    txt = '# 第' + re.search(r'第(\d+)章', fp).group(1) + '章 占位\n\n' if False else txt
    # 保留原章节标题行
    title = paras[0] if paras[0].startswith('第') else None
    rest = out[1:] if title and out and out[0] == title else out
    txt = ('\n\n'.join(([title] if title else []) + rest)) + '\n'
    open(fp, 'w', encoding='utf-8').write(txt)
    body2 = re.sub(r'^#.*$', '', txt, flags=re.M)
    n = len([p for p in body2.split('\n') if p.strip()])
    print(fp, '->', n, 'paras')
