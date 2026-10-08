# G323 — Reference Model 是干嘛的？为什么 PPO 离不开这个"躺平"的模型
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G323-reference-model.html

## 元信息

- 编号：G323
- 标题：Reference Model 是干嘛的？为什么 PPO 离不开这个"躺平"的模型
- BV：BV1Xd3R6kEdU
- 时长：04:28
- 发布日期：2026-08-08
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：PPO / RLHF（InstructGPT 式四模型架构）、DPO、LoRA

## 一句话总结

Reference model 是 SFT 模型的冻结副本，它在 PPO 里充当 KL 锚点：没有这根绳子拴住 actor，几轮训练就会因 reward hacking 崩盘。

## 核心

### 1. 问题/背景

RLHF 训练时显存里同时躺着四个模型：actor 生成回答、critic 估价值降方差、reward model（RM）按人类偏好打分，而第四个 reference model 参数全程冻结、一动不动，却占着和 actor 一样大的显存。它存在的理由是：RM 只是用有限偏好数据拟合出的代理，对分布外输入并不可靠；若放任 actor 无约束地冲 RM 高分，模型很快会找到 RM 的漏洞——重复高频词、堆夸张形容词、甚至输出乱码——分数飙升但回答退化成复读机，这就是 reward hacking。

### 2. 机制/方法

Reference model 与 actor 同架构、同初始化（都从 SFT checkpoint 加载），唯一区别是参数冻结、不进优化器。它的职责是为每个 token 给出参考 log 概率，作为 actor 的锚点。PPO 实际优化的不是纯 RM 分数，而是：

$$R = r_{RM} - \beta \cdot D_{KL}(\pi_\theta \| \pi_{ref})$$

KL 在 token 级计算：每个 token 取 actor 与 reference 的 log 概率之差，整句求和；actor 偏离 reference 越远，总奖励被扣得越多。系数 $ \beta $ 是最需要手感的超参之一：取大则惩罚重、训练稳但学得慢，模型停留在「SFT 味」；取小则探索激进、提升快但容易踩进 reward hacking。还有自适应变体，按当前 KL 与目标 KL 的差距动态调 $ \beta $ 。

### 3. 关键证据或数字

视频给出 $ \beta $ 的工程起调量级为 0.01 到 0.1，配合 KL 监控曲线双向调节：KL 涨太快就调大 $ \beta $ ，RM 分数上不去就调小。另一个关键数字在显存侧：每次 rollout 每句话要跑两次前向（actor 一次、reference 一次），显存里同时存在两份完整模型，这是 RLHF 显存远大于 SFT 的主因。

### 4. 结论/判断

Reference model 不是可有可无的陪跑，而是 PPO 不崩盘的守门员。省显存有两条路：LoRA 方案只加载一份 base，actor 在 base 上挂 adapter 训练，需要 reference 时关掉 adapter 用纯 base 前向，第二份模型几乎不占额外显存；DPO 则干脆把 reference 内化进损失、不显式加载，这也是 DPO 比 PPO 省显存的关键原因。注意它与 target network 的区别：不是缓慢追踪，而是真的全程不动。

## 关键数字

| 量 | 取值/说明 |
|---|---|
| 同显存模型数 | 4 个（actor / critic / RM / reference） |
| $ \beta $ 起调量级 | 0.01–0.1，配合 KL 曲线监控 |
| 每句 rollout 前向次数 | 2 次（actor + reference） |

## 可迁移

- 面试被问「四个模型各干嘛」时，把 reference 的角色落在 KL 锚点上，并主动补一句它与 target network 的区别（完全冻结 vs 软更新），这是高频区分点。
- 做 RL infra 显存预算时，reference 的那一份要单独计入；用 LoRA/adapter 开关共享 base 是把这份成本压到近零的标准手法。

## 疑问 / 下一步

- GRPO 等新算法里 reference 仍常驻，但 KL 的处理方式（如直接进 loss 或用估计器）与 PPO 不同，值得对照一期细看。
