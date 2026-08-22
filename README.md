# Consultative Sales Skill

An evidence-aware sales communication skill for Codex and other agent runtimes that support `SKILL.md` packages.

它帮助销售人员先判断客户信号和沟通阶段，再决定推进、澄清、等待或结束；输出自然、简短、可直接使用的中文沟通建议，而不是堆砌“万能话术”。

## What it does

- Diagnoses customer engagement without mistaking politeness for purchase intent.
- Selects one objective and one response entry point per conversation turn.
- Drafts concise messages for chat, calls, meetings, objections, and follow-ups.
- Separates confirmed facts, seller assumptions, and unknown information.
- Applies evidence gates to price, inventory, compatibility, delivery, and other commercial claims.
- Stops pressure after explicit rejection or repeated weak responses.
- Supports coaching mode so users learn the judgment process instead of relying only on generated copy.

## Core model

```text
Signal → Stage → Concern → One-turn goal → Action
```

The default message shape is:

```text
Acknowledge → Add one useful value → Leave one easy next step
```

Either part may be omitted when the situation calls for a shorter response. Explicit rejection should normally lead to acknowledgment and closure.

## Install

Clone the repository and run:

```bash
python3 scripts/install.py
```

The installer copies the skill to `~/.codex/skills/consultative-sales-communication` by default. It never installs the repository documentation or tests into the skill directory.

To choose another skills directory:

```bash
python3 scripts/install.py --skills-dir /path/to/skills
```

## Use

Invoke the skill explicitly:

```text
Use $consultative-sales-communication. The customer said “we already have a long-term supplier.” What should I reply?
```

Or describe the situation naturally:

```text
客户收到报价一周没回复，也没有新进展。现在要不要追？如果要，直接给我能发的话。
```

The default output is:

```text
Decision: send now / wait / close this turn
Copy-ready reply: ...
Evidence: customer signal ...; one-turn goal ...
Unknowns: ...
```

When the user asks for a short answer, the skill returns only the decision and the copy-ready reply.

## Repository layout

```text
skills/consultative-sales-communication/  Installable skill package
tests/                                    Behavioral and structural cases
scripts/install.py                        Local installer
scripts/audit_public_tree.py              Privacy and release guard
.github/workflows/validate.yml            Continuous validation
```

## Design principles

1. Evidence before confidence.
2. One turn, one primary objective.
3. Progress should match customer commitment.
4. Unknown facts remain unknown.
5. No fake scarcity, fake urgency, hidden conditions, or repeated pressure.
6. Customer-visible messages never contain internal costs, margins, supplier details, or private scoring.
7. Conversation advice does not replace technical, legal, pricing, or procurement validation.

## Privacy and content policy

This repository contains only original workflow instructions, synthetic examples, and validation cases.

Do not contribute:

- private customer conversations or identifying information;
- books, course files, PDFs, EPUBs, archives, or copied source passages;
- internal prices, costs, margins, supplier identities, credentials, or tokens;
- examples that make unsupported technical or commercial claims.

Use synthetic or fully anonymized cases when contributing tests.

## Validate

```bash
python3 scripts/audit_public_tree.py
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
```

The local release process additionally runs the official Codex `quick_validate.py` script when it is available.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New conversation patterns should be backed by a synthetic regression case and must pass the privacy and unsupported-claim checks.

## License

MIT. See [LICENSE](LICENSE).
