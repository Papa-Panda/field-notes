# B站 UP「古希腊掌管代码的神」视频纪要

按青稞Talk 同款流水线采集：枚举 → 字幕核验 → 提炼纪要 → HTML 阅读版。纪要为提炼总结（自有语言），不存逐字字幕。

- UP：古希腊掌管代码的神（UID 3632305977428186）
- 空间：https://space.bilibili.com/3632305977428186
- 总量：515 条（2026-03-28 – 2026-10-08），台账见 [catalog.md](catalog.md)
- 目录前缀：episodes/G<三位编号>-<slug>.md；编号顺序与 catalog 一致（新→旧）

## 进度

- 批 1（#1–#20）：20/20 完成（#8 于批 2 补齐）。
- 批 2（#21–#40）：20/20 完成。
- 批 3（#41–#60）：20/20 完成。
- 批 4（#61–#80）：20/20 完成。累计 80/515。

## 已完成纪要

| 编号 | 主题 |
|---|---|
| G001 | Terminal-Universe：轨迹倒推环境，SFT +11.9 |
| G002 | SFT 虚假遗忘：诊断与四步修法 |
| G003 | SFT 数据够不够：质量五维度与饱和点 |
| G004 | RL 微调 rank 1 LoRA 为何够用 |
| G005 | CrEST：多轮 Agent 信用分配 |
| G006 | SFT 与 RL 的顺序：两个基线 bug |
| G007 | SFT 过训与可塑性丧失 |
| G009 | GDPO：多奖励分开归一化 |
| G010 | DPO 训崩：似然位移与 β 错档 |
| G011 | SFT Packing 串样本与修复 |
| G012 | RL 训练 OOM：18 倍显存账 |
| G013 | Δlog p 定位 RL 改动的关键 token |
| G014 | 冷启动 SFT 该用多少条 |
| G015 | SFT 四个超参怎么设 |
| G016 | HORA / SARA：GRPO 采样预算分配 |
| G017 | GiGPO 等：多轮 Agent 稀疏奖励四条路 |
| G018 | DeepSeek-R1 配方（GRPO 入门 20） |
| G019 | Dr. GRPO 与 DAPO（GRPO 入门 19） |
| G020 | GRPO 改了 PPO 什么（GRPO 入门 18） |
| G008 | chat template 训推不一致的四种错法 |
| G021 | DPO 的推导：闭式解与隐式 reward |
| G022 | SFT 要不要给 prompt 算 loss |
| G023 | PPO 四模型与显存死穴（GRPO 入门 14） |
| G024 | 训练末期 grad norm 上升与 AdamC |
| G025 | LLMZero：RL 超参的 agent 诊断与树搜索 |
| G026 | KL 惩罚：β 取值与放奖励还是放损失 |
| G027 | 多样性坍塌在开头 token 与层插值 |
| G028 | RL 涨分还是背题：基准污染诊断 |
| G029 | RL 学习率为何比 SFT 小 10 倍 |
| G030 | Reward Model 训练：Bradley-Terry 细节 |
| G031 | QeRL：量化噪声当探索 |
| G032 | APRIL：partial rollout 治长尾 |
| G033 | RLHF 三阶段与对齐税 |
| G034 | GRPO 训练曲线的阻尼振子模型 |
| G035 | LLM 裁判的万能钥匙攻击与 Master-RM |
| G036 | OctoThinker：中段训练补推理语料 |
| G037 | 数据重复：记忆窗口决定过拟合 |
| G038 | 大模型即策略：老虎机与 token 级 MDP |
| G039 | 变长 SFT 梯度累积的归一化 bug |
| G040 | Cut Cross-Entropy 与 Liger Kernel |
| G041 | PPO 完整训练流程 |
| G042 | 奖励随机错 40% RL 还能训吗 |
| G043 | 进化策略 vs GRPO |
| G044 | SPT 专用预训练 |
| G045 | 多轮 Agent 工具 token 的 mask |
| G046 | 从 TRPO 到 PPO |
| G047 | TailSFT：为 RL 准备的 SFT |
| G048 | ARC / FACA：多轮交互 RL 学裁判偏好 |
| G049 | 重要性采样 |
| G050 | 思维链监控不能进 RL 奖励 |
| G051 | BroRL：rollout 16→512 |
| G052 | Likelihood Displacement 与安全 DPO |
| G053 | CPT Scaling Law |
| G054 | GAE 的 λ |
| G055 | 纯 bf16 训练停滞与舍入 |
| G056 | Adam β₂ 为什么是 0.95 |
| G057 | Actor-Critic 的代价 |
| G058 | 先 fuzz 你的 verifier |
| G059 | VerIF：硬约束代码校验 + 软约束模型判 |
| G060 | 中间阶段评估看流水线终点 |
| G061 | harness 原生 RL：训推同脚手架 |
| G062 | baseline 为什么无偏 |
| G063 | EnvHarness：改环境动态治饱和 |
| G064 | 层级 Dropout 与 1/ρ 缩放 |
| G065 | 策略梯度推导 |
| G066 | max response length 的放开节奏 |
| G067 | 多域混训 RL 的迁移矩阵 |
| G068 | DART-SD：多轮工具调用的 loss 位置 |
| G069 | CompactionRL：摘要纳入 RL |
| G070 | 蒙特卡洛 vs TD |
| G071 | Uniqueness-Aware RL |
| G072 | RL 后期熵暴涨 |
| G073 | V / Q / Advantage |
| G074 | RL 数据难度：跑 8 次筛题 |
| G075 | OPSA：不要老师的在线蒸馏 |
| G076 | VLM 要不要解冻视觉编码器 |
| G077 | VAPO：长 CoT 的 critic 七招 |
| G078 | 折扣因子 γ |
| G079 | SFT 六个决定 |
| G080 | Self-Routing：样本分四条路 |
