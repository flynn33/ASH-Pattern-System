#!/usr/bin/env python3
"""Local fixtures for the Gate Integrity protected-surface policy."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from gate_integrity_check import GatePolicyError, evaluate


HEAD = "1" * 40
OLD = "0" * 40
ROOT = Path(__file__).resolve().parents[2]


def item(path: str, status: str = "modified", previous: str | None = None) -> dict:
    data = {"filename": path, "status": status}
    if previous:
        data["previous_filename"] = previous
    return data


def approval(commit: str = HEAD) -> list[dict]:
    return [{"user": {"login": "flynn33"}, "state": "APPROVED", "commit_id": commit}]


def case(name: str, records: list[dict], ok: bool, *, labels=None, branch="release/aps-1.0.0-completion-clean", reviews=None):
    labels = set(labels or [])
    reviews = [] if reviews is None else reviews
    try:
        result = evaluate(records, labels, branch, HEAD, reviews)
        actual = result.ok
    except GatePolicyError:
        actual = False
    if actual != ok:
        raise AssertionError(f"{name}: expected ok={ok}, got ok={actual}")


def assert_workflow_hardening() -> None:
    workflow_dir = ROOT / ".github" / "workflows"
    mutable_uses = []
    for path in sorted(workflow_dir.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped.startswith("uses:"):
                continue
            if not re.search(r"@[0-9a-f]{40}\s*$", stripped):
                mutable_uses.append(f"{path.relative_to(ROOT)}:{line_no}: {stripped}")
        if "continue-on-error" in text:
            raise AssertionError(f"{path.relative_to(ROOT)} contains continue-on-error")

    if mutable_uses:
        raise AssertionError("mutable action reference(s): " + "; ".join(mutable_uses))

    gate_text = (workflow_dir / "gate-integrity.yml").read_text(encoding="utf-8")
    required = [
        "pull_request_target:",
        "contents: read",
        "pull-requests: read",
        "github.event.pull_request.base.sha",
        "gate_integrity_check.py",
    ]
    for token in required:
        if token not in gate_text:
            raise AssertionError(f"gate-integrity.yml missing required token: {token}")


def main() -> int:
    case("legitimate product file", [item("README.md")], True)
    case(
        "product math-change note addition",
        [item("specs/core/state-admissibility.pseudo.md"), item("governance/math-change-notes/2026-06-21-product-semantic-closure.md", "added")],
        True,
    )
    case("product math-change note readme edit", [item("governance/math-change-notes/README.md")], False)
    case(
        "product existing math-change note edit",
        [item("governance/math-change-notes/2026-05-02-self-contained-canonical-language.md")],
        False,
    )
    case("whole workflow bypass", [item(".github/workflows/alignment-agent.yml")], False)
    case("pattern-line exemption", [item(".github/scripts/gate_integrity_check.py")], False)
    case("changed-file skip for checker", [item(".github/scripts/gate_integrity_selftest.py")], False)
    case("actor or branch exception", [item(".github/workflows/gate-integrity.yml")], False, reviews=approval())
    case("narrowed trigger", [item(".github/workflows/gate-integrity.yml")], False)
    case("continue-on-error injection", [item(".github/workflows/docs-maintenance-agent.yml")], False)
    case("report-only downgrade", [item(".github/workflows/wiki-maintenance-agent.yml")], False)
    case("success replacement", [item(".github/scripts/math_integrity_check.py")], False)
    case("swallowed exception", [item(".github/scripts/docs_maintenance_check.py")], False)
    case(
        "deleted or renamed checker",
        [item(".github/scripts/gate_integrity_check_disabled.py", "renamed", ".github/scripts/gate_integrity_check.py")],
        False,
    )
    case("required-check ruleset removal", [item(".github/rulesets/main-release-platform-protection.md")], False)
    case(
        "mixed governance and product",
        [item(".github/workflows/gate-integrity.yml"), item("README.md")],
        False,
        labels={"governance-change"},
        branch="governance/gate-integrity-hardening",
        reviews=approval(),
    )
    case("branch-range logic modification", [item(".github/scripts/no_attribution_check.py")], False)
    case(
        "protected path touched then reverted in branch history",
        [item("docs/00-repository-purpose.md"), item(".github/workflows/no-ai-attribution.yml")],
        False,
    )
    case(
        "trusted governance-only change",
        [
            item(".github/workflows/gate-integrity.yml"),
            item(".github/scripts/gate_integrity_check.py"),
            item(".github/scripts/gate_integrity_selftest.py"),
            item(".github/CODEOWNERS"),
            item(".github/rulesets/main-release-platform-protection.md", "added"),
            item("completion-evidence/governance/gate-integrity-hardening-request.md", "added"),
        ],
        True,
        labels={"governance-change"},
        branch="governance/gate-integrity-hardening",
        reviews=approval(),
    )
    case(
        "stale owner approval",
        [item(".github/workflows/gate-integrity.yml")],
        False,
        labels={"governance-change"},
        branch="governance/gate-integrity-hardening",
        reviews=approval(OLD),
    )
    case(
        "missing owner approval",
        [item(".github/workflows/gate-integrity.yml")],
        False,
        labels={"governance-change"},
        branch="governance/gate-integrity-hardening",
    )

    try:
        evaluate([item("/absolute/path")], set(), "release/x", HEAD, [])
        raise AssertionError("malformed path did not fail closed")
    except GatePolicyError:
        pass

    assert_workflow_hardening()
    print("Gate Integrity self-test: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
