# G024 — 训练末期 grad norm 为什么反而上升？weight decay 与 LR 衰减的耦合，AdamC 一行修正
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G024-grad-norm-late.html

## 元信息

- 编号：G024
- 标题：训练末期 grad norm 为什么反而上升？weight decay 与 LR 衰减的耦合，AdamC 一行修正
- BV：BV1mMea6dEtA
- 时长：03:58
- 发布日期：2026-10-03
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Meta FAIR（Dehghani 等）关于 grad norm 末期上升与 AdamC（Adam with Corrected Weight Decay）的分析

## 一句话总结

长训练末期 grad norm 翻倍上升、loss 却正常下降，不是 bug 而是几何必然：归一化层前的权重与梯度正交，weight decay 把「梯度/权重」比值锁在与学习率成反比的稳态上，学习率衰减到零比值就冲向无穷；修法只有一行——让 weight decay 跟着学习率同步缩放（AdamC）。

## 核心

1. 问题/背景：现象在 120M 参数 Llama 架构、200B token、warmup + 余弦衰减的训练里看得很清楚：grad norm 曲线分三段——开头快速下降、中间长期平稳、最后 20% 学习率衰减段反而翻倍上冲，而 loss 仍在正常下降，与 loss spike 不是一回事；短训练（万 token 以下）看不到这个现象。
2. 机制/方法：关键前提是尺度不变性：紧跟归一化层的权重整体放大常数倍，归一化后输出不变、loss 不变（Transformer 里绝大多数矩阵满足，输出层与 embedding 除外）。尺度不变意味着 loss 沿权重方向无变化，于是梯度与权重正交。用勾股定理看一步 SGD + weight decay 的更新（新权重 = 衰减后的旧权重 − 学习率 × 梯度，两项垂直），稳态下令权重模长不变，解出梯度模长与权重模长之比被锁在 $\sqrt{2}$ 倍的「weight decay ÷ 学习率」附近：weight decay 像一根弹簧，把比值拉回稳态。
3. 关键证据或数字：问题出在学习率随时间衰减：余弦调度让分母趋向零，稳态比值趋向无穷；且学习率越小、追踪稳态的速度越慢，两个效应叠加，尾巴就炸了。修法一行：令每步的 weight decay 等于初始 weight decay 乘以「当前学习率 ÷ 峰值学习率」，代回稳态公式后学习率约掉，比值变成与时间无关的常数——这就是 AdamC，它不是新优化器，只是 AdamW 的 weight decay 调度修正，且只对归一化层前的权重做，输出层等保持标准 AdamW。实验上 200B token 训练中 grad norm 尾巴消失、权重范数不再快速下降、loss 全程更低；ImageNet 上 ResNet50 用 SGD 同样能消除末期上升。
4. 结论/判断：同一套推导顺带解释了经典面试题「AdamW 为什么优于 Adam」：推导对每个归一化层都成立，所有层的梯度/权重比会收敛到同一稳态，这正是单个全局学习率能训好几十层网络的原因；Adam 把 weight decay 以 L2 形式加进梯度，会被自适应分母按每层不同的尺度缩放，层间平衡被打破；AdamW 把 weight decay 从梯度中解耦、直接作用在权重上，平衡得以保住。实操三条：① 末期 grad norm 上升但 loss 正常，不是 bug，别急着把梯度裁剪调狠（那等效于降低学习率）；② 长训练 + 余弦/指数衰减 + 有归一化层，三个条件满足就用 AdamC，只需几行代码；③ 固定学习率或 WSD 的稳定段不受影响，没有归一化层的网络不适用这套分析。

## 可迁移

- 看训练日志时把「grad norm 末期上升 + loss 正常」识别为 weight decay 与 LR 调度的耦合伪影，避免误诊为数据或稳定性问题。
- 面试答 AdamW 优于 Adam，可从「解耦 weight decay 保住各层梯度/权重比的同一稳态」这一几何角度切入，比背定义更有说服力。

## 疑问 / 下一步

- Muon 等新优化器在归一化层前的权重上是否也有类似的稳态比值与调度耦合，值得查一下其实现是否做了等价修正。
