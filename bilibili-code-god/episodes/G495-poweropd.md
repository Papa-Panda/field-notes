# G495 — OPD 的 reward 设计合理吗？从 log 无界到 PowerOPD 幂变换

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G495-poweropd.html

## 元信息

- 编号：G495
- 标题：OPD 的 reward 设计合理吗？从 log 无界到 PowerOPD 幂变换
- BV：BV1DtTC6tEy4
- 时长：06:09
- 发布日期：2026-07-06
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：PowerOPD（Box-Cox 幂变换 reward）、On-Policy Distillation（OPD）、Full-vocab OPD

## 一句话总结

OPD 训练不稳的真凶是 reward 里的 log：学生概率接近零时 log 比值无界、单个 token 就能把梯度带飞；PowerOPD 用 Box-Cox 幂变换把 log 换成有界的幂差，梯度稳了三个数量级，还省一半算力。

## 核心

1. **问题/背景**：传统 SFT 让学生照抄老师轨迹，有暴露偏差（自己走偏了没学过怎么办）。OPD 让学生自己 rollout，老师在学生真正走到的每个 token 上打分——从 RL 视角看，老师与学生的对数概率之比就是乘在策略梯度前面的 reward，信号密集但 reward 设计有问题就每步都被它牵着走。主流的 sampled-token OPD 只在采样到的那个 token 上算 log 比值，病理明显：Qwen3 4B/7B 实验里准确率前 300 步不升反降、生成长度前 400 步剧烈震荡，最终 54.9%，比 full-vocab OPD 低 8 个点。
2. **机制/方法**：病根是 log 无界——学生自信踩中、老师几乎不认可的 token，概率比趋近零，reward 直接报到 −50，一个 token 的杠杆是正常 token 的几十倍；且极端值扎堆在轨迹开头，prefix 被推歪后整条轨迹漂移。常见补救全失败：clip 和 tanh 是在 log 已把微小概率差放大成极端值之后才压缩，太晚；z-score 标准化会翻转 reward 符号，而 OPD 里符号就是学习方向，翻了比不修更差。PowerOPD 保留 log 比值「先变换再相减」的结构，只把变换换成 Box-Cox 幂变换：reward 等于老师概率的 $\alpha$ 次方减学生概率的 $\alpha$ 次方，概率在 0 到 1 之间，天然有界在 −1 到 1，幂函数单调递增保证符号一致；vanilla OPD 只是 $\alpha$ 趋于 0 的退化极限。 $\alpha$ 的作用是概率区域选择器：log 只看比例、对绝对概率无视（0.01/0.0005 与 0.6/0.03 比值同为 20 给一样 reward），而 $\alpha$ 越大，低概率区的 reward 越被压成死区、越聚焦高概率 token 和真实信号。
3. **关键证据或数字**：vanilla OPD 初始梯度范数能飙到接近 1000，PowerOPD 始终在 0.3 上下，差 3000 倍以上；四组师生设置、六个数学基准上比 vanilla OPD 最高提升 6.37 个点，比后处理方法最高提升 3.01 个点，pass@8 甚至比 full-vocab OPD 最高还高 8.9 个点；训练时间省 59%、显存省 23%。
4. **结论/判断**：sampled-token OPD 的瓶颈从来不是采样本身，而是 reward 没设计好；reward 的问题往往不在后处理，而在「从概率到 reward」那个函数本身，换掉 log 一行就够。

## 关键数字

| 对比 | 基线（vanilla OPD） | PowerOPD |
|---|---|---|
| 极端 token 的 reward | 约 −50 | 有界在 −1 到 1 |
| 初始梯度范数 | 接近 1000 | 约 0.3 |
| 准确率（vs full-vocab OPD） | 低 8 个点 | pass@8 最高反高 8.9 个点 |
| 训练时间 / 显存 | — | 省 59% / 省 23% |

## 可迁移

- 设计 RL / 蒸馏的 reward 时，先检查 reward 函数本身是否有界、符号是否会被后处理翻转，再谈 clip 这类补救——无界的 log-ratio 是梯度爆炸的经典来源。
- 面试聊 OPD 可迁移一个判断框架：任何「比值型」信号都要问一句它对绝对量级是否盲视，幂变换是把量级信息加回来的通用手法。

## 疑问 / 下一步

$\alpha$ 在实验里越大越好，但有没有上限、要不要按训练阶段调度，视频没给结论，值得看原文的消融。
