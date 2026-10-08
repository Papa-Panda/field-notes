# G372 — Scatter/Gather/Reduce/AllReduce 分别是什么？5 个通信原语一张图讲透
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G372-comm-primitives.html

## 元信息

- 编号：G372
- 标题：Scatter/Gather/Reduce/AllReduce 分别是什么？5 个通信原语一张图讲透
- BV：BV1wCKx6hEoy
- 时长：02:52
- 发布日期：2026-07-23
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：集合通信原语；Ring All-Reduce

## 一句话总结

区分集合通信原语只看两点——数据往哪流、要不要做运算：Broadcast 复制、Scatter 切分、Gather 拼接、Reduce 聚合到一个节点、AllReduce 聚合后再分发给所有人。

## 核心

1. **问题/背景**：分布式训练里几十上百张 GPU 协同，Scatter、Gather、Reduce、AllReduce 名字像绕口令，面试还老爱考，需要一套不混淆的判别方法。
2. **机制/方法**：一对多的两个：Broadcast 把源节点数据原样复制发给所有节点（大家拿到的一模一样，典型场景是训练开始广播初始参数）；Scatter 把数据切成几块、每节点只拿一块且各不相同（典型场景是数据切片分发）。多对一的两个：Gather 把各节点的数据块原样收集拼到一个节点，是 Scatter 的逆操作；Reduce 不是拼接，而是做一次聚合运算（如求和）再存到目标节点，典型场景是梯度聚合。AllReduce 是 Reduce + Broadcast 的合体：先聚合所有节点的梯度，再把结果分发回每个节点，于是每步结束各卡都持有相同的全局平均梯度、参数保持同步。
3. **关键证据或数字**：对照表见下；AllReduce 太常用，工程上专门有 Ring All-Reduce 环状算法把带宽用得最省，可以说数据并行能跑起来全靠它。三组关系值得记牢：Scatter 与 Gather 互为逆操作，Broadcast 与 Reduce 互为逆操作，AllReduce = Reduce + Broadcast。
4. **结论/判断**：一句话记法——Reduce 是求和到一个节点，AllReduce 是求和再发给所有人。

## 关键数字

| 原语 | 数据流向 | 做不做运算 | 典型用途 |
|---|---|---|---|
| Broadcast | 一对多 | 复制 | 初始化参数 |
| Scatter | 一对多 | 切分 | 数据切片 |
| Gather | 多对一 | 拼接 | 收集结果 |
| Reduce | 多对一 | 聚合运算 | 梯度规约 |
| AllReduce | 多对多 | 聚合再分发 | 梯度同步 |

## 可迁移

- 读 DDP 源码时把每个通信调用对回这张表：梯度同步是 AllReduce、ZeRO/FSDP 的参数取回是 All-Gather、梯度分发是 Reduce-Scatter，很多框架行为都是这五个原语的组合。
- 面试被追问 Ring All-Reduce 时，先答它解决的是 AllReduce 的带宽最优实现，再展开环状分段流水。

## 疑问 / 下一步

- Reduce-Scatter 与 All-Gather 作为一对原语没有在本期出现，但 ZeRO/FSDP 正是建立在它们之上，值得补一期对照。
