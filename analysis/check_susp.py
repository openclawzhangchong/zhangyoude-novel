import json, re, glob

BASE = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source'
mapping = json.load(open(f'{BASE}/font_mapping.json', encoding='utf-8'))
orig = '\n'.join(open(f, encoding='utf-8').read() for f in sorted(glob.glob(f'{BASE}/fq/第0*.txt')))
susp = {k: v for k, v in mapping.items() if re.fullmatch(r'[a-zA-Z0-9]+', v) or len(v) > 2}

for k, v in susp.items():
    cnt = orig.count(k)
    if cnt:
        i = orig.find(k)
        ctx = orig[max(0, i - 20):i + 20]
        print(f'U+{ord(k):04X} -> {v!r}  ({cnt}x)')
        print('   ctx:', repr(ctx))
