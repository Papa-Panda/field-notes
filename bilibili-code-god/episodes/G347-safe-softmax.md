# G347 — Safe Softmax：一行 exp(100) 让模型崩溃，FlashAttention 的数学基石
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G347-safe-softmax.html

## 元信息
- 编号：G347
- 标题：Safe Softmax：一行 exp(100) 让模型崩溃，FlashAttention 的数学基石
- BV：BV1bigR6YEpq
- 时长：04:14
- 发布日期：2026-07-30
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：FlashAttention（online softmax）、log-sum-exp trick

## 一句话总结
朴素 softmax 在 logit 超过约 88 时指数溢出成 inf，safe softmax 靠"先减最大值再取指数"这一恒等变换把它压回安全区间，FlashAttention 的 online softmax 正是它的分块升级版。

## 核心
1. 问题/背景：softmax 要对每个 logit 算指数再归一化，但指数函数涨得太快： $e^{50}$ 已是 10 的 21 次方量级， $e^{89}$ 约 $4.5 \times 10^{38}$ ，逼近 float32 上限（约 $3.4 \times 10^{38}$ ），再大就溢出为 inf。而注意力里 QK 点积产生的 logits 动辄五六十、上百，朴素实现必然踩雷，loss 直接变 NaN。
2. 机制/方法：取指数前先减去全体最大值 $m$ 。分子分母同乘 $e^{-m}$ 后形式与原式完全等价，但减完后所有指数自变量都 ≤ 0 ，指数值被压进 $(0, 1]$ ，不可能溢出。举例 $x = (1, 100, -50)$ ：朴素算 $e^{100}$ 直接爆掉；减去 max 100 后变成 $e^{-99}$ 、 $e^{0}$ 、 $e^{-150}$ ，结果干净利落。
3. 关键证据或数字：溢出阈值约在 logit ≈ 88–89（float32）；FlashAttention 的 online softmax 进一步处理分块场景——逐块维护 running max，新块出现更大 max 时，把已累积的分子分母乘上修正因子 $e^{m_{old} - m_{new}}$ 再并入新块，全程不存完整注意力矩阵、数值始终稳定。
4. 结论/判断：同一思想还出现在 log-sum-exp trick 里（先减 max 再算 log），PPO 的 log-prob、InfoNCE、贝叶斯边缘似然都靠它续命；工程上宁可用这个零成本技巧，也不升 float64（速度掉一半）。

## 关键数字
| 量 | 值 |
| --- | --- |
| float32 可表示上限 | 约 $3.4 \times 10^{38}$ |
| 指数溢出阈值 | logit 约 > 88 |
| 升 float64 的代价 | 速度约掉一半 |

## 可迁移
- 面试高频：能把 safe softmax → online softmax → FlashAttention 省显存串成一条线讲，是理解现代注意力实现的基本功。
- 排障直觉：训练出现 inf/NaN 时，先怀疑未做 max 减法的 exp/log 运算，而不是先换精度。

## 疑问 / 下一步
- online softmax 的 running sum 修正细节与 FlashAttention 的 tiling 如何配合，可结合论文再推导一遍。
