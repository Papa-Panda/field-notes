# G151 — 可复现性详解：cuDNN、DataLoader 与分布式浮点误差三大随机源

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G151-reproducibility.html

## 元信息

- 编号：G151
- 标题：可复现性详解：cuDNN、DataLoader 与分布式浮点误差三大随机源
- BV：BV1iMbE6DEbj
- 时长：02:55
- 发布日期：2026-09-12
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：未标注

## 一句话总结

设了 seed 结果还飘，是因为只锁住了 Python 层随机数这一个源；cuDNN 非确定性算法、DataLoader 多进程随机状态、分布式 all-reduce 浮点求和顺序这三个隐藏随机源不逐一堵住，两次运行的 loss 曲线就对不上。

## 核心

1. **问题/背景**：同样代码、同样数据跑两遍 loss 曲线不一致，不是玄学。PyTorch 的 seed 只控制 Python 层面随机数，训练里还有多个隐藏随机源，每个引入的微小差异在百亿参数尺度上会累积放大成完全不同的结果。
2. **机制/方法**：三大随机源逐一堵。**cuDNN 非确定性算法**：默认用更快的非确定性算法（如原子加法的卷积/pooling，多线程写同一地址结果不确定），解法是设 `torch.backends.cudnn.deterministic = True` 强制确定性算法（慢一点但可复现），同时 `benchmark = False` 关掉自动算法选择。**DataLoader 多进程**：workers > 0 时每个进程有独立随机状态，seed 没传到每个 worker 则数据顺序不确定，解法是用 `worker_init_fn` 给每个 worker 设种子，且 DataLoader 内部的 random sampler 也要单独设种子。**分布式浮点误差**：all-reduce 的浮点加法不满足结合律，同梯度不同求和顺序结果有微小差异，解法是尽量固定归约顺序、接受微小差异，或用 fp32 归约减小舍入误差。
3. **关键证据或数字**：实操配置清单：设 Python / numpy / torch / CUDA 全部 seed；开 deterministic、关 benchmark；worker_init_fn 设种子；分布式用 barrier 同步；所有配置记入日志。现实目标不是逐位一致：同配置跑两遍 loss 趋势一致、最终效果差异在 1% 以内即可，差异大到影响结论才是 bug。
4. **结论/判断**：先测量差异有多大，再决定要不要追；完全复现尤其在多 GPU 上几乎不可能，目标是差异可控。

## 可迁移

- 复现别人 RL 结果对不上时，按「种子 / worker / 算子确定性 / 通信顺序」四项清单逐项排查，比反复重跑有效。
- 实验记录习惯：把完整配置落日志，是事后复现的前提，这条对 post-training 实验管理同样成立。

## 疑问 / 下一步

- 开 deterministic 对吞吐的实际损耗在自己的训练栈上有多大，值得实测一次再决定默认开关。
