#!/usr/bin/env python3
"""Validate that the public ChoiceScript demo stays within the released Act 1 slice."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNRELEASED_ACT = re.compile(r"act([2-9]|[1-9][0-9])", re.IGNORECASE)
IGNORED_DIRS = {".git", ".pytest_cache", "__pycache__", "tools/vendor/choicescript"}
FORBIDDEN_SUFFIXES = {".rpyc", ".rpyb", ".save", ".pyc"}
FORBIDDEN_TEXT = {
    "act2_",
    "act3_",
    "full corpus",
    "full cleaned",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def ignored(path: Path) -> bool:
    posix = rel(path)
    return any(part in {".git", ".pytest_cache", "__pycache__"} for part in path.parts) or posix.startswith(
        "tools/vendor/choicescript/"
    )


def main() -> int:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if path == Path(__file__).resolve() or ignored(path):
            continue
        if path.is_file() and path.suffix in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden generated file: {rel(path)}")
        if any(UNRELEASED_ACT.search(part) for part in path.parts):
            errors.append(f"unreleased act reference in public source path: {rel(path)}")
        if path.is_file() and path.suffix in {".md", ".txt", ".py", ".json"}:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            if any(token in text for token in FORBIDDEN_TEXT):
                errors.append(f"forbidden private-scope text in {rel(path)}")

    if errors:
        print("public-scope validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("public-scope validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
