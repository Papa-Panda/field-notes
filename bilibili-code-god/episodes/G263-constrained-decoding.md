# G263 — 约束解码怎么保证模型只吐合法 JSON？FSM/PDA 与 logit 屏蔽详解

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G263-constrained-decoding.html

## 元信息

- 编号：G263
- 标题：约束解码怎么保证模型只吐合法 JSON？FSM/PDA 与 logit 屏蔽详解
- BV：BV1bC826sEMX
- 时长：02:40
- 发布日期：2026-08-23
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：XGrammar、Outlines、llama.cpp（GBNF）、OpenAI Structured Outputs

## 一句话总结

约束解码把目标格式编译成自动机（正则用 FSM、嵌套 JSON 用 PDA），每步生成前先算出合法 token 集合，把非法 token 的 logit 砸成负无穷，从机制上保证输出 100% 合法。

## 核心

1. 问题/背景：Agent 调工具时最怕模型吐出的 JSON 少个逗号、引号没闭合，下游解析直接报错、整条调用链崩掉。光靠 prompt 要求「请输出 JSON」不可靠，自由采样随时可能混进非法字符。
2. 机制/方法：先把格式要求编译成自动机——正则编译为有限状态机 FSM，每个状态表示已生成的前缀、转移边标明下一步合法字符；但 JSON 有大括号嵌套配对，FSM 记不住嵌套层数，需要带栈的下推自动机 PDA。每生成一个 token 前先问自动机当前状态下哪些 token 合法，合法的保留，非法的 logit 设为负无穷，softmax 后概率为零、绝不会被采样。注意屏蔽改的是生成前的 logit，已吐出的 token 改不了（边界问题靠 token healing 修补）。
3. 关键证据或数字：工具谱系——XGrammar 把 JSON Schema 编译成 PDA 并预计算每个状态可接受的 token，速度很快，是 vLLM 的默认后端；Outlines 主管正则；llama.cpp 用 GBNF 文法；OpenAI 的 Structured Outputs API 底层也是同一套思路。
4. 结论/判断：约束解码卡的是合法性，与「猜多步」的推测解码是两回事；代价是屏蔽可能把模型逼到低概率 token 上，损害输出质量与多样性，需要权衡。

## 可迁移

- 做 Agent/工具调用的 serving 时，结构合法性应交给约束解码层（如 vLLM + XGrammar）兜底，而不是在 prompt 里反复叮嘱或在下游写容错解析。
- 面试被问「如何保证 LLM 输出合法 JSON」可分层答：文法编译（FSM/PDA）→ 逐步 logit 掩码 → 采样照常进行，并指出嵌套结构必须用 PDA 而非 FSM。

## 疑问 / 下一步

- 强约束与生成质量的 trade-off 缺量化数据：被屏蔽逼出的低概率路径对工具参数语义正确率的影响有多大，值得查 XGrammar/Outlines 的评测。
