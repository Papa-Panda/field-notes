# G011 — SFT Packing 为什么会串样本？position ids 重置、varlen 分块注意力与各框架开关
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G011-sft-packing.html

## 元信息

- 编号：G011
- 标题：SFT Packing 为什么会串样本？position ids 重置、varlen 分块注意力与各框架开关
- BV：BV1ETHn6yEUv
- 时长：03:01
- 发布日期：2026-10-06
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：FlashAttention varlen 接口、HuggingFace DataCollatorWithFlattening、verl 的 remove-padding（rmpad）

## 一句话总结

Packing 把多条短样本拼成一条长序列省掉 padding 浪费，但必须同时做 position ids 逐样本重置和样本内分块注意力，否则样本间互相可见，模型学到的是被污染的条件分布。

## 核心

1. **问题/背景**：一个 batch 内样本长短悬殊（如最长 4000、最短 200 token），padding 到最长后 attention 与 FFN 大量算力耗在 pad 位置上，一半以上算力浪费是常态。Packing 把多条短样本首尾相接拼成接近上限长度的一条序列，几乎没有 pad；但若 attention 仍是普通因果掩码，第二条样本能看到第一条的全部内容、位置编码也接着编，这就是串样本（cross-contamination）：训练 loss 看起来正常，评测时单条输入反而表现异常。
2. **机制/方法**：正确姿势两件套——① position ids 每条样本从 0 重新开始；② attention 只在样本内部做，FlashAttention 的 varlen 接口接受一个记录各样本边界的 cu_seqlens 数组，按块分别算注意力，数学上等价于块对角 mask，但不需要真的构造那个大 mask 矩阵。HF 的 DataCollatorWithFlattening 就是这套：把 batch 展平成一条、自动生成 position ids，模型开 FlashAttention-2 时自动走 varlen 路径。
3. **关键证据或数字**：视频称实测吞吐最高 2 倍、平均约 1.4 倍，且训练 loss 与不 packing 完全一致。各框架开关：verl 用 use_remove_padding（rmpad）；TRL 的 SFTTrainer 有 packing 参数，注意新版默认是不串样本的 BFD 模式、旧版 packing 会串；LLaMA-Factory 的 neat packing 专门指不串样本的那种。
4. **结论/判断**：两个副作用要一起处理——① 有效 batch 变了：packing 后一个 batch 里的样本数不固定，loss 按 token 归一化时长度量权重不同，学习率与 epoch 的口径要重新核算；② 每条样本的结束符 EOS 必须在拼接时保留，否则模型学不会停。上线前把一条 packed 序列解码出来肉眼检查边界。

## 关键数字

| 指标 | 基线 | 结果 |
|---|---|---|
| 训练吞吐（packing vs padding） | 1 倍 | 最高 2 倍、平均约 1.4 倍 |
| 训练 loss | 不 packing | 与 packing 完全一致 |

## 可迁移

- 面试答 packing 直接给三件套：position ids 重置、cu_seqlens 分块、varlen 内核等价块对角，再补两个副作用（有效 batch 与 loss 归一化、EOS 保留）就是完整答案。
- 自查清单：换框架或升级版本后，先解码一条 packed 序列确认边界与 EOS，再看 loss 归一化口径是否与超参假设一致。

## 疑问 / 下一步

- rmpad / BFD 这类「按 token 预算动态组 batch」的方案，与静态 packing 在梯度噪声和吞吐上各自适合什么数据分布？
