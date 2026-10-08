# G409 — Stable Diffusion 原理：潜空间扩散、CLIP、U-Net、cross-attention
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G409-stable-diffusion.html

## 元信息
- 编号：G409
- 标题：Stable Diffusion 原理：潜空间扩散、CLIP、U-Net、cross-attention
- BV：BV123Ks6YEfb
- 时长：03:35
- 发布日期：2026-07-20
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Latent Diffusion Models（Stable Diffusion，Rombach et al. 2022）；CLIP

## 一句话总结
Stable Diffusion 不在像素空间做扩散，而是先用 VAE 把图像压进小几十倍的潜空间，在潜空间里由 U-Net 迭代去噪、靠 cross-attention 注入 CLIP 的文本条件，最后再解码回像素。

## 核心
1. 问题/背景：扩散模型的生成方式是「从纯噪声出发，逐步去噪得到图像」。但一张 $512 \times 512$ 的彩色图摊开约 80 万维，直接在像素空间迭代几十上百步，算力完全扛不住。
2. 机制/方法：三段流水线——(1) 感知压缩：VAE 编码器把图像压成潜表示（如 $64 \times 64 \times 4$ ，约 1.6 万维），扔掉人眼不敏感的冗余，只留语义骨架；(2) 潜空间去噪：U-Net 在潜空间里反复预测当前表示中混入的噪声并减掉，逐步浮现图像轮廓；(3) 条件注入：CLIP 文本编码器把提示词变成文本向量，U-Net 每一步通过 cross-attention 把文本信息注入生成过程，决定「画什么」；最后 VAE 解码器把潜表示还原成像素图。
3. 关键证据或数字：潜空间维度约为像素空间的 $1/48$ ，后续每一步迭代的计算量随之同比缩小，这是它能在数秒内出图的根本原因。
4. 结论/判断：分工很清晰——VAE 管压缩与还原，U-Net 管去噪生成，cross-attention 管文本控制；「在压缩后的空间里做生成」是这条路线成立的前提。

## 关键数字
| 量 | 像素空间 → 潜空间 |
|---|---|
| 维度 | 约 80 万（ $512 \times 512 \times 3$ ）→ 约 1.6 万（ $64 \times 64 \times 4$ ） |
| 压缩比 | 约 48 倍 |

## 可迁移
- 面试讲文生图时按「为什么不在像素空间扩散 → 感知压缩 → 潜空间去噪 → cross-attention 条件注入」这条链组织答案，比罗列模块名更有说服力。
- 「先压缩再在低维空间做昂贵迭代」是通用优化范式，和 KV cache 压缩、量化推理是同一种思路。

## 疑问 / 下一步
- 潜空间压缩比继续加大时，细节保真（文字、人脸）先在哪里崩坏？可对照 SDXL / SD3 的 VAE 改进看。
