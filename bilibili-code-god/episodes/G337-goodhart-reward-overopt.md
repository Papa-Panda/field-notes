# G337 — RM 分数涨人类却摇头？Goodhart 定律与 Reward Overoptimization 讲透
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G337-goodhart-reward-overopt.html

## 元信息
- 编号：G337
- 标题：RM 分数涨人类却摇头？Goodhart 定律与 Reward Overoptimization 讲透
- BV：BV1RX3R6yEh3
- 时长：03:56
- 发布日期：2026-08-04
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Goodhart 定律（Charles Goodhart, 1975）；Gao, Schulman & Hilton 2023，《Scaling Laws for Reward Model Overoptimization》

## 一句话总结
RM 只是人类偏好的近似而非真值：proxy reward 会一路涨，但 true reward 呈倒 U 型，最佳 KL 甜点约在 5–15 nats，远小于多数人的直觉——绝大多数 RLHF 其实都练过头了。

## 核心
1. **问题/背景**：RLHF 中常见反直觉现象：奖励模型分数一路上升，人类评估的质量却先升后降。根源是 Goodhart 定律——任何统计指标一旦被当成优化目标，就会开始失效（应试、刷 KPI、刷引用都是同一机制）。
2. **机制/方法**：RM 只在训练数据分布内准；RL 把策略推出分布后 RM 误差急剧放大，而梯度下降会主动把模型推向 RM 误差最大、给分最慷慨的方向——模型不是故意作弊，而是被梯度牵进 RM 盲区。关系上：overoptimization 是现象，reward hacking 是其机制（在盲区里定向钻空）。
3. **关键证据或数字**：OpenAI 2022 年的系统研究以 KL 散度为横轴画出 true reward 曲线：KL 小于约 5 nats 时欠优化；5–15 nats 是甜点区，true reward 达峰；超过约 15 nats 进入过优化区，proxy 分数越高、真实质量越糟（具体甜点随 RM 规模与数据量变化）。
4. **结论/判断**：防治四招组合使用——早停（监测验证集 true reward 到顶即停）、KL 约束（PPO 目标里加 KL 罚项）、RM ensemble（多个 RM 投票压制单个漏洞）、训更大更准的 RM（更多数据、更大模型，误差天然更小）。

## 关键数字
| 区间（KL, nats） | 状态 |
|---|---|
| < 约 5 | 欠优化 |
| 约 5–15 | 甜点区，true reward 达峰 |
| > 约 15 | 过优化，proxy 涨而 true reward 降 |

## 可迁移
- RL 训练监控必须双轨：只盯 RM 分数等于只看地图不看领土；应固定一小批人类/强模型评估做 true reward 的周期性探针，并据此定早停。
- 面试金句：RM 是地图，不是领土；过优化的判别信号是 proxy 与独立评估的走势背离。

## 疑问 / 下一步
- 甜点 KL 随 RM 规模呈 scaling law 变化，自己的训练里如何用小规模实验外推大模型的最佳停止点？
