# Audit Iterations

## Iteration 1

- Timestamp: `2026-06-21T14:23:49Z`
- Base commit: `aa917162c915bb5904de3ddec6dbb0a9297300ac`
- Branch: `release/aps-1.0.0-completion-clean`
- Scope: product tooling red/green cycle and initial generation.

### Commands

- `python3 -m unittest discover -s tools/product/tests -v`
- `python3 tools/product/verify_canonical_data.py`
- `python3 tools/product/verify_conformance_corpus.py`

### Failures

- Product wrapper scripts could not import `tools.product.cli` when executed directly.
- Conformance layout did not include all package-required vector files.

### Root causes

- Direct script execution used `tools/product` as `sys.path[0]`.
- Initial corpus generator covered algebraic vectors before non-algebraic safety, diagnostic, axiom, generation, and materialization scenarios.

### Remediation

- Added explicit repository-root path setup in each product wrapper.
- Expanded `build_conformance_corpus` to emit all required vector files and invalid corpus metadata.
- Added regression tests for wrapper self-tests and package-required corpus layout.

### Retest

- `python3 -m unittest discover -s tools/product/tests -v` — PASS.

## Iteration 2

- Timestamp: `2026-06-21T14:23:49Z`
- Scope: semantic closure and documentation/wiki alignment.

### Commands

- `rg -n "TODO|TBD|FIXME|PLACEHOLDER|UNRESOLVED|pending research|future specification|not yet defined|implementation-defined|known valid state|recognized valid state|outside all known codeword orbits|guess|approximately|as needed|etc\\." README.md docs specs handoff-templates wiki --glob '*.md'`
- `python3 .github/scripts/docs_maintenance_check.py`
- `python3 .github/scripts/wiki_maintenance_check.py`
- `python3 .github/scripts/semantic_integrity_check.py`
- `python3 .github/scripts/math_integrity_check.py`
- `python3 <package>/tools/verify_protected_surface.py --policy <package>/controls/protected-surface-policy.json --base-ref origin/main --mode product --verify-baseline completion-evidence/protected-surface-baseline.json`

### Failures

- Baseline semantic scan found old known-reference-state and outside-orbit language.
- Branch was initially still named `docs/canonical-surface-refresh`.

### Root causes

- Previous repository text conflated structural realm membership with context-bound operational health.
- The dirty worktree was on a same-commit local branch instead of the required release branch.

### Remediation

- Switched worktree to `release/aps-1.0.0-completion-clean`.
- Rewrote state admissibility, diagnostics, classification, recoverability, recovery/fallback, and branching semantics.
- Added `governance/math-change-notes/2026-06-21-product-semantic-closure.md`.
- Updated docs, handoff wording, and wiki summaries.

### Retest

- Unresolved-language scan — PASS with no hits.
- Docs maintenance — PASS.
- Wiki maintenance — PASS.
- Semantic integrity — PASS.
- Protected surface verification — PASS.

## Iteration 3

- Timestamp: `2026-06-21T14:23:49Z`
- Scope: release archive and reproducibility.

### Commands

- `python3 tools/product/build_release_archive.py --verify`
- `python3 tools/product/verify_release_archive.py --archive release/ash-pattern-system-1.0.0-rc.1.zip`
- `python3 -m unittest discover -s tools/product/tests -v`

### Failures

- Rebuilding the corpus over an existing corpus included the previous `SHA256SUMS` in the manifest.
- Initial release manifest contained only archive path and hash.

### Root causes

- The corpus builder did not clear the versioned corpus directory before regeneration.
- Release tooling lacked a file-inventory manifest helper.

### Remediation

- Added a repeated-generation regression test.
- Made conformance generation clear `conformance/1.0/` before writing.
- Excluded top-level `manifest.json` and `SHA256SUMS` from their own corpus manifest.
- Added `release_manifest()` and CLI output for archive metadata plus per-file SHA-256 inventory.

### Retest

- `python3 -m unittest discover -s tools/product/tests -v` — PASS.
- `python3 tools/product/verify_canonical_data.py` — PASS.
- `python3 tools/product/verify_conformance_corpus.py` — PASS.
- `python3 tools/product/build_release_archive.py --verify` — PASS.
- `python3 tools/product/verify_release_archive.py --archive release/ash-pattern-system-1.0.0-rc.1.zip` — PASS.

## Iteration 4

- Timestamp: `2026-06-21T16:22:59Z`
- Base commit: `74df3d068d8cb977c3b589ffb39765a432a6d47a`
- Branch: `fix/release-evidence-main-alignment`
- Scope: post-merge release evidence alignment.

### Commands

- `python3 .github/scripts/downstream_conformance_check.py`
- `python3 tools/product/build_release_archive.py --source-commit 639e0cfe8b1c276e03cd3351e04311fc845936d1 --verify`
- `python3 tools/product/release_readiness.py --strict --offline --source-commit 639e0cfe8b1c276e03cd3351e04311fc845936d1`
- `python3 tools/product/verify_release_archive.py --archive release/ash-pattern-system-1.0.0-rc.1.zip`
- `python3 <package>/tools/verify_protected_surface.py --policy <package>/controls/protected-surface-policy.json --base-ref origin/main --mode product --verify-baseline completion-evidence/protected-surface-baseline.json`

### Failures

- The committed release archive inventory was stale relative to the current merged product tooling files from PR #11.
- Protected-surface baseline verification failed because `completion-evidence/protected-surface-baseline.json` still recorded the earlier base commit `aa917162c915bb5904de3ddec6dbb0a9297300ac`.
- `python3 .github/scripts/downstream_conformance_check.py` failed because the top-level downstream conformance evidence files were not present under `conformance/`.

### Root causes

- PR #11 updated release-validation tooling and the root product manifest without rebuilding the release archive and release manifest against the merged `main` baseline.
- The protected-surface hashes themselves still matched, but the baseline evidence commit field had not been recaptured after the merge sequence.
- The executable conformance corpus existed under `conformance/1.0/`, but the reusable downstream conformance contract also requires six top-level Markdown evidence documents.

### Remediation

- Added the six required top-level conformance evidence documents and updated `canonical-data/1.0/normative-artifact-index.json`.
- Committed that product-content update as `639e0cfe8b1c276e03cd3351e04311fc845936d1`.
- Updated `product-manifest.json` and `release/release-manifest.json` to use release source commit `639e0cfe8b1c276e03cd3351e04311fc845936d1`.
- Rebuilt `release/ash-pattern-system-1.0.0-rc.1.zip` and `release/SHA256SUMS`.
- Recaptured `completion-evidence/protected-surface-baseline.json` from current `origin/main`.
- Refreshed release-readiness, reproducibility, security, and final-acceptance evidence.

### Retest

- Release archive build — PASS.
- Release readiness — PASS.
- Release archive verification — PASS.
- Downstream conformance artifact check — PASS.
- Protected surface verification — PASS.

## Remaining findings

- Final public release approval remains owner-controlled.
- Server-side ruleset state is recorded by owner direction in `completion-evidence/owner-server-side-override.md`; local product work did not modify protected enforcement surfaces.
