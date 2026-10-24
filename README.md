# 客户关系与销售助手 Skill

[中文](README.md) | [English](README.en.md)

**v1.7.0：一个 Skill 包，同时支持中文和英文。** 顶部链接切换 GitHub 说明文档；不会保存语言偏好，也不会改变 Skill 的实际输出语言。

面向 B2B 与项目型销售，帮助你成为理解客户、值得长期信赖的合作伙伴，让合适的产品匹配真实需求。

| 核心目标 | 要弄清、做到什么 |
|---|---|
| 产品价值 | 我们的产品能解决什么问题，在什么条件下适用，有什么限制 |
| 真实需求 | 客户是否确实有这方面要求，具体目标、约束和优先级是什么 |
| 信任：了解与兑现 | 理解其工作处境、真实顾虑、沟通偏好和主动分享的兴趣，并持续兑现答应的事 |

三项独立判断：信任不能用熟悉程度或购买概率代替，关系也不能代替产品适配。了解客户不只是找朋友圈话题或做画像打分，不强行从聊天中套取需求。没有当前需求也可以正常来往；产品不匹配时如实说明；需求、适配和购买条件确认后，仍明确推进采购申请、订单确认等下一步。

默认直接协助处理真实沟通，给出自然、简短、可使用的表达。社交话题可以止于关心、祝贺或共同兴趣，不必每次转成产品推销；只有你明确要求练习时才进入训练。

## 能做什么

- 根据实际可用的客户材料理解其工作处境、顾虑与偏好，选择合适的回应并跟进已作承诺。
- 判断客户的实际动作，不把礼貌、热情或沉默当成购买意向。
- 每轮选一个目标，起草消息、电话、拜访、异议与跟进表达；自然交流可以不提问、不索取动作。
- 综合客户说明，区分需求、约束、未知，以及使用、评审、下单、付款和服务角色。
- 对齐方案范围、核对成本假设，讲清差异是否值得；条件具备时提出具体采购动作。
- 对价格、库存、兼容性、交付、权限等保留事实核验门禁。
- 尊重拒绝，避免假紧迫、连续施压和无依据承诺。
- 用实际客户反馈修正后续动作，分别记录关系变化与成交进展。

内含 M01–M26 共 26 条原创方法，每条都有触发条件、动作、停止线与反例。它们是沟通判断工具，不是成交率、心理学规律或技术可行性的证明。

## 主要参考模块

| 模块 | 用途 |
|---|---|
| [客户背景与话题](skills/consultative-sales-communication/references/customer-context.md) | 理解客户处境、顾虑与偏好，从可见事实自然回应，保留来源和日期，不从社交内容猜测购买意愿 |
| [了解与信任](skills/consultative-sales-communication/references/ethics-and-trust.md) | 听懂并允许纠正，按偏好合作、兑现承诺与修复失约，不把熟悉程度当信任 |
| [项目与成交推进](skills/consultative-sales-communication/references/deal-progress.md) | 理清 ICT 交易链、当前阻塞和关闭条件，条件确认后提出下单等具体动作 |
| [价值比较](skills/consultative-sales-communication/references/value-comparison.md) | 对齐比较口径，使用可核对的成本公式与明确假设，区分工时等值和实际现金收益 |

上述模块均提供包内英文对应资料。沿用按需读取、事实核验、拒绝范围与服务责任判断，以及中英文混合文案检查。

朋友圈话题仅支持你提供的文字、截图，或你明确授权且当前工具实际可读取的材料。当前版本没有朋友圈自动读取、监控或抓取功能，也不会声称看过未读到的内容。

## 安装与更新

克隆本仓库后，在仓库目录运行：

```bash
python3 scripts/install.py
```

只安装 `consultative-sales-communication` 一个包，中英文内容都在其中。日常使用不需要远程 API 或密钥。

更新已有安装，旧版本会备份到技能发现目录之外：

```bash
python3 scripts/install.py --force
```

从 v1.4.0 的两个独立包迁移到一个包：

```bash
python3 scripts/install.py --force --migrate-legacy-en
```

安装器先安装统一包，再将旧独立英文包移入备份目录，不删除旧内容。默认安装位置为 `~/.codex/skills/consultative-sales-communication`，备份位置为 `~/.codex/skill-backups`。

指定其他技能目录：

```bash
python3 scripts/install.py --skills-dir /path/to/skills
```

## 使用与输出语言

无论中文还是英文，都使用同一个技能名：

```text
使用 $consultative-sales-communication。客户说“已经有长期供应商”，给我一版中文回复。
```

```text
Use $consultative-sales-communication. The customer said “we already have a long-term supplier.” Draft a concise English reply.
```

明确指定的输出语言优先；否则跟随用户请求语言，无法判断时默认中文。不需要重新安装。英文任务只按需读取包内英文指南和参考资料。

默认输出：

```text
判断：现在发／等一下／结束本轮
可直接发送：……
依据：客户信号……；本轮目标……
未知：……（没有则省略）
```

用户要求“直接给我怎么回”时，只给判断和必要的可发送文本；等待且无需回应时省略话术。默认只起草，不自动发送；外部发送需要当前授权。

常用请求：

```text
自然联系：客户发了完成半马的动态，平时聊过跑步，帮我自然祝贺一下，不带产品。
业务推进：配置和服务范围都确认了，客户还没下单，帮我提出一个明确的采购下一步。
修改草稿：保留我的语气，只改这条消息里最关键的问题。
```

文案检查在安装后的 Skill 目录内运行，也支持通过标准输入读取：

```bash
python3 scripts/message_lint.py --file /path/to/customer-message.txt
```

结果中的 `ok` 仅表示未命中已实现的检查规则；`matches` 给出命中片段和位置，`scope` 标明启发式检查范围。脚本不会联网核实价格、库存、兼容性或授权；实际文案仍需结合上下文判断。

## 包结构

```text
skills/consultative-sales-communication/
  SKILL.md                  唯一技能入口
  references/               中文参考资料
  languages/en/guide.md      包内英文指南
  languages/en/references/   英文参考资料
  scripts/                  文案风险检查工具
README.md                   中文说明
README.en.md                English documentation
```

## 隐私与边界

仓库只含原创方法、合成案例和校验工具，不含原始学习资料或私有客户聊天。
不贡献原文件、摘录、来源清单、内部成本、毛利、供应商信息或凭据。沟通建议不能替代配置、核价、合同、采购和交付核验；未知必须保持未知。

朋友圈可见不等于内容公开。真实客户截图、聊天和客户记录保留在用户指定的私有范围，不进入公共 Skill；不遍历好友，不用社交话题绕过拒绝联系的边界。

## 验证与贡献

```bash
python3 scripts/audit_public_tree.py
python3 scripts/validate_skill.py
python3 scripts/audit_case_vocabulary.py
python3 -m unittest discover -s tests -v
```

校验覆盖包结构、链接、双语规则与判定口径、安装迁移和文案风险检查。测试通过不证明所有模型回答正确或真实销售效果。

本版 5 个原创合成场景的独立代理实际回复及协调代理复核见 [v1.7.0 行为抽查](tests/behavioral-review-1.7.0.md)。这是有限行为抽查，不是自动评分的模型评测或真实关系、销售效果证明。历史记录保留在 [v1.6.0](tests/behavioral-review-1.6.0.md) 和 [v1.5.0](tests/behavioral-review-1.5.0.md)。

贡献约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。许可证为 [MIT](LICENSE)。
