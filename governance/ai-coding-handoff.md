# AI Coding Handoff

## Purpose

This document tells a coding agent how to use this repository when building a target implementation.

The ASH Pattern System is a **resilient software semantics framework** — not just an abstract state model. It defines the semantic foundation for self-healing, self-correcting, safe-failure, fallback, and deterministic recovery behavior. Every implementation must preserve these resilience semantics.

## Handoff rule

Treat this repository as the semantic authority.
Do not infer core semantics from convenience, local idiom, or language defaults.
The corrected-core derivation rule is authoritative: expected control semantics for correctable cores are defined on the corrected admissible core.

## Required coding-agent workflow

1. read `README.md`
2. read all files in `docs/`
3. read all files in `specs/core/`, paying particular attention to:
   - `ash-state-space.pseudo.md` — the canonical state definition
   - `control-bit-derivation.pseudo.md` — the control-bit derivation spec and its closure status
   - `core-admissibility.pseudo.md` — the admissibility rules and their closure status
   - `state-validity-diagnostics.pseudo.md` — the canonical diagnostic model
   - `system-state-classification.pseudo.md` — canonical system-state classes and class-to-action mapping
   - `recoverability-semantics.pseudo.md` — recoverability categories and recovery mapping
4. read all files in `specs/algorithms/`, paying particular attention to:
   - `recovery-fallback-semantics.pseudo.md` — deterministic recovery and fallback selection
   - `containment-safe-failure-semantics.pseudo.md` — containment and safe-failure behavior
5. read `specs/interfaces/semantic-contracts.md` and all files in `specs/interfaces/contracts/`
6. read `governance/repository-governance.md`
7. confirm that the locked algebraic definitions (parity formula, 16-codeword set) match the canonical specs
8. check for any remaining unresolved items (e.g., fallback-policy registry)
9. only then begin target-specific design and implementation planning

## What the coding agent must preserve

The coding agent must preserve:

- the ASH state space as **F2^9**
- the special role of the first 8 coordinates as the stabilizing algebraic core
- the special role of the 9th coordinate as a derived control/parity dimension
- deterministic normalization
- deterministic realm identity
- deterministic transition behavior
- deterministic topology expansion
- full axiom diagnostics
- explicit separation between generation planning and materialization
- system-state classification (all 7 canonical classes)
- deterministic recoverability mapping (class-to-recovery-category)
- deterministic recovery and fallback behavior
- containment and safe-failure behavior
- the corrected-core derivation rule (expected control from corrected admissible core for correctable states)
- diagnosable recovery — no silent healing

## What the coding agent must not do

The coding agent must not:

- reinterpret the 9th coordinate as a normal peer bit for ordinary transitions
- silently collapse the core/control distinction
- make one platform's file structure into the engine's identity
- replace semantic planning with direct side effects
- treat convenience behavior as canonical if the specs do not say so
- substitute a different control-bit derivation formula for the locked parity formula
- substitute a different admissibility codeword set for the locked normative 16-codeword set
- treat the locked algebraic definitions as configurable, optional, or open to local variation
- guess any foundational semantic that is explicitly marked as unresolved in this repository (e.g., the fallback-policy registry)
- silently heal or mutate state without producing a diagnostic record
- skip containment when the recovery/fallback specifications require it
- allow a `FAILED` state to continue normal operations without escalation
- allow transitions from `SAFE_HALT` to any other state

## Locked design decisions

The following foundational algebraic items are **locked** (Design Package C) and must be implemented exactly:

- **Control-bit derivation formula** — overall parity: `b0 ⊕ b1 ⊕ b2 ⊕ b3 ⊕ b4 ⊕ b5 ⊕ b6 ⊕ b7` (see `specs/core/control-bit-derivation.pseudo.md`)
- **Admissibility law** — the exact [8,4,4] extended Hamming code with normative 16-codeword set and generator matrix G (see `specs/core/core-admissibility.pseudo.md`)
- **Corrected-core derivation rule** — for correctable cores, expected control is derived from the corrected admissible core, not the raw core

These are not open choices. The coding agent must not substitute alternatives.

The following structural items are **locked** (Design Package D) and must be implemented exactly:

- **Fallback-policy registry** — the canonical registry for deterministic fallback selection (see `specs/registries/fallback-policy-registry.md`). Implementations must implement fallback selection against this registry. Local invention of fallback policy is prohibited.
- **Diagnostic schema** — the shared diagnostic envelope for all diagnostic contexts (see `specs/interfaces/diagnostic-schema.md`). All diagnostics must conform to this schema. Local invention of diagnostic structures is prohibited.
- **Rule-ID taxonomy** — the canonical rule identifier structure and governance (see `specs/interfaces/rule-id-taxonomy.md`). All rule IDs in diagnostics must conform to this taxonomy.

The following implementation contracts are **locked** (Phase 2) and are canonical for module-level behavior:

- **Detailed contract files** — 9 contract files in `specs/interfaces/contracts/` define the exact implementation behavior for each required semantic module. These are authoritative for module-level implementation decisions.
- **Materialization boundary** — `GenerationPlanner` plans (no artifacts, no side effects); `ArtifactEmitter` materializes (no inventing semantics). Neither may cross the other's boundary.
- **Umbrella contract** — `specs/interfaces/semantic-contracts.md` is the umbrella contract document referencing the detailed contracts.

The coding agent must not invent module behavior outside the canonical contract files.

## Design package status

- **Design Package A** — complete (state-layer formal foundation)
- **Design Package B** — formally closed (resilient software semantics layer)
- **Design Package C** — complete (algebraic lock package)
- **Design Package D** — complete (registry and diagnostics layer closure)
- **Phase 2** — complete (implementation-contract lock)

## Required delivery shape for implementation repos

A downstream implementation handoff should include, at minimum:

- mapping from spec modules to implementation modules
- invariant-based test plan
- materialization boundary design
- diagnostics design
- target-runtime constraints
- packaging and build decisions for that target repo
