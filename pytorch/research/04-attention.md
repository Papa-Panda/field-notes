# Research 04 — 注意力机制手写（SDPA、多头、KV cache）

- **定位**：Research PyTorch 轮次的模型结构面。注意力是唯一一个"面试官敢让你在白板/编辑器里从零写"的组件 —— 能写出来、能和官方实现对齐数值，才算过关。
- **配套 notebook**：[04-attention.ipynb](04-attention.ipynb)（Colab 可直接跑，CPU 即可）

## 一句话总结

注意力 = 三次线性投影 + 一次缩放点积 + softmax 加权和。多头是把 $ d_{model} $ 切成 $ h $ 份各做一遍再拼回来。难点全在维度 shuffle 和 mask 位置。

## 核心（动机 + 机制）

**缩放点积注意力**。$ Q = XW_Q $ 、 $ K = XW_K $ 、 $ V = XW_V $ ，则：

$$ \mathrm{Attn}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right) V $$

为什么除 $ \sqrt{d_k} $ ：$ Q, K $ 各维独立同分布时，点积的方差随 $ d_k $ 线性增长，不缩放则 softmax 饱和到 one-hot、梯度消失。这是面试最爱问的"为什么"。

**causal mask**：自回归要求位置 $ t $ 只能看 $ \le t $ 的位置。实现上把 mask 加在 **softmax 之前**的分数上（未来位置置 $ -\infty $ ），不是在权重上乘 0 —— 乘 0 再 renormalize 是数学等价但数值不同的另一种写法，面试给代码找 bug 时专门设这个套。

**多头**：$ \mathrm{head}_i = \mathrm{Attn}(QW^Q_i, KW^K_i, VW^V_i) $ ，输出 $ \mathrm{Concat}(\mathrm{head}_1, ..., \mathrm{head}_h) W^O $ 。实现要点：$ d_{model} $ 必须能被 $ h $ 整除、投影是一个大矩阵做完再切分（不是 $ h $ 个小矩阵，工程实现如此，数学等价）、切分时维度顺序是 (batch, heads, seq, head_dim) 不能错。

**KV cache**：推理时每步只新算一个 token 的 Q，历史的 K、V 缓存复用。复杂度从每步重算 $ O(T^2) $ 降到 $ O(T) $ ；代价是显存随 $ T $ 线性涨（长上下文推理的显存瓶颈就在这）。

**FlashAttention**（概念面）：分块（tiling）+ online softmax（用 running max/sum 增量修正），避免把 $ T \times T $ 注意力矩阵落盘到 HBM。数学结果与普通 attention 严格等价，快在 IO 不是 FLOPs。

## 面试考点

1. 为什么除 $ \sqrt{d_k} $ 不除 $ d_k $ （方差论证）
2. multi-head 实现：一个大投影矩阵切分 vs 多个小矩阵，参数量相同但计算图不同
3. mask 加在 softmax 前后等价吗（数值稳定性上：$ -\infty $ vs 大负数 $-10^9$ 的区别）
4. KV cache 的显存公式：$ 2 \times \text{层数} \times T \times d_{model} \times \text{bytes} $
5. 训练时用 causal attention 和推理时 KV cache 的关系（数学等价，实现两条路）

## 常见 bug 清单

- mask 在 softmax **之后**乘到权重上还不 renormalize → 未来信息泄漏，loss 好得不真实
- 维度转置错：(batch, seq, heads, head_dim) 和 (batch, heads, seq, head_dim) 搞混 → 能跑但结果全错（shape 不报错是最阴险的）
- 缩放因子用了 $ \sqrt{d_{model}} $ 而不是每个 head 的 $ \sqrt{d_k} $
- RoPE 的位置在 Q、K 投影后、attention 前 —— 顺序写错很常见（进阶题）

## 思考题

1. batch 里不同长度序列做 padding 时，attention mask 和 causal mask 怎么合并？
2. 为什么推理时 Q 只有一个 token 时，attention 的 softmax 还需要 causal mask 吗？
3. FlashAttention 的 online softmax 中，running max 的作用是什么？省掉它会怎样？

---
*上一篇：Research 03 — PPO/GRPO loss · 本系列完（Research 04/04）*
