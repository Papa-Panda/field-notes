# field-notes

Personal notes and working drafts.

## pytorch/research — Research PyTorch 系列（2026-10-02，4/4 完）

训练代码手感线：手写 + debug。每篇含 MD 笔记（公式与考点）+ Colab 可跑的 notebook（全部代码已实测）。

- [01 — 训练循环零起](pytorch/research/01-training-loop.md) · [notebook](pytorch/research/01-training-loop.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Papa-Panda/field-notes/blob/main/pytorch/research/01-training-loop.ipynb) — 五步循环、grad accumulation 等价性、三个经典 bug
- [02 — DPO loss 手写 + debug](pytorch/research/02-dpo-loss.md) · [notebook](pytorch/research/02-dpo-loss.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Papa-Panda/field-notes/blob/main/pytorch/research/02-dpo-loss.ipynb) — log-prob 命门（shift/mask/sum）、toy LM 实训、三个 bug 指纹
- [03 — PPO/GRPO loss](pytorch/research/03-ppo-grpo-loss.md) · [notebook](pytorch/research/03-ppo-grpo-loss.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Papa-Panda/field-notes/blob/main/pytorch/research/03-ppo-grpo-loss.ipynb) — clip 语义、GAE、组内 advantage、KL 三估计器
- [04 — 注意力机制手写](pytorch/research/04-attention.md) · [notebook](pytorch/research/04-attention.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Papa-Panda/field-notes/blob/main/pytorch/research/04-attention.ipynb) — SDPA/多头与官方实现对拍、KV cache 等价验证

## pytorch — 分布式 / 并行线

- [Day 01 — 集合通信与 DDP](pytorch/day-01-distributed-ddp.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Papa-Panda/field-notes/blob/main/pytorch/day-01-distributed-ddp.ipynb) — ring all-reduce 公式、gradient bucketing、2 进程 DDP 最小闭环、`day-01-ddp-minimal.py`（torchrun 版）
