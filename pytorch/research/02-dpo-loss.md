# Research 02 — DPO loss 手写 + Debug

- **定位**：Research PyTorch 轮次的正主。电话里点名的实操形式就是 *real DPO debugging* —— 给你一段能跑但训不动的 DPO 代码，现场定位。
- **配套 notebook**：[02-dpo-loss.ipynb](02-dpo-loss.ipynb)（Colab 可直接跑，CPU 即可）

## 一句话总结

DPO 把 RLHF 的最优策略闭式解代回 Bradley-Terry 模型，得到一个只依赖 policy 与 ref 的 log-prob 差的二分类 loss。面试考的就是这个代入过程你熟不熟、log-prob 算得对不对。

## 核心（动机 + 机制）

**从 RLHF 到 DPO 的一步代入**。RLHF 先训 reward model $ r(x, y) $ ，再在 KL 约束下最大化 reward，最优策略有闭式解：

$$ \pi^*(y|x) \propto \pi_{ref}(y|x) \exp\left(\frac{1}{\beta} r(x, y)\right) $$

反解出 reward：$ r(x, y) = \beta \log \frac{\pi^*(y|x)}{\pi_{ref}(y|x)} + \beta \log Z(x) $ 。代回 Bradley-Terry 偏好模型 $ P(y_w \succ y_l | x) = \sigma(r(x, y_w) - r(x, y_l)) $ ，配分函数 $ Z(x) $ 在差里消掉，得到 DPO loss：

$$ \mathcal{L}_{DPO} = -\mathbb{E}\left[\log \sigma\left(\beta \log \frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}\right}\right] $$

记号：$ y_w $ chosen、$ y_l $ rejected、$ \beta $ 控制 KL 强度（$ \beta $ 小 → 约束弱 → 偏离 ref 远）。

**log-prob 怎么算（实操命门）**：自回归模型里 $ \log \pi(y|x) = \sum_t \log p(y_t | x, y_{<t}) $ 。代码上三步：logits 右移一位对齐 labels、gather 取目标 token 的 log-softmax、按 mask **求和**（不是平均）。平均会让长回答被系统性压低，是最经典的坑。

## 面试考点

1. 为什么 log-prob 用求和不用平均 —— 长度偏置，平均等价于给长序列打折
2. ref 模型的 log-prob 要不要 detach —— 要，ref 是常数；忘了 detach 等于 policy 在追自己的影子
3. $ \beta $ 的作用、调大调小分别什么症状（大 → 几乎不动，小 → reward hacking / 退化）
4. DPO vs PPO：省了 reward model 和采样，但吃离线数据的分布偏移（chosen/rejected 之外的行为不归它管）

## 常见 bug 清单

- **符号写反**：`rejected - chosen` → loss 也能降，但模型在学反偏好（reward accuracy < 0.5 是报警信号）
- **mean 代替 sum**：长 chosen 被惩罚，训完模型偏好短回答
- **ref 没 detach / 共用 optimizer**：ref 跟着 policy 一起动，KL 项失效
- **mask 漏掉 prompt 部分**：把 prompt 的 token 也算进 log-prob，等于在教模型背 prompt
- **label 没 shift**：logits 与 labels 错位一位，log-prob 全错但 loss 数值看起来正常 —— 最阴险的一个

> 可跑现场版在同名 notebook：BUG 1 符号写反 / BUG 2 mean 代替 sum / BUG 3 ref 没 detach，每个 bug 下面带修复版演示。

## 思考题

1. 如果 chosen 和 rejected 共享长前缀，log-prob 求和时前缀部分会怎样？对梯度有什么影响？
2. DPO 训练后 policy 在 chosen 上的绝对 log-prob 可能**下降**，为什么这不矛盾？
3. $ \beta \to 0 $ 和 $ \beta \to \infty $ 时 loss 分别退化成什么？

---
*上一篇：Research 01 — 训练循环零起 · 下一篇：Research 03 — PPO/GRPO loss*
