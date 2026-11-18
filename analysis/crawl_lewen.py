import re, time, os, sys, requests

BASE = 'https://m.lewennwx.cc/11/11428/{}.html'
HEAD = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Referer': 'https://m.lewennwx.cc/11/11428/',
}
OUT = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/lewen'
os.makedirs(OUT, exist_ok=True)

s = requests.Session()
s.headers.update(HEAD)

def get(page_id):
    for attempt in range(4):
        try:
            r = s.get(BASE.format(page_id), timeout=25)
            return r.content.decode('gbk', 'ignore')
        except Exception as e:
            time.sleep(2 + attempt * 2)
    raise RuntimeError(f'fetch fail {page_id}')

def page_text(h):
    m = re.search(r'<div[^>]*id="chaptercontent"[^>]*>(.*?)</div>', h, re.S)
    if not m:
        return '', None, None
    body = re.sub(r'<br\s*/?>', '\n', m.group(1))
    body = re.sub(r'<[^>]+>', '', body)
    body = re.sub(r'\u3000|[\u00a0 ]{2,}', '', body)
    # 去掉站点水印行
    body = re.sub(r'记住手机版网址[^\n]*|mchaptererror\(\);|第\(\d+/\d+\)页|\(本章未完,请翻页\)', '', body)
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    nxt = re.search(r'<a[^>]*href="/11/11428/(\d+)(?:_(\d+))?\.html"[^>]*id="pb_next"', h) or \
          re.search(r'<a[^>]*id="pb_next"[^>]*href="/11/11428/(\d+)(?:_(\d+))?\.html"', h)
    title = re.search(r"lastread\.set\('11428','\d+','[^']*','([^']*)'", h)
    return body, (nxt.group(1), nxt.group(2)) if nxt else None, title.group(1) if title else ''

start_id = '11111102'   # 第一章 掌门张莫
MAX_CH = int(sys.argv[1]) if len(sys.argv) > 1 else 40

cur = start_id
for n in range(1, MAX_CH + 1):
    fp = f'{OUT}/{n:03d}.txt'
    if os.path.exists(fp) and os.path.getsize(fp) > 2000:
        # 已有文件，需要推进cur到下一章——简化：跳过爬链（首次运行不适用）
        print(f'{n:3d} cached, stop-chain', flush=True)
        break
    full = []
    ch_title = ''
    page = cur
    base_id = cur
    for p in range(1, 8):
        h = get(page)
        txt, nxt, t = page_text(h)
        if t and (not ch_title):
            ch_title = t
        full.append(txt)
        if not nxt:
            break
        nid, sub = nxt
        if sub is None or nid != base_id:
            cur = nid
            break
        page = f'{nid}_{sub}'
        time.sleep(0.5)
    text = f'{ch_title}\n\n' + '\n\n'.join(x for x in full if x)
    open(fp, 'w', encoding='utf-8').write(text)
    print(f'{n:3d} {len(text):6d}  {ch_title[:36]}  next={cur}', flush=True)
    time.sleep(0.9)
print('done')
