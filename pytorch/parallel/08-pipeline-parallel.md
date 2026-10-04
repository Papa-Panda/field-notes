# Parallel 08 — PP 流水线并行：按层切，气泡是唯一的敌人

- **定位**：并行基础线第四篇，补上 TP/DP/PP 三件套的最后一件。TP 切层内、DP 切数据、PP 切层间 —— 三者的通信长相完全不同，组合方式是并行策略设计的主题。
- **配套 notebook**：[08-pipeline-parallel.ipynb](08-pipeline-parallel.ipynb)（Colab 可直接跑）

## 一句话总结

PP 把模型按层切成 $ p $ 段摊到 $ p $ 个设备上，代价是流水线气泡：填满和排空阶段总有设备在等。micro-batch 数 $ m $ 越大，气泡占比 $ (p-1)/(m+p-1) $ 越小 —— 但激活显存随 $ m $ 涨，这就是 PP 的核心交易。

## 核心（动机 + 机制）

**动机**：TP 能切的层内宽度有上限（一个 head 的维度不能再切），DP/ZeRO 不解决"层数太深、单层激活太大"。按层切是最后一块拼图：设备 $ i $ 只持有第 $ i $ 段层，前向时激活像流水线一样逐段传递。

**气泡从哪来**：第一个 micro-batch 要依次流过 $ p $ 段才能产出，最后一个段在最初的 $ p-1 $ 步里无事可做（填不满）；结尾对称地排空。把 batch 切成 $ m $ 个 micro-batch 轮流喂，稳态时所有段都在工作，气泡只剩头尾：

$$ \text{bubble 比例} = \frac{p-1}{m+p-1} \quad (\text{前向+反向合计，GPipe 口径}) $$

$ m $ 拉大，气泡趋近于 0 —— 但每个 in-flight 的 micro-batch 都要存激活等反向，**激活显存 $ \propto m $ **。GPipe（全部前向完再全部反向）把 $ m $ 份激活全存下来；1F1B（稳态时每段 1 次前向紧跟 1 次反向）把 in-flight 压到约 $ p $ 份，气泡不变、显存大降 —— 这就是 1F1B 成为标配的原因。Interleaved 1F1B（每设备持多段虚拟 stage）再把气泡压到约 $ 1/v $ （$ v $ = 每设备段数），代价是通信次数变多。

**通信长相**：PP 只在 stage 边界上传激活（点对点 send/recv，一次一个 micro-batch 的边界激活），通信量远小于 TP 的 all-reduce，但对延迟敏感。推论：**PP 适合放跨节点（通信少、能忍延迟），TP 适合放节点内（通信多、吃 NVLink 低延迟）** —— 并行策略组合的总原则在 06 里已经立过，这里再收一次。

## 面试考点

1. bubble 公式现场推导：为什么分子是 $ p-1 $ 、分母是 $ m+p-1 $
2. GPipe 与 1F1B 的区别只在激活显存不在气泡 —— 给数字：同样 $ p, m $ 下各存多少份激活
3. 为什么 PP 的通信能跨节点而 TP 不能（消息大小与频率的量级对比）
4. $ m $ 的选择：气泡、激活显存、与 DP 的有效 batch size 三者怎么权衡（$ m $ 太大时 gradient accumulation 步数被吃掉）

## 常见 bug 清单

- send/recv 顺序写死对：rank 0 先 send、rank 1 先 recv 必须配对，反了直接死锁（PP 版的 hang 与 DDP 的 hang 是两种死法）
- micro-batch 的梯度忘了除以 $ m $ （和 Research 01 的 accumulation 同款 bug，PP 里再犯一次）
- 权重初始化跨 stage 不一致没关系（各段本来就不同），但同一段在 DP 副本间必须一致 —— PP 与 DP 组合时最容易漏
- 1F1B 的 warmup 步数算错：每段的 warmup 前向数 = $ p - \text{rank} - 1 $ ，写错一位整条流水线错位

> 可跑现场版在同名 notebook 第 3 节「Debug 演练」：BUG 1 micro-batch 没除以 m / BUG 2 stage 切分不均，每个 bug 下面带修复。

## 思考题

1. $ p=8, m=32 $ 时 bubble 占多少？$ m $ 翻倍到 64 省了多少，激活显存付了多少？
2. 为什么反向的 in-flight 激活在 1F1B 里是 $ p $ 份而不是 $ m $ 份？
3. 如果 stage 之间计算量不均（第一段 embedding 特别慢），气泡公式会怎么变？工程上怎么切才均衡？

---
*上一篇：Parallel 06 — TP 手写 linear · 并行基础线完（DDP/ZeRO-FSDP/TP/PP）*
