#!/usr/bin/env python3
"""校验 tests/cases.json 的判定标签是否有权威口径。

检查三类事实：
1. 案例使用的每个 expected_decision 都能在 decision-vocabulary.md 中找到定义。
2. 每个定义都同时写明「可观测行为」与「反例」，缺一不算可判定。
3. 文件中是否有已定义但没有任何案例使用的标签（仅报告，不判失败）。
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "consultative-sales-communication"
VOCAB = SKILL / "references" / "decision-vocabulary.md"
CASES = ROOT / "tests" / "cases.json"


def load_definitions(text: str) -> dict[str, str]:
    """按 `### label` 切块，返回 label -> 正文。"""
    definitions: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^###\s+([a-z0-9_]+)\s*$", line)
        if match:
            if current is not None:
                definitions[current] = "\n".join(buffer)
            current = match.group(1)
            buffer = []
            continue
        if current is not None:
            buffer.append(line)
    if current is not None:
        definitions[current] = "\n".join(buffer)
    return definitions


def main() -> int:
    definitions = load_definitions(VOCAB.read_text(encoding="utf-8"))
    cases = json.loads(CASES.read_text(encoding="utf-8"))

    usage: dict[str, list[str]] = {}
    for case in cases:
        usage.setdefault(case["expected_decision"], []).append(case["id"])

    missing = sorted(label for label in usage if label not in definitions)
    thin = sorted(
        label
        for label, body in definitions.items()
        if "可观测行为" not in body or "反例" not in body
    )
    unused = sorted(label for label in definitions if label not in usage)

    print(f"cases={len(cases)} labels_used={len(usage)} labels_defined={len(definitions)}")
    for name, items in (
        ("missing_definition", missing),
        ("thin_definition", thin),
        ("defined_but_unused", unused),
    ):
        suffix = ": " + ", ".join(items) if items else ""
        print(f"{name}={len(items)}{suffix}")

    ok = not missing and not thin
    print("ok=" + ("true" if ok else "false"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
