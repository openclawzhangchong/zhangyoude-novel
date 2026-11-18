import re, json

h = open('C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/dy2.html',
         'rb').read().decode('utf-8', 'ignore')
i = h.find('_ROUTER_DATA')
print('idx:', i)
print(repr(h[i:i + 200]))
# 提取 JSON:从第一个 { 开始配对
start = h.find('{', i)
depth = 0
end = start
for k in range(start, min(start + 2_000_000, len(h))):
    c = h[k]
    if c == '{':
        depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            end = k + 1
            break
blob = h[start:end]
print('blob len:', len(blob))
data = json.loads(blob)

def walk(o, path=''):
    hits = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('image_list', 'desc', 'images', 'uri') and not isinstance(v, (dict, list)):
                hits.append((path + '/' + k, str(v)[:200]))
            hits += walk(v, path + '/' + k)
    elif isinstance(o, list):
        for n, v in enumerate(o[:30]):
            hits += walk(v, f'{path}[{n}]')
    return hits

hits = walk(data)
for p, v in hits[:40]:
    print(p, '=>', v)

# 找图片 url 数组
def find_urls(o, out):
    if isinstance(o, dict):
        for v in o.values():
            find_urls(v, out)
    elif isinstance(o, list):
        for v in o:
            find_urls(v, out)
    elif isinstance(o, str) and 'douyinpic' in o:
        out.append(o)

out = []
find_urls(data, out)
uniq = []
for u in out:
    if u not in uniq:
        uniq.append(u)
print('pic urls:', len(uniq))
for u in uniq[:15]:
    print(u[:180])
