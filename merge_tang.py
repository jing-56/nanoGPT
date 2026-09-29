import json, glob, os

src_dir  = r'C:\Users\96244\PycharmProjects\NanoGPT\nanoGPT\tang_json'   # ← 绝对路径
out_path = r'C:\Users\96244\PycharmProjects\NanoGPT\nanoGPT\data\chinese\input.txt'

files = glob.glob(os.path.join(src_dir, 'poet.tang.*.json'))
assert len(files) > 0, f'在 {src_dir} 没找到任何 JSON！实际文件数：{len(files)}'  # fail fast

poems = []
for fp in sorted(files):
    with open(fp, 'r', encoding='utf-8') as f:
        for item in json.load(f):
            if item['paragraphs']:
                poems.append('\n'.join(item['paragraphs']))

text = '\n\n'.join(poems)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'共 {len(poems)} 首诗，{len(text):,} 字符，已写入 {out_path}')