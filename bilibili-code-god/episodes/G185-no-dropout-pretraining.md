# G185 — 大模型预训练为什么不用 Dropout？三个副作用与替代的正则化机制
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G185-no-dropout-pretraining.html

## 元信息

- 编号：G185
- 标题：大模型预训练为什么不用 Dropout？三个副作用与替代的正则化机制
- BV：BV1xY8468Evd
- 时长：02:48
- 发布日期：2026-09-06
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Dropout（Srivastava et al.）；GPT、LLaMA、Qwen 等主流模型预训练配方

## 一句话总结

Dropout 没被淘汰，是万亿 token 的数据规模让它失去用武之地：预训练阶段它只剩副作用，正则化由 weight decay、LayerNorm 与单 epoch 训练接管。

## 核心

1. **问题/背景**：Dropout 在训练时随机把一部分神经元输出置零，防止神经元过度协同适应，在 CV 与小模型时代几乎是标配；但 GPT、LLaMA、Qwen 等主流大模型预训练时都不用它。
2. **机制/方法**：核心原因是规模本身就是最强正则——模型在万亿 token 上训练，数据多样性使过拟合几乎不可能，模型连记住全部训练数据都做不到，Dropout 的边际收益微乎其微。而它的副作用却很实在：一是每次前向随机 mask、反向也要处理 mask，计算开销增加约 5%–10%；二是训练时丢弃信息等于浪费算力；三是在 attention 层加 Dropout 会扰动注意力权重分布，影响长依赖建模。
3. **关键证据或数字**：替代机制组合是 weight decay 做 L2 约束、LayerNorm 防激活爆炸、数据规模与多样性提供隐式正则、只跑一个 epoch 防记忆。Dropout 并非完全弃用：微调阶段数据量小、容易过拟合，可以打开，LLaMA 的微调配方建议 0.1–0.2，严重过拟合可到 0.3；分类头也可用；判读方法是监控 train loss 与 val loss 的差距。
4. **结论/判断**：实操上预训练不开（省算力、防信息损失），SFT 微调从 0.1 起步按过拟合程度调整，attention 与 FFN 层预训练时保持关闭。

## 关键数字

| 项 | 数值 |
|---|---|
| Dropout 计算开销 | 约 +5%–10% |
| SFT 微调建议值 | 0.1–0.2（严重过拟合至 0.3） |
| 预训练正则组合 | weight decay + LayerNorm + 单 epoch |

## 可迁移

- 回答「大模型怎么防过拟合」时，先讲数据规模与单 epoch，再讲显式正则，比罗列技巧更有结构。
- SFT 数据量小时记得 dropout 与早停是第一线手段，这与预训练的配方逻辑正好相反，容易在面试里被追问。

## 疑问 / 下一步

- 小规模 RL 微调（如几千条轨迹多 epoch 训练）是否应重新启用 dropout 防过拟合，视频未覆盖，值得留意。
