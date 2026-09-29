import requests, os

os.makedirs('tang_json', exist_ok=True)
base = 'https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%85%A8%E5%94%90%E8%AF%97/poet.tang.{}.json'

# 全唐诗分片是 poet.tang.0.json 到 poet.tang.57000.json，步长1000
for i in range(0, 58000, 1000):
    url = base.format(i)
    r = requests.get(url, timeout=30)
    if r.status_code == 200:
        with open(f'tang_json/poet.tang.{i}.json', 'w', encoding='utf-8') as f:
            f.write(r.text)
        print(f'poet.tang.{i}.json  OK')
    else:
        print(f'poet.tang.{i}.json  不存在(码{r.status_code})，跳过')