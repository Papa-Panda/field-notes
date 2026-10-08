# G182 — GPU 利用率周期性归零：IO 瓶颈的定位与优化
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G182-gpu-io-bottleneck.html

## 元信息

- 编号：G182
- 标题：GPU 利用率周期性归零：IO 瓶颈的定位与优化
- BV：BV1xfb56cEdo
- 时长：03:14
- 发布日期：2026-09-06
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Alluxio 数据缓存、WebDataset 数据打包格式

## 一句话总结

GPU 利用率周期性归零几乎不是算力问题，而是数据喂不上：定位到 CPU 预处理与远程存储两处根因，再用 DataLoader 四参数加缓存层解决。

## 核心

1. **问题/背景**：GPU 算完一个 batch 后要等下一批数据就绪；数据加载慢时，每批之间出现几百毫秒到几秒的空转，利用率呈周期性归零，整体训练速度远低于预期。
2. **机制/方法**：根因一是预处理太慢——tokenization、数据增强、动态 padding 若都压在主线程里串行现算，必然跟不上 GPU 消费速度，解法是多进程并行预处理加锁页内存加速 CPU 到 GPU 的传输。根因二是存储读取慢——数据放在 NFS 上时单文件延迟可达几十毫秒，海量小文件（如每个几 KB 的 JSON）场景下读取开销远大于数据本身，解法是把数据预打包成大文件、内存映射读取，或预取到本地 SSD。
3. **关键证据或数字**：DataLoader 四个关键参数——`num_workers` 设为 GPU 数的 2–4 倍、`pin_memory` 开启、`prefetch_factor` 设 2–4 提前备好下一批、`persistent_workers` 避免每个 epoch 重启 worker。在存储与 GPU 之间加 Alluxio 缓存层把热点数据预取到 SSD 与内存，知乎团队报告 GPU 利用率可从约 60% 提升到 90%。
4. **结论/判断**：利用率上不去先别怀疑算力，先看数据流水线；IO 优化在大规模分布式训练里是标配而非可选项。

## 关键数字

| 项 | 基线 | 优化后/建议值 |
|---|---|---|
| GPU 利用率（Alluxio 缓存） | 约 60% | 约 90% |
| num_workers | 默认单进程 | GPU 数的 2–4 倍 |
| prefetch_factor | 默认 | 2–4 |

## 可迁移

- RL 训练里 rollout 与训练共用机器时，数据侧的 IO 抖动会直接放大 step 时间方差，排障顺序应先看利用率波形再看算子。
- 面试谈训练吞吐优化时，「预打包大文件 + 多进程加载 + 缓存层」是完整的三段式答案。

## 疑问 / 下一步

- 自己的训练脚本里 `num_workers` 与 `persistent_workers` 当前取值如何，值得对照清单逐项核一遍。
