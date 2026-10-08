# G171 — 专家忙闲不均怎么治？aux loss 调参与 DeepSeek-V3 动态偏置
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G171-moe-load-balancing.html

## 元信息

- 编号：G171
- 标题：专家忙闲不均怎么治？aux loss 调参与 DeepSeek-V3 动态偏置
- BV：BV1kKbL6xEm1
- 时长：03:14
- 发布日期：2026-09-08
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：DeepSeek-V3（无辅助损失动态偏置方案）；Mixtral、GShard（aux loss 系数经验值来源）

## 一句话总结

MoE 路由的正反馈会让少数专家赢者通吃直至坍塌，经典解法是 aux loss 惩罚不均，DeepSeek-V3 改用路由偏置直接干预、且不掉点。

## 核心

1. **问题/背景**：Router 给每个 token 打分选 top-k 专家，但被选中越多的专家训练得越强、越强越容易被选中，形成马太效应。几轮之后可能只有三五个专家在干活、其余几十个完全闲置，即专家坍塌，MoE 退化成小 dense 模型。
2. **机制/方法**：方案一是辅助损失（aux loss）：统计每个专家分到的 token 比例，分布越不均辅助损失越大，乘系数 ， $\alpha$ ，加到总损失里，用梯度反过来逼 router 均摊负载。方案二是 DeepSeek-V3 的动态偏置（aux-loss-free）：给每个专家维护一个偏置项，近期被选太多的专家偏置上调以降低其被选概率、闲置专家则下调，偏置直接加在路由打分上干预决策，不靠损失间接惩罚。另有稳定化手段 router z-loss：惩罚 router logits 的平方和，防止 logits 过大导致 softmax 分布过尖、梯度不稳，思路与 attention 的 QK-norm 相通。
3. **关键证据或数字**：aux loss 系数 ， $\alpha$ ，的经验区间为 0.01 到 0.1（Mixtral 取 0.02、GShard 取 0.01），需按模型规模与专家数调整；， $\alpha$ ，太小均衡不住、继续坍塌，太大则强迫均匀使用不合适的专家、损害性能。z-loss 系数一般很小，约 0.001。
4. **结论/判断**：不干预则路由必然偏心；aux loss 简单有效但要拿性能换均衡，动态偏置更直接高效且不掉点，是更新的默认选项。调参的关键变量就是 ， $\alpha$ ，。

## 关键数字

| 项 | 取值 |
|---|---|
| aux loss 系数 $\alpha$ 经验区间 | 0.01–0.1 |
| Mixtral 的 $\alpha$ | 0.02 |
| GShard 的 $\alpha$ | 0.01 |
| router z-loss 系数 | 约 0.001 |

## 可迁移

- 训练 MoE 时把「每专家 token 占比」做成常驻监控曲线，坍塌在 loss 异常前就能从负载分布看出来。
- 面试答 MoE 负载均衡可按「aux loss 惩罚式 → 偏置干预式」两代方案展开，并带上 ， $\alpha$ ，的经验值与过大过小的双向失效模式。

## 疑问 / 下一步

- 动态偏置的更新步长如何设、与学习率如何配合，视频未展开，值得查 DeepSeek-V3 技术报告原文核对。
