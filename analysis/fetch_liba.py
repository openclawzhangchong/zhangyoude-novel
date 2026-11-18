import re, time, requests, os

OUT = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/liba'
os.makedirs(OUT, exist_ok=True)
BASE = 'https://www.libahao2.com/book/10332847_14160/{}.html'
HEAD = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0',
        'Referer': 'https://www.libahao2.com/book/10332847_14160/'}

ok = 0
for n in range(1, 41):
    fp = f'{OUT}/{n:03d}.txt'
    if os.path.exists(fp) and os.path.getsize(fp) > 1000:
        ok += 1
        continue
    try:
        h = requests.get(BASE.format(n), headers=HEAD, timeout=30).text
        t = re.search(r'<h1[^>]*>([^<]+)</h1>', h)
        title = t.group(1).strip() if t else f'第{n}章'
        # 取正文容器
        m = re.search(r'<div[^>]*(?:id="content"|class="[^"]*content[^"]*")[^>]*>(.*?)</div>', h, re.S)
        body = m.group(1) if m else ''
        if not body:
            # 退路：取<h1>之后所有<p>
            seg = h.split('</h1>', 1)[-1]
            body = '<p>' + seg
        body = re.sub(r'<br\s*/?>', '\n', body)
        body = re.sub(r'<p[^>]*>', '', body)
        body = re.sub(r'</p>', '\n', body)
        body = re.sub(r'<[^>]+>', '', body)
        body = re.sub(r'[\u00a0\u3000 ]{2,}', '', body)
        body = re.sub(r'\n{3,}', '\n\n', body).strip()
        open(fp, 'w', encoding='utf-8').write(f'{title}\n\n{body}')
        ok += 1
        print(f'{n:3d} {len(body):5d}  {title[:40]}')
        time.sleep(0.8)
    except Exception as e:
        print(f'{n:3d} ERROR {e}')
        time.sleep(2)
print('done', ok, '/40')
