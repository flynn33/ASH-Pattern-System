# Server Ruleset Evidence

Collected on 2026-06-21 from the GitHub repository rulesets API.

## Branch Ruleset

- Ruleset ID: `17945521`
- Name: `APS bootstrap branch protection`
- Target: `branch`
- Enforcement: `active`
- Bypass actors: `[]`
- Target refs:
  - `refs/heads/main`
  - `refs/heads/release/*`
  - `refs/heads/Mac/iOS`
  - `refs/heads/windows-cpp`
- Rules:
  - `deletion`
  - `non_fast_forward`
  - `required_linear_history`
  - `pull_request`
  - `required_status_checks`
- Required checks:
  - `Alignment check`
  - `Canonical semantic integrity check`
  - `Math integrity check`
  - `Check for AI Attribution`
  - `Docs maintenance check`
  - `Wiki maintenance check`

Gate Integrity is not required in this bootstrap ruleset because
`.github/workflows/gate-integrity.yml` is not yet present on protected `main`.
After the bootstrap governance pull request is merged, this ruleset must be
updated to require `Gate Integrity` before any product completion branch is
created.

## Tag Ruleset

- Ruleset ID: `17945522`
- Name: `APS release tag immutability`
- Target: `tag`
- Enforcement: `active`
- Bypass actors: `[]`
- Target refs:
  - `refs/tags/aps-v*`
  - `refs/tags/aps-ios-v*`
  - `refs/tags/aps-macos-v*`
  - `refs/tags/aps-windows-v*`
- Rules:
  - `deletion`
  - `non_fast_forward`
  - `update`

## Remaining Server-Side Gate

Product completion remains blocked until:

- PR #5 receives GitHub-valid owner review after the latest push;
- PR #5 is merged;
- the branch ruleset is updated to require `Gate Integrity`;
- the hardened `main` SHA is recorded.
