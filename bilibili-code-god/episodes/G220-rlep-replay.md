# G220 — RLEP 经验回放：把高质量 rollout 存进 buffer 反复利用

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G220-rlep-replay.html

## 元信息

- 编号：G220
- 标题：RLEP 经验回放：把高质量 rollout 存进 buffer 反复利用
- BV：BV1fK8S6jE8G
- 时长：01:03
- 发布日期：2026-08-31
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：RLEP（经验回放式 RL）；verl 与 OpenRLHF 的 replay buffer 实现

## 一句话总结

纯 on-policy 训练把每条 rollout 只用一次就扔掉，高质量轨迹尤其浪费；RLEP 把高分 rollout 存进 replay buffer 反复采样复用，代价是数据变成 off-policy，必须用重要性采样修正分布偏差，换来的是样本效率提升和训练成本下降。

## 核心

1. 问题/背景：on-policy 算法要求数据来自当前策略，每批 rollout 训完即弃；在奖励稀疏、好轨迹稀缺的推理 RL 里，这意味着最宝贵的成功样本利用率只有一次。
2. 机制/方法：RLEP 把高质量 rollout 存入 buffer，后续训练时反复采样复用。buffer 设计要回答三个问题：存什么（以高质量轨迹为主）、怎么采样、以及过期策略产生的数据如何修正。
3. 关键证据或数字：复用的数据来自旧策略，与当前策略存在分布偏差，用 importance sampling 按概率比加权来修正；框架层面，verl 支持异步 rollout 并把好轨迹存入 buffer，OpenRLHF 的 buffer 更成熟、支持优先级采样，但工程复杂度也更高。
4. 结论/判断：视频给出的效果判断是训练效率显著提升、成本降低；本质上是拿一点 off-policy 修正的复杂度和偏差风险，换稀缺成功样本的复用收益。

## 关键数字

（本条以机制与框架对比为主，未给出量化基线数字。）

## 可迁移

- 做推理 RL infra 时，replay buffer 是 rollout 侧最直接的成本优化：rollout 生成最贵，把高分轨迹复用等于摊薄生成成本。
- 引入回放时必须同时设计 staleness 控制（数据过期上限）与重要性采样修正，否则旧轨迹会把策略拖向过期分布。

## 疑问 / 下一步

- buffer 中轨迹的准入阈值与过期策略（按奖励分、按年龄还是按与当前策略的 KL）如何定，视频只点到设计问题，未给经验值，需查 verl/OpenRLHF 实现细节。
