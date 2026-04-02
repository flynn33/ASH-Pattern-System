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

## Required behaviors

### `StateModel`
Must:

- normalize states
- distinguish the 8-bit core from the derived control dimension
- derive the control bit deterministically
- validate state consistency

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

## Portability rule

Implementations may differ in syntax, packaging, runtime model, memory layout, and tooling.
They may not differ in the semantic behavior defined by this repository.
