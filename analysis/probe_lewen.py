import re, time, requests

BASE = 'https://m.lewennwx.cc/11/11428/{}.html'
HEAD = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Referer': 'https://m.lewennwx.cc/11/11428/',
}

def probe(item_id):
    r = requests.get(BASE.format(item_id), headers=HEAD, timeout=20)
    h = r.content.decode('gbk', 'ignore')
    m = re.search(r"lastread\.set\('11428','(\d+)','[^']*','([^']*)'", h)
    if m:
        return m.group(1), m.group(2)
    m2 = re.search(r'<h1[^>]*>([^<]+)</h1>', h)
    return item_id, (m2.group(1) if m2 else 'MISS')

for i in [11109849, 11109850, 11109860, 11109900, 11109500, 11109200, 11108800, 11108600, 11108500, 11108400, 11108300, 11108100, 11108000]:
    try:
        print(i, '->', probe(i), flush=True)
    except Exception as e:
        print(i, 'ERR', e)
    time.sleep(0.6)
