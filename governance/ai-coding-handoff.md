# AI Coding Handoff

## Purpose

This document tells a coding agent how to use the repository when implementing, auditing, or extending the ASH Pattern System in a downstream target.

The ASH Pattern System is a resilient software semantics framework defined by the canonical math in this repository. The canonical state space is `F2^9` with 512 vertices, a fixed 16-member codeword set `C ⊂ F2^9`, XOR-by-codeword transformations, an averaging operator with `T² = T`, and first-class branching semantics.

## Handoff rule

Treat this repository as the semantic authority.
Do not infer core semantics from convenience, local idiom, or language defaults.
When a mathematical question is ambiguous, resolve it against the canonical specifications in this repository before proceeding.

## Required coding-agent workflow

1. Read `README.md`.
2. Read all files in `docs/`.
3. Read all files in `specs/core/`, paying particular attention to:
   - `ash-state-space.pseudo.md`
   - `codeword-set.pseudo.md`
   - `state-admissibility.pseudo.md`
   - `state-validity-diagnostics.pseudo.md`
   - `system-state-classification.pseudo.md`
   - `recoverability-semantics.pseudo.md`
   - `realm-identity.pseudo.md`
4. Read all files in `specs/algorithms/`, paying particular attention to:
   - `codeword-transformation-semantics.pseudo.md`
   - `averaging-operator-semantics.pseudo.md`
   - `branching-semantics.pseudo.md`
   - `recovery-fallback-semantics.pseudo.md`
   - `containment-safe-failure-semantics.pseudo.md`
5. Read `specs/interfaces/semantic-contracts.md`, all files in `specs/interfaces/contracts/`, and all files in `specs/verification/`.
6. Read `governance/repository-governance.md` and `governance/github-agents-governance.md`.
7. Read `handoff-templates/` when the task is a downstream implementation handoff or audit.
8. When a math detail needs grounding, use the canonical definitions and enumerations in `specs/core/codeword-set.pseudo.md` and the related core specs.
9. Only then begin target-specific design and implementation planning.

## What the coding agent must preserve

The coding agent must preserve:

- the ASH state space as full `F2^9`
- the fixed 16-member canonical codeword set `C ⊂ F2^9`
- XOR-by-codeword as the canonical state transformation mechanism
- the averaging operator semantics with `T² = T`
- first-class branching semantics
- deterministic normalization on full 9-bit states
- deterministic realm identity from full 9-bit states
- deterministic transition behavior via codeword transformations
- deterministic topology expansion
- explicit separation between generation planning and materialization
- system-state classification based on full-state diagnostics
- deterministic recoverability mapping
- deterministic recovery and fallback behavior using codeword-based correction
- containment and safe-failure behavior
- diagnosable recovery with no silent healing

## What the coding agent must not do

The coding agent must not:

- invent or extend codewords beyond the canonical 16-member set
- replace the full-state `F2^9` model with any alternate foundational decomposition
- make one platform's file structure into the system's identity
- replace semantic planning with direct side effects
- treat convenience behavior as canonical if the specs do not say so
- guess foundational math that lacks explicit canonical definition
- silently heal or mutate state without producing a diagnostic record
- skip containment when the recovery/fallback specifications require it
- allow a `FAILED` state to continue normal operations without escalation
- allow transitions from `SAFE_HALT` to any other state

## Canonical baseline

The following are canonical:

- **State space** — full `F2^9`, 512 vertices, 9-bit states
- **Transformation** — XOR-by-codeword: `x' = x ⊕ c` where `c ∈ C ⊂ F2^9`
- **Averaging operator** — `T f(x) = (1/|C|) Σ f(x ⊕ c)` with `T² = T`
- **Branching** — first-class canonical capability
- **Recovery and safety** — deterministic diagnostics, fallback, containment, and safe halt on full 9-bit states

**Codeword-set closure**: The codeword set `C ⊂ F2^9` is fully closed. `C` is a [9, 4, 4] doubly-even linear code with 16 members, fully enumerated in `specs/core/codeword-set.pseudo.md`. Implementations must use exactly the specified 16-codeword set and must not invent or extend codewords.

## Downstream implementation handoff

The `handoff-templates/` directory contains downstream build handoff templates that define what each target-class implementation repository must contain.

**Coding agent workflow for downstream implementations:**

1. Read the canonical specifications, contracts, and verification requirements first.
2. Read `handoff-templates/common-downstream-handoff-requirements.md` for universal handoff expectations.
3. Read the appropriate target-class template (`desktop-`, `mobile-`, or `service-implementation-handoff-template.md`).
4. Use the template to structure the downstream repository, plan deliverables, and track conformance.

Handoff templates constrain downstream repository structure and proof-of-conformance inputs. They do not override canonical specifications, contracts, or verification requirements. The canonical agnostic repository remains the semantic authority.
