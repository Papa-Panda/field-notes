# G316 — Token-level MDP：LLM 的 state 和 action 到底是什么？
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G316-token-level-mdp.html

## 元信息
- 编号：G316
- 标题：Token-level MDP：LLM 的 state 和 action 到底是什么？
- BV：BV1R63Z6nEeD
- 时长：04:08
- 发布日期：2026-08-10
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：未标注（RLHF / PPO 的标准 token-level MDP 建模）

## 一句话总结
把 LLM 生成建模成 MDP：state 是 prompt 加已生成 token 的整段历史，action 是从几万词表里挑下一个 token，转移完全确定（拼接），奖励只在整句结束时由 RM 给一次——这四点决定了 PPO 在 LLM 上的一切工程形态。

## 核心
1. **问题/背景**：RLHF 用 PPO，但先得回答一个更基础的问题：LLM 的「环境」到底是什么？经典 RL 的 state 是棋盘快照、action 是落子，而 LLM 面对的既不是游戏画面也不是机械臂。
2. **机制/方法**：token-level MDP 的四个要素——**state**：时刻 $t$ 的状态是 prompt 与已生成 token 拼成的整段序列，因为 Transformer 必须看完整前缀才能预测下一个 token，「历史即状态」，一个 episode 的步数就等于生成 token 数（几十到几百）；**action**：从词表选一个 token，现代模型词表 3 万到 13 万量级，动作空间比围棋落点大上百倍，policy 输出的是整个词表上的概率分布再采样（或 argmax）；**transition**：完全确定——给定 state 与 action，下一个 state 必然是序列末尾拼上这个 token，没有环境随机性，随机性只来自 policy 采样；**reward**：通常只在终止步由 reward model 给一次总分，中间步全为零。
3. **关键证据或数字**：与经典 RL 对照：状态是历史序列而非当前快照；转移是确定性的而非随机；动作空间是几万维而非几个到几百个；奖励是终端一次性的稀疏奖励而非逐步反馈。确定性转移带来一个工程红利：任何轨迹都能精确回放，off-policy 评估方便。
4. **结论/判断**：稀疏的终端奖励使信用分配极难，PPO 在 LLM 上的工程技巧本质都在解决「怎么把终端分数摊回每个 token」：critic 必须逐 token 估值、GAE 在 token 级别反传优势、KL 惩罚也逐 token 计算。理解这套建模，才算理解 RLHF 为什么长这样。

## 可迁移
- 面试被问「LLM 怎么做 RL」时，先按 state / action / transition / reward 四要素展开，再落到「所以 critic、GAE、KL 都必须 token 级」这一推论链，比背 PPO 公式更有说服力。
- 做 RL infra 时记住转移确定性这条：rollout 轨迹可精确复现与重放，logprob 对齐校验、off-policy 评估都建立在这条性质上。

## 疑问 / 下一步
- 终端奖励摊回每个 token 的信用分配仍是近似（GAE 依赖 critic 质量），过程奖励 / 稠密奖励如何改变这个 MDP 的奖励结构，值得接着看 PRM 一类工作。
