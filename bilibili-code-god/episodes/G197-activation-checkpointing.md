# G197 — 激活检查点选层策略：Uniform、Selective 与根号 n 法则
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G197-activation-checkpointing.html

## 元信息

- 编号：G197
- 标题：激活检查点选层策略：Uniform、Selective 与根号 n 法则
- BV：BV1xg8t6NEQW
- 时长：01:51
- 发布日期：2026-09-04
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：DeepSpeed（默认 uniform 策略）、FlashAttention 作者的检查点建议（字幕提及）

## 一句话总结

激活检查点用约 30% 的额外计算换显存：检查点数量取总层数的平方根是甜点，uniform 起步、再对大激活层做 selective 混合。

## 核心

1. **问题/背景**：正常训练要把每层激活都存进显存，长文本下显存吃不消；激活检查点只存少数层的激活，其余在反向时重算，本质是用计算换显存。
2. **机制/方法**：Uniform 策略等间距选检查点（如 80 层存 4 个、每 20 层一个），实现最简单、显存节省可预测，DeepSpeed 默认为此；缺点是所有层同等对待，而有些层激活大得多。Selective 策略只存激活大的层、跳过小的：Transformer 中 attention 层激活远大于 LayerNorm，同等显存预算下计算量更少、更高效。
3. **关键证据或数字**：检查点数量的经验法则是总层数的平方根（80 层约 9 个），激活显存从 $O(n)$ 降到 $O(\sqrt{n})$ ，计算开销增加约 30% 。
4. **结论/判断**：检查点不是存得越少越好，间隔取根号 n 才划算；实操从 uniform + 根号 n 开始，显存仍不够就减少检查点，追求效率再上 selective 混合（基础 uniform + 高开销层必存）。

## 关键数字

| 项 | 数值 |
|---|---|
| 检查点数量 | 总层数平方根（80 层 → 约 9 个） |
| 激活显存 | $O(n)$ → $O(\sqrt{n})$ |
| 额外计算开销 | 约 +30% |

## 可迁移

- RL infra 中 rollout/训练显存紧张时，先按根号 n 法则估检查点数，再对 attention 等大激活层做 selective，是低风险的显存优化顺序。
- 面试答激活检查点不要只说「用计算换显存」，要给出根号 n 的数量级与约 30% 的开销数字。

## 疑问 / 下一步

- Selective 策略在不同框架（Megatron / DeepSpeed / FSDP）里的实现粒度差异有多大，值得对照源码确认。
