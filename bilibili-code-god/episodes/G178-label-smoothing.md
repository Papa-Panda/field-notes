# G178 — Label Smoothing 在大模型上为什么基本不用？

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G178-label-smoothing.html

## 元信息

- 编号：G178
- 标题：Label Smoothing 在大模型上为什么基本不用？
- BV：BV1cVbL6DEHz
- 时长：01:52
- 发布日期：2026-09-07
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Label Smoothing（Szegedy et al.）；GPT、LLaMA、Qwen 等主流大模型均未采用

## 一句话总结

Label smoothing 在图像分类里是标配，但大词表把它的假设打碎了：平滑出去的那点概率质量全撒到几万个无关词上，有害无益，GPT、LLaMA、Qwen 都不用。

## 核心

1. 问题/背景：Label smoothing 把 one-hot 标签从 $1$ 软化为 $1-\varepsilon$ ，其余概率均分给其他类别，防止 softmax 追求极端尖锐分布、让模型过度自信。在图像分类上有效（ImageNet 上 $\varepsilon=0.1$ 约涨 $0.5$ 个点），因为类别少、标签本身有噪声，承认模糊性有好处。
2. 机制/方法：它起作用的前提是「错类别之间差不多一样错」。换到 next-token prediction：多数位置的下一个词近乎确定，且词表有几万个 token，把 $\varepsilon$ 均分给所有词等于给完全无关的词发概率，系统性污染训练信号。
3. 关键证据或数字：主流大模型（GPT、LLaMA、Qwen）的训练配方里都没有 label smoothing；再加上大模型数据量极大、过拟合不是主要矛盾，它要解决的问题本身就不突出。
4. 结论/判断：不是 smoothing 本身不好，是几万词表打碎了它的假设。仍可试的场景：训练 loss 降到接近零、严重过拟合时；标签本身有模糊性的任务；以及蒸馏、噪声标签场景。真要用 $\varepsilon$ 取小，$0.05$ 或 $0.01$ ，不要照搬图像的 $0.1$ 。

## 关键数字

| 项目 | 数值 |
|---|---|
| 图像分类常用 $\varepsilon$ | $0.1$（ImageNet 约涨 $0.5$ 点） |
| 大模型场景上限（若用） | $0.05$ 或 $0.01$ |

## 可迁移

- 面试判断题模板：一个经典技巧到了 LLM 还成不成立，要看它的隐含假设（类别数、标签噪声、数据量）在新场景是否还成立，而不是记结论本身。
- 后训练里同类讨论：SFT 阶段过拟合通常靠数据配比和 epoch 数控制，而不是 label smoothing；偏好优化里对标签噪声的处理走的是另一套（丢弃低置信偏好对）。

## 疑问 / 下一步

- 视频提到蒸馏场景仍值得一试，但没给机制：软标签蒸馏本身已经提供平滑的教师分布，再叠 label smoothing 是否重复，值得查蒸馏文献确认。
