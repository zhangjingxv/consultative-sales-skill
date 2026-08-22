#!/usr/bin/env python3
"""Reject files that should never enter the public skill repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache"}
DENIED_SUFFIXES = {
    ".pdf", ".epub", ".zip", ".7z", ".rar", ".doc", ".docx", ".xls", ".xlsx"
}
MAX_FILE_BYTES = 1_000_000
SECRET_PATTERNS = {
    "generic API key": re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}"),
    "GitHub token": re.compile(r"gh[opsu]_[A-Za-z0-9]{20,}"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def iter_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts)
    )


def main() -> int:
    failures: list[str] = []
    for path in iter_files():
        relative = path.relative_to(ROOT)
        if path.suffix.lower() in DENIED_SUFFIXES:
            failures.append(f"denied file type: {relative}")
            continue
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            failures.append(f"oversized file ({size} bytes): {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"unexpected binary file: {relative}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"possible {label}: {relative}")

    if failures:
        print("Public-tree audit failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Public-tree audit passed: {len(iter_files())} files checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
