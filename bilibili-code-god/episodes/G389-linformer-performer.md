# G389 — Linformer & Performer：低秩投影、核化+结合律，O(n²) 降到 O(n)

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G389-linformer-performer.html

## 元信息

- 编号：G389
- 标题：Linformer & Performer：低秩投影、核化+结合律，O(n²) 降到 O(n)
- BV：BV1GJKW6uEEH
- 时长：03:21
- 发布日期：2026-07-21
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Linformer（Wang et al., 2020）；Performer / FAVOR+（Choromanska et al., 2021）

## 一句话总结

自注意力的平方复杂度来自 $n \times n$ 注意力矩阵，两条经典路线把它压回线性：Linformer 利用注意力近似低秩、把 K/V 沿序列投影成少数代表；Performer 用随机特征核化拆开 softmax，再靠矩阵乘法结合律先算小矩阵、全程绕开 $n \times n$ 。

## 核心

1. **问题/背景**：每个 token 都要和全部 token 打一遍分，序列长 $n$ 就有 $n^2$ 个格子：1000 个词是 100 万格，1 万个词飙到 1 亿，计算量与显存都被这张表拖死。想提速，唯一的出路是干掉 $n \times n$ 。
2. **机制/方法**：Linformer 走「压缩」——实证发现注意力矩阵近似低秩，大表的信息用少数几行就能概括，于是算注意力前先把 K、V 沿序列方向投影成 $k$ 个代表（ $k$ 为远小于 $n$ 的常数，如 256），注意力表从 $n \times n$ 变成 $n \times k$ 的瘦长条，复杂度随之线性。Performer 走「换序」——softmax 把 Q、K 锁死在 $n \times n$ 里拆不开，就用随机特征映射把核函数拆成只依赖 Q 的部分与只依赖 K 的部分；拆开后利用结合律把括号右移，先算 K 侧特征与 V 的乘积（尺寸与序列长度无关的小矩阵），再左乘 Q 侧，全程不 materialize $n \times n$ 。
3. **关键证据或数字**：两条路线结果一致——陡峭的平方曲线被压成平缓直线，且序列越长省得越狠；一个改的是数据形状（低秩投影），一个改的是计算次序（核化 + 结合律）。
4. **结论/判断**：理解线性注意力的钥匙就是这两把：要么承认注意力信息冗余去压缩，要么换掉 softmax 的耦合形式去重排计算。后续 FlashAttention 等工作不改数学、只改访存，是另一条正交路线。

## 关键数字

| 方法 | 关键动作 | 复杂度 |
|---|---|---|
| 标准自注意力 | 完整 $n \times n$ 打分表 | $O(n^2)$ |
| Linformer | K/V 投影到 $k$ 个代表（例 $k = 256$ ） | $O(n \cdot k)$ ，即线性 |
| Performer | 随机特征核化 + 结合律先算小矩阵 | $O(n)$ |

## 可迁移

- 面试聊长上下文优化时能把方法分家：稀疏/低秩/核化改的是数学结构，FlashAttention 改的是 IO 与访存，两类常被混为一谈。
- 做 RL infra 里长轨迹 rollout 的成本估算时，先判断瓶颈在 $n^2$ 计算还是 KV 显存，选的优化完全不同。

## 疑问 / 下一步

- 低秩假设在多头、短序列或强局部依赖任务上会不会失效？Linformer 的投影维度该如何随任务选取？
