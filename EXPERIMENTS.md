# 实验记录 · nanoGPT 个人学习改造

> 本仓库 fork 自 karpathy/nanoGPT，用于个人学习 Transformer 的完整训练闭环。
> 每个 Run 记录：数据、配置、结果、预测 vs 实际、踩坑与观察。

## Run 1: 莎士比亚字符级模型（默认配置）

- **硬件**: RTX 3050（笔记本），torch 2.8.0+cu126，Windows 11
- **数据**: tiny_shakespeare，111.5 万字符，词表 65（字符级）
- **配置**: `config/train_shakespeare_char.py`（10.65M 参数，6 层 6 头，block_size 256）
- **训练**: 5000 iters，batch 64，loss 起点 4.28（≈ ln 65 随机基线 ✅）
- **结果**: best val loss **1.4687**（perplexity ≈ 4.4）
- **生成样例**: 莎士比亚剧本风格，角色名/台词格式完整，有生造词。节选：

> KING RICHARD II:
> Shall I, be made to bear the army take
> Be gall'd by this foul common back:
- **踩坑**: ① torch 装成 CPU 版 → 重装 cu126 版；② Windows 无 Triton，torch.compile 不可用 → `--compile=False`；③ nanoGPT 默认 `device='cuda'` 写死，CPU 需命令行覆盖
- **对应笔记**: `model.py` 内中文注释（逐行精读）

## Run 2: 全唐诗字符级模型（中文语料改造）

- **数据**: 繁体《全唐诗》**57,603 首 / 3,993,966 字符**
  - 来源: chinese-poetry/chinese-poetry（poet.tang.*.json 分片）
  - 管线: `download_tang.py`（requests 拉取 58 个分片）→ `merge_tang.py`（提取 paragraphs，诗间空行分隔）→ `data/chinese/prepare.py`（字符级编码，UTF-8）
- **词表**: **9,589**（vs Run 1 的 65）→ 模型 **11.9M** 参数（embedding 表占 123 万）
- **配置**: `config/train_chinese.py`，与 Run 1 严格对齐（控制变量）
- **结果**: final train loss **3.2122** / val loss **3.8848**（perplexity 25 / 48）

### 预测 vs 实际（理论是排错工具）

| 预测 | 实际 | 结论 |
|---|---|---|
| 随机基线 ln(9589) ≈ **9.17** | step 0 loss ≈ 9.2 | ✅ 符合 |
| 最终 loss 高于 Run 1 的 1.0 | 3.88 | ✅ 词表大 147 倍 + 诗歌更凝练 |

### 关键排错记录

首跑 step 0 loss = 4.28（≈ ln 72），与理论基线 9.17 严重不符 →
判定模型仍在用莎士比亚词表 → 定位 `config/train_chinese.py` 的 `dataset` 未生效。
**程序正常运行 ≠ 在做你以为的事；ln(V) 基线可当哨兵。**

### 生成 vs 背诵（亲手复现"LLM 记忆争议"）

模型生成：
> 蕭颯復蕭蕭，繁陰生野橋。但將一杯酒，不覺五弦銷。

- "蕭颯復蕭蕭"：语料中 **0 次** → 模型自创
- "五弦銷"：语料中 1 次（原句"堂上五弦銷暇日"）→ **短语级记忆，跨句重组**

结论：小模型同样呈现"统计规律学习 + 片段记忆"的混合行为。

### 观察与遗留问题

- train-val gap = 0.67 → **有过拟合倾向**（词表大、数据被翻多遍）→ Run 3 方向：调大 dropout / 减步数 / 加《全宋诗》
- iter 5000 单步耗时 28s（含最终评估+存 ckpt），常规 iter 耗时待从日志确认
- 待验证：生诗格式（五言断句、平仄节奏）学习程度

## 后续计划

- [ ] Run 3: 针对过拟合的正则化实验（dropout 0.2 → 0.35）
- [ ] train.py 训练循环精读
- [ ] 位置编码升级 RoPE（对应课程第 1 级改造）
