# Parallel 06 — TP 手写 linear：把一层网络横着切开

- **定位**：并行基础线第三篇，也是 RL track 电话里点名的实现题（TP implementation）。DDP/ZeRO 切的是数据和存储，这一刀切的是**单层计算本身**。
- **配套 notebook**：[06-tensor-parallel.ipynb](06-tensor-parallel.ipynb)（Colab 可直接跑）

## 一句话总结

Megatron 的 TP 就两个动作：第一层按列切（各算一半输出）、第二层按行切（各算一半输入再 all-reduce 求和）—— 这样一个 MLP 只通信一次。手写一遍，与单卡实现数值对齐，才算真懂。

## 核心（动机 + 机制）

**动机**：当一层的权重矩阵大到单卡装不下（或一层的矩阵乘慢到成为瓶颈），数据并行无能为力 —— 每个 rank 都要算完整的这一层。必须把层内的矩阵乘本身拆到多卡。

**两种切法**（$ Y = XW $ ，$ W $ 是 $ (d_{in}, d_{out}) $ ）：

| 切法 | 怎么切 | 前向通信 | 反向通信 |
|---|---|---|---|
| Column-parallel | $ W $ 按列切：$ W = [W_1 \| W_2] $ ，每 rank 持一列块 | 无需（或出口 all-gather 拼输出） | 输入梯度要 all-reduce |
| Row-parallel | $ W $ 按行切：输入 $ X $ 也按特征维切开 | 出口 all-reduce 求和 | 无需 |

**为什么 MLP 只通信一次**：第一层 column-parallel 输出的是"半截特征"（每 rank 只有一半 hidden 维），非线性（GELU）是逐元素的，半截也能各算各的；第二层正好按行切，吃半截特征、产出部分和，最后 all-reduce 一次求和得到完整输出。整个 MLP 前向 1 次 all-reduce（反向再 1 次），激活全程不落地同步 —— 这是 Megatron 设计的核心手感：**通信点选在非线性之后、求和之处**。

**两个算子 f/g**（Megatron 论文的记法）：f = 前向恒等、反向 all-reduce；g = 前向 all-reduce、反向恒等。column-parallel 的输入端挂 f，row-parallel 的输出端挂 g。用 `torch.autograd.Function` 手写这两个算子，就是这道面试题的全部骨架。

**注意力同理**：QKV 投影按列切（天然按 head 分片），输出投影按行切 —— 每个 attention block 同样只在出口通信一次。

## 面试考点

1. column 与 row 切法的通信位置（前向哪步、反向哪步），能对着 $ Y=XW $ 现场推
2. 为什么 GELU 放在两层之间不增加通信（逐元素、不跨维）
3. f/g 算子的反向定义 —— 给代码让你补 backward 是常见形式
4. TP 放节点内、DP 放节点间的原因（TP 通信频繁且延迟敏感，吃 NVLink；DP 每步一次，吃 IB）

## 常见 bug 清单

- row-parallel 忘了出口 all-reduce → 每 rank 只有部分和，输出量级大约小 $ N $ 倍，loss 能降但不对
- column-parallel 的 bias 也跟着切了两份、求和时被加两遍（bias 应该只在 row-parallel 的出口加一次）
- 反向把 f 和 g 写反 → 前向数值全对、梯度全错（前向对拍发现不了，必须连梯度一起对拍）
- 切分维度与权重初始化不一致（每 rank 用不同种子初始化自己那片，拼起来不是同一个 $ W $ ）

> 可跑现场版在同名 notebook 第 4 节「Debug 演练」：BUG 1 row 出口忘 all-reduce / BUG 2 f 的 backward 漏规约 / BUG 3 bias 加两遍，每个 bug 下面带修复。

## 思考题

1. 如果 MLP 中间不用 GELU 而用需要跨维归一化的 LayerNorm，两层之间还能不通信吗？
2. column-parallel 切完之后，每 rank 的计算量是原来的 $ 1/N $ ，通信量呢？和 $ d_{in}, d_{out} $ 什么关系？
3. 为什么 attention 的 QKV 适合 column-parallel，而输出投影适合 row-parallel？

---
*上一篇：Parallel 05 — ZeRO/FSDP · 下一篇：RL Systems 07 — rollout→train 系统骨架*
