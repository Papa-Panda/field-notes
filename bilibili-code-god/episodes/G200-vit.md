# G200 — ViT 视觉 Transformer：把图像切成 patch，Transformer 也能做视觉
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G200-vit.html

## 元信息

- 编号：G200
- 标题：ViT 视觉 Transformer：把图像切成 patch，Transformer 也能做视觉
- BV：BV1VR846LEY6
- 时长：04:48
- 发布日期：2026-09-03
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：ViT 论文《An Image is Worth 16x16 Words》（Google，2020）

## 一句话总结

ViT 把图像切成 patch 当 token、原封不动塞进标准 Transformer（无卷积无池化），证明归纳偏置是拐杖：小数据打不过 CNN，大数据上反超，并成为多模态大模型的视觉基石。

## 核心

1. **问题/背景**：CNN 统治计算机视觉约 30 年（LeNet、AlexNet、ResNet、EfficientNet），共识是图像必须用卷积做。2020 年 Google 的 ViT 直接把 Transformer 原样搬到视觉上，在 ImageNet 做到 SOTA。
2. **机制/方法**：核心是把图像重新组织成序列：一张 224×224 图像按 16×16 切成 196 个 patch，每 patch 展平成 768 维向量，经可学习线性投影到模型维度，加上 1D 可学习位置编码，序列最前面拼一个 class token（借鉴 BERT）聚合全局信息做分类，主体就是标准 Transformer encoder——全程没有一个卷积核。三处关键设计：patch 越小 token 越多、归纳偏置越少但越吃数据；位置编码用 1D 而非 2D，消融显示 2D 感知没有明显提升，因为自注意力本身能学到空间关系。
3. **关键证据或数字**：与 CNN 的本质差异是归纳偏置：CNN 靠局部性先验在小数据集上快速收敛，ViT 第一层就是全局感受野、必须从数据里从头学。ViT-H/14 在 ImageNet 达到 88.55% top-1；但只有在 JFT-300M（3 亿张图像）量级预训练后才反超 CNN，只在 ImageNet-1K 上训还不如 ResNet。
4. **结论/判断**：归纳偏置数据少时有用、数据多时反而限制上限；ViT 后来成为 CLIP、BLIP、LLaVA 及各家 VL 模型的图像编码器，没有 ViT 就没有今天的多模态大模型。局限是吃数据，且自注意力计算量是 token 数的平方，高分辨率很贵，后续 Swin Transformer 即针对此改进。

## 关键数字

| 项 | 数值 |
|---|---|
| 224×224 图 @16×16 patch | 196 个 token |
| ViT-L/14 patch 切法 | token 数升至 256 |
| ViT-H/14 ImageNet top-1 | 88.55% |
| 反超 CNN 的预训练规模 | JFT-300M（3 亿张） |

## 可迁移

- 理解多模态架构时先抓住「视觉编码器 = ViT + projector 进 LLM」这条主线，CLIP/LLaVA 等都是它的变体。
- 面试对比 CNN 与 ViT 时用归纳偏置这条轴：局部性先验换小数据效率，无先验换大数据上限。

## 疑问 / 下一步

- 高分辨率下 token 数平方级膨胀，除了 Swin 的窗口注意力，patch 合并/ token pruning 在 VL 模型里哪种更主流？
