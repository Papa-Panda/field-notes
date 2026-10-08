# G328 — π_θ/π_θ_old 是怎么算的？token-level log prob 的 3 个工程坑
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G328-token-logprob-pitfalls.html

## 元信息
- 编号：G328
- 标题：π_θ/π_θ_old 是怎么算的？token-level log prob 的 3 个工程坑
- BV：BV1Dw3d6BEYP
- 时长：04:40
- 发布日期：2026-08-06
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：PPO、GRPO、vLLM

## 一句话总结
PPO 的重要性采样比必须在 log 空间逐 token 累加计算，且 log-prob 计算路径要全程 FP32、用 log_softmax、复用 prompt 的 KV cache 并与 rollout 保持同一采样温度，否则 ratio 静默偏移、训练悄悄崩掉。

## 核心
1. **问题/背景**：训练数据来自旧策略，要优化新策略就必须用重要性采样比校正分布差异；但整句概率是逐 token 条件概率连乘，直接算会数值下溢到零，所以工程上没人直接算概率相除。
2. **机制/方法**：标准做法是先取对数再作差、最后取指数还原，即 $\log r = \log \pi_\theta - \log \pi_{\theta_{\text{old}}}$ ；整句的 log 概率等于逐 token 条件 log 概率之和，每个 token 都要单独取 logits 做 log_softmax 后累加。数值稳定三原则：用 log_softmax 而非对 softmax 输出再取 log；在 log 空间累加而非连乘概率；关键路径强制 FP32，因为 bf16 尾数只有 8 位，累加几十上百个 log prob 后误差足以让 ratio 明显偏移。
3. **关键证据或数字**：三个工程坑——(1) KV cache 复用：一次迭代要算新旧两个策略的 log prob，prompt 部分的 KV 只算一次缓存、两次 forward 共用，更进一步可在 rollout 阶段顺手把旧策略 log prob 算好存下，训练时省掉一次 forward，这也是推理框架 prefill/decode 分离的根源之一；(2) 温度一致性：rollout 用什么 temperature 采样，训练重算 log prob 必须用同一温度，否则重要性校正失效；(3) bf16 累加误差：logits 应先 cast 到 FP32 再做 log_softmax 与累加，bf16 下算出的 ratio 误差量级足以让 KL 爆炸。
4. **结论/判断**：GRPO 的 ratio 计算与 PPO 完全相同，只是优势估计从 critic 换成组内 baseline；PPO/GRPO 的工程难度不在公式，而在 log prob 的每一个实现细节。

## 可迁移
- 自研 RL 训练框架时，把 log-prob 计算路径单独定为 FP32 契约，并在对拍测试里专门检查 rollout 与训练两侧的温度、padding 与 mask 是否一致。
- 面试被问 PPO 落地难点时，按"逐 token 累加 + 三个坑（KV 复用、温度一致、bf16 误差）"的结构作答。

## 疑问 / 下一步
- 视频提到旧策略 log prob 在 rollout 阶段顺手算好——需核对 verl 等框架实际是在 rollout 还是训练侧重算，两者数值一致性如何保证。
