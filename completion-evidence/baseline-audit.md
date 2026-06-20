# Baseline Audit

## Scope

- Product: ASH Pattern System
- Repository: `flynn33/ASH-Pattern-System`
- Working branch: `release/aps-1.0.0-completion`
- Baseline date: 2026-06-20
- Audit package path: `/Users/jim/AI/Codex/APS/aps-product-completion-package`

## Baseline capture

| Item | Result |
|---|---|
| Audited baseline commit | `e123f5d7fdbb381179971f721a3292c31eb1cbc2` |
| Current `origin/main` after fetch | `e123f5d7fdbb381179971f721a3292c31eb1cbc2` |
| Delta from audited baseline to `origin/main` | None |
| Working branch created | `release/aps-1.0.0-completion` |
| Branch tracking source | `origin/main` |
| Tracked file count | 75 |
| Starting worktree status | Clean |

## Package instruction verification

The completion package was read from the extracted directory and verified with the package preflight tool.

| Command | Result | Notes |
|---|---|---|
| `python3 tools/package_preflight.py` | Fail | System Python is 3.9.6 and does not support `zip(..., strict=True)`. |
| `/Users/jim/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/package_preflight.py` | Pass | Bundled Python is 3.12.13; preflight validated 36 files. |

Reference asset baseline:

- Codewords: 16
- Orbits: 32
- Realms: 512
- Transformations: 8,192
- Reachable ordered pairs: 8,192
- Code dimension: 4
- Minimum nonzero weight: 4
- Minimum pairwise distance: 4
- Weight distribution: `{0: 1, 4: 14, 8: 1}`
- All codewords preserve `b8`: true

## Existing local checks

All commands were run from the repository root with `REPORT_ONLY` unset, using the bundled Python 3.12 runtime.

| Check | Command | Exit | Result |
|---|---|---:|---|
| Alignment | `python3 .github/scripts/alignment_check.py` | 0 | Pass |
| Semantic integrity | `python3 .github/scripts/semantic_integrity_check.py` | 0 | Pass |
| Math integrity | `python3 .github/scripts/math_integrity_check.py` | 0 | Pass; no math-critical files changed |
| Documentation maintenance | `python3 .github/scripts/docs_maintenance_check.py` | 0 | Pass |
| Wiki maintenance | `python3 .github/scripts/wiki_maintenance_check.py` | 0 | Pass |
| Downstream conformance | `python3 .github/scripts/downstream_conformance_check.py` | 1 | Fail; required `conformance/` deliverables are absent |

Downstream conformance missing paths:

- `conformance/module-mapping.md`
- `conformance/verification-report.md`
- `conformance/diagnostics-conformance.md`
- `conformance/materialization-boundary.md`
- `conformance/deviation-log.md`
- `conformance/acceptance-judgment.md`

## Workflow baseline findings

- Release-critical workflows currently use mutable action references such as `actions/checkout@v4` and `actions/setup-python@v5`.
- Multiple workflows set `REPORT_ONLY: "1"`.
- Downstream reusable workflow documentation references `@main`.
- Attribution/naming policy surface still uses `.github/workflows/no-ai-attribution.yml`.
- Governance handoff surface still uses `governance/ai-coding-handoff.md`.

## External repository settings

| Setting area | Baseline observation | Status |
|---|---|---|
| GitHub CLI access | `gh` is not installed in the local environment | Pending authenticated verification |
| Repository metadata API | Unauthenticated request returned `404` | Pending authenticated verification |
| Branch protection API | Unauthenticated request returned `401` | Pending authenticated verification |
| Branch/ruleset protection | Cannot be verified from local files | External configuration gate |
| Security advisory/reporting path | Cannot be verified from local files | External configuration gate |
| Release immutability setting | Cannot be verified from local files | External configuration gate |

## Baseline blockers inherited from completion package

- Active specs still conflate well-formed state membership, known-valid state language, transformation compatibility, and operational health.
- No versioned `schemas/`, `canonical-data/`, `conformance/`, or `examples/` product surfaces exist.
- No product manifest, public specification API, version, changelog, compatibility, migration, release-process, or product-status files exist.
- No root license, notice, security, support, contribution, conduct, or citation files exist.
- Existing checks are not sufficient release gates because several are report-only in workflows and scripts contain fail-open helper behavior.

## Phase 0 status

Phase 0 baseline capture has started and produced the initial evidence files in `completion-evidence/`. No semantic edits have been made yet.
