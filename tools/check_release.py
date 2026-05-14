#!/usr/bin/env python3
"""Run deterministic release gates for the ChoiceScript demo repo."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "tools" / "vendor" / "choicescript"
SOURCE_GAME = ROOT / "web" / "mygame"
TEST_GAME_NAME = "starforge_test"
TEST_GAME = ENGINE / "web" / TEST_GAME_NAME


def run(label: str, command: list[str], cwd: Path = ROOT) -> int:
    print(f"\n== {label} ==")
    print("+ " + " ".join(command))
    return subprocess.run(command, cwd=cwd, check=False).returncode


def run_captured(label: str, command: list[str], cwd: Path = ROOT) -> int:
    print(f"\n== {label} ==")
    print("+ " + " ".join(command))
    result = subprocess.run(command, cwd=cwd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = result.stdout.splitlines()
    if result.returncode == 0:
        summary = [line for line in lines if "PASSED" in line or line.startswith("Time:")]
        for line in summary[-5:]:
            print(line)
    else:
        print(result.stdout)
    return result.returncode


def prepare_test_game() -> None:
    if TEST_GAME.exists():
        shutil.rmtree(TEST_GAME)
    shutil.copytree(SOURCE_GAME, TEST_GAME)


def clean_test_game() -> None:
    if TEST_GAME.exists():
        shutil.rmtree(TEST_GAME)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--regenerate", action="store_true", help="Regenerate ChoiceScript scenes from the sibling public Act 1 corpus before validating.")
    args = parser.parse_args()

    if not (ENGINE / "quicktest.js").exists():
        print("ChoiceScript engine missing; expected tools/vendor/choicescript/quicktest.js")
        return 1

    failures = 0
    if args.regenerate:
        failures += run("Full Act 1 route generation", [sys.executable, "tools/generate_full_act1.py"])
    failures += run("Public-scope validation", [sys.executable, "tools/validate_public_scope.py"])

    prepare_test_game()
    try:
        failures += run_captured("ChoiceScript quicktest", ["node", "quicktest.js", TEST_GAME_NAME], ENGINE)
        failures += run_captured(
            "ChoiceScript randomtest",
            [
                "node",
                "randomtest.js",
                f"game={TEST_GAME_NAME}",
                "num=10000",
                "seed=0",
                "showCoverage=false",
                "showChoices=false",
            ],
            ENGINE,
        )
    finally:
        clean_test_game()

    if failures:
        print(f"\nrelease gate failed: {failures} check(s) failed")
        return 1

    print("\nrelease gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
