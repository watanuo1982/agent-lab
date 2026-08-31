#!/usr/bin/env python3
"""Validate agent-lab Global Memory structure and registered Project Memory.

This is intentionally dependency-free so it can run in GitHub Actions and locally.
It checks repository registration, required project-memory files, and Unknown registry fields.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "PROJECTS.md"
UNKNOWN = ROOT / "UNKNOWN_REGISTRY.md"

REQUIRED = [
    "README.md",
    "PROJECT_CONTEXT.md",
    "CURRENT_STATE.md",
    "NEXT_WORK.md",
    "GITHUB_WORKFLOW.md",
]


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR: {error}")
    return 1


def registered_repositories() -> list[tuple[str, str]]:
    repos = []
    for line in PROJECTS.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "Project ID" in line or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        project_id, repo = cells[0], cells[1].strip("`")
        if repo.startswith("watanuo1982/") and project_id != "agent-hub":
            repos.append((project_id, repo))
    return repos


def remote_exists(repo: str, path: str) -> bool:
    url = f"https://raw.githubusercontent.com/{repo}/main/{path}"
    request = Request(url, method="HEAD", headers={"User-Agent": "agent-lab-memory-validator"})
    try:
        with urlopen(request, timeout=10):
            return True
    except Exception:
        return False


def validate_unknown_registry(errors: list[str]) -> None:
    if not UNKNOWN.exists():
        errors.append("UNKNOWN_REGISTRY.md is missing")
        return
    text = UNKNOWN.read_text(encoding="utf-8")
    required_columns = ["ID", "Status", "Discovered", "Review by", "Owner", "Decision", "Evidence"]
    header = next((line for line in text.splitlines() if line.startswith("| ID |")), "")
    for column in required_columns:
        if column not in header:
            errors.append(f"Unknown registry is missing required column: {column}")
    for line in text.splitlines():
        if not line.startswith("| U-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 7:
            errors.append(f"Unknown registry row has wrong field count: {line}")
            continue
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[2]):
            errors.append(f"Invalid discovered date for {cells[0]}: {cells[2]}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[3]):
            errors.append(f"Invalid review_by date for {cells[0]}: {cells[3]}")
        if cells[5] == "":
            errors.append(f"Unknown {cells[0]} has empty decision")


def main() -> int:
    errors: list[str] = []
    if not PROJECTS.exists():
        return fail(["PROJECTS.md is missing"])

    for project_id, repo in registered_repositories():
        for path in REQUIRED:
            if not remote_exists(repo, path):
                errors.append(f"{project_id} ({repo}) missing required Project Memory file: {path}")

    validate_unknown_registry(errors)

    if errors:
        return fail(errors)

    print("OK: agent-lab memory structure and registered Project Memory are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
