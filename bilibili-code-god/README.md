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
- 批 9（#161–#180）：20/20 完成（其中 4 条首轮 harvest 串台，re-harvest 补齐）。
- 批 10（#181–#200）：19/20 完成；#193（冷启动 SFT）字幕接口两轮均未返回，待换时间窗口重试。
- 批 11（#201–#220）：20/20 完成；#193 第三轮重试仍未返回字幕。
- 批 12（#221–#240）：17/20 完成；#222、#231、#235 与 #193 同属字幕接口持续返回空，列入待重试名单（共 4 条）。
- 批 13（#241–#260）：19/20 完成；#260（DAPO）加入待重试名单（共 5 条）。
- 批 14（#261–#280）：20/20 完成（含 #260、#279 待重试捞回）。
- 批 15（#281–#300）：19/20 完成；#290（NoThinking）加入待重试名单。
- 批 16（#301–#320）：19/20 完成。台账原 BV 列自 #313 起整体错位一位，已按页面标题实证修正 #313–#319；#320 的真实 BV 待重新枚举确认。
- 批 17（#320–#339）：20/20 完成。重新枚举 #300–#515 与台账逐行标题对齐，BV 错位范围确认仅 #313–#336，已全部修正并复核 0 不一致。
- 批 18（#340–#359）：20/20 完成。
- 批 19（#360–#379）：20/20 完成。
- 批 20（#380–#399）：15/20 完成；#382、#383、#389、#392、#394 加入待重试名单。累计 388/515。
- 批 21（#400–#419）：20/20 完成。累计 408/515。待重试共 11 条（#193、#222、#231、#235、#271、#290、#382、#383、#389、#392、#394）。
- 批 22（#420–#439）：20/20 完成。累计 428/515。
- 批 21（#400–#419）：16/20 完成；#401、#404、#408、#419 加入待重试名单（共 15 条）。累计 404/515。

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
| G181 | 梯度噪声尺度与最优 batch |
| G182 | GPU 利用率归零：IO 瓶颈 |
| G183 | FP8 训练实操 |
| G184 | embedding 微调与难负样本 |
| G185 | 预训练为什么不用 Dropout |
| G186 | reference model 与 KL 约束 |
| G187 | 数据回放防遗忘 |
| G188 | 文本数据增强三法 |
| G189 | 课程学习与 pacing |
| G190 | critic / GAE / GRPO 砍 critic |
| G191 | 学习率衰减：cosine / linear / WSD |
| G192 | 继续预训练配比与 D-CPT Law |
| G194 | BF16 / FP16 / FP8 选型决策树 |
| G195 | Critical Batch Size |
| G196 | attention sink 与 StreamingLLM |
| G197 | 激活检查点选层 |
| G198 | RIRM + RAPO：答后反思负奖励 |
| G199 | 预训练为什么只跑 1 epoch |
| G200 | ViT 视觉 Transformer |
| G201 | Transformer 会被取代吗 |
| G202 | 四级省显存阶梯 |
| G203 | 训练不收敛排查清单 |
| G204 | loss 变 NaN 三路排查 |
| G205 | 数不清 r 的 tokenizer 根因 |
| G206 | SwiGLU 的 8/3·d 推导 |
| G207 | StreamingLLM 与 sink token |
| G208 | Spike-Aware Adam |
| G209 | SigLIP vs CLIP |
| G210 | SFT vs 预训练：损失掩码 |
| G211 | 第二个 epoch loss 断崖 |
| G212 | SFT 后的三种退化 |
| G213 | SFT 数据量：LIMA vs Alpaca |
| G214 | 自洽性采样 |
| G215 | SAE 稀疏自编码器 |
| G216 | 规则奖励 vs 奖励模型 |
| G217 | RLHF 三大崩溃诊断 |
| G218 | PPO 为什么需要四个模型 |
| G219 | 奖励稀疏四解 |
| G220 | RLEP 经验回放 |
| G221 | 奖励模型训练：成对比较损失 |
| G223 | R1 四阶段配方 |
| G224 | 预测下一个词与曝光偏差 |
| G225 | PD 分离：Prefill vs Decode |
| G226 | PPO 奖励为何只在末 token 发 |
| G227 | PPO clip 四象限 |
| G228 | PPO 显存爆炸与 offload |
| G229 | 存在惩罚 vs 频率惩罚 |
| G230 | MMLU 三大坑 |
| G232 | Medusa 多解码头 |
| G233 | 离群激活 |
| G234 | 机器遗忘三法 |
| G236 | Lost in the Middle |
| G237 | LoRA 显存悖论 |
| G238 | LoRA 超参调优 |
| G239 | LongRoPE |
| G240 | Logit Lens 逐层结晶 |
| G241 | 绿名单水印 |
| G242 | 多位数乘法三重根因 |
| G243 | Linear Attention |
| G244 | 大规模训练容错 |
| G245 | KV Cache 为何不缓存 Q |
| G246 | Stable LatentMoE 三件套 |
| G247 | GSPO 序列级重要性比率 |
| G248 | Grokking 延迟泛化 |
| G249 | 梯度裁剪与 AdaGC |
| G250 | 梯度累积 vs 真大 batch |
| G251 | GLM-5.2 在线守卫：作弊不丢 rollout |
| G252 | Gated Attention |
| G253 | 灾难性遗忘五法 |
| G254 | 偏好数据构造 |
| G255 | DPO loss 降了模型反而变差 |
| G256 | 通信瓶颈 |
| G257 | 扩散语言模型 |
| G258 | 采样参数调序 |
| G259 | 温度 / Top-K / Top-P 区别 |
| G260 | DAPO：token 级归一化 |
| G261 | DAPO 动态采样 |
| G262 | 余弦相似度的维度灾难 |
| G263 | 约束解码：FSM 与 logit 屏蔽 |
| G264 | 一致性模型与 LCM-LoRA |
| G265 | 断点续训四件套 |
| G266 | chat template 不一致 |
| G267 | 自回归三局限 |
| G268 | Attention Residuals |
| G269 | ASPO：比率翻转治熵崩塌 |
| G270 | Agent 项目失败五道鸿沟 |
| G272 | WSD 为什么能随时停 |
| G273 | 视觉 Token 压缩：ToMe / FastV |
| G274 | TTT 层 |
| G275 | 思维树 ToT |
| G276 | Titans 神经长期记忆 |
| G277 | 测试时算力四招 |
| G278 | 滑动窗口注意力 |
| G279 | SimPO vs DPO |
| G280 | 自投机解码 |
| G281 | Self-Refine |
| G282 | Self-RAG 反思 token |
| G283 | rStar-Math |
| G284 | 旋转量化治离群点 |
| G285 | 推理模型四支柱 |
| G286 | Quiet-STaR |
| G287 | QK-Norm 治 NaN |
| G288 | PRM vs ORM |
| G289 | ParaThinker 并行思考 |
| G291 | NaViT 原生分辨率 |
| G292 | μTransfer |
| G293 | MTP 多 token 预测 |
| G294 | 模型合并 TIES 与 DARE |
| G295 | Mixture-of-Depths |
| G296 | 美杜莎解码 |
| G297 | M-RoPE |
| G298 | Lookahead Decoding |
| G299 | Late Chunking |
| G300 | KV 驱逐：H2O 与 SnapKV |
| G301 | KTO 前景理论对齐 |
| G302 | Jamba 混合架构 |
| G303 | GraphRAG |
| G304 | 思维图 GoT |
| G305 | 生成式奖励模型 GRM |
| G306 | DPO 变体全家桶 |
| G307 | CRAG 纠错式检索 |
| G308 | 宪法 AI 与 RLAIF |
| G309 | Chameleon 早融合 |
| G310 | Chain-of-Draft |
| G311 | Byte Latent Transformer |
| G312 | BitNet b1.58 |
| G313 | 无辅助损失负载均衡 |
| G314 | Attention Sink |
| G315 | Toolformer |
| G316 | Token-level MDP |
| G317 | SFT 与 RLHF 的 KL 两面 |
| G318 | Self-Rewarding LM |
| G319 | RM 校准 |
| G320 | RLHF 三阶段 |
| G321 | RM Ensemble |
| G322 | RetNet |
| G323 | Reference Model |
| G324 | importance ratio + clip |
| G325 | Phi-2 教科书数据 |
| G326 | RM 损失 Pairwise Ranking |
| G327 | Online vs Offline RLHF |
| G328 | token log prob 工程坑 |
| G329 | LLM-as-Judge 四大偏差 |
| G330 | Adam 挑战者 |
| G331 | Length Bias |
| G332 | LATS |
| G333 | KL 系数 β |
| G334 | Iterative DPO |
| G335 | HyDE |
| G336 | Anthropic HH 数据集 |
| G337 | Goodhart 与奖励过优化 |
| G338 | Elo 与 Bradley-Terry |
| G339 | DeepSeekMoE |
| G340 | Bradley-Terry 模型 |
| G341 | 对齐税与 PPO-ptx |
| G342 | ALiBi |
| G343 | TTFT vs ITL |
| G344 | H100 理论 TPS |
| G345 | TD 时序差分 |
| G346 | SARSA vs Q-learning |
| G347 | Safe Softmax |
| G348 | RoPE |
| G349 | RLOO |
| G350 | ReMax |
| G351 | RadixAttention |
| G352 | Prefill vs Decode |
| G353 | PD 分离部署 |
| G354 | 逻辑回归 |
| G355 | L1 vs L2 正则 |
| G356 | K-means |
| G357 | 决策树三兄弟 |
| G358 | Continuous Batching |
| G359 | Continuous Batching（重发） |
| G360 | Chunked Prefill |
| G361 | GPipe vs 1F1B |
| G362 | Ring AllReduce 与 DDP |
| G363 | Megatron 张量并行 |
| G364 | 序列并行 × 专家并行 |
| G365 | ZeRO 显存三刀 |
| G366 | badcase 解决顺序 |
| G367 | DeepSpeed ZeRO Stages |
| G368 | 熵坍塌与 Clip-Higher |
| G369 | Muon 优化器 |
| G370 | GRPO clip 的梯度 |
| G371 | sequence 级负载均衡损失 |
| G372 | 5 个通信原语 |
| G373 | Decoder 张量并行通信次数 |
| G374 | MQA 与 GQA |
| G375 | 质数与埃氏筛 |
| G376 | MoE 设备受限路由 |
| G377 | 训练显存计算 |
| G378 | self-attention 公式 |
| G379 | BN vs LN |
| G380 | GSM8K 数据污染 |
| G381 | pass@k 无偏估计 |
| G384 | VAE |
| G385 | Actor-Critic / A2C / A3C |
| G386 | MinHash 去重 |
| G387 | 预训练数据清洗 |
| G388 | Longformer & BigBird |
| G390 | 高效 Transformer 四流派 |
| G391 | PI / NTK / YaRN |
| G393 | 长度外推全景 |
| G395 | Whisper |
| G396 | 多臂老虎机 |
| G397 | 策略梯度定理 |
| G398 | SparseGPT / Wanda |
| G399 | 张量并行列切行切 |
| G400 | 彩票假设 |
| G401 | HNSW / IVF-PQ |
| G402 | Q-Learning 到 DQN |
| G403 | Flow Matching |
| G404 | Plan-and-Execute vs ReAct |
| G405 | 模型剪枝原理 |
| G406 | Reflexion |
| G407 | 集成 / 自蒸馏 |
| G408 | DiT |
| G409 | Stable Diffusion |
| G410 | 音频 Tokenizer |
| G411 | 蒸馏温度系数 |
| G412 | VITS |
| G413 | 知识蒸馏 KD |
| G414 | MDP 与贝尔曼方程 |
| G415 | 学习率 Warmup |
| G416 | 视觉编码器盘点 |
| G417 | 解码策略 |
| G418 | LLaVA |
| G419 | weight tying |
| G420 | BLIP-2 Q-Former |
| G421 | 训练算力 6ND |
| G422 | CLIP |
| G423 | 7B 参数量手算 |
| G424 | Classifier-Free Guidance |
| G425 | Score / SDE 统一视角 |
| G426 | DDIM |
| G427 | DDPM |
| G428 | Embedding 与 √d |
| G429 | 什么是语言模型 |
| G430 | BLEU 与 ROUGE |
| G431 | PEFT 五种方法 |
| G432 | 指令微调 |
| G433 | RNN vs CNN vs Transformer |
| G434 | 注意力 O(n²) |
| G435 | Few-shot 与 ICL |
| G436 | 涌现能力之争 |
| G437 | ICL 机理 |
| G438 | 学习率 Warmup（重发） |
| G439 | 梯度裁剪 |
| G400 | 彩票假设 |
| G402 | Q-Learning 到 DQN |
| G403 | Flow Matching / Rectified Flow |
| G405 | 模型剪枝原理 |
| G406 | Reflexion |
| G407 | 集成、蒸馏与自蒸馏 |
| G409 | Stable Diffusion |
| G410 | 音频 Tokenizer |
| G411 | 蒸馏温度系数 |
| G412 | VITS 端到端 TTS |
| G413 | 知识蒸馏 KD |
| G414 | MDP 与贝尔曼方程 |
| G415 | 学习率 Warmup |
| G416 | 视觉编码器盘点 |
| G417 | 解码策略 |
| G418 | LLaVA 视觉对齐 |
