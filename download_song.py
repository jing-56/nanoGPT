import requests, os, time

os.makedirs('song_json', exist_ok=True)
base = 'https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%85%A8%E5%94%90%E8%AF%97/poet.song.{}.json'
# 注意: URL路径仍是 全唐诗 目录? —— 不是! 全宋诗在 json 目录, 见下方说明

ok, fail = 0, []
for i in range(0, 255000, 1000):
    fp = f'song_json/poet.song.{i}.json'
    if os.path.exists(fp) and os.path.getsize(fp) > 0:
        ok += 1                      # 已下载，跳过（断点续传）
        continue
    url = base.format(i)
    for attempt in range(3):         # 最多重试 3 次
        try:
            r = requests.get(url, timeout=60)
            if r.status_code == 200:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(r.text)
                ok += 1
                print(f'poet.song.{i}.json  OK ({ok}/255)')
                break
        except requests.RequestException:
            print(f'poet.song.{i}.json  第{attempt+1}次失败，重试...')
            time.sleep(2)
    else:
        fail.append(i)

print(f'\n成功 {ok}/255，失败 {len(fail)}: {fail[:10]}')
assert len(fail) == 0, '有分片没下成功，重跑一次本脚本即可（会自动续传）'