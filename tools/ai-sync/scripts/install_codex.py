#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
AI_SYNC_ROOT = REPO_ROOT / "tools" / "ai-sync"
REGISTRY_PATH = AI_SYNC_ROOT / "registry.yaml"
CODEX_PLUGINS_DIR = REPO_ROOT / "plugins" / "codex"


def load_registry() -> dict[str, Any]:
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise SystemExit("registry.yaml must contain a mapping at the top level")
    return data


def default_dest() -> Path:
    return Path("~/.codex/skills").expanduser()


def install(adapter: str, dest: Path) -> list[Path]:
    source = CODEX_PLUGINS_DIR / f"epic-workflow-{adapter}" / "skills"
    if not source.exists():
        raise SystemExit(
            f"Codex plugin skills for adapter `{adapter}` do not exist. Run render.py first."
        )

    dest.mkdir(parents=True, exist_ok=True)
    installed: list[Path] = []
    for source_skill in sorted(path for path in source.iterdir() if path.is_dir()):
        target = dest / source_skill.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source_skill, target)
        installed.append(target)
    return installed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install rendered Codex plugin skills into ~/.codex/skills for local development."
    )
    parser.add_argument(
        "--adapter",
        default="github",
        choices=["github", "tkt"],
        help="Rendered Codex adapter to install",
    )
    parser.add_argument("--dest", help="Override the Codex skills install directory")
    args = parser.parse_args()

    load_registry()
    destination = Path(args.dest).expanduser() if args.dest else default_dest()
    installed = install(args.adapter, destination)

    print(f"Installed {len(installed)} Codex skill(s) into {destination}.")
    for path in installed:
        print(f"- {path}")
    print("For normal distribution, add the marketplace and install through Codex's plugin manager.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
