# G513 — QwenVL到Qwen3.5技术改进

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G513-qwenvl-qwen35.html

## 元信息

- 编号：G513
- 标题：QwenVL到Qwen3.5技术改进
- BV：BV1GpXaBGEoE
- 时长：03:36
- 发布日期：2026-03-29
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Qwen-VL、Qwen2-VL、Qwen2.5-VL、Qwen3-VL、Qwen3.5（阿里通义千问多模态系列）

## 一句话总结

五代 Qwen-VL 的演进主线是：视觉编码器越来越「LLM 化」、位置编码从绝对走向多维旋转、融合从浅层投影走向深度融合又回归简洁，训练阶段则越分越细。

## 核心

1. **问题/背景**：面试常问 Qwen-VL 各版本改了什么，这条线也是窥探多模态大模型发展史的窗口。
2. **机制/方法**：初代 Qwen-VL 是经典三段式：OpenCLIP ViT-bigG 视觉编码器（可学习绝对位置编码）+ 单层交叉注意力 projector（Perceiver Resampler，用 256 个可学习 query 把视觉特征压到固定长度）+ Qwen-7B，三阶段训练（对齐预训练冻 LLM → 多任务预训练全参数 → 指令微调冻视觉编码器）。Qwen2-VL 重训 675M ViT，引入 NaViT 与 2D 旋转位置编码支持动态分辨率；projector 改为两层 MLP 的 patch merger；位置编码移到 LLM 侧，升级为分别编码时间、高度、宽度的三维 M-RoPE。Qwen2.5-VL 让 ViT 更像 LLM：交错 window attention、FFN 换 SwiGLU、LayerNorm 换 RMSNorm，视频侧 M-RoPE 对齐真实帧率，训练加 SFT + DPO。Qwen3-VL 是最大升级：LLM 换 Qwen3 的 MoE 版本并引入 QK-Norm，DeepStack 在前若干层做视觉与语言特征的多层深度融合，M-RoPE 升级为交错版实现全频率覆盖，训练扩为四阶段、序列长度扩到 256K 并细化 RL 流程。Qwen3.5 则回归三段式（去掉 DeepStack），LLM 侧引入交错注意力架构：每 4 层中 3 层 Gated DeltaNet + 1 层 gated attention（3:1），可看作 Qwen3-Next 的多模态版，改进重心转到预训练数据与 RL 规模化。
3. **关键证据或数字**：patch merger 通过 spatial merge 把 patch 数压到原来的 1/4 ；Qwen2-VL 训练规模约 600B–800B token ；Qwen3.5 的线性/全注意力层配比为 3:1 。
4. **结论/判断**：三条趋势——ViT 结构持续向 LLM 靠拢（归一化、激活、注意力形态统一）、位置编码从绝对 → 旋转 → 多维旋转、训练策略从三阶段粗分走向四阶段 + RL 精细化；Qwen3.5 的「回归」说明深度融合的收益未必抵得过简洁架构 + 线性注意力的效率账。

## 关键数字

| 维度 | 初代 Qwen-VL | 近期版本（Qwen3-VL / 3.5） |
| --- | --- | --- |
| projector | 交叉注意力，256 个 query | 两层 MLP patch merger，patch 数压到 1/4 |
| 位置编码 | 可学习绝对位置编码 | M-RoPE 三维 / 交错版，全频率覆盖 |
| 训练阶段 | 3 阶段 | 4 阶段 + 细化 RL，序列长度 256K |

## 可迁移

- 面试答多模态演进时按「编码器 / 连接器 / 位置编码 / 训练策略」四条线组织，比逐版本背发布说明更有结构。
- DeepStack 被 Qwen3.5 放弃是一个提醒：架构创新要算总账（收益 vs 复杂度与推理成本），这与做 RL infra 时选机制的逻辑相通。

## 疑问 / 下一步

- Qwen3.5 用 Gated DeltaNet 替代大部分全注意力层后，长视频等长上下文场景的精度保持如何，值得找官方技术报告核对。
