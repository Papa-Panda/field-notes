# G172 — ZeRO Stage 怎么选、offload 怎么开：config.json 手把手
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G172-zero-offload-config.html

## 元信息

- 编号：G172
- 标题：ZeRO Stage 怎么选、offload 怎么开：config.json 手把手
- BV：BV1WTbL6REnE
- 时长：02:15
- 发布日期：2026-09-08
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：DeepSpeed ZeRO

## 一句话总结

DeepSpeed 配置的核心是 ZeRO 分级切分显存：切得越深越省显存、通信越贵，选型按模型规模逐级升档，真 OOM 才开 offload。

## 核心

1. **问题/背景**：DeepSpeed 的 config.json 有几十个参数，但真正决定显存与速度的是少数几个：zero optimization、optimizer、scheduler、bf16 混合精度与 activation checkpointing，其中 zero optimization 决定模型状态怎么在卡间切分。
2. **机制/方法**：ZeRO 三级递进——Stage 1 只切优化器状态，最保守；Stage 2 再切梯度；Stage 3 连参数一起切，最省显存。Offload 是在此之上的进一步卸载：offload optimizer 把优化器状态放 CPU（Stage 2 加它约省四倍参数量对应的优化器显存），offload param 把参数也放 CPU，最省但最慢。原则是能用 Stage 2 就不上 Stage 3，offload 只在 OOM 时逐级打开：先 Stage 2，OOM 再加 optimizer offload。精度侧强烈建议 bf16，配置里 loss scale 设 0 即可；只有 fp16 才需要 loss scale 与 initial scale power 等动态缩放参数。
3. **关键证据或数字**：给了两套实操模板：7B、8 卡 A100 用 Stage 2 + optimizer offload + bf16 + activation checkpointing + gradient clipping 1.0，每卡约 40 GB；70B 则升 Stage 3 并加 param offload。规模分界大致为：7B 以下 Stage 1，7B–30B Stage 2，30B 以上 Stage 3。
4. **结论/判断**：ZeRO 选型是一条「显存不够才升档」的阶梯：切得越深通信越贵，不要一上来就全开；bf16 是默认精度选择。

## 关键数字

| 模型规模 | ZeRO Stage | 备注 |
|---|---|---|
| 7B 以下 | Stage 1 | 只切优化器状态 |
| 7B–30B | Stage 2 | 再切梯度 |
| 30B 以上 | Stage 3 | 连参数一起切 |
| 7B / 8×A100 实例 | Stage 2 + optimizer offload | 每卡约 40 GB |

## 可迁移

- 写 DeepSpeed 配置时按「规模定 stage → OOM 再逐级加 offload」的顺序决策，避免无谓的通信开销拖慢吞吐。
- 与自研训练框架对照：ZeRO 的分级切分本质是显存—通信权衡曲线，面试聊分布式训练时可直接借这条阶梯组织答案。

## 疑问 / 下一步

- Stage 3 + param offload 的实际吞吐损失量级视频未给数字，值得在自己的小规模实验里测一次对照。
