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

## Remaining findings

- Final public release approval remains owner-controlled.
- Server-side ruleset state is recorded by owner direction in `completion-evidence/owner-server-side-override.md`; local product work did not modify protected enforcement surfaces.
