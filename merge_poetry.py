"""Merge Tang (tang_json/) and Song (song_json/) poetry shards into one corpus.

Key design decision: poems are SHUFFLED (fixed seed) before writing, so that
prepare.py's sequential 90/10 split yields train/val sets with the SAME
distribution (mixed Tang+Song). Without shuffling, the val set would be
100% Song poetry - a distribution shift that would confound experiments.
"""
import json, glob, os, random

src_dirs = ['tang_json', 'song_json']
out_path = 'data/poetry/input.txt'

poems = []
for d in src_dirs:
    files = glob.glob(os.path.join(d, 'poet.*.json'))
    assert len(files) > 0, f'在 {d} 里没找到任何分片！'
    for fp in sorted(files):
        with open(fp, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                if item['paragraphs']:
                    poems.append('\n'.join(item['paragraphs']))
    print(f'{d}: 累计 {len(poems)} 首')

random.seed(42)                 # 固定种子，保证可复现
random.shuffle(poems)           # 打乱唐/宋顺序，消除切分的分布偏移

text = '\n\n'.join(poems)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'\n共 {len(poems)} 首诗，{len(text):,} 字符，已写入 {out_path}')
print('（唐+宋已随机混合，prepare.py 顺序切分即可得到同分布的 train/val）')
