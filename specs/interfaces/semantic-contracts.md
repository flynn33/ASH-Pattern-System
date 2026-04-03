# Semantic Contracts for Future Implementations

## Required semantic modules

Every downstream implementation must provide semantic equivalents of the following modules:

1. `StateModel`
2. `RealmEncoder`
3. `TransitionRegistry`
4. `TopologyGenerator`
5. `AxiomEvaluator`
6. `GenerationPlanner`
7. `ArtifactEmitter`
8. `Diagnostics`
9. `RecoveryEngine`

## Required behaviors

### `StateModel`
Must:

- normalize states deterministically where normalization is defined
- distinguish the 8-bit core from the derived control dimension
- derive the control bit deterministically using the function defined in `control-bit-derivation.pseudo.md`
- classify core admissibility using the rules defined in `core-admissibility.pseudo.md`
- validate state consistency and produce a `StateValidityDiagnostic` as defined in `state-validity-diagnostics.pseudo.md`
- report diagnosable failure when normalization cannot proceed (e.g., inadmissible core beyond correctable distance, or malformed input)
- implement the exact locked parity formula for control-bit derivation: `b0 ⊕ b1 ⊕ b2 ⊕ b3 ⊕ b4 ⊕ b5 ⊕ b6 ⊕ b7`
- implement the exact locked normative 16-codeword admissibility law from `core-admissibility.pseudo.md`
- never substitute a different derivation formula or codeword set
- classify system state using the classes defined in `system-state-classification.pseudo.md`
- classify recoverability using the categories defined in `recoverability-semantics.pseudo.md`
- apply the corrected-core derivation rule: for correctable cores, expected control is derived from the corrected admissible core, not the raw inadmissible core

### `RecoveryEngine`
Must:

- implement deterministic recovery as defined in `recovery-fallback-semantics.pseudo.md`
- implement deterministic fallback selection against the canonical fallback-policy registry
- implement containment as defined in `containment-safe-failure-semantics.pseudo.md`
- implement safe halt as defined in `containment-safe-failure-semantics.pseudo.md`
- produce a `RecoveryDiagnostic` for every recovery, fallback, containment, and safe-halt action
- never silently heal — all recovery must produce diagnosable records
- escalate monotonically when recovery fails (fallback failure -> containment, containment breach -> safe halt)
- respect the deterministic class-to-action mapping from `system-state-classification.pseudo.md`
- produce minimum diagnostic content for every action as specified in `recovery-fallback-semantics.pseudo.md` and `containment-safe-failure-semantics.pseudo.md`

### `RealmEncoder`
Must:

- encode realm identity from normalized state
- produce deterministic results
- represent control semantics explicitly

### `TransitionRegistry`
Must:

- resolve transitions deterministically
- apply transitions to normalized states
- preserve the rule that ordinary transitions operate on the core and then re-derive control

### `TopologyGenerator`
Must:

- generate deterministic ternary topology
- preserve stable ordering and lineage

### `AxiomEvaluator`
Must:

- return the full diagnostic record
- explain failure states in diagnostic notes

### `GenerationPlanner`
Must:

- produce an abstract generation plan before any side effects occur
- include topology, role assignment, axiom diagnostics, and artifact descriptions

### `ArtifactEmitter`
Must:

- materialize a generation plan for a target platform
- preserve the meaning of the plan rather than invent new semantics

### `Diagnostics`
Must:

- expose explainable validation information for states, transitions, topology, and axioms

## Prohibited shortcuts

A downstream implementation must not:

- treat the 9th coordinate as an ordinary unrestricted peer bit during ordinary transitions
- treat syntax as the source of truth over semantics
- skip normalization before encoding or transition application
- collapse planning and materialization into one opaque semantic step
- replace semantic validation with superficial metadata checks
- silently accept an inadmissible core as valid
- produce a control bit by any means other than the canonical derivation function
- skip admissibility classification before normalization

## Mandatory algebraic conformance

The control-bit derivation formula and the core admissibility law are **locked design decisions** (Design Package C). They are not open choices.

A downstream implementation **must**:

- implement the exact locked parity formula: `b0 ⊕ b1 ⊕ b2 ⊕ b3 ⊕ b4 ⊕ b5 ⊕ b6 ⊕ b7`
- implement the exact locked normative 16-codeword set from `core-admissibility.pseudo.md`
- preserve the corrected-core derivation rule: for correctable cores, derive expected control from the corrected admissible core
- not substitute a different derivation formula, codeword set, or generator matrix
- not treat the formula or codeword set as configurable, optional, or open to local variation
- use an equivalent implementation (e.g., popcount mod 2, reduction XOR) only if it produces identical results for all inputs in F2^8

A downstream implementation **must not**:

- invent or substitute an alternative derivation formula
- invent or substitute an alternative codeword set
- treat these locked decisions as suggestions or defaults that may be overridden

## Portability rule

Implementations may differ in syntax, packaging, runtime model, memory layout, and tooling.
They may not differ in the semantic behavior defined by this repository.
