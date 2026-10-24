# 销售沟通 Skill

[中文](README.md) | [English](README.en.md)

**v1.5.0：一个 Skill 包，同时支持中文和英文。** 顶部链接切换 GitHub 说明文档；不会保存语言偏好，也不会改变 Skill 的实际输出语言。

面向 B2B 与项目型销售，先判断客户信号和沟通阶段，再决定推进、澄清、等待或结束。输出自然、简短、可直接使用的话术，而不是“万能成交句”。

## 能做什么

- 判断客户的实际动作，不把礼貌、热情或沉默当成购买意向。
- 每轮选一个目标，起草消息、电话、拜访、异议与跟进表达。
- 综合客户长段说明，区分需求、约束、未知及组织决策角色。
- 对价格、库存、兼容性、交付、权限等保留事实核验门禁。
- 尊重拒绝，避免假紧迫、连续施压和无依据承诺。
- 支持复盘训练，区分判断偏差与表达偏差。

内含 M01–M26 共 26 条原创方法，每条都有触发条件、动作、停止线与反例。它们是沟通判断工具，不是成交率、心理学规律或技术可行性的证明。

## 本版改进

- 直接回复、修改草稿、复盘训练按请求选择，短回复只加载必要参考。
- 等待时明确建议「这轮先不发」；拒绝范围、已有服务责任和约定反馈节点有明确优先级。
- 区分卖方折扣授权与买方采购权限，避免问错对象。
- 文案检查支持中英文及混合文本，报告命中片段与位置，重复命中合并为同一规则。

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

三种常用请求：

```text
直接回复：客户已经说预算批准前别联系，新库存到了，这轮要不要发？
修改草稿：保留我的语气，只改这条消息里最关键的问题。
复盘训练：你扮演客户，先让我练一轮需求发现，再给反馈。
```

文案检查在安装后的 Skill 目录内运行，也支持通过标准输入读取：

```bash
python3 scripts/message_lint.py --file /path/to/customer-message.txt
```

结果中的 `ok` 仅表示未命中已实现的检查规则。脚本不会联网核实价格、库存、兼容性或授权；实际文案仍需结合上下文判断。

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

## 验证与贡献

```bash
python3 scripts/audit_public_tree.py
python3 scripts/validate_skill.py
python3 scripts/audit_case_vocabulary.py
python3 -m unittest discover -s tests -v
```

校验覆盖包结构、链接、双语规则与判定口径、安装迁移和文案风险检查。测试通过不证明所有模型回答正确或真实销售效果。

本版另做了六个原创合成场景的独立试用，实际结果见 [行为抽查记录](tests/behavioral-review-1.5.0.md)。

贡献约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。许可证为 [MIT](LICENSE)。
