# ASH Pattern System

## Canonical Agnostic Repository

This repository is the **platform-neutral, language-neutral source of truth** for the ASH Pattern System.

It is the agnostic specification repository grounded in the **full 9-dimensional ASH research math**.

> **Post-R3 status**: This repository is grounded in the full 9D ASH research baseline (R1). State/recovery semantics (R2) and contract/verification layers (R3) have been rebuilt on the 9D foundation. The codeword set `C ⊂ F2^9` is fully closed — exact generators and exhaustive enumeration have been extracted from published research (see `specs/core/codeword-set.pseudo.md`). The canonical semantic, contract, verification, and downstream build handoff template layers are complete. The canonical main repository is now closed as the agnostic specification baseline and operates in maintenance mode: platform-specific implementation work is out of scope for main, and future edits are limited to canonical corrections, ambiguity resolution, and governance or source-of-truth maintenance.

## Repository purpose

The ASH Pattern System is a **platform-agnostic and code-agnostic framework** for:

- **self-healing software** — systems that detect and correct their own state errors
- **self-correcting software** — systems that restore valid state from corrupted state
- **safe-failure behavior** — systems that halt safely when correction is impossible
- **fallback behavior** — systems that select known-good states when correction is ambiguous
- **deterministic recovery planning** — systems that plan recovery actions from structured diagnostics
- **resilient system design** — systems that degrade gracefully through containment rather than fail silently

This repository defines:

- the canonical ASH state space as **F2^9** — full 9-dimensional binary state space with 512 vertices
- canonical state transformations via **XOR-by-codeword** (`x' = x ⊕ c` for `c ∈ C ⊂ F2^9`)
- canonical **averaging operator** `T` with `T² = T` (projection onto C-invariant functions)
- canonical **branching / leaf expansion** as a first-class capability
- deterministic transition semantics on full 9-bit states
- deterministic topology expansion semantics
- axiom evaluation semantics
- generation-planning semantics
- realm identity encoding from full 9-bit states
- resilient software semantics (classification, recovery, fallback, containment, safe failure) — rebuilt on 9D baseline
- implementation contracts for all 9 required semantic modules — rebuilt on 9D baseline in R3
- invariant-based verification requirements for downstream conformance — rebuilt on 9D baseline in R3
- downstream build handoff templates for desktop, mobile, and service target classes

This repository does **not** define:

- a canonical programming language
- a canonical operating system or platform
- a canonical build system
- a canonical CLI
- a canonical UI or rendering layer
- a canonical filesystem layout for emitted projects

## Design stance

The engine core must remain stable even when downstream implementations differ.

That means:

- the **specifications are canonical**
- implementations are adapters to the specifications
- semantics come before syntax
- planning comes before materialization
- the state model comes before platform behavior

## Core state-space model (Research Baseline)

The ASH state space is **F2^9** — the full 9-dimensional binary state space with **512 states** (vertices / realms).

Each state is a 9-bit binary vector `(b0, b1, b2, b3, b4, b5, b6, b7, b8)`. All 9 coordinates participate in the algebraic structure. No coordinate is structurally privileged as a "derived" dimension at the foundational level.

Canonical motion between states is **XOR-by-codeword**: `x' = x ⊕ c` where `c ∈ C ⊂ F2^9`.

## Repository map

- `docs/00-repository-purpose.md` — what this repository is for
- `docs/01-design-philosophy.md` — governing design principles
- `docs/02-target-repository-shape.md` — canonical repository structure
- `docs/03-design-roadmap.md` — planning sequence for future work
- `specs/core/ash-state-space.pseudo.md` — canonical ASH state definition
- `specs/core/control-bit-derivation.pseudo.md` — control-bit derivation semantics and closure status
- `specs/core/core-admissibility.pseudo.md` — core admissibility rules and state classification
- `specs/core/codeword-set.pseudo.md` — canonical codeword set definition (research baseline)
- `specs/core/state-admissibility.pseudo.md` — full 9-bit state admissibility and validity
- `specs/core/state-validity-diagnostics.pseudo.md` — canonical state-validity diagnostic model (9D)
- `specs/core/system-state-classification.pseudo.md` — canonical system-state classes and class-to-action mapping (9D)
- `specs/core/recoverability-semantics.pseudo.md` — recoverability categories and deterministic recovery mapping (9D)
- `specs/core/realm-identity.pseudo.md` — realm identity and encoding semantics
- `specs/algorithms/codeword-transformation-semantics.pseudo.md` — canonical XOR-by-codeword state transformation
- `specs/algorithms/averaging-operator-semantics.pseudo.md` — canonical averaging operator (T² = T)
- `specs/algorithms/branching-semantics.pseudo.md` — canonical branching / leaf expansion
- `specs/algorithms/recovery-fallback-semantics.pseudo.md` — deterministic recovery and fallback selection (9D)
- `specs/algorithms/containment-safe-failure-semantics.pseudo.md` — containment and safe-failure behavior (9D)
- `specs/algorithms/transition-system.pseudo.md` — transition semantics (realigned to XOR-by-codeword)
- `specs/algorithms/topology-expansion.pseudo.md` — topology generation semantics
- `specs/algorithms/axiom-evaluation.pseudo.md` — axiom evaluation semantics
- `specs/algorithms/generation-planning.pseudo.md` — abstract generation planning flow
- `specs/registries/fallback-policy-registry.md` — canonical fallback-policy registry for deterministic fallback selection
- `specs/interfaces/semantic-contracts.md` — umbrella contract document referencing detailed module contracts
- `specs/interfaces/diagnostic-schema.md` — shared diagnostic envelope for all diagnostic contexts
- `specs/interfaces/rule-id-taxonomy.md` — canonical rule-ID structure and governance
- `specs/interfaces/contracts/state-model-contract.md` — StateModel implementation contract
- `specs/interfaces/contracts/recovery-engine-contract.md` — RecoveryEngine implementation contract
- `specs/interfaces/contracts/realm-encoder-contract.md` — RealmEncoder implementation contract
- `specs/interfaces/contracts/transition-registry-contract.md` — TransitionRegistry implementation contract
- `specs/interfaces/contracts/topology-generator-contract.md` — TopologyGenerator implementation contract
- `specs/interfaces/contracts/axiom-evaluator-contract.md` — AxiomEvaluator implementation contract
- `specs/interfaces/contracts/generation-planner-contract.md` — GenerationPlanner implementation contract
- `specs/interfaces/contracts/artifact-emitter-contract.md` — ArtifactEmitter implementation contract
- `specs/interfaces/contracts/diagnostics-module-contract.md` — Diagnostics module implementation contract
- `specs/verification/invariant-spec.md` — canonical invariant set for downstream conformance verification
- `specs/verification/conformance-categories.md` — 5 conformance categories for verification grouping
- `specs/verification/implementation-acceptance.md` — acceptance criteria and judgment language
- `handoff-templates/README.md` — downstream build handoff template layer overview
- `handoff-templates/common-downstream-handoff-requirements.md` — universal downstream handoff requirements
- `handoff-templates/desktop-implementation-handoff-template.md` — desktop target class template
- `handoff-templates/mobile-implementation-handoff-template.md` — mobile target class template
- `handoff-templates/service-implementation-handoff-template.md` — service/backend target class template
- `wiki/Home.md` — GitHub Wiki home source (version-controlled in `wiki/`)
- `wiki/Wiki-Maintenance-Playbook.md` — wiki upkeep and refresh policy
- `governance/repository-governance.md` — governance rules for this repository
- `governance/ai-coding-handoff.md` — handoff instructions for coding agents
- `governance/github-agents-governance.md` — GitHub-native sentinel agent layer (alignment, semantic integrity, math integrity, downstream conformance, no-AI-attribution, wiki maintenance, docs maintenance)
- `.github/workflows/no-ai-attribution.yml` — CI gate that blocks AI attribution markers
- `.github/workflows/wiki-maintenance-agent.yml` — CI gate that validates wiki completeness, links, and drift
- `.github/workflows/docs-maintenance-agent.yml` — CI gate that validates README/docs/governance integrity

## Intended use

A future coding agent should receive this repository plus a build-target instruction such as:

- implement the ASH Pattern System for Rust
- implement the ASH Pattern System for Swift
- implement the ASH Pattern System for C++
- implement the ASH Pattern System for TypeScript
- implement the ASH Pattern System for a service runtime
- implement the ASH Pattern System for a mobile runtime

The build target may change.
The semantic source of truth must not.
