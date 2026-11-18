import re

h = open('C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/xxsy.html',
         encoding='utf-8', errors='ignore').read()

patterns = [
    r'https?://[^"\'<> ]+\.(?:txt|zip|rar|epub)',
    r'https?://[^"\'<> ]*api[^"\'<> ]*',
    r'"(?:downloadUrl|down_url|txt_url|file_url|bookUrl)"\s*:\s*"[^"]+"',
    r'window\.__NUXT__|__NEXT_DATA__|__INITIAL_STATE__',
    r'href="[^"]*(?:down|txt|dl)[^"]*"',
]
for p in patterns:
    ms = sorted(set(re.findall(p, h)))
    if ms:
        print(f'--- {p[:40]} ({len(ms)})')
        for m in ms[:8]:
            print('   ', m[:150])
