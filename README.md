# ASH Pattern System

## Canonical Agnostic Repository

This repository is the platform-neutral, language-neutral specification baseline for the ASH Pattern System.

Its canonical math is self-contained in this repository: the full 9-bit state space `F2^9`, the fixed 16-member codeword set `C ⊂ F2^9`, XOR-by-codeword transitions, the averaging operator `T² = T`, and first-class branching semantics.

## Repository purpose

The ASH Pattern System is a platform-agnostic framework for:

- self-healing and self-correcting software
- deterministic diagnostics, recovery, fallback, containment, and safe halt
- platform-neutral transition, planning, and topology semantics
- downstream implementation conformance against a fixed canonical baseline

This repository defines:

- the canonical ASH state space as `F2^9` with 512 states
- the canonical codeword set `C ⊂ F2^9` as a fixed 16-member `[9, 4, 4]` doubly-even code with 32 orbits
- canonical XOR-by-codeword transitions, averaging, branching, topology expansion, and realm identity
- canonical admissibility, diagnostics, classification, recoverability, fallback, containment, and safe-failure semantics
- canonical contracts, diagnostic schema, taxonomy, and verification requirements
- versioned schemas, canonical data, examples, and conformance corpus artifacts for downstream validation
- governance, GitHub agents, wiki material, and handoff templates that reinforce the same canonical baseline

This repository does not define:

- a canonical programming language
- a canonical operating system or runtime
- a canonical build system or package manager
- a platform implementation or emitted artifact tree

## Repository map

- `VERSION` — current product version
- `product-manifest.json` — machine-readable product manifest
- `CHANGELOG.md` — release history for the canonical specification baseline
- `PRODUCT-STATUS.md` — current objective release-candidate status
- `PUBLIC-SPECIFICATION-API.md` — public APS compatibility surface
- `schemas/` — versioned JSON Schema entry points
- `canonical-data/` — versioned codewords, realms, orbits, transitions, policies, rule registry, and artifact index
- `conformance/` — versioned implementation-neutral conformance corpus
- `examples/` — valid and invalid schema examples
- `docs/00-repository-purpose.md` — repository role and boundaries
- `docs/01-design-philosophy.md` — governing design principles
- `docs/02-target-repository-shape.md` — canonical repository structure
- `docs/03-design-roadmap.md` — current canonical alignment roadmap
- `specs/core/` — state, codeword, diagnostic, classification, recovery, and identity specifications
- `specs/algorithms/` — transformation, averaging, branching, recovery, containment, topology, and planning semantics
- `specs/registries/` — canonical fallback policy registry
- `specs/interfaces/` — contracts, diagnostic schema, and rule-ID taxonomy
- `specs/verification/` — invariants, conformance categories, and acceptance requirements
- `handoff-templates/` — downstream delivery templates and conformance evidence requirements
- `tools/product/` — standard-library product generation, validation, conformance, and archive tooling
- `wiki/` — GitHub Wiki source pages aligned to canonical repository content
- `governance/` — repository rules, protected handoff/governance policy, and math-change notes
- `.github/workflows/` — repository agent workflows
- `.github/scripts/` — repository agent scripts
- `completion-evidence/` — temporary completion evidence, protected-surface baseline, and verification reports

## Intended use

An implementation agent should use this repository as the semantic authority for ASH Pattern System behavior.

If an implementation disagrees with this repository, the specification here wins. If repository wording drifts internally, the repository must be corrected to match its canonical baseline.

The repository remains in maintenance mode as a canonical baseline: future edits should preserve internal mathematical consistency and improve clarity, enforcement, and downstream conformance.
