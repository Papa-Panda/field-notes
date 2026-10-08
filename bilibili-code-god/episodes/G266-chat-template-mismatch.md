# G266 — chat template 不一致：不报错但效果暴降的 silent error

> 📖 阅读版：https://papa-panda.github.io/field-notes/bilibili-code-god/episodes/G266-chat-template-mismatch.html

## 元信息

- 编号：G266
- 标题：chat template 不一致：不报错但效果暴降的 silent error
- BV：BV1t68264Eyx
- 时长：02:42
- 发布日期：2026-08-23
- 来源：Bilibili UP「古希腊掌管代码的神」
- 相关论文/工作：未标注（涉及 LLaMA Factory、vLLM、HuggingFace Tokenizer 配置）

## 一句话总结

训练与推理用了不同的 chat template 时，模型看到的输入格式与训练时完全对不上，不报错、loss 也看不出异常，但输出质量暴降，是 SFT 落地最隐蔽的 silent error。

## 核心

1. 问题/背景：chat template 定义了多轮对话如何序列化成字符串喂给模型，不同模型用不同的角色标签、特殊 token 或换行冒号格式。训练时模型学到的是某种格式下的回复能力；推理时 serving 框架换了模板，模型照样输出文字，只表现为答非所问、重复、偏离——不报错不崩溃，最难排查。
2. 机制/方法：常见 mismatch 场景有三——训练用 LLaMA Factory、推理用 vLLM，两者默认 template 不同；基座模型本身没有 chat template，硬套对话格式；多轮对话序列化方式不同（训练时每轮独立、推理时拼成长序列）。还有一个易忽略点：训练时新增的特殊 token（如 `<|im_start|>`、`<|im_end|>`）若推理侧 tokenizer 没加载同一份配置，会被当成普通文字处理，效果直接崩。
3. 关键证据或数字：排查四步——打印训练与推理两侧的实际输入 token 序列逐 token 对比；确认 tokenizer 的 chat template 属性是否一致；检查特殊 token 的 id 是否对齐；同一条测试数据分别在训练框架与推理框架跑预处理看输出是否一致。
4. 结论/判断：最可靠的预防是把 chat template 随 tokenizer 配置一起保存（HF tokenizer 的 JSON 里有 chat_template 字段），推理时加载同一份 tokenizer；上线前必跑端到端回归，用同一组 prompt 对比训练框架与推理框架的输出。

## 可迁移

- SFT 模型交付/上线 checklist 加一条：训推 template 一致性核对（逐 token diff + 特殊 token id 对齐 + 同一 tokenizer 配置文件），这是零成本防住一类最难查的线上事故。
- RL 训练里 rollout 引擎（如 vLLM）与训练框架的模板不一致会污染奖励信号，排查 reward 异常时应把 template 一致性列入前几项检查。

## 疑问 / 下一步

- 视频未量化 template mismatch 的典型掉点幅度；实际排查时可先在小评测集上做训推两侧同 prompt 对照，拿到自己的量级感。
