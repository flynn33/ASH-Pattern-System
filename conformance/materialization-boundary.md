# Materialization Boundary Conformance

## Boundary

APS separates generation planning from artifact materialization.

- `GenerationPlanner` produces a complete plan with no side effects.
- `ArtifactEmitter` materializes only outputs described by the plan.
- The emitter must not invent missing semantic data.
- Every emitted output must reference the plan element that authorized it.

## Normative sources

- `specs/algorithms/generation-planning.pseudo.md`
- `specs/interfaces/contracts/generation-planner-contract.md`
- `specs/interfaces/contracts/artifact-emitter-contract.md`

## Evidence

| Evidence | Purpose |
|---|---|
| `conformance/1.0/vectors/generation-plans.jsonl` | Generation request and plan behavior |
| `conformance/1.0/vectors/materialization-boundary.jsonl` | Emitter traceability and refusal cases |
| `schemas/1.0/generation-plan.schema.json` | Plan record schema |
| `schemas/1.0/emission-result.schema.json` | Emission result schema |

## Result

The release-candidate corpus includes boundary vectors for planner determinism, plan-hash sensitivity, emitter traceability, and emitter refusal on incomplete or ambiguous plans.
