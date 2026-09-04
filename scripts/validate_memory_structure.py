#!/usr/bin/env python3
"""Validate agent-lab Global Memory, Project registry, Unknowns and Issue status."""
from __future__ import annotations
import json, os, re, sys
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "PROJECTS.md"
UNKNOWN = ROOT / "UNKNOWN_REGISTRY.md"
HUB_REQUIRED = ["README.md", "PROJECT_CONTEXT.md", "CURRENT_STATE.md", "NEXT_WORK.md"]
PROJECT_REQUIRED = ["README.md", "PROJECT_CONTEXT.md", "CURRENT_STATE.md", "NEXT_WORK.md", "GITHUB_WORKFLOW.md"]
UNKNOWN_STATUSES = {"OPEN", "REVIEW_DUE", "RESOLVED", "RETAINED_UNKNOWN", "ARCHIVED"}
ISSUE_STATUS = {"status:ready", "status:in-progress", "status:done", "status:verified", "status:blocked", "status:hold"}


def fail(errors: list[str]) -> int:
    for error in errors: print(f"ERROR: {error}")
    return 1


def api_json(url: str, token: str | None = None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "agent-lab-validator"}
    if token: headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=15) as response:
        return json.load(response)


def registered_repositories() -> list[tuple[str, str]]:
    repos = []
    for line in PROJECTS.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "Project ID" in line or "---" in line: continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 2:
            project_id, repo = cells[0], cells[1].strip("`")
            if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) and project_id != "agent-hub":
                repos.append((project_id, repo))
    return repos


def validate_unknown_registry(errors: list[str]) -> None:
    if not UNKNOWN.exists(): errors.append("UNKNOWN_REGISTRY.md is missing"); return
    text = UNKNOWN.read_text(encoding="utf-8")
    required = ["ID", "内容", "状态", "登记日期", "review_by", "复查触发条件", "裁决方", "decision", "evidence"]
    header = next((x for x in text.splitlines() if x.startswith("| ID |")), "")
    for col in required:
        if col not in header: errors.append(f"Unknown registry is missing required column: {col}")
    rows = []
    for line in text.splitlines():
        if not line.startswith("| U-"): continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 9: errors.append(f"Unknown registry row has wrong field count: {line}"); continue
        rows.append(cells)
        item_id, content, status, discovered, review_by, trigger, owner, decision, evidence = cells
        if not re.fullmatch(r"U-[A-Z]+", item_id): errors.append(f"Invalid Unknown ID: {item_id}")
        if status not in UNKNOWN_STATUSES: errors.append(f"Invalid status for {item_id}: {status}")
        if not content or not trigger or not evidence: errors.append(f"Unknown {item_id} is missing content, review trigger, or evidence")
        try: discovered_date = date.fromisoformat(discovered)
        except ValueError: errors.append(f"Invalid discovered date for {item_id}: {discovered}"); discovered_date = None
        if status in {"OPEN", "REVIEW_DUE", "RETAINED_UNKNOWN"}:
            if not review_by: errors.append(f"Active Unknown {item_id} must have review_by")
            else:
                try: review_date = date.fromisoformat(review_by)
                except ValueError: errors.append(f"Invalid review_by for {item_id}: {review_by}"); review_date = None
                if discovered_date and review_date and review_date < discovered_date: errors.append(f"review_by precedes discovered date for {item_id}")
            if owner not in {"Human", "ChatGPT", "Human + ChatGPT"}: errors.append(f"Invalid owner for active Unknown {item_id}: {owner}")
            if decision != "PENDING": errors.append(f"Active Unknown {item_id} must have decision=PENDING")
        elif status == "RESOLVED" and decision in {"", "PENDING"}: errors.append(f"Resolved Unknown {item_id} must record a decision")
    ids = [r[0] for r in rows]
    if len(ids) != len(set(ids)): errors.append("Unknown registry contains duplicate IDs")


def validate_issue_status(errors: list[str]) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY", "watanuo1982/agent-lab")
    if not token:
        print("WARN: GITHUB_TOKEN unavailable; Issue status metadata check skipped")
        return
    try:
        issues = api_json(f"https://api.github.com/repos/{repo}/issues?state=open&per_page=100", token)
    except Exception as exc:
        errors.append(f"Unable to inspect open Issue status labels: {exc}")
        return
    for issue in issues:
        if "pull_request" in issue: continue
        labels = {x["name"] for x in issue.get("labels", []) if x.get("name") in ISSUE_STATUS}
        if len(labels) != 1:
            valid = "|".join(sorted(ISSUE_STATUS))
            errors.append(
                f"Issue #{issue['number']} must have exactly one status:* Label; found {sorted(labels)}. "
                f"Fix: add exactly one of [{valid}] via the GitHub UI or "
                f"POST /repos/{repo}/issues/{issue['number']}/labels. "
                f"See README.md '状态模型' for the transition rule."
            )


def validate_project_registry_remote() -> None:
    """Optional cross-repository check. Requires a token with access to private project repos."""
    token = os.environ.get("PROJECT_REGISTRY_TOKEN")
    if not token:
        print("WARN: PROJECT_REGISTRY_TOKEN unavailable; cross-repository existence/file check skipped")
        return
    errors = []
    for project_id, repo in registered_repositories():
        try:
            metadata = api_json(f"https://api.github.com/repos/{repo}", token)
            default_branch = metadata.get("default_branch", "main")
            for path in PROJECT_REQUIRED:
                api_json(f"https://api.github.com/repos/{repo}/contents/{path}?ref={default_branch}", token)
        except Exception as exc:
            errors.append(f"{project_id} ({repo}) registry check failed: {exc}")
    if errors: raise RuntimeError("; ".join(errors))
    print("OK: PROJECTS.md repository existence and Project Memory files verified")


def main() -> int:
    errors: list[str] = []
    for path in HUB_REQUIRED:
        if not (ROOT / path).exists(): errors.append(f"Agent Hub missing required state file: {path}")
    if not PROJECTS.exists(): return fail(errors + ["PROJECTS.md is missing"])
    # Local registry syntax is always checked. Remote private-repo checks are opt-in via PROJECT_REGISTRY_TOKEN.
    for project_id, repo in registered_repositories():
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo): errors.append(f"Invalid repository reference for {project_id}: {repo}")
    validate_unknown_registry(errors)
    validate_issue_status(errors)
    try: validate_project_registry_remote()
    except RuntimeError as exc: errors.append(str(exc))
    return fail(errors) if errors else (print("OK: agent-lab memory structure, Unknown registry and Issue status are valid") or 0)

if __name__ == "__main__": sys.exit(main())
