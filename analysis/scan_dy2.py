import re

h = open('C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/dy2.html',
         'rb').read().decode('utf-8', 'ignore')
urls = sorted(set(re.findall(r'https://p[0-9][^"\'<> ]+?(?:webp|jpeg|jpg|png)', h)))
print('img urls:', len(urls))
for u in urls[:12]:
    print(u[:170])
print('---desc---')
m = re.search(r'<meta name="description" content="([^"]{0,300})', h)
print(m.group(1) if m else 'N/A')
i = h.find('一觉醒来')
print('一觉醒来 idx:', i)
if i > 0:
    print(repr(h[max(0, i - 200):i + 400]))
# RENDER_DATA?
j = h.find('__loacl_data') 
for kw in ['RENDER_DATA', 'window.__INIT', 'ROUTER_DATA', 'item_list', 'image_list']:
    print(kw, h.count(kw))
