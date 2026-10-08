# G008 — chat template 训推不一致的四种错法，Thinking 模型多轮拼接规则与逐 token 验证
> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G008-chat-template-mismatch.html

## 元信息

- 编号：G008
- 标题：chat template 训推不一致的四种错法，Thinking 模型多轮拼接规则与逐 token 验证
- BV：BV1qgHn6kEwe
- 时长：03:12
- 发布日期：2026-10-07
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：Qwen3 chat template、HuggingFace apply_chat_template / return_assistant_tokens_mask、LLaMA-Factory / TRL 等框架的模板实现

## 一句话总结

chat template 是训练与推理之间不成文的契约：特殊 token 与换行只要有一处对不上，模型看到的就是分布外前缀——不报错，只掉分；上线前唯一靠谱的验证是把训练侧与推理侧的 token 序列逐位比对。

## 核心

1. 问题/背景：一整段对话在模型眼里不是 JSON，而是一串由角色标记、特殊 token 和换行拼成的 token 序列；这些位置是在 SFT 阶段学死的。训练侧手工拼字符串、推理侧用 tokenizer 模板，两边差一个换行、一个默认 system，就会让上线评测无声掉分（本期开场案例掉了 5 分，排查了三天）。
2. 机制/方法：四种常见错法——① add_generation_prompt 混用：推理要设 true 让模板在末尾追加 assistant 起始标记，训练用完整对话要设 false，否则模型学成「答完还要再开一个回合」；② 重复加特殊 token：模板本身已含 BOS/EOS，手工再让 tokenizer 加一次 special tokens 会出现两个 BOS 连在一起（Llama 系列最常见）；③ system 不一致：训练数据没有 system、推理时模板自动注入默认 system（或反过来），模型没见过这段前缀，行为就偏；④ assistant mask 区间没盖住结束符：只在 assistant token 上算 loss 是对的，但区间必须包含结束标记，否则模型学不会停；HF 的 return_assistant_tokens_mask 配合模板里的 generation 块能自动算对。
3. 关键证据或数字：Thinking 模型（以 Qwen3 模板为例）把问题升级：多轮对话时历史轮次的 think 内容不保留、只保留最后一轮推理；enable_thinking=false 时模板会插入一个空 think 块。若做多轮 RL / 多轮 SFT 时把历史轮的 think 一起塞回上下文，训练分布就与推理 serving 分布错开。一线经验是严格按官方模板拼、每轮剥掉历史 think；小模型多轮 agent 每轮重复目标与前几步动作会更稳。
4. 结论/判断：验证方法只有一个——逐 token 比对：把训练样本经数据管道得到的 input ids 解码出来，再把同一段对话用推理服务的 apply_chat_template 跑一遍，两串 token 逐位对比，差异为空才算对齐。不同框架（LLaMA-Factory、TRL 等）的模板实现各有差异，不能只看文档，必须实测。

## 可迁移

- 上线/换框架/换 tokenizer 时，把「训练侧 token 序列 vs 推理侧 token 序列逐位 diff」做成固定检查项，能省掉数天排查。
- 多轮 RL 数据拼接必须复刻推理侧的模板规则（尤其 thinking 模型的历史 think 剥离），否则训推分布错位会以掉分而非报错的形式出现。

## 疑问 / 下一步

- 各主流框架（vLLM、SGLang、TRL）对同一模型模板的实现差异有多大，下次换 serving 框架时先跑一次逐 token 对照再决定。
