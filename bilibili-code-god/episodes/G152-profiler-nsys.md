# G152 — 给训练做体检：PyTorch Profiler 与 nsys 的用法与瓶颈定位

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G152-profiler-nsys.html

## 元信息

- 编号：G152
- 标题：给训练做体检：PyTorch Profiler 与 nsys 的用法与瓶颈定位
- BV：BV1eMbE6DEWh
- 时长：02:55
- 发布日期：2026-09-11
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：未标注

## 一句话总结

训练慢、GPU 利用率低时不要凭感觉猜：先用 PyTorch Profiler 看算子级耗时排名，需要更底层的时间线再用 nsys（NVIDIA Nsight Systems）看 kernel 调度与通信空泡，按利用率→传输→通信→kernel 四步定位瓶颈。

## 核心

1. **问题/背景**：profiling 就是给训练做全身检查，记录每一步每个操作的时间、显存与通信开销，用数据指出瓶颈在哪，而不是靠直觉调参。
2. **机制/方法**：两件工具分工。**PyTorch Profiler** 内置于 PyTorch，自动记录 CPU 操作、GPU kernel、内存分配，结果用 TensorBoard 可视化，一眼看到哪个操作最耗时，重点看各 kernel 的执行时间、CPU–GPU 传输时间和显存峰值（回顾里强调看 top-k 算子的 self time）。**nsys** 更底层，在 GPU 驱动层面记录，能看到 CUDA kernel 调度、NCCL 通信、CPU 线程切换的完整时间线，trace 可逐毫秒回放，多 GPU 时能看出哪张卡在等其他卡（找 kernel 之间的空泡）。
3. **关键证据或数字**：定位四步：GPU 利用率持续低于 90% 说明 GPU 在等待、瓶颈不在计算；CPU–GPU 传输占比高说明数据加载或权重同步是瓶颈；多卡 NCCL 通信占比超过 20% 就有优化空间；kernel 耗时前五名就是优化重点。对应解法：数据加载瓶颈加 workers、用 pin memory、预加载到 SSD；通信瓶颈用梯度压缩、通信计算重叠、增大 batch 减少 all-reduce 频率；kernel 效率低用 FlashAttention、算子融合、Tensor Core 友好的矩阵布局；显存碎片定期 `empty_cache` 或调分配器。
4. **结论/判断**：实操路径是先 Profiler 跑 5 个 step 看大概，不够再上 nsys 跑完整 trace，优化后必须再 profile 一次验证效果——先测量再优化，不要盲目调参。

## 关键数字

| 信号 | 判读 |
| --- | --- |
| GPU 利用率 < 90% | GPU 在等待，瓶颈不在计算 |
| NCCL 通信占比 > 20% | 通信有优化空间 |

## 可迁移

- RL 训练里 rollout 与训练两段的耗时拆分同样先 profile 再动手；这套「利用率→传输→通信→kernel」决策树可直接迁移到 verl 等框架的性能排障。
- 面试聊性能优化时，「先测量、按 top-5 kernel 下手、优化后复测」是比罗列优化技巧更可信的叙事。

## 疑问 / 下一步

- nsys trace 在大规模多节点训练里的采样开销与文件体积如何控制，视频未展开，可另查 Nsight 的采样模式文档。
