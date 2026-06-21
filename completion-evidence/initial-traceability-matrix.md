# Initial APS Traceability Matrix

| Requirement ID | Requirement | Rule ID(s) | Normative source | Schema/field | Module contract | Invariant | Vector(s) | Release gate | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| APS-P0-001 | Preserve the 512-state `F2^9` universe. | Pending rule registry | `specs/core/ash-state-space.pseudo.md` | Pending `ash-state.schema.json` | State Model | Pending | Pending state vectors | Mathematical verification | OPEN | Baseline scan |
| APS-P0-002 | Preserve the exact 16-member canonical codeword set. | Pending rule registry | `specs/core/codeword-set.pseudo.md` | Pending `codeword-set.schema.json` | Transition Registry | Pending | Pending codeword vectors | Mathematical verification | OPEN | Baseline scan |
| APS-P0-003 | Separate malformed input from well-formed states. | Pending rule registry | Completion package semantic closure section 1 | Pending `state-input.schema.json` | State Model, Diagnostics Module | Pending | Pending input-validation vectors | Semantic closure | OPEN | `completion-evidence/unresolved-language-inventory.md` |
| APS-P0-004 | Assign every well-formed state exactly one orbit. | Pending rule registry | Completion package semantic closure section 1.2 | Pending `orbit-record.schema.json` | State Model, Realm Encoder | Pending | Pending orbit vectors | Mathematical verification | OPEN | Baseline scan |
| APS-P0-005 | Define reachability as pairwise membership of `source XOR target` in `C`. | Pending rule registry | Completion package semantic closure section 1.3 | Pending `reachability-result.schema.json` | Transition Registry | Pending | Pending reachability vectors | Conformance | OPEN | Baseline scan |
| APS-P0-006 | Define deterministic topology identifiers, counts, lineage, and ordering. | Pending rule registry | Completion package semantic closure section 8 | Pending topology schemas | Topology Generator | Pending | Pending topology vectors | Conformance | OPEN | `specs/algorithms/branching-semantics.pseudo.md` baseline conflict |
| APS-P0-007 | Publish machine-readable schemas, canonical data, examples, and conformance corpus. | Pending rule registry | `MACHINE-READABLE-PRODUCT-REQUIREMENTS.md`, `CONFORMANCE-CORPUS-REQUIREMENTS.md` | Pending all `schemas/1.0/*` | All contracts | Pending | Pending corpus | Release readiness | OPEN | Missing product surfaces |
| APS-P0-008 | Keep protected governance surfaces unchanged on the product branch. | Protected-surface policy | `PROTECTED-GOVERNANCE-BOUNDARY.md` | N/A | N/A | Protected-surface hash baseline | N/A | Gate Integrity | ACTIVE | `completion-evidence/protected-surface-baseline.json` |

## Completeness checks

- Total normative requirements: pending full rule extraction.
- Requirements mapped to rule IDs: pending rule registry.
- Requirements mapped to schemas: pending schema implementation.
- Requirements mapped to contracts: pending contract reconciliation.
- Requirements mapped to invariants: pending invariant rewrite.
- Requirements mapped to vectors: pending conformance corpus.
- Requirements mapped to release gates: pending release readiness tooling.
- Orphan rules: pending rule registry.
- Orphan schema fields: pending schemas.
- Orphan vectors: pending corpus.
- Open gaps: all semantic and product-completion workstreams remain open after Phase 0 baseline capture.
