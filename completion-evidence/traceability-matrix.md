# Traceability Matrix

| Requirement | Rule IDs | Normative source | Schema/data | Conformance vectors | Evidence | Status |
|---|---|---|---|---|---|---|
| Preserve full `F2^9` state space and 512 realms. | `ASH-STATE-001`, `ASH-REALM-001` | `specs/core/ash-state-space.pseudo.md` | `schemas/1.0/ash-state.schema.json`, `canonical-data/1.0/realms.json` | `conformance/1.0/vectors/states.jsonl`, `realm-identities.jsonl` | `python3 tools/product/verify_canonical_data.py` | PASS |
| Preserve exact 16-member codeword set and closure. | `ASH-CODEWORD-001` | `specs/core/codeword-set.pseudo.md` | `canonical-data/1.0/codewords.json` | `conformance/1.0/vectors/codewords.jsonl` | Product unit tests and canonical verifier | PASS |
| Assign every well-formed state one orbit. | `ASH-ORBIT-001` | `specs/core/state-admissibility.pseudo.md` | `canonical-data/1.0/orbits.json` | `states.jsonl`, `reachability.jsonl` | `test_orbits_partition_all_512_states` | PASS |
| Define pairwise reachability as codeword-difference membership. | `ASH-TRANSITION-001`, `ASH-ORBIT-001` | `specs/core/state-admissibility.pseudo.md` | `schemas/1.0/reachability-result.schema.json` | `conformance/1.0/vectors/reachability.jsonl`, `transformations.jsonl` | Conformance verifier | PASS |
| Preserve `b8` across canonical transitions. | `ASH-TRANSITION-001` | `specs/core/codeword-set.pseudo.md` | `canonical-data/1.0/mathematical-properties.json` | `transformations.jsonl` | `test_codewords_are_closed_rank_four_and_preserve_b8` | PASS |
| Separate malformed input from operational health. | `ASH-INPUT-001`, `ASH-CLASSIFICATION-001` | `specs/core/state-admissibility.pseudo.md`, `state-validity-diagnostics.pseudo.md` | `schemas/1.0/state-input.schema.json`, `state-assessment.schema.json` | `state-assessments.jsonl`, `diagnostics.jsonl` | Semantic integrity scan | PASS |
| Define correction, fallback, containment, failure, and halt without overlap. | `ASH-RECOVERY-001`, `ASH-FALLBACK-001`, `ASH-CONTAINMENT-001`, `ASH-HALT-001` | `specs/core/recoverability-semantics.pseudo.md`, `specs/algorithms/recovery-fallback-semantics.pseudo.md` | `recovery-result.schema.json`, `fallback-policy-definition.schema.json`, `containment-record.schema.json`, `safe-halt-record.schema.json` | `recovery.jsonl`, `fallback.jsonl`, `containment.jsonl`, `safe-halt.jsonl` | Conformance verifier | PASS |
| Define deterministic topology IDs, ordering, lineage, and counts. | `ASH-TOPOLOGY-001` | `specs/algorithms/branching-semantics.pseudo.md` | `topology-request.schema.json`, `topology-node.schema.json`, `topology-result.schema.json` | `topology.jsonl` | `test_topology_depth_two_is_deterministic` | PASS |
| Define axiom, generation, emission, and diagnostic product surfaces. | `ASH-AXIOM-001`, `ASH-GENERATION-001`, `ASH-EMISSION-001`, `ASH-DIAGNOSTIC-001` | `specs/algorithms/axiom-evaluation.pseudo.md`, `generation-planning.pseudo.md`, `specs/interfaces/diagnostic-schema.md` | Required schemas under `schemas/1.0/` | `axioms.jsonl`, `generation-plans.jsonl`, `materialization-boundary.jsonl`, `diagnostics.jsonl` | Schema and conformance validators | PASS |
| Publish machine-readable product data. | `ASH-CONFORMANCE-001`, `ASH-RELEASE-001` | `MACHINE-READABLE-PRODUCT-REQUIREMENTS.md` package | `schemas/1.0/`, `canonical-data/1.0/`, `product-manifest.json` | All corpus vectors | Product validators | PASS |
| Build deterministic release candidate. | `ASH-RELEASE-001` | `RELEASE-PROCESS.md` | `release/release-manifest.json`, `release/SHA256SUMS` | Archive verification | `python3 tools/product/build_release_archive.py --verify` | PASS |
| Preserve protected governance surfaces. | Protected-surface policy | package `PROTECTED-GOVERNANCE-BOUNDARY.md` | `completion-evidence/protected-surface-baseline.json` | N/A | Protected verifier PASS | PASS |

## Notes

This matrix maps the release-candidate product surfaces. Final publication approval remains owner-controlled and is not represented as completed here.
