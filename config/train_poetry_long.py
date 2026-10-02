# Run 6: training-amount experiment — 4x longer training on the Tang+Song corpus
# Hypothesis: model is under-trained (Chinchilla: ~20 tokens/param = 320M tokens;
# Run 4/5 only saw 82M). Same architecture as Run 4 baseline (depth didn't help).

out_dir = 'out-poetry-long'
eval_interval = 1000 # less frequent eval: each eval costs ~200 forward passes
eval_iters = 100
log_interval = 50

# still only save when val improves
always_save_checkpoint = False

wandb_log = False # override via command line if you like
wandb_project = 'chinese'
wandb_run_name = 'mini-gpt'

dataset = 'poetry'
gradient_accumulation_steps = 1
batch_size = 64
block_size = 256 # context of up to 256 previous characters

# same baseline architecture as Run 4 (n_layer=6, depth experiment showed nothing)
n_layer = 6
n_head = 6
n_embd = 384
dropout = 0.2

learning_rate = 1e-3
max_iters = 20000
lr_decay_iters = 20000 # make equal to max_iters usually
min_lr = 1e-4 # learning_rate / 10 usually
beta2 = 0.99 # make a bit bigger because number of tokens per iter is small

warmup_iters = 100 # not super necessary potentially
