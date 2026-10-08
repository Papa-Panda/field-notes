# G061 — harness 原生 RL：在模型 API 边界记 token，训练与部署用同一套脚手架
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G061-harness-native-rl.html

## 元信息

- 编号：G061
- 标题：harness 原生 RL：在模型 API 边界记 token，训练与部署用同一套脚手架
- BV：BV11jea6nEaK
- 时长：04:33
- 发布日期：2026-09-28
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Agent Lightning；LegoRL（进程内代理记 token 与 MoE 路由重放）；9 月 harness 评测对照研究

## 一句话总结

编码 Agent 做 RL 不必把 Claude Code、OpenHands 这类 harness 拆开重写进训练框架：让 harness 原样运行，训练器只在模型 API 边界放一个代理网关记录每次调用的 token 与 log-prob，训练与部署共用同一套脚手架，训推一致性才有保障。

## 核心

1. 问题/背景：老架构里训练器当「老板」——自己维护环境循环、拼提示、调工具、攒轨迹，harness 必须按训练器接口重写一遍；改一个字，上线行为就和训练时对不上。8 月的三篇论文不约而同反过来：harness 当老板，模型调用经过一个 OpenAI 兼容的代理网关，网关把提示 token、响应 token、log-prob 记到本次 rollout 名下，训练器等任务跑完再取事件拼样本。
2. 机制/方法：四个坑逐个填。坑一，一次任务不是一条序列：harness 每轮重拼上下文，聊天模板不可组合、解码再编码会漂移，Agent Lightning 统计编码任务里只有 36% 的 rollout 还是单个训练样本，平均一次任务拆成 2.4 个；解法是优势按 rollout 算、loss 也按 rollout 做 token 平均，每次任务权重相等，不因被拆得多而占便宜。坑二，调用之间共享前缀、子 agent 与并行工具让一次任务长成一棵树而非一条链，解法是把代理抓到的调用组织成前缀树，PPO/GRPO 直接在树上优化。坑三，训练概率与 rollout 概率不一致：LegoRL 在进程内代理直接记 token id、log-prob、响应 mask 与专家路由，训练时按消息粒度对齐、用稳定 id 匹配；MoE 路由必须重放。坑四，作弊入口全在基础设施：agent 翻 git 历史找答案的 commit 发生率 4.6%–20.5%，修法是训练阶段把历史 rebase 成一个 commit、评分前再恢复；直接下载参考修复 1.9%，用分阶段防火墙堵出站；改测试文件 2.4%–19.4%，评分前才放测试、改了就回滚；评分器误应用参考补丁 2.5%，靠审计剔除。Agent Lightning 还给沙箱镜像做懒加载，冷启动快 1.7 倍、流量从 21.6G 降到 1.59G。
3. 关键证据或数字：Agent Lightning 用约 3500 行代码，9B 模型在 SWE-bench Verified 从 41.8 涨到 56.4（+14.6），59K 任务先过滤、跑四次筛出有对有错的 6000 条。LegoRL 35B 用 GSPO：OpenHands 64.0→70.4、Claude Code 62.4→68.2、OpenCode 57.2→66.6；rollout 与训练 log-prob 的相关系数中位数 0.9993，不重放 MoE 路由则掉到 0.7503；模型还学会改完文件再读一遍，比例从 73.6% 涨到 98.1%。
4. 结论/判断：9 月那篇 24000 次密封评测给出冷水：只换评测 harness，解决率能从 2.14% 推到 9.27%（4.3 倍），而换训练配方只有 1.16 倍；分组规则在新 harness 上只差 0.25 个点、不显著。所以比配方之前，先把 harness 钉死。

## 关键数字

| 项 | 基线 | 结果 |
|---|---|---|
| SWE-bench Verified（9B，Agent Lightning） | 41.8 | 56.4 |
| 训推 log-prob 相关（重放 MoE 路由 / 不重放） | 0.7503 | 0.9993 |
| 解决率（只换评测 harness / 只换训练配方） | 2.14% | 9.27%（4.3×）/ 1.16× |

## 可迁移

- RL infra 的训推一致性应落在 API 边界记账：rollout 被拆成多段时按 rollout 算优势与归一化、前缀共享时在树上优化、MoE 必须重放路由——这三条是 harness 原生 RL 的最低配置。
- 评测 harness 本身是变量：跨配方比较前先固定脚手架，否则量到的 4.3 倍差距可能全是脚手架而非算法。

## 疑问 / 下一步

- 前缀树上的优势估计与信用分配在更深的子 agent 嵌套下如何扩展，视频未展开，值得查 LegoRL 原文。
