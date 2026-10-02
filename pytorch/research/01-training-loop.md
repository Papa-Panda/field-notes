# Research 01 — 训练循环零起（Training Loop from Scratch）

- **定位**：Research PyTorch 轮次的底盘。这一轮考的不是会不会用 Trainer，是给你一段裸训练代码，能不能现场看出它错在哪、改对。
- **配套 notebook**：[01-training-loop.ipynb](01-training-loop.ipynb)（Colab 可直接跑，CPU 即可）

## 一句话总结

一个训练 step 只有五件事：forward → loss → zero_grad → backward → step。所有的坑都藏在顺序和状态管理里。

## 核心（动机 + 机制）

**为什么 zero_grad 必须手动调？** PyTorch 的 autograd 默认**累积**梯度（`.grad +=`），不清零会让上一步的梯度污染这一步。这不是 bug，是设计：梯度累积（grad accumulation）就是靠这个机制实现的。

**一个 step 的状态变化**（以 SGD+momentum 为例）：

- forward：用当前参数 $ \theta_t $ 算出预测，autograd 建计算图
- backward：链式法则回填 $ \nabla_\theta \mathcal{L} $ 到每个参数的 `.grad`
- step：更新规则 $ \theta_{t+1} = \theta_t - \eta \cdot \hat{g}_t $ ，其中 SGD 的 $ \hat{g}_t = g_t + \mu v_t $ ，Adam 的 $ \hat{g}_t = \hat{m}_t / (\sqrt{\hat{v}_t} + \epsilon) $

**scheduler 顺序**：PyTorch 1.1 之后，`optimizer.step()` 必须在 `scheduler.step()` **之前**，否则第一个 epoch 的 lr 会被跳过。面试常考。

**grad accumulation 的等价性**：batch 切成 $ k $ 个 micro-batch，每个做 `loss/k` 再 backward，最后 step —— 梯度严格等于大 batch 一步（只差浮点误差）。除以 $ k $ 是关键，忘了除就是把 lr 放大了 $ k $ 倍。

**eval 三件套**：`model.eval()`（关 dropout/BN 的 train 行为）+ `torch.no_grad()`（不建图，省显存）+ 测完切回 `model.train()`。漏了 no_grad 是最常见的显存溢出原因之一。

## 面试考点

1. loss 不下降的排查顺序：先看 lr 量级 → 数据/label 对齐 → 梯度有没有回传（`param.grad` 是否为 None）→ 参数有没有真的在更新（`p.data` 前后对比）
2. `optimizer.step()` 前 `zero_grad()` 和之后的区别（前后等价，但必须每步一次）
3. AMP 混合精度：`autocast` 包 forward、`GradScaler` 包 backward→step，GradScaler 必须在 unscale 后再 clip

## 常见 bug 清单

- 忘了 `zero_grad()` → 梯度无限累积，loss 玄学震荡
- eval 时忘 `no_grad()` → 显存涨、验证集越大越慢
- `scheduler.step()` 放在 `optimizer.step()` 前 → lr 曲线整体错位一格
- accumulation 忘除 $ k $ → 等效 lr 爆炸
- 用训练集的 running loss 报 test 指标（没切 eval 模式，BN 统计量被污染）

## 思考题

1. 如果把 zero_grad 放在 step 之后、backward 之前，和放在 backward 之前等价吗？什么情况下不等价？（提示：梯度累积多步时）
2. Adam 的 $ \hat{m}, \hat{v} $ 做 bias correction 是为了解决什么时期的什么问题？
3. 为什么 clip_grad_norm 要在 scaler.unscale_ 之后调用？

---
*下一篇：Research 02 — DPO loss 手写 + debug（这一轮的正主）*
