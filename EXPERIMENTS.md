# nanoGPT 实验记录

本仓库基于 karpathy/nanoGPT，记录个人学习 Transformer 的训练实验。

## Run 1: 莎士比亚字符级模型（默认配置）

- **硬件**: RTX 3050（笔记本），torch 2.8.0+cu126，Windows 11
- **配置**: `config/train_shakespeare_char.py`（10.65M 参数，6 层 6 头，block_size 256）
- **训练**: 5000 iters，batch 64，约 XX 分钟
- **结果**:
  - train loss: X.XXX
  - val loss: X.XXX
  - 随机基线 loss = ln(65) ≈ 4.17
- **生成样例**（python sample.py --out_dir=out-shakespeare-char）:

&gt; KING RICHARD II:
&gt; Shall I, be made to bear the army take
&gt; Be gall'd by this foul common back:
&gt; （How cheer there, resolve now, my lord, for that I am here in
the regal of this interior servant, But if
I think not so satisfied to the trick. Should you promise
the prince, the heart of your breath, I say your own
will say your brother's elder wills prove him like offence.
)

- **观察**: （写两三句你自己的话，比如"角色名格式完全学会了""有生造词但语法结构成型"）
- **踩过的坑**: torch 装成 CPU 版、Windows 上 torch.compile 缺 Triton → --compile=False

## 后续计划

- [ ] 精读 model.py，输出中文逐行注释笔记
- [ ] 换中文语料训练
- [ ] 超参数对比实验
- [ ] 位置编码升级为 RoPE