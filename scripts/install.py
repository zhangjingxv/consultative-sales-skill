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
    parser.add_argument("--language", choices=("zh", "en", "both"), default="zh",
                        help="Chinese (default), English, or both independent packages")
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help="backup directory used with --force; defaults beside the skills directory",
    )
    args = parser.parse_args()

    sources = ([SOURCE] if args.language == "zh" else
               [SOURCE.with_name(SOURCE.name + "-en")] if args.language == "en" else
               [SOURCE, SOURCE.with_name(SOURCE.name + "-en")])
    # Preflight every selected package before replacing any existing installation.
    for source in sources:
        if not (source / "SKILL.md").is_file():
            parser.error(f"skill package missing: {source}")
        destination = args.skills_dir.expanduser().resolve() / source.name
        if not destination.exists():
            continue
        if not args.force:
            parser.error(f"destination exists: {destination}; use --force to replace it")
        if destination.is_symlink() or not destination.is_dir():
            parser.error(f"refusing to replace non-directory destination: {destination}")

    for source in sources:
        install_source(source, args, parser)
    return 0


def install_source(source: Path, args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    destination = args.skills_dir.expanduser().resolve() / source.name
    if destination.exists():
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup_root = (
            args.backup_dir.expanduser().resolve()
            if args.backup_dir
            else args.skills_dir.expanduser().resolve().parent / "skill-backups"
        )
        backup_root.mkdir(parents=True, exist_ok=True)
        backup = backup_root / f"{destination.name}-{timestamp}"
        if backup.exists():
            parser.error(f"backup destination already exists: {backup}")
        shutil.move(destination, backup)
        print(f"Backed up existing installation to {backup}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    print(f"Installed {source.name} to {destination}")


if __name__ == "__main__":
    raise SystemExit(main())
