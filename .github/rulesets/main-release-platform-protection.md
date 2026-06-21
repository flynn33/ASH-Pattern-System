# Main, Release, and Platform Protection Ruleset

This file records the required server-side ruleset shape. It is not evidence
that GitHub protection is active; authenticated repository settings output or
owner screenshots must be stored under `completion-evidence/governance/`.

## Branch Targets

- `main`
- `release/*`
- `Mac/iOS`
- `windows-cpp`

## Required Controls

- Require pull requests before merging.
- Prohibit direct pushes.
- Prohibit force pushes.
- Prohibit branch deletion.
- Require at least one approving review.
- Require CODEOWNER approval for protected paths.
- Dismiss stale approvals after new commits.
- Require approval of the latest reviewable push.
- Require all conversations to be resolved.
- Require branches to be up to date before merge.
- Require linear history unless the owner records a reviewed merge policy.
- Configure no bypass actors for normal operation.
- Restrict ruleset edits to owner-controlled governance changes.

## Required Checks

- Alignment check
- Canonical semantic integrity check
- Math integrity check
- Check for AI Attribution
- Docs maintenance check
- Wiki maintenance check
- Gate Integrity
- Release Readiness when present

Platform release branches must additionally require their owner-approved build,
test, conformance, accessibility, security, packaging, installation, signing,
and release checks.

## Tags

Release tags must be immutable after publication. Force updates and deletion
must be blocked for:

- `aps-v*`
- `aps-ios-v*`
- `aps-macos-v*`
- `aps-windows-v*`
