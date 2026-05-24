#!/usr/bin/env python3
"""Deterministic playtest audit for the ChoiceScript route."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENES = ROOT / "web" / "mygame" / "scenes"
QUEUE_MARKERS = re.compile(r"\b(TODO|FIXME|DEAD[- ]?LETTER|PLAYTEST[- ]?QUEUE|BALANCE[- ]?QUEUE)\b|\bBUG:", re.IGNORECASE)
SCENE_REF = re.compile(r"^\s*\*(?:goto_scene|gosub_scene)\s+([A-Za-z0-9_]+)", re.IGNORECASE)


def parse_scene_list(startup: Path) -> list[str]:
    lines = startup.read_text(encoding="utf-8").splitlines()
    scenes: list[str] = []
    in_list = False
    for line in lines:
        if line.strip().lower() == "*scene_list":
            in_list = True
            continue
        if in_list:
            if not line.startswith("  "):
                break
            scene = line.strip()
            if scene:
                scenes.append(scene)
    return scenes


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    startup = SCENES / "startup.txt"
    scene_list = parse_scene_list(startup)
    scene_set = set(scene_list)
    files = {path.stem: path for path in SCENES.glob("*.txt")}
    allowed_extra = {"choicescript_stats"}

    for scene in scene_list:
        if scene not in files:
            errors.append(f"scene_list entry has no scene file: {scene}")

    for scene in sorted(set(files) - scene_set - allowed_extra):
        errors.append(f"scene file is not routed through scene_list: {scene}")

    if scene_list[0] != "startup":
        errors.append("scene_list must begin with startup")
    if "act1_ending" not in scene_set:
        errors.append("scene_list must include act1_ending")

    scene_refs = []
    choices = 0
    stat_mutations = 0
    marker_hits = []
    for scene, path in files.items():
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if line.lstrip().startswith("#"):
                choices += 1
            if line.strip().lower().startswith("*set "):
                stat_mutations += 1
            ref = SCENE_REF.match(line)
            if ref:
                target = ref.group(1)
                scene_refs.append((scene, line_no, target))
                if target not in files:
                    errors.append(f"{scene}:{line_no}: missing scene target {target}")
            if QUEUE_MARKERS.search(line):
                marker_hits.append(f"{scene}:{line_no}: {line.strip()}")

    if choices < 70:
        warnings.append(f"choice count is low for full Act 1 route: {choices}")
    if stat_mutations < 60:
        warnings.append(f"stat mutation count is low for full Act 1 route: {stat_mutations}")
    warnings.extend(marker_hits)

    print("ChoiceScript playtest audit")
    print(f"- scene_list entries: {len(scene_list)}")
    print(f"- scene files: {len(files)}")
    print(f"- choices: {choices}")
    print(f"- stat mutations: {stat_mutations}")
    print(f"- scene refs: {len(scene_refs)}")
    print(f"- dead-letter marker hits: {len(marker_hits)}")

    if warnings:
        print("\nDead-letter / balance queue:")
        for warning in warnings[:40]:
            print(f"- {warning}")
        if len(warnings) > 40:
            print(f"- ... {len(warnings) - 40} more queue item(s)")

    if errors:
        print("\nplaytest audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("playtest audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

