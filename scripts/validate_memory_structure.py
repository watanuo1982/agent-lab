#!/usr/bin/env python3
"""Validate agent-lab Global Memory structure and registered Project Memory.

This is intentionally dependency-free so it can run in GitHub Actions and locally.
It checks repository registration, required project-memory files, and Unknown registry schema.
"""

from __future__ import annotations

import re
import sys
from datetime import date
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

UNKNOWN_STATUSES = {
    "OPEN",
    "REVIEW_DUE",
    "RESOLVED",
    "RETAINED_UNKNOWN",
    "ARCHIVED",
}


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


def parse_date(value: str, field: str, item_id: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"Invalid {field} for {item_id}: {value}")
        return None


def validate_unknown_registry(errors: list[str]) -> None:
    if not UNKNOWN.exists():
        errors.append("UNKNOWN_REGISTRY.md is missing")
        return

    text = UNKNOWN.read_text(encoding="utf-8")
    required_columns = [
        "ID",
        "内容",
        "状态",
        "登记日期",
        "review_by",
        "复查触发条件",
        "裁决方",
        "decision",
        "evidence",
    ]
    header = next((line for line in text.splitlines() if line.startswith("| ID |")), "")
    for column in required_columns:
        if column not in header:
            errors.append(f"Unknown registry is missing required column: {column}")

    rows = []
    for line in text.splitlines():
        if not line.startswith("| U-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 9:
            errors.append(f"Unknown registry row has wrong field count: {line}")
            continue
        rows.append(cells)

        item_id, content, status, discovered, review_by, trigger, owner, decision, evidence = cells
        if not re.fullmatch(r"U-[A-Z]+", item_id):
            errors.append(f"Invalid Unknown ID: {item_id}")
        if status not in UNKNOWN_STATUSES:
            errors.append(f"Invalid status for {item_id}: {status}")
        if not content or not trigger or not evidence:
            errors.append(f"Unknown {item_id} is missing content, review trigger, or evidence")
        discovered_date = parse_date(discovered, "discovered date", item_id, errors)

        if status in {"OPEN", "REVIEW_DUE", "RETAINED_UNKNOWN"}:
            if review_by == "":
                errors.append(f"Active Unknown {item_id} must have review_by")
            else:
                review_date = parse_date(review_by, "review_by", item_id, errors)
                if discovered_date and review_date and review_date < discovered_date:
                    errors.append(f"review_by precedes discovered date for {item_id}")
            if owner not in {"Human", "ChatGPT", "Human + ChatGPT"}:
                errors.append(f"Invalid owner for active Unknown {item_id}: {owner}")
            if decision != "PENDING":
                errors.append(f"Active Unknown {item_id} must have decision=PENDING")
        else:
            if status == "RESOLVED" and decision in {"", "PENDING"}:
                errors.append(f"Resolved Unknown {item_id} must record a decision")

    # IDs are historical and must be unique; they are never reused.
    ids = [row[0] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("Unknown registry contains duplicate IDs")


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

    print("OK: agent-lab memory structure and Unknown registry are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
