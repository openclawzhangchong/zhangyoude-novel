import re, json

SRC = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/xxsy.html'
OUT = 'C:/Users/Administrator/.zcode/workspace/draft-c2ec0543-d287-42b3-bc1e-4d7dafa7f258/source/qidian_chapter_index.json'

h = open(SRC, encoding='utf-8', errors='ignore').read()
items = re.findall(
    r'<a href="(https://www\.qidian\.com/chapter/[^"]+)"[^>]*title="首发时间：[^"]*章节字数：(\d+)"[^>]*>([^<]+)</a>',
    h)
print('total chapters found:', len(items))
chapters = []
for url, words, title in items:
    bid, cid = re.search(r'chapter/(\d+)/(\d+)/', url).groups()
    chapters.append({'no': len(chapters) + 1, 'title': title.strip(),
                     'words': int(words), 'bookId': bid, 'chapterId': cid})
json.dump(chapters, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
total_w = sum(c['words'] for c in chapters)
print(f'words total ~{total_w/10000:.0f}万, avg {total_w/max(1,len(chapters)):.0f}字/章')
for c in chapters[:5] + chapters[-3:]:
    print(c['no'], c['title'], c['words'])
