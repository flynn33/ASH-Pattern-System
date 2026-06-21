# Governance Change Request

## Scope

- Protected paths changed:
  - `.github/CODEOWNERS`
  - `.github/rulesets/main-release-platform-protection.md`
  - `.github/scripts/_common.py`
  - `.github/scripts/alignment_check.py`
  - `.github/scripts/gate_integrity_check.py`
  - `.github/scripts/gate_integrity_selftest.py`
  - `.github/scripts/no_attribution_check.py`
  - `.github/workflows/*.yml`
  - `governance/github-agents-governance.md`
  - `governance/repository-governance.md`
- Base branch and SHA: `main` at `e123f5d7fdbb381179971f721a3292c31eb1cbc2`
- Head branch and SHA: `governance/gate-integrity-hardening` at the branch `HEAD` commit containing this evidence. Resolve with `git rev-parse governance/gate-integrity-hardening` after the final push.
- Reason a product-only remediation is insufficient: product branches are not allowed to modify the workflows, scripts, CODEOWNERS, ruleset policy, or governance boundary that evaluate product work.

## Behavior before change

- Failing or unsafe behavior:
  - sentinel workflows ran in report-only mode;
  - workflow actions used mutable major-version refs;
  - the downstream reusable workflow fetched canonical scripts from mutable `main`;
  - no trusted `pull_request_target` Gate Integrity check existed;
  - no CODEOWNERS file existed;
  - attribution checks did not inspect branch, tag, or changed-path metadata.
- Reproduction command or fixture:
  - `python3 .github/scripts/gate_integrity_selftest.py` was unavailable before this change.
- Evidence:
  - baseline `main` contains no `.github/workflows/gate-integrity.yml`.

## Proposed behavior

- Exact policy change:
  - add trusted Gate Integrity from protected base code;
  - add owner CODEOWNERS coverage for protected paths;
  - pin GitHub Actions to full commit SHAs;
  - promote canonical sentinels to blocking workflow mode;
  - remove mutable canonical `main` fetch from downstream conformance workflow;
  - harden attribution metadata checks.
- Why it does not weaken the gate:
  - product pull requests fail on any protected path touched in final diff or branch history;
  - governance changes require `governance/` branch, `governance-change` label, governance-only paths, and owner approval on the current head commit;
  - API, payload, pagination, and policy errors fail closed.
- Compatibility and false-positive impact:
  - ordinary product documentation/spec changes outside protected paths remain allowed;
  - governance-only changes require explicit owner review;
  - wiki and docs drift notices remain warnings while hard violations block.

## Self-protection review

- [x] No product files changed.
- [x] No whole-file, path, actor, branch, author, or content bypass added.
- [x] No required trigger narrowed.
- [x] No required failure changed to warning or success.
- [x] No report-only or `continue-on-error` escape introduced.
- [x] Deleted and renamed protected files remain detectable.
- [x] Internal errors fail closed.
- [ ] Trusted base-branch Gate Integrity check passed.
- [ ] Owner approved after latest push.

## Tests

- Positive fixtures:
  - legitimate product change outside protected paths;
  - owner-reviewed governance-only change.
- Malicious fixtures:
  - workflow edit;
  - pattern-line edit;
  - checker edit;
  - actor or branch exception;
  - narrowed trigger;
  - `continue-on-error`;
  - report-only downgrade;
  - success replacement;
  - swallowed exception;
  - deleted or renamed checker;
  - ruleset required-check removal;
  - mixed governance and product files;
  - branch-range logic edit;
  - protected path touched then reverted in branch history;
  - stale owner approval;
  - malformed changed-file path.
- False-positive fixtures:
  - ordinary `README.md` product change.
- Full unchanged-check results:
  - recorded in `local-verification.md`.

## Owner decision

- Status: PENDING_OWNER_APPROVAL
- Approval reference:
- Approved protected-base SHA:
