# G030 — Reward Model 是怎么训出来的？Bradley-Terry 与 batch 的反直觉细节
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G030-reward-model-training.html

## 元信息

- 编号：G030
- 标题：Reward Model 是怎么训出来的？Bradley-Terry 与 batch 的反直觉细节
- BV：BV1LJhU6kEkp
- 时长：00:55
- 发布日期：2026-10-02
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：InstructGPT（Bradley-Terry 奖励模型）；本期为「RL 入门到 GRPO」系列第 14 期

## 一句话总结

Reward model 不让人打绝对分、只让人比相对好坏：每个回答有一个标量分，两回答谁赢的概率等于分差过 sigmoid，训练就是在人类选择上做逻辑回归；工程上最反直觉的一条是同一提问的全部比较对必须放进同一个 batch，且只训一个 epoch。

## 核心

1. 问题/背景：让人给一篇文章打 73 分很难且不一致，问「两篇哪篇好」却很容易——奖励模型的训练信号就建立在成对比较上。
2. 机制/方法：背后的模型是 Bradley-Terry：回答 $a$ 胜过回答 $b$ 的概率由两者分数差决定，形式为 $P(a \succ b) = \sigma(r_a - r_b)$ 。训练即逻辑回归：人类选了谁，就最大化其分差过 sigmoid 后的概率。InstructGPT 的做法是每条提问给标注员 4–9 个回答做排序，由此展开成比较对。
3. 关键证据或数字：两个容易踩的细节。其一，同一条提问产生的所有比较对高度相似，若打散混训、一遍就过拟合，所以论文把同一提问的全部对放进同一个 batch，并只训一个 epoch。其二，分数只有相对意义、可以整体平移，工程上再把示范答案的分数均值定在零做归一化锚点。
4. 结论/判断：RM 学的是人的偏好，也因此能被「讨好」——这是 reward hacking 的源头；视频顺带提到 DeepSeek-R1 的判断：神经网络 reward model 在大规模 RL 里可能被 hack（下一期展开如何拴住它）。

## 关键数字

| 量 | 取值 |
|---|---|
| 每条提问的回答数（InstructGPT） | 4–9 个，人工排序 |
| 训练轮数 | 1 个 epoch |
| 获胜概率 | $\sigma(r_a - r_b)$ |

## 可迁移

- 自己训 RM 或做偏好数据管线时记住「同 prompt 的对不拆 batch」这条：数据组织方式错了，再好的损失函数也救不回来。
- 面试讲 RM 时强调分数的平移不变性：RM 输出没有绝对刻度，跨 RM、跨版本比分数大小没有意义。

## 疑问 / 下一步

- RM 可被讨好的问题在过程奖励（PRM）和规则奖励下形态如何变化，留待与 RLVR 各期对照。
