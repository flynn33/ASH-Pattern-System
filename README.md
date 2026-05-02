# ASH Pattern System

## Canonical Agnostic Repository

This repository is the platform-neutral, language-neutral specification baseline for the ASH Pattern System.

Its canonical math is grounded in the ASH Model source of truth: the full 9-bit state space `F2^9`, the fixed 16-member codeword set `C ⊂ F2^9`, XOR-by-codeword transitions, the averaging operator `T² = T`, and first-class branching semantics.

## Repository purpose

The ASH Pattern System is a platform-agnostic framework for:

- self-healing and self-correcting software
- deterministic diagnostics, recovery, fallback, containment, and safe halt
- platform-neutral transition, planning, and topology semantics
- downstream implementation conformance against a fixed canonical baseline

This repository defines:

- the canonical ASH state space as `F2^9` with 512 states
- the canonical codeword set `C ⊂ F2^9` as a fixed 16-member `[9, 4, 4]` code
- canonical XOR-by-codeword transitions, averaging, branching, topology expansion, and realm identity
- canonical admissibility, diagnostics, classification, recoverability, fallback, containment, and safe-failure semantics
- canonical contracts, diagnostic schema, taxonomy, and verification requirements
- governance, GitHub agents, wiki material, and handoff templates that reinforce the same source of truth

This repository does not define:

- a canonical programming language
- a canonical operating system or runtime
- a canonical build system or package manager
- a platform implementation or emitted artifact tree

## Repository map

- `docs/00-repository-purpose.md` — repository role and boundaries
- `docs/01-design-philosophy.md` — governing design principles
- `docs/02-target-repository-shape.md` — canonical repository structure
- `docs/03-design-roadmap.md` — current source-of-truth alignment roadmap
- `specs/core/` — state, codeword, diagnostic, classification, recovery, and identity specifications
- `specs/algorithms/` — transformation, averaging, branching, recovery, containment, topology, and planning semantics
- `specs/registries/` — canonical fallback policy registry
- `specs/interfaces/` — contracts, diagnostic schema, and rule-ID taxonomy
- `specs/verification/` — invariants, conformance categories, and acceptance requirements
- `handoff-templates/` — downstream delivery templates and conformance evidence requirements
- `wiki/` — GitHub Wiki source pages aligned to canonical repository content
- `governance/repository-governance.md` — repository rules for current canonical content
- `governance/ai-coding-handoff.md` — coding-agent instructions for downstream implementation work
- `governance/github-agents-governance.md` — GitHub agent policy and enforcement boundaries
- `.github/workflows/` — repository agent workflows
- `.github/scripts/` — repository agent scripts

## Intended use

An implementation agent should use this repository as the semantic authority for ASH Pattern System behavior and use the ASH Model grounding captured here as the math source of truth.

If an implementation disagrees with this repository, the specification here wins. If repository wording drifts from the ASH Model source grounding, the repository must be corrected to match the source of truth.

The repository remains in maintenance mode as a canonical baseline: future edits should preserve alignment with the ASH Model and improve clarity, enforcement, and downstream conformance.
