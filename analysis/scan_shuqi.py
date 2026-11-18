import re

h = open('C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/shuqi_ch1.html',
         encoding='utf-8', errors='ignore').read()

# 搜索章节正文特征
for kw in ['掌门张莫', '八辈贫农', '拉了壮丁', '"content"', 'chapterContent', 'api.shuqi', 'getJSON', 'ajax']:
    idxs = [m.start() for m in re.finditer(re.escape(kw), h)][:3]
    print(kw, '->', idxs)

# 抽取所有接口URL
urls = sorted(set(re.findall(r'https?://[^"\'<> ]*shuqi[^"\'<> ]*', h)))
for u in urls[:15]:
    print('URL:', u[:130])
