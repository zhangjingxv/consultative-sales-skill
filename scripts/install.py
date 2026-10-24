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
    parser.add_argument("--migrate-legacy-en", action="store_true",
                        help="archive the old separate English installation after installing the unified package")
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help="backup directory used with --force; defaults beside the skills directory",
    )
    args = parser.parse_args()

    if not (SOURCE / "SKILL.md").is_file():
        parser.error(f"skill package missing: {SOURCE}")
    skills_dir = args.skills_dir.expanduser().resolve()
    destination = skills_dir / SOURCE.name
    legacy = skills_dir / (SOURCE.name + "-en")
    backup_root = (args.backup_dir.expanduser().resolve() if args.backup_dir
                   else skills_dir.parent / "skill-backups")
    if backup_root == skills_dir or skills_dir in backup_root.parents:
        parser.error("backup directory must be outside skill discovery")
    # Preflight selected targets before changing either installation.
    targets = [destination] + ([legacy] if args.migrate_legacy_en else [])
    for target in targets:
        if target.is_symlink() or (target.exists() and not target.is_dir()):
            parser.error(f"refusing to replace non-directory destination: {target}")
    if destination.exists() and not args.force:
        parser.error(f"destination exists: {destination}; use --force to replace it")
    if args.migrate_legacy_en and legacy.exists():
        entry = legacy / "SKILL.md"
        if not entry.is_file() or f"name: {legacy.name}\n" not in entry.read_text(encoding="utf-8"):
            parser.error("legacy English skill identity does not match; refusing migration")
    if destination.exists():
        archive(destination, backup_root, parser)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, destination,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store"))
    print(f"Installed {SOURCE.name} (Chinese + English) to {destination}")
    if args.migrate_legacy_en and legacy.exists():
        archive(legacy, backup_root, parser)
    return 0


def archive(destination: Path, backup_root: Path, parser: argparse.ArgumentParser) -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup_root.mkdir(parents=True, exist_ok=True)
    backup = backup_root / f"{destination.name}-{timestamp}"
    if backup.exists():
        parser.error(f"backup destination already exists: {backup}")
    shutil.move(destination, backup)
    print(f"Backed up existing installation to {backup}")


if __name__ == "__main__":
    raise SystemExit(main())
