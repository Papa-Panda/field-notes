# Parallel 05 — ZeRO / FSDP：把显存墙按 $ N $ 切开

- **定位**：并行基础线第二篇。DDP 解决了梯度同步的效率，但每个 rank 还存着全量参数 + 全量优化器状态 —— 显存墙原样还在。ZeRO 的回答是：副本可以复制，状态不必复制。
- **配套 notebook**：[05-zero-fsdp.ipynb](05-zero-fsdp.ipynb)（Colab 可直接跑）

## 一句话总结

ZeRO 把 DDP 里每份副本重复存的东西（优化器状态 → 梯度 → 参数）依次按 rank 切片，每切一级省一截显存、多付一点通信；FSDP 是 ZeRO-3 的 PyTorch 原生实现。

## 核心（动机 + 机制）

**先算总账**（混合精度 + Adam，每参数）：参数 bf16 2B + 梯度 bf16 2B + fp32 主参数 4B + 动量 4B + 方差 4B = **16B/参数**。70B 模型是 1.1TB，DDP 下每个 rank 都要存满这 1.1TB —— 复制计算可以，复制存储是浪费：$ N $ 个 rank 里有 $ N $ 份一模一样的优化器状态，而每份只有 1/N 真正被更新逻辑需要。

**三级分片**（$ \Psi $ = 参数量，$ N $ = rank 数）：

| 阶段 | 切什么 | 每 rank 显存 | 通信（vs DDP 的 $ 2\Psi $ ) |
|---|---|---|---|
| DDP | 不切 | $ 16\Psi $ | $ 2\Psi $ （梯度 all-reduce） |
| ZeRO-1 | 优化器状态（12B 那部分） | $ 4\Psi + 12\Psi/N $ | $ 2\Psi $ （不变） |
| ZeRO-2 | + 梯度 | $ 2\Psi + 14\Psi/N $ | $ 2\Psi $ （不变） |
| ZeRO-3 | + 参数 | $ 16\Psi/N $ | $ 3\Psi $ （1.5 倍） |

**为什么 ZeRO-1/2 不加通信、ZeRO-3 要加**：优化器状态本来就不参与通信，切它免费；梯度把 all-reduce 换成 reduce-scatter（每人只收自己那片的规约结果），通信量不变。参数一切片， forward/backward 用到某层参数时必须先 all-gather 把它拼回来 —— 前向拼一次、反向再拼一次、梯度 reduce-scatter 一次，共 $ 3\Psi $ 。多付的 50% 通信就是 ZeRO-3 拿显存换带宽的交易条款。

**FSDP 的实现要点**：把一个模块的参数 flatten 成一维 `FlatParameter` 再切片；前向计算前 all-gather 拼回、算完释放（reshard）；反向同理。工程旋钮：prefetch（提前拼下一层，和计算重叠）、backward prefetch、混合精度策略（计算 bf16、规约 fp32）、`summon_full_params`（保存 checkpoint / 评估时临时拼全量）。

## 面试考点

1. 16B/参数的构成，脱口而出；ZeRO 三级各切哪部分、显存公式怎么写
2. ZeRO-3 为什么是 1.5 倍通信（前向 AG + 反向 AG + 梯度 RS = $ 3\Psi $ )
3. ZeRO-1 在小模型上几乎免费，为什么生产里还是常直接用 ZeRO-3/FSDP（显存压力通常来自总账而不是某一项）
4. FSDP 与 gradient checkpointing 的关系（都拿计算/通信换显存，组合使用时注意 all-gather 的重复触发）
5. FSDP 什么时候反而更慢：模型小、通信延迟主导时，all-gather 的粒度太碎

## 常见 bug 清单

- 保存模型时直接 `state_dict()` 拿到的是分片参数 → 必须 `summon_full_params` 或用 FSDP 的 state dict 模式拼全量再存
- FSDP 里混用 `find_unused_parameters` 的 DDP 思维（FSDP 的处理方式不同，多余参数会 hang）
- wrap 粒度太粗（一整个大模型一个 FlatParameter）→ all-gather 一次拼太多、峰值显存爆炸；粒度太细 → 通信次数爆炸
- 在 FSDP 模块外面对分片参数做手动 `.data` 操作 → 形状对不上，报错还难定位

## 思考题

1. $ N=8 $ 、70B 模型，ZeRO-2 每 rank 显存多少 GB？ZeRO-3 呢？（按表里的公式算）
2. 为什么梯度用 reduce-scatter 而不是 all-reduce 之后 ZeRO-2 的通信不变？差在哪一步省回来了？
3. FSDP 的 prefetch 为什么能藏通信？它和 DDP 的通信/计算重叠是同一种机制吗？

---
*上一篇：Day 01 — 集合通信与 DDP · 下一篇：Parallel 06 — TP 手写 linear*
