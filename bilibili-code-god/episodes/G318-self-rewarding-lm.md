# G318 — Self-Rewarding LM：不要 Reward Model，让 LLM 自己当裁判
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G318-self-rewarding-lm.html

## 元信息
- 编号：G318
- 标题：Self-Rewarding LM：不要 Reward Model，让 LLM 自己当裁判
- BV：BV1XZ3R63EYU
- 时长：04:19
- 发布日期：2026-08-09
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Self-Rewarding Language Models（Meta，2024）

## 一句话总结
Self-Rewarding LM 让同一个模型身兼两职：当生成器产出多个候选回答，再换上 LLM-as-judge 的提示词给自己打分，用最高分与最低分凑偏好对做 DPO，如此迭代——生成与评分能力互相喂养、同步变强，全程不需要外部 reward model。

## 核心
1. **问题/背景**：标准 RLHF 要单独训练一个 reward model 提供奖励信号，但 RM 本身的数据与训练又是一套成本。能否把奖励信号源搬进模型内部？
2. **机制/方法**：一轮迭代四步——① 生成：对同一指令采样多个候选回答，给评分留出可挑选的差异；② 评分：同一个模型换上评审提示词（内置 few-shot 示例与分档标准），从相关性、覆盖度、有用性、清晰度等维度给每个候选打 0–5 分；③ 构对：最高分当 chosen、最低分当 rejected，组成 DPO 偏好集；④ 更新：DPO 直接拉高 chosen 概率、压低 rejected 概率（这一步本身也不需要 RM）。得到的新模型进入下一轮，重复生成—评分—DPO。
3. **关键证据或数字**：Meta 在 Llama-2 70B 上迭代三轮，生成能力（AlpacaEval 胜率）持续上升，最终超过 Claude 2 与早期 GPT-4；同时评分与人类标注的一致率也同步提升——模型不只是更会答题，连「批改」水平都跟着涨，两个能力互为因果。
4. **结论/判断**：核心风险是自我吹捧式的 reward hacking：模型可能学会无论好坏都给自己高分。缓解靠工程手段——评审提示词风格多样化、更换 few-shot 示例、引入外部校验，避免模型形成自我偏好的捷径。

## 可迁移
- 与 RLAIF 对比记忆：RLAIF 是请「别的」模型当裁判，Self-Rewarding 是自己当裁判；面试讲自举式对齐时这条对照很出彩。
- 做无外部标注的迭代对齐 pipeline 时，可复用「多候选采样 → 自评构偏好对 → DPO」这条最小闭环，但要把防自捧的评审多样性设计当一等公民。

## 疑问 / 下一步
- 自评分的可靠性上限受模型自身判断力制约，迭代多轮后评分能力是否会先于生成能力饱和、进而卡住整个循环，论文的曲线之外还值得继续追踪。
