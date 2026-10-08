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
- 批 4（#61–#80）：20/20 完成。
- 批 5（#81–#100）：20/20 完成。
- 批 6（#101–#120）：20/20 完成。
- 批 7（#121–#140）：20/20 完成。
- 批 8（#141–#160）：20/20 完成。
- 批 9（#161–#180）：20/20 完成（其中 4 条首轮 harvest 串台，re-harvest 补齐）。累计 180/515。

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
| G081 | RL 到底在学什么 |
| G082 | RL 微调的幻觉税与 SUM |
| G083 | 无标准答案任务的 RL：裁判配参考 |
| G084 | 长程工具 Agent 的 RL 配方 |
| G085 | SFT token 选择：Rho-1 与 ProFit |
| G086 | SFT 后措辞鲁棒性 |
| G087 | RL batch 与 √B 学习率缩放 |
| G088 | RL 后 Agent 更爱作弊与环境加固 |
| G089 | 在线蒸馏的数据效率 |
| G090 | SFT 教新知识反而更爱编 |
| G091 | RLVE：程序化可验证环境 |
| G092 | ProRL：停滞时重置参考策略 |
| G093 | 线上流量变后训练（T-Tech） |
| G094 | 探针裁判 |
| G095 | LoRA 梯度检查点 loss 不动排障 |
| G096 | Qwen3 思考/非思考融合 |
| G097 | RL 防遗忘靠 on-policy 数据 |
| G098 | OTC-PO：工具生产率进奖励 |
| G099 | OraRL：标准答案进 GRPO 的优势反转 |
| G100 | MOPD：多教师在线蒸馏 |
| G101 | 训推不一致是优化问题 |
| G102 | RLVR 该不该给格式奖励 |
| G103 | BCIT：配方跨基座复用 |
| G104 | μ-GRPO：250 倍陈旧数据 |
| G105 | k3 估计器与 KL 梯度偏差 |
| G106 | R3：重放路由治 MoE RL 崩溃 |
| G107 | GRAPE：按目标模型概率选数据 |
| G108 | GPT-OSS 做 RL 的三个坑 |
| G109 | River：过滤劣质合成环境 |
| G110 | SIGNBALANCE 与 DA3PO |
| G111 | Distilled RL |
| G112 | Cliff：标注第一处出错 |
| G113 | Batch 不变内核 |
| G114 | PPO-EWMA：异步 RL 重要性比拆分 |
| G115 | Agent-Omit |
| G116 | WandB / TensorBoard 与六大指标 |
| G117 | varlen attention 配置 |
| G118 | 预训练数据配比 |
| G119 | credit assignment 与 GRPO advantage |
| G120 | 投机解码加速 rollout |
| G121 | 学习率实操：十分之一法则 |
| G122 | SFT 数据自动筛选三段流水线 |
| G123 | Packing 实现：装箱与 varlen 隔离 |
| G124 | 序列长度与分阶段扩展 |
| G125 | rollout 采样温度 |
| G126 | 探索与利用 |
| G127 | 中英数据配比 |
| G128 | 从零训 MoE：初始化与路由 |
| G129 | Model Soup |
| G130 | target KL 与 KL 曲线诊断 |
| G131 | 同步 vs 异步：staleness |
| G132 | 梯度范数基线与预警阈值 |
| G133 | 数据污染三重检测 |
| G134 | 早停配置 |
| G135 | DPO 的 beta 参数 |
| G136 | 长度分桶 |
| G137 | 数据不均衡诊断与配比 |
| G138 | 数据去重：MinHash + LSH |
| G139 | 持续学习三路线：回放/EWC/adapter |
| G140 | 代码与数学数据配比 |
| G141 | Best-of-N 与 RFT |
| G142 | benchmark 分数为什么会骗你 |
| G143 | 标注质控与 Cohen Kappa |
| G144 | 初始化标准差 0.02 的由来 |
| G145 | Weight Decay 与 AdamW 解耦 |
| G146 | warmup 步数 |
| G147 | 训练 pipeline 与 PAFT 并行范式 |
| G148 | loss 之外必看的五指标 |
| G149 | 评测频率：proxy 高频 / 完整低频 |
| G150 | train vs val loss 判读 |
| G151 | 可复现性三大随机源 |
| G152 | Profiler 与 nsys 做训练体检 |
| G153 | tokenizer 词表设计 |
| G154 | token mean vs sequence sum |
| G155 | 合成数据 pipeline |
| G156 | 压力测试六维度 |
| G157 | 红队测试实操 |
| G158 | reward 归一化 |
| G159 | rollout 瓶颈：vLLM + 异步 |
| G160 | entropy bonus 与熵坍缩 |
| G161 | RL batch 组织策略 |
| G162 | reward hacking 与 Goodhart 定律 |
| G163 | RFT 拒绝采样微调 |
| G164 | 推理能力蒸馏三法 |
| G165 | QAT vs PTQ |
| G166 | PPO 三大超参 |
| G167 | 并行策略选型决策树 |
| G168 | padding 方向：训练 right / 推理 left |
| G169 | 多轮对话训练与 loss mask |
| G170 | loss 权重平衡三法 |
| G171 | MoE 忙闲不均：aux loss 与动态偏置 |
| G172 | ZeRO Stage 与 offload 配置 |
| G173 | Mixture of Depths |
| G174 | LR Finder |
| G175 | Loss Scaling 与 GradScaler |
| G176 | 上下文扩展：PI / NTK / YaRN |
| G177 | Logit Lens 训练诊断 |
| G178 | Label Smoothing 为何不用 |
| G179 | Self-Instruct 与 Evol-Instruct |
| G180 | RLVR 数据准备全流程 |
