import re
h = open('C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/liba_ch1.html',
         encoding='utf-8', errors='ignore').read()
print('size:', len(h))
t = re.search(r'<title>([^<]{0,80})', h)
print('title:', t.group(1) if t else 'N/A')
for pat in ['id="content"', 'read-content', '章正文', '<article', 'adsbygoogle', 'VIP', '百度']:
    print(f'{pat!r}: {h.count(pat)}')
i = h.find('张莫')
print('first 张莫 at', i)
if i > 0:
    print(repr(h[max(0, i - 250):i + 350]))
