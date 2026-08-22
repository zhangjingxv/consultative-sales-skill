#!/usr/bin/env python3
"""Install the packaged skill into a Codex-compatible skills directory."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "consultative-sales-communication"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path.home() / ".codex" / "skills",
        help="parent directory where the skill folder will be installed",
    )
    parser.add_argument("--force", action="store_true", help="replace an existing installation")
    args = parser.parse_args()

    if not (SOURCE / "SKILL.md").is_file():
        parser.error(f"skill package missing: {SOURCE}")

    destination = args.skills_dir.expanduser().resolve() / SOURCE.name
    if destination.exists():
        if not args.force:
            parser.error(f"destination exists: {destination}; use --force to replace it")
        if destination.is_symlink() or not destination.is_dir():
            parser.error(f"refusing to replace non-directory destination: {destination}")
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = destination.with_name(f"{destination.name}.backup-{timestamp}")
        if backup.exists():
            parser.error(f"backup destination already exists: {backup}")
        shutil.move(destination, backup)
        print(f"Backed up existing installation to {backup}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, destination)
    print(f"Installed {SOURCE.name} to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
