# G117 — varlen attention 配置详解：cu_seqlens、position_ids 与 packing 的配套关系
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G117-varlen-attention.html

## 元信息

- 编号：G117
- 标题：varlen attention 配置详解：cu_seqlens、position_ids 与 packing 的配套关系
- BV：BV1MZbj6zEeK
- 时长：01:55
- 发布日期：2026-09-17
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：FlashAttention varlen 接口

## 一句话总结

Packing 只负责把多条样本拼进一条定长序列省 padding，注意力不跨样本要靠 varlen attention：用 cu_seqlens 累计边界数组喂给 FlashAttention 的 varlen 接口自动按样本切片，同时 position_ids 在每个样本边界重置，两者缺一不可。

## 核心

1. **问题/背景**：packing 把短序列拼成一条后，若按普通注意力整条计算，不同样本会互相 attend，信息串扰、训练信号完全错误；只拼不用 varlen 等于省了算力却学错东西。
2. **机制/方法**：落地四步——先做 packing 把短序列拼成定长块（如 4096）；再算 cu_seqlens，即每个块内各样本的累计边界（0、第一条长度、前两条之和、…）；把边界数组传给 FlashAttention 的 varlen 接口，kernel 自动按样本切片做注意力；同时 position_ids 在每个样本边界处重置，保证每条样本的位置编码自成一套。
3. **关键证据或数字**：示例中 cu_seqlens 形如 [0, 200, 350, 4096] 表示一个块内拼了三条样本。
4. **结论/判断**：packing 与 varlen 是配套关系：前者省 padding 算力，后者保证不串题；配置时三件事必须齐——cu_seqlens 边界、varlen 接口、position_ids 边界重置。

## 可迁移

- 与 G011（SFT Packing 串样本）是同一议题的配置面版本：排障时先查框架开关是否真的打开了 varlen/position_ids 重置，而不是默认 packing 就安全；写自己的 packing 数据管线时，cu_seqlens 应在数据预处理阶段就算好随样本一起落盘。

## 疑问 / 下一步

- 不同框架（HF / TRL / LLaMA-Factory / veRL）打开 varlen 的开关名与默认行为不一致，实际用时需逐个核对文档与源码。
