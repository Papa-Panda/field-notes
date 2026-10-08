# G501 — 大模型为什么很少用Dropout？从过拟合讲到单epoch时代，config考古实锤

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G501-dropout-llm.html

## 元信息

- 编号：G501
- 标题：大模型为什么很少用Dropout？从过拟合讲到单epoch时代，config考古实锤
- BV：BV1YhT46HEhM
- 时长：03:56
- 发布日期：2026-07-04
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Dropout（2014）、GPT-2 / GPT-3、PaLM、LLaMA、LoRA

## 一句话总结

Dropout 没过时，是它的适应症消失了：预训练进入万亿 token 单 epoch 时代后模型根本没机会重复看数据、不存在过拟合，于是全员弃用；但小数据多 epoch 的微调场景里它依然在岗。

## 核心

1. **问题/背景**：过拟合本质是「背题」——训练 loss 一路下降、验证 loss 中途拐头向上，两条线的距离即泛化鸿沟；它只在小数据反复刷很多 epoch 时发生。
2. **机制/方法**：Dropout 训练时随机关闭一部分神经元（其余按比例放大保总量），每步都在训练一个不同的子网络，等价于白嫖指数级模型的集成，逼每个神经元学真本事。BERT、GPT-2、T5 时代数据只有十几 GB 到几百 GB、要刷几十个 epoch，0.1 的 dropout 是标配救命药。
3. **关键证据或数字**：大模型预训练语料涨到十几万亿 token，模型连一遍都看不完，训练/验证曲线贴着走、没有分叉，模型处于欠拟合而非过拟合。此时硬加 Dropout 是三宗罪：白扔容量、加噪拖慢收敛（GPU 时就是钱）、训练/推理行为不一致。配置考古：GPT-2 有整整 3 个 dropout 字段全是 0.1；LLaMA 的 config 通篇找不到 dropout；PaLM 论文明写不用 dropout；2025 年有实测表明单 epoch 预训练去掉 dropout 后语法、问答、推理成绩全面更好。
4. **结论/判断**：判断标准只有一条——数据会不会被重复看。会重复（SFT / LoRA 只有几千到几万条数据、刷好几个 epoch），过拟合就回来，LoRA 的 dropout 默认 0.05 至今保留。

## 关键数字

| 事项 | 旧时代 | 大模型时代 |
|---|---|---|
| 预训练语料量级 | 十几 GB–几百 GB | 十几万亿 token |
| 数据重复遍数 | 几十个 epoch | 单 epoch（甚至看不完一遍） |
| Dropout 设置 | 0.1（BERT / GPT-2 / T5） | 预训练弃用；LoRA 微调默认 0.05 |

## 可迁移

- 面试答「为什么大模型不用 Dropout」：先讲过拟合的前提条件（数据重复），再讲单 epoch 让前提消失，最后补一句微调例外，一条线说清。
- 自己跑 SFT/LoRA 时别盲目照搬预训练配置：小数据多 epoch 场景要把 dropout 和其它正则加回来。

## 疑问 / 下一步

- 多 epoch 训练推理模型（如 RL 阶段反复用同一批 prompt）时，Dropout 类正则是否会重新变得有价值，值得留意后续工作。
