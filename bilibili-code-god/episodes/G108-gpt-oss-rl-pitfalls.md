# G108 — GPT-OSS 做 RL 为什么 KL 一开训就爆炸？MoE 路由、attention sink 与显存三个坑
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G108-gpt-oss-rl-pitfalls.html

## 元信息

- 编号：G108
- 标题：GPT-OSS 做 RL 为什么 KL 一开训就爆炸？MoE 路由、attention sink 与显存三个坑
- BV：BV1VpeY6KEtn
- 时长：03:37
- 发布日期：2026-09-21
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：GPT-OSS-20B 的 Agentic RL 训练复盘（16 台 H200 节点；问题在 verl、OpenRLHF 等框架上普遍出现）

## 一句话总结

新架构模型做 RL 时 KL 与熵一起爆炸、reward 不涨，根因不在算法而在训推没对齐：MoE 路由不确定让重要性比偏离 1、FlashAttention 缺 sink 反向让训推跑两个不同的注意力函数、HF 的 MoE 实现让显存峰值冲到 180 GB。

## 核心

1. 问题/背景：设置是 GPT-OSS-20B（bf16、MoE、带 attention sink），prompt 8K、回答最长 16K，任务为 GSM8K 类可验证奖励，Harmony 模板要在 rollout 轨迹构造、工具解析、训练三处保持一致。开训即 KL/熵爆炸，是架构与训练栈没对齐的典型症状。
2. 机制/方法：坑一，MoE 路由在两次前向里可能不同，同一回答的 log-prob 对不上，PPO/GRPO 第一次更新要求的重要性比 ， $= 1$ ，被悄悄破坏，clip 与 KL 全乱；修法是严格 on-policy 的那次更新里把 old log-prob 直接取当前 log-prob 的 detach，数学上强制比率为 1（仅单次更新合法，多 epoch 不行）。坑二，GPT-OSS 每个注意力头有一个可学习的 sink 参数（相当于常驻空 token 分走注意力），vLLM 内核支持它，但训练用的 FlashAttention v2 没实现、v3 只有前向没有 sink 的反向，训推实际是两个注意力函数；修法是参照 vLLM 前向给 FA3 补上 sink 反向，这一步修完训练才稳定、reward 稳步上升，是决定性修复。坑三，HF 的 MoE 实现把 hidden states 复制给每个专家再算 log-prob，峰值显存 180 GB 超过 H200 的 139.7 GB；修法是逐专家串行执行、只送路由到的 token，再叠加带 sync 的序列并行把长上下文激活切到多卡。
3. 关键证据或数字：显存峰值 180 GB 对单卡 139.7 GB，必然 OOM；三处单独修都不够（先只做 rollout correction 无效），合起来修才稳。
4. 结论/判断：新架构做 RL 的检查清单是模板一致、路由确定、注意力内核语义一致、显存峰值可控；训推一致要对齐到内核语义层，而不只是算法公式层。

## 关键数字

| 项 | 数值 |
|---|---|
| 模型 / 规模 | GPT-OSS-20B，16 台 H200 节点 |
| 上下文 | prompt 8K + 回答最长 16K |
| HF MoE 实现显存峰值 | 180 GB（单卡上限 139.7 GB） |

## 可迁移

- RL infra 排障顺序：KL 开训爆炸先查训推一致性（路由确定性、注意力内核是否同函数），再怀疑算法超参。
- 面试可讲：on-policy 第一步比率恒为 1 是可检验的不变量，MoE 路由不确定会静默破坏它，detach 强制对齐是合法的单步修法。

## 疑问 / 下一步

- sink 反向补进 FA3 后与 vLLM 前向的数值一致性如何做回归测试，视频未展开。
