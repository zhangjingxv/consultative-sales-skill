#!/usr/bin/env python3
"""Dependency-free structural validation for the packaged skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "consultative-sales-communication"


def main() -> int:
    failures: list[str] = []
    entry = SKILL / "SKILL.md"
    if not entry.is_file():
        failures.append("SKILL.md is missing")
    else:
        text = entry.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
        if not match:
            failures.append("SKILL.md frontmatter is missing or malformed")
        else:
            pairs = []
            for line in match.group(1).splitlines():
                if ":" not in line:
                    failures.append(f"invalid frontmatter line: {line}")
                    continue
                key, value = line.split(":", 1)
                pairs.append((key.strip(), value.strip()))
            keys = [key for key, _ in pairs]
            if keys != ["name", "description"]:
                failures.append(f"frontmatter keys must be name, description; got {keys}")
            values = dict(pairs)
            name = values.get("name", "")
            if not re.fullmatch(r"[a-z0-9-]{1,63}", name):
                failures.append(f"invalid skill name: {name}")
            if name != SKILL.name:
                failures.append(f"folder/name mismatch: {SKILL.name} vs {name}")
            if len(values.get("description", "")) < 40:
                failures.append("description is too short to trigger reliably")

        for link in re.findall(r"\]\((references/[^)]+)\)", text):
            if not (SKILL / link).is_file():
                failures.append(f"missing reference: {link}")

    agent_yaml = SKILL / "agents" / "openai.yaml"
    if not agent_yaml.is_file():
        failures.append("agents/openai.yaml is missing")
    elif "$consultative-sales-communication" not in agent_yaml.read_text(encoding="utf-8"):
        failures.append("default prompt must mention $consultative-sales-communication")

    if failures:
        print("Skill validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("Skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
