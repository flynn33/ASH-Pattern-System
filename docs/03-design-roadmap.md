# Design Roadmap

## Goal

Move from a corrected semantic baseline to implementation-ready handoff materials without collapsing the design into any single language or platform.

## Sequence

### Phase 1 — lock the semantic foundation

Complete and stabilize:

- ASH state-space specification
- realm identity specification
- transition semantics
- topology expansion semantics
- axiom evaluation semantics
- generation-planning semantics

### Phase 1.5 — close the formal layers

Complete the formal layers that sit between the semantic kernel and implementation contracts:

- **control-bit derivation** — define the semantic role, interface, invariants, and diagnostic behavior of the derived control dimension; lock the exact derivation formula (currently an unresolved closure item)
- **core admissibility** — define which 8-bit core vectors are structurally admissible under the [8,4,4] extended Hamming code; lock the exact codeword set / generator matrix (currently an unresolved closure item)
- **state-validity diagnostics** — define a canonical diagnostic record that every implementation must produce for any candidate state

Specifications created for this phase:

- `specs/core/control-bit-derivation.pseudo.md`
- `specs/core/core-admissibility.pseudo.md`
- `specs/core/state-validity-diagnostics.pseudo.md`

**Status**: Specification structure complete. Two unresolved closure items remain:

1. the exact derivation formula for `derive_control_bit`
2. the exact codeword set for core admissibility

These must be resolved before Phase 2 can be considered implementation-ready.

### Phase 1.75 — define resilient software semantics (Design Package B)

Build the system-behavior layer on top of the state-validity foundation:

- **system-state classification** — define the 7 canonical state classes (STABLE, UNSTABLE, CORRECTABLE, DEGRADED, CONTAINED, FAILED, SAFE_HALT) and the deterministic class-to-action mapping
- **recoverability semantics** — define the recovery category for each state class and blocked-recovery conditions
- **recovery/fallback semantics** — define the algorithmic flow for deterministic correction, fallback selection, and escalation
- **containment/safe-failure semantics** — define when containment overrides correction, when safe failure is mandatory, and what SAFE_HALT means as a terminal state
- **corrected-core derivation rule** — harmonize all state-layer specs so expected-control semantics for correctable cores are defined on the corrected admissible core

Specifications created for this phase:

- `specs/core/system-state-classification.pseudo.md`
- `specs/core/recoverability-semantics.pseudo.md`
- `specs/algorithms/recovery-fallback-semantics.pseudo.md`
- `specs/algorithms/containment-safe-failure-semantics.pseudo.md`

**Status**: Specification structure complete. Unresolved closure items from Phase 1.5 remain:

1. the exact derivation formula for `derive_control_bit`
2. the exact codeword set for core admissibility

Additionally, a new future specification is needed:

3. the fallback-policy registry (`specs/registries/fallback-policy-registry.md`)

### Phase 2 — lock the implementation contracts

Define the exact capabilities that any implementation must expose, including:

- state normalization
- control derivation
- transition application
- topology generation
- axiom diagnostics
- generation planning
- artifact materialization boundary

### Phase 3 — define invariant-based verification requirements

Describe what downstream test suites must prove, including:

- deterministic normalization
- deterministic realm encoding
- no uncontrolled mutation of the control dimension
- deterministic transition outcomes
- deterministic topology expansion
- stable axiom diagnostics
- stable generation-plan structure

### Phase 4 — create platform build handoff packages

For each target implementation repo, the coding agent should receive:

- this repository
- target platform constraints
- target language constraints
- runtime constraints
- packaging constraints
- performance constraints if applicable

## Immediate next design step

The current design milestone is to **close remaining Phase 1.5 algebraic items and define the fallback-policy registry**:

1. **Lock the control-bit derivation formula** — select and record the exact algebraic function `F2^8 -> F2` in `specs/core/control-bit-derivation.pseudo.md`
2. **Lock the core admissibility law** — select and record the exact generator matrix and codeword enumeration for the [8,4,4] extended Hamming code in `specs/core/core-admissibility.pseudo.md`
3. **Define the fallback-policy registry** — create `specs/registries/fallback-policy-registry.md` specifying how fallback candidates are registered, ordered, and selected
4. **Verify end-to-end diagnostic completeness** — confirm that the full chain from state validity through classification, recovery, fallback, containment, and safe halt produces complete, auditable diagnostics

Once these items are resolved, the repository can proceed to Phase 2 (locking implementation contracts) with confidence that downstream repositories have a complete semantic foundation for resilient software.
