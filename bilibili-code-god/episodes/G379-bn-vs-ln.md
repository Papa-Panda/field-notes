# G379 — BatchNorm 与 LayerNorm 的区别：为什么 Transformer 只用 LayerNorm？
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G379-bn-vs-ln.html

## 元信息
- 编号：G379
- 标题：BatchNorm 与 LayerNorm 的区别：为什么 Transformer 只用 LayerNorm？
- BV：BV1j7gD6cE75
- 时长：03:00
- 发布日期：2026-07-22
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Batch Normalization（Ioffe & Szegedy, 2015）；Layer Normalization（Ba et al., 2016）

## 一句话总结
BN 与 LN 公式一模一样，唯一区别是统计方向：BN 跨 batch 对同一特征归一化，LN 对单个 token 跨特征归一化——方向决定了 LN 天然适配变长文本。

## 核心
1. 问题/背景：两种归一化做的事相同——减均值、除标准差，再乘可学习缩放 $\gamma$ 、加平移 $\beta$ 。区别只在均值方差沿哪个方向、在哪些数上统计。
2. 机制/方法：把数据看成 batch × token × feature 的立方体。BN 固定某个特征、跨整个 batch 收集所有样本在该特征上的值统计（竖着切）；LN 固定某个 token、只用这个 token 向量自己的全部特征统计（横着切），每个 token 独立处理，与其他样本无关。
3. 关键证据或数字：BN 用在文本上有两处硬伤——其一，batch 内句子长短不一，短句靠 padding 补齐，跨 batch 统计会把无意义的 pad 也算进去、污染真实 token 的分布；其二，同一 token 在不同 batch 里和不同邻居一起归一化，处理方式随 batch 随机变化，破坏上下文一致性；再加上推理时 batch 常为 1，BN 统计量根本不可靠。LN 逐 token 独立归一化，这三个坑全部避开。
4. 结论/判断：一句话记法是「BN 看别人，LN 看自己」；从 Transformer 到今天的大模型，归一化清一色用 LN 及其变体（如 RMSNorm）。

## 可迁移
- 面试答 BN/LN 不要只背定义，要落到 NLP 场景的两个具体失效模式（pad 污染、跨 batch 不一致）加推理 batch=1 的统计问题。
- RL/推理服务里 batch 大小动态变化，用 LN 类归一化保证了单条样本的数值行为不随同批样本改变，调试时少一类诡异不一致。

## 疑问 / 下一步
- RMSNorm 省掉了减均值一步只保留缩放，它为什么在大模型上效果不降，值得与 LN 做一次对照推导。
