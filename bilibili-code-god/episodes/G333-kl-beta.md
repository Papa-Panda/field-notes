# G333 — KL 惩罚系数 β 怎么调？太小 Reward Hacking，太大学不动
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G333-kl-beta.html

## 元信息
- 编号：G333
- 标题：KL 惩罚系数 β 怎么调？太小 Reward Hacking，太大学不动
- BV：BV1ck3R6pE2G
- 时长：04:07
- 发布日期：2026-08-05
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：InstructGPT、Llama 2、Anthropic HH RLHF

## 一句话总结
$\beta$ 是 KL 约束的温度旋钮：太小则约束形同虚设、模型钻 RM 漏洞出现 reward hacking，太大则模型被拴死在参考模型旁学不动；经典取值从 0.01 到 0.02 不等，当下主流是把 $\beta$ 做成盯住目标 KL 的自适应闭环控制。

## 核心
1. **问题/背景**：RLHF 的总奖励是 RM 打分减去 $\beta$ 倍的当前策略与参考模型之间的 KL 散度， $\beta$ 一个系数就决定了训练是崩掉还是收敛，却没有跨工作通用的取值。
2. **机制/方法**：$\beta$ 本质在权衡"多努力讨好 RM"与"多老实守住原有语言能力"。太小：actor 很快发现 RM 的判断盲区，输出看似高深的乱码或重复特定 token 也能刷高分，reward 曲线飙升而生成全是垃圾。太大：任何偏离参考模型的尝试都被重罚，梯度信号被 KL 项淹没，reward 长期停在初始水平，模型什么也学不到。自适应 $\beta$ 把 KL 当被控变量做 PID 式闭环：先定目标 KL（约 6–8 nats），每步比较实际 KL 与目标，超了就调大 $\beta$ 收紧、低于就调小 $\beta$ 松绑，使 KL 稳定在目标区间，reward 尺度或学习率变化时 $\beta$ 自动跟随。
3. **关键证据或数字**：InstructGPT 取 $\beta = 0.02$ ，约束相对紧，保住 1.3B 小模型不跑偏；Llama 2 取 0.01，松一半，因其 RM 经过多轮迭代更鲁棒、可以给 actor 更多自由；Anthropic 则让 $\beta$ 在 0.001 到 0.1 之间自适应变化。可见 $\beta$ 与 RM 质量、模型规模、数据分布强耦合，不存在万能值。
4. **结论/判断**：调 $\beta$ 先看 RM 可信度：RM 越不可靠越要收紧；工程上优先用自适应闭环盯目标 KL，而不是手调固定值或预设 schedule。

## 关键数字
| 工作 | $\beta$ 取值 |
|---|---|
| InstructGPT | 0.02 |
| Llama 2 | 0.01 |
| Anthropic | 0.001–0.1 自适应 |
| 自适应目标 KL | 约 6–8 nats |

## 可迁移
- RL 训练监控中 KL 应与 reward 一起画曲线：reward 涨而 KL 暴冲是 hacking 前兆，KL 贴地不动则多半是 $\beta$ 过大或学习率问题。
- 面试答 $\beta$ 调参时强调它与 RM 质量耦合，并给出自适应 KL 控制这一现代解法，胜过背固定数值。

## 疑问 / 下一步
- GRPO 等新算法常弱化甚至去掉显式 KL 项，其稳定性依赖什么替代机制，与 $\beta$ 自适应相比代价在哪，值得对照后续视频与框架实现核对。
