# Sales Communication Assistant Skill

[中文](README.md) | [English](README.en.md)

Help sell a suitable product and build a relationship the customer wants to maintain.
This bilingual B2B sales assistant works with Codex and other runtimes that support `SKILL.md` packages.

**v1.6.0 — One skill, Chinese and English.** The unified package includes 26 operational
judgment rules with triggers, stop lines and counterexamples. They are communication
guidance, not claims of guaranteed conversion or psychological laws.

Understand the person and business, find natural conversation topics, explain value,
and resolve buying obstacles. When the buying conditions are confirmed, propose a
specific purchase request, order confirmation, or other appropriate next step.

The default is practical help with the conversation at hand. A social exchange can
end with genuine interest or congratulations; it does not need a product pitch.
Actual customer feedback informs the next action; relationship and deal outcomes stay separate.

The language links above switch this GitHub documentation only. They do not save
a language preference or change the skill's output language.

## New in v1.6.0

| Module | Purpose |
|---|---|
| [Customer context](skills/consultative-sales-communication/languages/en/references/customer-context.md) | Choose natural topics from available facts, retain sources and dates, and avoid inferring buying intent from social posts |
| [Deal progress](skills/consultative-sales-communication/languages/en/references/deal-progress.md) | Map ICT buying roles, define the present blocker and closure evidence, then ask for a concrete purchasing action |
| [Value comparison](skills/consultative-sales-communication/languages/en/references/value-comparison.md) | Align scope, use checkable cost formulas and explicit assumptions, and distinguish labor-cost equivalents from cash savings |

All three modules have Chinese counterparts in the same package. Selective reference
loading, factual checks, contact boundaries, service obligations, and bilingual draft checking remain supported.

For WeChat Moments and similar customer posts, use material the user supplies, or
material they explicitly authorize and the current tools can actually read. This version
does not implement automatic reading, monitoring, or scraping of Moments. It must not
claim to have seen content it has not read.

## What it does

- Uses available customer context to find a topic appropriate to the relationship.
- Assesses customer engagement without mistaking politeness for purchase intent.
- Selects one objective and at most one response entry point per turn; social exchanges may need no question or request.
- Drafts concise messages for chat, calls, meetings, objections, and follow-ups.
- Separates confirmed facts, seller assumptions, and unknown information.
- Applies evidence gates to price, inventory, compatibility, delivery, and other commercial claims.
- Stops pressure after explicit rejection or repeated weak responses.
- Explains comparable value and asks for a purchasing step when the necessary conditions are confirmed.
- Uses actual customer feedback to improve the next action and tracks relationship and deal outcomes separately.
- Synthesizes long customer answers before proposing a solution or asking another question.
- Separates one contact's support from the buying organization's technical, commercial, budget, and approval path.
- Separates the seller's own urge to follow up from an actual reason to contact the customer.
- Adapts delivery — pace, pauses, channel, message length — and keeps one goal per turn.
- Keeps humor, small talk, and relationship maintenance inside explicit stop lines.

## Core model

```text
Signal → Stage → Concern → One-turn goal → Action
```

The default message shape is:

```text
Acknowledge → Add one useful value → Leave one easy next step
```

Any part may be omitted when the situation calls for a shorter response. Social exchanges need not turn into a pitch. Explicit rejection should normally lead to acknowledgment and closure of the rejected outreach.

## Install

Clone the repository and run:

```bash
python3 scripts/install.py
```

One installation includes both languages; no language-specific package is needed.
Use `--force` to update an installation with a recoverable backup.
The skill needs no remote service or API credential at use time.

To upgrade from v1.4.0's separate packages:

```bash
python3 scripts/install.py --force --migrate-legacy-en
```

This installs the unified package and archives the old separate English installation
outside skill discovery. No existing installation is deleted.

The installer copies the skill to `~/.codex/skills/consultative-sales-communication` by default. It never installs the repository documentation or tests into the skill directory.
When `--force` replaces an installation, the previous copy is stored in `~/.codex/skill-backups` so it cannot be discovered as a second active Skill.

To choose another skills directory:

```bash
python3 scripts/install.py --skills-dir /path/to/skills
```

## Use

Invoke the skill explicitly:

```text
Use $consultative-sales-communication. The customer said “we already have a long-term supplier.” What should I reply?
```

English-first invocation:

```text
Use $consultative-sales-communication. The customer said “we already have a long-term supplier.” Draft a concise English reply.
```

An explicit output-language request takes priority. Otherwise, the skill follows
the language of your request, falling back to Chinese when unclear. Chinese and
English M01–M26 rules and stop lines align within the same package. English
references are loaded only for English tasks.

Or describe the situation naturally:

```text
The customer hasn't replied to our quote for a week, and there is no new development. Should I follow up? If so, give me a copy-ready reply.
```

The default output is:

```text
Decision: send now / wait / close this turn
Copy-ready reply: ...
Evidence: customer signal ...; one-turn goal ...
Unknowns: ...
```

When the user asks for a short answer, the skill returns only the decision and a reply if one is needed.
For silent waiting, it says “Do not send this turn” and omits the draft.

Try:

```text
Natural contact: The customer posted about finishing a half marathon. We have talked about running before. Help me congratulate them without a product pitch.
Deal progress: The configuration and service scope are confirmed, but the customer has not ordered. Help me propose one concrete purchasing step.
Draft editing: Keep my voice and fix the most important problem in this message.
```

From the installed skill directory, check a draft using a file or standard input:

```bash
python3 scripts/message_lint.py --file /path/to/customer-message.txt
```

`ok` means no implemented rule matched. `matches` provides matched text and locations;
`scope` identifies the heuristic checking boundary. The checker does not verify prices,
stock, compatibility or authority online; review its findings in the conversation's context.

## Repository layout

```text
skills/consultative-sales-communication/  Installable skill package
  languages/en/                           English guide and references inside the same package
README.md                                 Chinese documentation
README.en.md                              English documentation
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

A visible social post is not necessarily public material. Keep real customer screenshots,
conversations, and records within the user's designated private scope, outside this public
package. Do not enumerate friends or use a social topic to bypass a no-contact request.

## Validate

```bash
python3 scripts/audit_public_tree.py
python3 scripts/validate_skill.py
python3 scripts/audit_case_vocabulary.py
python3 -m unittest discover -s tests -v
```

The local release process additionally runs the official Codex `quick_validate.py` script when it is available.

An independent agent's actual answers to eight original synthetic requests, reviewed
by the coordinating agent, are in the [v1.6.0 behavioral spot check](tests/behavioral-review-1.6.0.md).
This is not an automatically scored model evaluation or proof of real sales results.
The [v1.5.0 historical record](tests/behavioral-review-1.5.0.md) is also retained.

`tests/linter_cases.json` contains safe and unsafe near-boundary examples. They verify that the message linter catches pressure and unsupported claims without treating cautious wording such as “不能保证” as a promise. The scenario contracts in `tests/cases.json` are evaluation fixtures, not proof that every model response is correct.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New conversation patterns should be backed by a synthetic regression case and must pass the privacy and unsupported-claim checks.

## License

MIT. See [LICENSE](LICENSE).
