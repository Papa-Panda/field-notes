# G209 — Google 用 sigmoid 替代 softmax——SigLIP vs CLIP 讲透
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G209-siglip-vs-clip.html

## 元信息

- 编号：G209
- 标题：Google 用 sigmoid 替代 softmax——SigLIP vs CLIP 讲透
- BV：BV1GZ846VETv
- 时长：04:23
- 发布日期：2026-09-02
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：CLIP（OpenAI, 2021）；SigLIP（Google, 2023）；InfoNCE；SigLIP 2

## 一句话总结

SigLIP 把 CLIP 对比损失里的 softmax 全局归一化换成逐对 sigmoid 二分类，去掉了对全 batch 的依赖，训练更简单、更省通信，且 batch 越大优势越明显。

## 核心

1. **问题/背景**：CLIP 的对比损失本质是 InfoNCE：正确图文对的相似度做分子，分母是 batch 内全部候选配对的相似度之和。这个分母要求每一步都看到全局相似度矩阵，分布式训练时需要跨 GPU 全局通信；batch 很大时，大量简单负样本还会稀释掉真正有价值的难负样本。CLIP 的扩展性天花板就卡在这个全局归一化上。
2. **机制/方法**：softmax 是「多选一」的全局归一化，sigmoid 是逐样本独立的二分类。SigLIP 让每一对图文独立判断匹配与否、输出 0 到 1 的概率，每对自成一个完整计算单元，梯度互不耦合。从 InfoNCE 的视角看，就是拿掉全局分母的简化版。各 GPU 可以各算各的，只在参数同步时通信。
3. **关键证据或数字**：Google 在 ImageNet 零样本分类上系统对比：ViT-B/16 从 CLIP 的 68.3% 提升到 SigLIP 的 69.7%；ViT-L/16 从 75.5% 提升到 77.1%。图文检索、多模态理解等下游任务打平或小幅领先，且 batch 越大相对优势越明显。SigLIP 已被 Gemini、Gemma 等 Google 系模型的视觉编码器采用；后续 SigLIP 2 在此基础上又加了 captioning 损失与自蒸馏，但 sigmoid 核心未变。
4. **结论/判断**：全局归一化不是对比学习的必需品；独立二分类同样能学到好表征，还换来更短的计算图和更好的大规模扩展性。

## 关键数字

| 模型 | CLIP | SigLIP |
|---|---|---|
| ViT-B/16（ImageNet 零样本） | 68.3% | 69.7% |
| ViT-L/16（ImageNet 零样本） | 75.5% | 77.1% |

## 可迁移

- 这是一个典型的「损失函数的归一化方式决定分布式通信模式」的案例：做 RL / 偏好学习时同样要问，一项损失是否隐含了跨样本、跨卡的耦合（如组内归一化），它会怎样影响扩展性与实现。
- 面试被问 CLIP 的改进版时，除了 ALIGN、FILIP，应能讲出 SigLIP 的 sigmoid 替换及其三点收益：更简单、更高效、更适合大规模。

## 疑问 / 下一步

- SigLIP 对可学习温度与偏置（bias）项的初始化较敏感，视频未展开；实际复现时值得查原论文的超参设置。
