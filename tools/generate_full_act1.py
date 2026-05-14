#!/usr/bin/env python3
"""Generate a full Act 1 ChoiceScript route from the public Act 1 prose files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import textwrap


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "starforge-narrative-tools" / "prose" / "act1"
SCENES = ROOT / "web" / "mygame" / "scenes"


@dataclass(frozen=True)
class Scene:
    path: Path
    stem: str
    number: int
    letter: str
    title: str
    scene_name: str


def title_from_stem(stem: str) -> str:
    text = re.sub(r"^\d+[a-z]?_", "", stem)
    return text.replace("_", " ").title()


def scene_from_path(path: Path) -> Scene | None:
    if path.name == "act1_combined.md":
        return None
    match = re.match(r"^(\d+)([a-z]?)_", path.stem)
    if not match:
        return None
    number = int(match.group(1))
    letter = match.group(2)
    title = title_from_stem(path.stem)
    suffix = f"{number:02d}{letter}" if letter else f"{number:02d}"
    scene_name = f"ch_{suffix}_{re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')}"
    return Scene(path, path.stem, number, letter, title, scene_name)


def load_scenes() -> tuple[list[Scene], dict[int, list[Scene]]]:
    scenes = [scene for path in sorted(SOURCE.glob("*.md")) if (scene := scene_from_path(path))]
    main = [scene for scene in scenes if not scene.letter]
    optional: dict[int, list[Scene]] = {}
    for scene in scenes:
        if scene.letter:
            optional.setdefault(scene.number, []).append(scene)
    for values in optional.values():
        values.sort(key=lambda scene: scene.letter)
    return main, optional


def clean_line(line: str) -> str:
    line = line.replace("\u00a0", " ").replace("\ufeff", "").replace("ï»¿", "")
    if line.startswith("*") or line.startswith("#"):
        return "\\" + line
    return line


def prose_text(path: Path) -> str:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(clean_line(line.rstrip()) for line in lines).strip() + "\n"


def write_startup(main: list[Scene], optional: dict[int, list[Scene]]) -> None:
    scene_names = ["startup"]
    for scene in main:
        scene_names.append(scene.scene_name)
        scene_names.extend(extra.scene_name for extra in optional.get(scene.number, []))
    scene_names.append("act1_ending")
    lines = [
        "*title Starforge Act 1",
        "*author Cessnya Lin",
        "",
        "*scene_list",
        *[f"  {name}" for name in scene_names],
        "",
        "*create resolve 50",
        "*create empathy 50",
        "*create tech 50",
        "*create lattice 50",
        "*create crew_trust 50",
        "*create scenes_seen 0",
        "",
        "Full Act 1 is routed here as a ChoiceScript build.",
        "",
        "The spine follows every released Act 1 main chapter. Lettered scenes are exposed as branch choices at the relevant chapter.",
        "",
        "*choice",
        "  #Begin Act 1.",
        f"    *goto_scene {main[0].scene_name}",
        "  #Review the route contract.",
        "    This build routes all released Act 1 main chapters and optional lettered scenes through native ChoiceScript scenes.",
        "    *page_break",
        f"    *goto_scene {main[0].scene_name}",
    ]
    (SCENES / "startup.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_stats() -> None:
    (SCENES / "choicescript_stats.txt").write_text(
        textwrap.dedent(
            """\
            *stat_chart
              percent resolve
              percent empathy
              percent tech
              percent lattice
              percent crew_trust
              text scenes_seen
            """
        ),
        encoding="utf-8",
    )


def scene_choice(target: Scene | None) -> tuple[str, str]:
    if target is None:
        return "Finish Act 1.", "act1_ending"
    return f"Continue to Chapter {target.number:02d}: {target.title}.", target.scene_name


def write_scene(scene: Scene, next_scene: Scene | None, extras: list[Scene]) -> None:
    lines = [f"Chapter {scene.number:02d}: {scene.title}", "", f"Source: {scene.path.name}", "", prose_text(scene.path)]
    lines.extend(["", "*set scenes_seen +1", "", "What does the route do next?", "", "*choice"])
    for extra in extras:
        lines.extend([f"  #Read optional scene {extra.number:02d}{extra.letter}: {extra.title}.", f"    *goto_scene {extra.scene_name}"])
    label, target = scene_choice(next_scene)
    lines.extend([f"  #{label}", f"    *goto_scene {target}"])
    (SCENES / f"{scene.scene_name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_optional(scene: Scene, next_target: Scene | None, next_extra: Scene | None) -> None:
    lines = [f"Optional {scene.number:02d}{scene.letter}: {scene.title}", "", f"Source: {scene.path.name}", "", prose_text(scene.path)]
    lines.extend(["", "*set scenes_seen +1", "", "What does the route do next?", "", "*choice"])
    if next_extra is not None:
        lines.extend([f"  #Continue to optional scene {next_extra.number:02d}{next_extra.letter}: {next_extra.title}.", f"    *goto_scene {next_extra.scene_name}"])
    label, target = scene_choice(next_target)
    lines.extend([f"  #{label}", f"    *goto_scene {target}"])
    (SCENES / f"{scene.scene_name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_ending() -> None:
    (SCENES / "act1_ending.txt").write_text(
        textwrap.dedent(
            """\
            Act 1 route complete.

            Scenes seen: ${scenes_seen}

            Resolve, empathy, tech, lattice, and crew trust remain available for the next adaptation pass.

            *ending
            """
        ),
        encoding="utf-8",
    )


def main() -> int:
    main_scenes, optional = load_scenes()
    if not main_scenes:
        print(f"no Act 1 scenes found at {SOURCE}")
        return 1
    SCENES.mkdir(parents=True, exist_ok=True)
    for path in SCENES.glob("*.txt"):
        path.unlink()
    write_startup(main_scenes, optional)
    write_stats()
    for index, scene in enumerate(main_scenes):
        next_scene = main_scenes[index + 1] if index + 1 < len(main_scenes) else None
        extras = optional.get(scene.number, [])
        write_scene(scene, next_scene, extras)
        for extra_index, extra in enumerate(extras):
            next_extra = extras[extra_index + 1] if extra_index + 1 < len(extras) else None
            write_optional(extra, next_scene, next_extra)
    write_ending()
    print(f"generated {len(main_scenes)} main scenes and {sum(len(values) for values in optional.values())} optional scenes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
