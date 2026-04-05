# Common Downstream Handoff Requirements

## Purpose

This document defines the **universal requirements** that every downstream implementation repository must satisfy, regardless of target class (desktop, mobile, service, or other).

## Canonical-authority boundary

The canonical agnostic repository is the semantic authority for the ASH Pattern System. This handoff requirements document and the target-class templates constrain downstream repository structure, required deliverables, and proof-of-conformance inputs. They do **not** override canonical semantics.

Specifically:
- Canonical specifications (`specs/core/`, `specs/algorithms/`) define what the system means
- Canonical contracts (`specs/interfaces/contracts/`) define what each module must do
- Canonical registries (`specs/registries/`) define policy-driven behavior
- Canonical verification (`specs/verification/`) defines what must be proven
- Canonical diagnostics (`specs/interfaces/diagnostic-schema.md`, `rule-id-taxonomy.md`) define how diagnostics must be structured

Handoff templates define how a downstream repository must be organized, what deliverables it must produce, and what conformance evidence it must provide. They do not define new semantics.

## Required semantic-module mapping

Every downstream implementation must map each of the 9 canonical semantic modules to a concrete implementation module:

| Canonical module | Downstream must provide |
|---|---|
| `StateModel` | Full 9-bit state representation, normalization, admissibility, diagnostics, classification, recoverability |
| `RecoveryEngine` | Codeword-based recovery, registry-driven fallback, containment, safe halt, monotonic escalation |
| `RealmEncoder` | Deterministic realm identity encoding from valid 9-bit states |
| `TransitionRegistry` | XOR-by-codeword transition resolution and application |
| `TopologyGenerator` | Deterministic topology generation with stable ordering and lineage |
| `AxiomEvaluator` | Explainable axiom evaluation with diagnostic records |
| `GenerationPlanner` | Abstract plan production with no side effects |
| `ArtifactEmitter` | Plan materialization with no semantic invention |
| `Diagnostics` | Schema-conformant diagnostics with taxonomy-compliant rule IDs |

The mapping must be documented in the downstream repository.

## Required invariant / conformance verification inputs

The downstream repository must include a verification plan that addresses:

- All invariants defined in `specs/verification/invariant-spec.md`
- All 5 conformance categories defined in `specs/verification/conformance-categories.md`
- Acceptance criteria defined in `specs/verification/implementation-acceptance.md`

The verification plan must identify which invariants are testable with the current target platform and which require specific tooling or infrastructure.

## Diagnostics integration expectations

The downstream implementation must:

- Produce diagnostics conforming to `specs/interfaces/diagnostic-schema.md`
- Use rule IDs conforming to `specs/interfaces/rule-id-taxonomy.md`
- Maintain diagnostic chain integrity from detection through terminal halt
- Never silently omit diagnostics

## Materialization-boundary expectations

The downstream implementation must respect the locked materialization boundary:

- `GenerationPlanner` plans — no artifacts, no side effects
- `ArtifactEmitter` materializes — no semantic invention
- The plan is the sole interface between planner and emitter

## Packaging / build / deployment decision surface

The downstream repository must document its target-specific decisions for:

- Build system and toolchain
- Dependency management
- Packaging format and distribution
- Deployment target and runtime environment
- Configuration management

These are downstream decisions — the canonical repository does not prescribe them.

## Performance / resource constraint section

The downstream repository must document:

- Target performance requirements (latency, throughput, memory, storage)
- Resource constraints imposed by the target environment
- How these constraints affect module implementation choices

## Caveat / deviation tracking section

The downstream repository must maintain a tracking document for:

- Any deviations from canonical semantics (with justification and approval)
- Any caveats that affect conformance claims
- Any target-specific limitations that prevent full invariant coverage

Deviations from canonical semantics require explicit documentation and must not be silently introduced.

## Proof-of-conformance deliverables

Before downstream work is considered implementation-ready, the repository must produce:

1. **Module mapping document** — maps each canonical module to its downstream implementation
2. **Verification report** — results of running the invariant/conformance verification suite
3. **Diagnostics conformance report** — evidence that diagnostics conform to the schema and taxonomy
4. **Materialization-boundary report** — evidence that the planner/emitter boundary is respected
5. **Deviation log** — documented deviations (if any) with justification
6. **Acceptance judgment** — CONFORMANT, CONFORMANT WITH CAVEATS, or NON-CONFORMANT per `implementation-acceptance.md`
