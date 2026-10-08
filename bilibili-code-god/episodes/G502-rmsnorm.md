# G502 — LayerNorm为什么被RMSNorm全面取代？从0讲透归一化+手撕LLaMA同款代码

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G502-rmsnorm.html

## 元信息

- 编号：G502
- 标题：LayerNorm为什么被RMSNorm全面取代？从0讲透归一化+手撕LLaMA同款代码
- BV：BV1owTx6pEqM
- 时长：04:29
- 发布日期：2026-07-04
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：LayerNorm（2016）、RMSNorm（2019）、LLaMA、Google 大规模架构复现研究

## 一句话总结

RMSNorm 发现 LayerNorm 的功劳几乎全在「缩放」而非「平移归零」，于是砍掉算均值、减均值和 $\beta$ ，只用均方根把能量拧回标准刻度：参数减半、训练快约四分之一、效果一分不掉。

## 核心

1. **问题/背景**：几十层 block 堆叠时每层都会轻微放大或缩小数值，几十层连乘就是指数级爆炸或消失，训练必崩，所以要在每层入口装「音量校准器」——现代模型用 Pre-Norm，每个 block 在 attention 前和 FFN 前各装一次。
2. **机制/方法**：LayerNorm 三步——算均值、减均值归零、除以标准差，最后乘可学习 $\gamma$ 加可学习 $\beta$ 拉回表达力，两组参数向量、又管零点又管音量。RMSNorm 只留一步：算均方根（每个数平方取平均再开根号，即这组数的平均能量），全体除以它，最后乘 $\gamma$ 收工；条形形状和分布不变、均值信息保留，只把音量拧到标准刻度。归一化公式对比：

$$RMS(x) = \sqrt{\frac{1}{d} \sum_{i=1}^{d} x_i^2}$$

3. **关键证据或数字**：RMSNorm 原论文拆解实验表明 LayerNorm 的效果几乎全来自缩放不变性，减均值贡献微乎其微。同一翻译模型：LayerNorm 每 1000 步 665 秒，换 RMSNorm 只要 501 秒，快 24.7%，BLEU 还从 23.6 涨到 23.7。Google 大规模复现几十种 Transformer 魔改，绝大多数换框架就失灵，RMSNorm 是极少数真抗打的（SuperGLUE 71.66 → 75.45）。附带收益：参数减半、归约少算一趟、除数是能量加 $\epsilon$ 不易趋零、深层梯度更稳。
4. **结论/判断**：便宜、更快、不掉分，LLaMA 之后 Qwen、Mistral、DeepSeek、Gemma 全员标配，PyTorch 也已收进官方标准库，没人回头。

## 关键数字

| 事项 | LayerNorm | RMSNorm |
|---|---|---|
| 每 1000 步耗时（翻译模型） | 665 秒 | 501 秒（快 24.7%） |
| BLEU | 23.6 | 23.7 |
| SuperGLUE（Google 复现） | 71.66 | 75.45 |
| 可学习参数 | $\gamma$ + $\beta$ 两组 | 仅 $\gamma$ 一组 |

## 可迁移

- 手撕代码要点：RMSNorm 前向一行写完——平方取均值、加 $\epsilon$ 开根号取倒数乘回去，全程不减均值；被追问就答「LayerNorm 砍掉减均值和 $\beta$ 」。
- 读新模型架构时可以直接默认 Pre-Norm + RMSNorm，把注意力放在真正有差异的地方（注意力变体、FFN、位置编码）。

## 疑问 / 下一步

- 归一化位置之争（Pre-Norm vs Post-Norm vs 近年的新摆法）本期没展开，值得单独找一期/一篇补上。
