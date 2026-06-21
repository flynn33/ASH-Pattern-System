# Canonical Module Mapping

## Purpose

This file maps the canonical APS specification-product surfaces to the nine required semantic modules. Platform repositories must provide their own implementation-specific mapping before claiming downstream conformance.

## Canonical mapping

| Canonical module | Normative source | Release evidence |
|---|---|---|
| `StateModel` | `specs/core/ash-state-space.pseudo.md`, `specs/core/state-admissibility.pseudo.md`, `specs/interfaces/contracts/state-model-contract.md` | `conformance/1.0/vectors/states.jsonl`, `state-assessments.jsonl` |
| `RecoveryEngine` | `specs/core/recoverability-semantics.pseudo.md`, `specs/algorithms/recovery-fallback-semantics.pseudo.md`, `specs/interfaces/contracts/recovery-engine-contract.md` | `conformance/1.0/vectors/recovery.jsonl`, `fallback.jsonl`, `containment.jsonl`, `safe-halt.jsonl` |
| `RealmEncoder` | `specs/core/realm-identity.pseudo.md`, `specs/interfaces/contracts/realm-encoder-contract.md` | `conformance/1.0/vectors/realm-identities.jsonl` |
| `TransitionRegistry` | `specs/algorithms/transition-system.pseudo.md`, `specs/algorithms/codeword-transformation-semantics.pseudo.md`, `specs/interfaces/contracts/transition-registry-contract.md` | `conformance/1.0/vectors/transformations.jsonl`, `reachability.jsonl` |
| `TopologyGenerator` | `specs/algorithms/topology-expansion.pseudo.md`, `specs/interfaces/contracts/topology-generator-contract.md` | `conformance/1.0/vectors/topology.jsonl` |
| `AxiomEvaluator` | `specs/algorithms/axiom-evaluation.pseudo.md`, `specs/interfaces/contracts/axiom-evaluator-contract.md` | `conformance/1.0/vectors/axioms.jsonl` |
| `GenerationPlanner` | `specs/algorithms/generation-planning.pseudo.md`, `specs/interfaces/contracts/generation-planner-contract.md` | `conformance/1.0/vectors/generation-plans.jsonl` |
| `ArtifactEmitter` | `specs/interfaces/contracts/artifact-emitter-contract.md` | `conformance/1.0/vectors/materialization-boundary.jsonl` |
| `Diagnostics` | `specs/interfaces/diagnostic-schema.md`, `specs/interfaces/rule-id-taxonomy.md`, `specs/interfaces/contracts/diagnostics-module-contract.md` | `conformance/1.0/vectors/diagnostics.jsonl` |

## Boundary

The canonical repository publishes specification semantics, schemas, canonical data, and conformance vectors. It does not contain platform implementation modules.
