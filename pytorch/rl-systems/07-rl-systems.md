# RL Systems 07 — rollout→train 的系统骨架

- **定位**：RL track 第三轮（RL systems coding）的主题：不是写 loss，是把"生成—打分—训练"三段搭成一个能跑的系统，并说清每段之间的接口与代价。
- **配套 notebook**：[07-rl-systems.ipynb](07-rl-systems.ipynb)（Colab 可直接跑）

## 一句话总结

RL 训练的系统难点不在 loss，在负载错配：生成是访存瓶颈的推理负载、训练是算力瓶颈的矩阵乘负载，两者节奏不同。同步式互相等待，异步式拿样本新鲜度换利用率。

## 核心（动机 + 机制）

**为什么 RL 比 SFT 难 scale**。SFT 的样本是现成的，训练就是一条流水线。在线 RL 的样本是 policy **自己生成**的：生成（rollout）慢在自回归解码（逐 token、访存受限、要靠推理引擎的 continuous batching 才喂得饱），训练（learner）慢在大矩阵乘。把两段绑在同一批 GPU 上轮流跑，任何一段工作时另一段都在闲置。

**系统拆成三段**：

| 段 | 干什么 | 瓶颈 | 典型实现 |
|---|---|---|---|
| Rollout | 用当前策略采样 trajectory | 显存带宽（解码） | vLLM 式推理引擎、独立 GPU 池 |
| Reward | 给 trajectory 打分 | 外部服务延迟 | 规则验证器 / reward model / 代码沙盒 |
| Learner | 用 trajectory 算 loss 更新策略 | 算力（FLOPs） | 训练框架（本系列前几篇的世界） |

**Trajectory 的存储格式是三段的接口契约**，至少要有：prompt、completion 的 token ids、**采样时每个 token 的 logp**、reward、**策略版本号**。logp 和版本号不是可选项：异步下样本来自旧策略，learner 要用它们做重要性采样修正和新鲜度过滤；缺了这两样，off-policy 的程度无法量化，只能盲训。

**同步 vs 异步**：

- 同步：rollout 一批 → 训练 → 换新权重再 rollout。样本永远 on-policy（版本号差 = 0），但 GPU 利用率被两段的串行等待吃掉。
- 异步 actor-learner：rollout worker 持续生成、learner 持续消费，利用率高；代价是样本滞后 $ k $ 个版本，分布偏移随 $ k $ 涨，靠重要性权重截断（如 ratio clip 进 PPO 目标、或直接丢弃太旧的样本）控制。

**权重同步**：learner 每更新一次，版本号 +1；新权重推送给 rollout 引擎的时机决定滞后分布。停顿式同步（训完一批统一换）简单但有气泡；滚动更新（worker 各自在空闲时换）平滑但版本分布更散。

## 面试考点

1. 为什么 RL 训练要把生成和训练拆开部署（负载画像完全不同：带宽 vs 算力、batch 形态不同）
2. 同步/异步的取舍：on-policy 纯度 vs GPU 利用率，滞后几个版本开始伤害效果
3. trajectory 里为什么必须存采样 logp 和版本号（重要性采样 + 新鲜度过滤的输入）
4. reward 服务的工程问题：超时、重试、批量打分、reward hacking 的监控（reward 涨但真实质量跌的检测）
5. 一次权重更新后 rollout 引擎换权重的代价（重新加载权重、KV cache 失效）

## 常见 bug / 事故清单

- **stale policy 盲训**：没记版本号，异步样本滞后十几代还在当 on-policy 用 → 训练发散且看不出原因
- **logp 对不齐**：存的 logp 是生成引擎算的，learner 重算时因数值精度/实现差异对不上 → ratio 系统性偏移，先写一个 logp 一致性检查再谈调参
- **reward 超时拖死流水线**：reward 服务慢调用没有超时和降级，一批 trajectory 卡住全体等待
- **权重推送竞态**：rollout 正在生成时权重被换一半 → 同一条 trajectory 前后半段来自不同策略，logp 全废
- **截断样本当完整样本训**：超长被截断的 completion 没有 mask 标记，模型学到"戛然而止也算对"

## 思考题

1. 异步滞后 $ k $ 个版本时，重要性 ratio 的分布会怎么变？clip 区间要不要随 $ k $ 调整？
2. 如果 reward 只能给序列级分数（没有 token 级），credit assignment 在系统层能做什么补救？
3. rollout 引擎换权重的气泡时间怎么估算？和模型大小、权重传输带宽什么关系？

---
*上一篇：Parallel 06 — TP 手写 linear · 本系列阶段 3 首篇*
