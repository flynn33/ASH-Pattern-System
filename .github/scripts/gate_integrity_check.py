#!/usr/bin/env python3
"""Trusted protected-surface gate for pull requests.

The workflow that invokes this script runs with pull_request_target from the
protected base branch and never checks out head-branch code.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass
from fnmatch import fnmatch
from typing import Any


OWNER_DEFAULT = "flynn33"
GOVERNANCE_LABEL = "governance-change"

PROTECTED_EXACT = {
    ".github/CODEOWNERS",
    ".github/workflows/alignment-agent.yml",
    ".github/workflows/canonical-semantic-integrity-agent.yml",
    ".github/workflows/docs-maintenance-agent.yml",
    ".github/workflows/downstream-conformance-agent.yml",
    ".github/workflows/gate-integrity.yml",
    ".github/workflows/math-integrity-agent.yml",
    ".github/workflows/no-ai-attribution.yml",
    ".github/workflows/wiki-maintenance-agent.yml",
    ".github/scripts/_common.py",
    ".github/scripts/alignment_check.py",
    ".github/scripts/docs_maintenance_check.py",
    ".github/scripts/downstream_conformance_check.py",
    ".github/scripts/gate_integrity_check.py",
    ".github/scripts/gate_integrity_selftest.py",
    ".github/scripts/math_integrity_check.py",
    ".github/scripts/no_attribution_check.py",
    ".github/scripts/semantic_integrity_check.py",
    ".github/scripts/wiki_maintenance_check.py",
    "governance/ai-coding-handoff.md",
    "governance/github-agents-governance.md",
    "governance/math-change-notes/2026-05-02-self-contained-canonical-language.md",
    "governance/math-change-notes/README.md",
    "governance/repository-governance.md",
}

PROTECTED_PREFIXES = (
    ".github/workflows/",
    ".github/scripts/",
    ".github/rulesets/",
    "governance/",
)

GOVERNANCE_ALLOWED_EXACT = {
    ".github/CODEOWNERS",
}

GOVERNANCE_ALLOWED_PREFIXES = (
    ".github/workflows/",
    ".github/scripts/",
    ".github/rulesets/",
    "completion-evidence/governance/",
    "governance/",
)

PRODUCT_ALLOWED_PROTECTED_ADDITION_GLOBS = (
    "governance/math-change-notes/*.md",
)

KNOWN_FILE_STATUSES = {
    "added",
    "changed",
    "copied",
    "modified",
    "removed",
    "renamed",
    "unchanged",
}

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class GatePolicyError(RuntimeError):
    pass


@dataclass(frozen=True)
class Violation:
    path: str | None
    message: str


@dataclass(frozen=True)
class GateResult:
    ok: bool
    violations: tuple[Violation, ...]
    changed_count: int
    protected_count: int


def fail(message: str) -> GatePolicyError:
    return GatePolicyError(message)


def valid_path(path: Any) -> str:
    if not isinstance(path, str) or not path:
        raise fail("changed-file payload contains a missing path")
    if path.startswith("/") or "\\" in path:
        raise fail(f"changed-file payload contains an invalid path: {path!r}")
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise fail(f"changed-file payload contains an unsafe path: {path!r}")
    return path


def protected(path: str) -> bool:
    return path in PROTECTED_EXACT or any(path.startswith(prefix) for prefix in PROTECTED_PREFIXES)


def governance_allowed(path: str) -> bool:
    return path in GOVERNANCE_ALLOWED_EXACT or any(
        path.startswith(prefix) for prefix in GOVERNANCE_ALLOWED_PREFIXES
    )


def product_allowed_protected_addition(path: str, status: str) -> bool:
    if status != "added":
        return False
    if path.endswith("/README.md"):
        return False
    return any(fnmatch(path, pattern) for pattern in PRODUCT_ALLOWED_PROTECTED_ADDITION_GLOBS)


def collect_changed_paths(records: list[dict[str, Any]]) -> dict[str, str]:
    changed: dict[str, str] = {}
    for item in records:
        if not isinstance(item, dict):
            raise fail("changed-file payload item is not an object")
        status = item.get("status", "unknown")
        if status not in KNOWN_FILE_STATUSES:
            raise fail(f"changed-file payload contains unknown status: {status!r}")
        filename = valid_path(item.get("filename"))
        changed[filename] = status
        previous = item.get("previous_filename")
        if previous:
            changed[valid_path(previous)] = "renamed-from"
    return changed


def owner_approved_current_head(reviews: list[dict[str, Any]], owner: str, head_sha: str) -> bool:
    latest_state = None
    latest_commit = None
    for review in reviews:
        user = review.get("user") or {}
        if user.get("login") != owner:
            continue
        latest_state = review.get("state")
        latest_commit = review.get("commit_id")
    return latest_state == "APPROVED" and latest_commit == head_sha


def evaluate(
    records: list[dict[str, Any]],
    labels: set[str],
    head_ref: str,
    head_sha: str,
    reviews: list[dict[str, Any]],
    owner: str = OWNER_DEFAULT,
) -> GateResult:
    if not head_ref:
        raise fail("pull-request head ref is empty")
    if not SHA_RE.fullmatch(head_sha):
        raise fail("pull-request head SHA is missing or invalid")

    changed_status = collect_changed_paths(records)
    changed = sorted(changed_status)
    protected_changed = sorted(path for path in changed if protected(path))
    violations: list[Violation] = []

    if not protected_changed:
        return GateResult(True, (), len(changed), 0)

    governance_mode = GOVERNANCE_LABEL in labels
    if not governance_mode:
        for path in protected_changed:
            if not product_allowed_protected_addition(path, changed_status[path]):
                violations.append(Violation(path, "Product pull request changes a protected governance surface"))
        return GateResult(not violations, tuple(violations), len(changed), len(protected_changed))

    if not head_ref.startswith("governance/"):
        violations.append(Violation(None, "Governance change must use a governance/ branch"))

    outside = [path for path in changed if not governance_allowed(path)]
    for path in outside:
        violations.append(Violation(path, "Governance pull request contains a product or unrelated file"))

    if not owner_approved_current_head(reviews, owner, head_sha):
        violations.append(Violation(None, f"Owner approval from {owner} is required on the current head commit"))

    return GateResult(not violations, tuple(violations), len(changed), len(protected_changed))


def request_json(repo: str, token: str, path: str) -> Any:
    url = f"https://api.github.com/repos/{repo}{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def paged_request(repo: str, token: str, path: str, *, max_pages: int = 100) -> list[Any]:
    items: list[Any] = []
    for page in range(1, max_pages + 1):
        sep = "&" if "?" in path else "?"
        page_items = request_json(repo, token, f"{path}{sep}per_page=100&page={page}")
        if not isinstance(page_items, list):
            raise fail(f"GitHub API returned a non-list response for {path}")
        items.extend(page_items)
        if len(page_items) < 100:
            return items
    raise fail(f"GitHub API pagination exceeded {max_pages} pages for {path}")


def pr_file_records(repo: str, token: str, pr_number: str) -> list[dict[str, Any]]:
    items = paged_request(repo, token, f"/pulls/{pr_number}/files")
    if not all(isinstance(item, dict) for item in items):
        raise fail("pull-request files payload contains a non-object item")
    return items


def pr_history_file_records(repo: str, token: str, pr_number: str) -> list[dict[str, Any]]:
    commits = paged_request(repo, token, f"/pulls/{pr_number}/commits")
    records: list[dict[str, Any]] = []
    for commit in commits:
        if not isinstance(commit, dict):
            raise fail("pull-request commits payload contains a non-object item")
        sha = commit.get("sha")
        if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
            raise fail("pull-request commits payload contains an invalid commit SHA")
        detail = request_json(repo, token, f"/commits/{sha}")
        files = detail.get("files")
        if files is None:
            raise fail(f"commit detail for {sha} did not include changed files")
        if not isinstance(files, list):
            raise fail(f"commit detail for {sha} has invalid changed-file payload")
        for file_item in files:
            if not isinstance(file_item, dict):
                raise fail(f"commit detail for {sha} contains a non-object changed-file item")
            records.append(file_item)
    return records


def parse_labels(raw: str) -> set[str]:
    try:
        labels = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise fail(f"labels payload is invalid JSON: {exc}") from exc
    if not isinstance(labels, list) or not all(isinstance(item, str) for item in labels):
        raise fail("labels payload must be a JSON list of strings")
    return set(labels)


def env_required(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise fail(f"required environment variable is missing: {name}")
    return value


def print_violation(violation: Violation) -> None:
    if violation.path:
        print(f"::error file={violation.path}::{violation.message}")
    else:
        print(f"::error::{violation.message}")


def main() -> int:
    try:
        token = env_required("GH_TOKEN")
        repo = env_required("REPOSITORY")
        pr_number = env_required("PR_NUMBER")
        head_ref = env_required("HEAD_REF")
        head_sha = env_required("HEAD_SHA")
        labels = parse_labels(os.environ.get("LABELS_JSON", "[]"))
        owner = os.environ.get("OWNER_LOGIN", OWNER_DEFAULT) or OWNER_DEFAULT

        records = pr_file_records(repo, token, pr_number)
        records.extend(pr_history_file_records(repo, token, pr_number))
        reviews = paged_request(repo, token, f"/pulls/{pr_number}/reviews")
        if not all(isinstance(review, dict) for review in reviews):
            raise fail("pull-request reviews payload contains a non-object item")

        result = evaluate(records, labels, head_ref, head_sha, reviews, owner)
        print(f"Gate Integrity examined {result.changed_count} changed path(s).")
        print(f"Protected changed path(s): {result.protected_count}.")
        if result.ok:
            print("Gate Integrity: protected boundary satisfied.")
            return 0
        for violation in result.violations:
            print_violation(violation)
        return 1
    except GatePolicyError as exc:
        print(f"::error::Gate Integrity failed closed: {exc}")
        return 2
    except Exception as exc:
        print(f"::error::Gate Integrity unexpected failure: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
