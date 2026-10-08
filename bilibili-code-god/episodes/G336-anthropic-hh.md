# G336 — Anthropic HH 数据集：Helpful 和 Harmless 是怎么标注的？
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G336-anthropic-hh.html

## 元信息
- 编号：G336
- 标题：Anthropic HH 数据集：Helpful 和 Harmless 是怎么标注的？
- BV：BV1oQ3R6LEgz
- 时长：04:00
- 发布日期：2026-08-04
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Anthropic HH 数据集（Bai et al. 2022，《Training a Helpful and Harmless Assistant with RLHF》）；Bradley-Terry 偏好建模

## 一句话总结
HH 把对齐拆成 helpful 与 harmless 两个价值维度：同一套「采样-两两对比-训 RM」流程、两份目标相反的标注指南、两个奖励模型分别打分再加权组合。

## 核心
1. **问题/背景**：模型既要有问必答、主动帮忙，又要拒绝有害请求——这两个目标会冲突：一个回答可能非常有用但极其危险，另一个可能绝对安全但毫无用处（如对一切问题都拒绝）。单一奖励模型无法同时表达这两个维度。
2. **机制/方法**：数据集分两部分，共约 16 万条偏好对，每条都是 chosen/rejected 对比。标注流程是教科书式的：同一基础模型对同一 prompt 采样多个回答 → 标注员按指南两两对比选更好的 → 用 Bradley-Terry 模型训练奖励模型。helpful 部分采普通提问，指南强调「多做、详细做、主动做」——给完整步骤、食材清单、注意事项，模糊问题主动澄清；harmless 部分采诱导性问题并做对抗性测试（伪装安全研究员、角色扮演诱导），指南强调识别有害意图、礼貌拒绝、提供安全替代方案（如自伤问题应表达关心并建议求助专业人士）。
3. **关键证据或数字**：Anthropic 的解法是训练两个 RM——一个评 helpful、一个评 harmless——RLHF 时把两个分数加权组合，让模型在有用与无害间找平衡。这一设计直接启发了后来的 Constitutional AI 与 RLAIF。
4. **结论/判断**：HH 的标注指南比数据本身更有价值，它定义了 RLHF 数据工程的教科书标准：先拆价值维度，再为每个维度写可执行的标注规范。

## 关键数字
| 项 | 值 |
|---|---|
| 偏好对总量 | 约 16 万条 |
| 子集构成 | helpful + harmless 两部分 |
| 奖励模型 | 2 个（分维度训练，加权组合） |

## 可迁移
- 自建偏好数据时先做维度拆分：把「质量」拆成可独立标注的维度并分别训 RM，比一个大杂烩指南更可控，也便于事后调权重。
- 面试高频：HH 是 RLHF 的「ImageNet 时刻」，能讲清对抗性测试（红队式诱导标注）与双 RM 加权就是加分项。

## 疑问 / 下一步
- helpful 与 harmless 分数加权的比例如何定、能否随场景动态调？这是后来多目标 RLHF / Pareto 前沿方法要回答的问题。
