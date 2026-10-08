# G128 — 从零训练完整流程：专家初始化、router 设置与训练 schedule
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G128-moe-training-pipeline.html

## 元信息

- 编号：G128
- 标题：从零训练完整流程：专家初始化、router 设置与训练 schedule
- BV：BV1Qvb76VE4D
- 时长：01:48
- 发布日期：2026-09-15
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：DeepSeek-V3（负载均衡做法提及）

## 一句话总结

从零训 MoE 的胜负手在专家初始化与路由均衡，最稳的路线是先用 dense 模型打底，再把 FFN 复制成多个专家切成 MoE。

## 核心

1. 问题/背景：MoE 把每层的单个 FFN 换成多个专家加一个 router，需要同时训专家和 router，还要防止路由坍缩（所有 token 挤向少数专家）。
2. 机制/方法：专家初始化有三条路——随机初始化（不同种子）、从 dense 的 FFN 复制并加噪声打破对称性、从 dense 做 SVD 分解初始化；router 本质是一个线性层，用小标准差正态初始化、偏置为零，让训练早期路由接近均匀。训练路线同样分三档：先 dense warmup、从 dense 预训练权重替换 FFN 再微调、或直接从零训 MoE。
3. 关键证据或数字：负载均衡靠辅助损失（aux loss）或动态 bias 两手一起上，其系数 `alpha` 建议从 0.01 起试。
4. 结论/判断：专家数量不是决定因素；初始化方式和均衡机制才是。实践上「dense 复制 + 小噪声」是最实用的专家初始化。

## 可迁移

- 面试答 MoE 训练时，先讲「结构 = FFN 拆多专家 + router 选 top-k」，再讲初始化与防坍缩两件事，比堆专家数量更能打。
- 自己做 MoE 实验时，router 用小标准差初始化保证早期均匀，是低成本避免开局偏心的默认项。

## 疑问 / 下一步

- aux loss 系数与动态 bias 两种均衡手段在什么规模下各自更优，视频未展开，可结合 DeepSeek-V3 的做法对照看。
