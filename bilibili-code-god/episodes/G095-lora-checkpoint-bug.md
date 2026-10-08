# G095 — LoRA 开梯度检查点后 loss 纹丝不动，根因是什么？enable_input_require_grads 与 use_reentrant

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G095-lora-checkpoint-bug.html

## 元信息

- 编号：G095
- 标题：LoRA 开梯度检查点后 loss 纹丝不动，根因是什么？enable_input_require_grads 与 use_reentrant
- BV：BV1ezea6vE4D
- 时长：03:20
- 发布日期：2026-09-23
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Hugging Face Transformers / PEFT 的梯度检查点实现（该问题在相关仓库有多个 issue，从 2023 年排到 2026 年）

## 一句话总结

LoRA 冻结了 embedding，使梯度检查点第一段的输入不带梯度，重入式重算据此判定整段无可训参数而跳过反向，LoRA 梯度全为 None、训练在假跑；打开输入梯度并改用非重入实现即可修复。

## 核心

1. 问题/背景：开了梯度检查点后显存省了一半，但 loss 一步不动。三种症状：loss 曲线是直线；日志里只有一行警告（不是报错）说没有任何输入带梯度、梯度将为 None；或直接报错说 loss 不带梯度。共同点是训练在假跑，LoRA 权重拿不到梯度。
2. 机制/方法：梯度检查点只保存每段的输入，反向时从段输入重算一遍前向，用时间换显存。重入式实现（use_reentrant）在重算时检查段输入张量是否 requires_grad，没有就判定这段没有可训参数、直接跳过反向。LoRA 把基座全部冻结（包括 embedding），第一段的输入正是 embedding 的输出——一个不带梯度的张量，于是 autograd 在第一段就把链断掉，后面的 LoRA 权重全部拿不到梯度。
3. 关键证据或数字：修法三条——① 调用 `model.enable_input_require_grads()` ，给 embedding 输出注册 hook 把 requires_grad 打开，链就通了；② 开启顺序要先开 gradient checkpointing 再包 PEFT 模型，反过来可能没有任何权重带梯度；③ `use_reentrant` 设为 False（非重入实现不靠输入张量判断，更稳），并顺手关掉 use_cache。LLaMA-Factory 的做法是自定义检查点包装器、把浮点输入显式设为带梯度。另注意：新版 Trainer 检测到 PEFT 会自动调用 enable_input_require_grads，所以升级后问题消失不等于理解了它；use_reentrant 的默认值随 PyTorch 版本变，要显式写出来。
4. 结论/判断：这是 LoRA + 梯度检查点的静默失败组合，根因不在 LoRA 本身，而在「冻结 embedding → 段输入无梯度 → 重入式重算跳过反向」这条链。开训前花几秒做三项自检可以省掉几小时假跑：打印 requires_grad 为 True 的参数个数（应等于 LoRA 参数个数而非零）；跑一个 batch 前向后检查 loss 的 requires_grad 为 True；backward 后检查任意一个 LoRA 参数的 grad 非 None。

## 可迁移

- 排障习惯：loss 不动先查梯度链是否真的通——按「参数 requires_grad → loss requires_grad → 参数 grad 非 None」三点自检，比盯着 loss 曲线猜原因快得多。
- 面试/工程常识：梯度检查点的重入与非重入实现行为不同，框架默认值会随版本漂移，关键开关（use_reentrant、use_cache）要显式写进配置。

## 疑问 / 下一步

- 非重入实现虽然绕开了这个坑，但它与重入式在显存和速度上的取舍在不同框架版本下是否仍成立，值得在自己的训练脚本里实测一次。
