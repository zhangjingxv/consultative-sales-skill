# 判定标签口径覆盖核查 — 2026-09-17

阶段 3 的前置条件：案例断言必须先有可判定口径，否则「12 类案例满足事实门禁和节奏
规则」无法判真也无法判假。本文件记录该前置条件从「无口径」到「可机器核查」的一次变更。

## 变更内容

| 文件 | 变更 |
| --- | --- |
| `skills/consultative-sales-communication/references/decision-vocabulary.md` | 新增：为 26 个判定标签写明「适用 / 可观测行为 / 反例 / 红线」 |
| `scripts/audit_case_vocabulary.py` | 新增：校验案例标签是否有口径，且定义是否同时含可观测行为与反例 |
| `skills/consultative-sales-communication/SKILL.md` | 新增一行指向判定口径文件的链接 |

## 复现命令与实测输出

```
$ python3 scripts/audit_case_vocabulary.py
cases=32 labels_used=26 labels_defined=26
missing_definition=0
thin_definition=0
defined_but_unused=0
ok=true

$ python3 scripts/validate_skill.py
Skill validation passed

$ python3 scripts/audit_public_tree.py
Public-tree audit passed: 34 files checked

$ python3 -m pytest tests -q
8 passed, 9 subtests passed
```

## 判定

- 已完成（有证据）：32 条行为案例使用的 26 个 `expected_decision` 标签，全部有可观测
  行为与反例定义；无「定义含混」标签；无未使用标签。
- 待确认：案例内的 `required` / `forbidden` 行为断言共 126 个，仍未逐条建立标签级
  口径，也没有「给定回复 → 逐条判定」的离线评分器。因此**阶段 3 的盲测仍不能执行**，
  也不能声称已通过。
- 未验证：本文件只覆盖公开仓库自身的标签文本，不含私有资料库内容；发布前仍须运行
  `audit_public_against_private.py` 的隔离检查。

## 下一步

1. 为 126 个行为断言建立标签口径（可观测行为 + 反例），并让 `audit_case_vocabulary.py`
   一并核查。
2. 实现离线评分器：输入「case id + 候选回复」，输出每条 required/forbidden 的命中判断。
3. 用隐藏 expected 字段的盲测跑 12 类案例，失败项回填到 SKILL.md 规则，而不是新增话术。

## 边界

本文件与新增文件只使用公开仓库自有的英文标签与原创中文口径，不含私有资料库的书名、
作者名或原文摘录。
