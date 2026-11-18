import json, re, glob

MAP = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/font_mapping.json'
SRC_DIR = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/fq'
OUT_DIR = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/decoded'
import os
os.makedirs(OUT_DIR, exist_ok=True)

mapping = json.load(open(MAP, encoding='utf-8'))
# 可疑映射：OCR结果为单字母/数字/多字异常
suspicious = {k: v for k, v in mapping.items() if re.fullmatch(r'[a-zA-Z0-9]+', v) or len(v) > 2}
print('suspicious mappings:', len(suspicious))
for k, v in list(suspicious.items())[:20]:
    print(f'  U+{ord(k):04X} -> {v!r}')

n = 0
for fp in sorted(glob.glob(f'{SRC_DIR}/第0*.txt')):
    txt = open(fp, encoding='utf-8').read()
    for k, v in mapping.items():
        txt = txt.replace(k, v)
    open(f'{OUT_DIR}/{os.path.basename(fp)}', 'w', encoding='utf-8').write(txt)
    n += 1
print('decoded files:', n)
