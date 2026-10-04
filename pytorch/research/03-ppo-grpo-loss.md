# Research 03 — PPO/GRPO loss：clip、advantage、KL

- **定位**：Research PyTorch 轮次里 RL 算法面的核心。DPO 是离线偏好优化，PPO/GRPO 是在线 RL —— 面试会让你手写任意一个的 loss 并解释每一项的来历。
- **配套 notebook**：[03-ppo-grpo-loss.ipynb](03-ppo-grpo-loss.ipynb)（Colab 可直接跑，CPU 即可）

## 一句话总结

PPO 用 importance ratio + clip 把策略更新限制在可信域内，GRPO 把 PPO 的 critic 扔掉、用同组样本的相对名次当 advantage。两者共用一个骨架：per-token ratio、advantage 广播、KL 拴住 ref。

## 核心（动机 + 机制）

**策略梯度的出发点**：最大化 $ J(\theta) = \mathbb{E}_{y \sim \pi_\theta}[R(y)] $ ，梯度 $ \nabla J = \mathbb{E}[\nabla \log \pi_\theta(y) \cdot A] $ ，$ A $ 是 advantage（这一步比平均好多少）。减 baseline 不改变期望、只降方差，这是 $ A = Q - V $ 的来历。

**PPO 的 ratio 与 clip**。采样用的是旧策略 $ \pi_{old} $ ，importance ratio $ \rho_t = \frac{\pi_\theta(a_t|s_t)}{\pi_{old}(a_t|s_t)} $ 做分布修正。目标：

$$ \mathcal{L}^{clip} = \mathbb{E}\left[\min\left(\rho_t A_t, \mathrm{clip}(\rho_t, 1-\epsilon, 1+\epsilon) A_t\right)\right] $$

$ \rho $ 跑出 $ [1-\epsilon, 1+\epsilon] $ 后梯度置零 —— 不是把 ratio 拉回来，是**拒绝在可信域外继续优化**。$ \epsilon $ 常用 0.2。LLM 场景还有两个工程细节：loss 只在 completion token 上算（prompt 位置 mask 掉）、ratio 在 token 级算而 advantage 在序列级广播。

**GAE**：advantage 的估计器。TD 残差 $ \delta_t = r_t + \gamma V(s_{t+1}) - V(s_t) $ ，$ A^{GAE}_t = \sum_l (\gamma\lambda)^l \delta_{t+l} $ 。$ \lambda=0 $ 是纯 TD（低方差高偏差）、$ \lambda=1 $ 是蒙特卡洛（高方差低偏差），常用 0.95。

**GRPO**：同一 prompt 采样 $ G $ 个回答（$ G $ 常用 8–64），advantage 用组内标准化：

$$ A_i = \frac{R_i - \mathrm{mean}(R_{1..G})}{\mathrm{std}(R_{1..G})} $$

省掉 critic（省一份模型显存和一整套训练问题），代价是方差更高、$ G $ 太小时 advantage 噪声大。Dr. GRPO 指出 std 分母会引入难度偏置（简单题 advantage 被放大），主张去掉 std 项。

**KL 拴 ref 的两个位置**：① 当 reward 的一部分（$ r - \beta \cdot KL $ ，PPO 经典做法）；② 当 loss 里的显式正则项（GRPO 常用）。估计器三兄弟：$ k_1 = -\log \frac{\pi_{ref}}{\pi_\theta} $ （无偏、高方差）、$ k_2 $ （低方差、有偏）、$ k_3 $ （无偏、低方差，实现里最常见）。

## 面试考点

1. clip 为什么取 min 而不是直接 clamp ratio 后求梯度 —— min 保证悲观估计，$ A<0 $ 时行为不同
2. PPO 的四个网络（policy / ref / reward / critic）在 LLM 场景各省不省，GRPO 省了哪个、省出什么代价
3. KL 放 reward 里和放 loss 里的区别（梯度路径不同：前者经 advantage，后者直接对 logp 求导）
4. advantage 广播：序列级 $ A_i $ 怎么摊到 token 级 loss（每个 completion token 共用同一个 $ A_i $ ，除以长度与否是实现分歧点）

## 常见 bug 清单

- ratio 用 `logp_new - logp_old` 后忘了 exp（或者反过来）
- clip 区间写错方向：`clip(rho, 1+eps, 1-eps)` 直接报错/静默出错
- prompt token 没 mask 进 loss，模型在学复读 prompt
- GRPO 的 std 用全体 batch 的而不是组内的 —— advantage 失去"相对名次"含义
- KL 符号反了：越训离 ref 越远还以为在正则

> 可跑现场版在同名 notebook 第 5 节「Debug 演练」：BUG 1 log-ratio 忘 exp / BUG 2 clip 上下界写反 / BUG 3 advantage 没 detach / BUG 4 全同 reward 组 NaN / BUG 5 KL 符号反，每个 bug 下面带修复。

## 思考题

1. $ \epsilon \to 0 $ 和 $ \epsilon \to \infty $ 时 PPO 分别退化成什么？
2. GRPO 中同一 prompt 的 $ G $ 个样本 advantage 之和恒为多少？这对梯度有什么含义？
3. 为什么 LLM 的 PPO 常用 token 级 ratio + 序列级 advantage，而不是都用序列级？

---
*上一篇：Research 02 — DPO loss 手写 + debug · 下一篇：Research 04 — 注意力机制手写*
