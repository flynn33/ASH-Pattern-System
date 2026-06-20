# Initial Traceability Matrix

This is the Phase 0 seed matrix. It records the package-required workstreams before semantic repair. It is not the final zero-gap traceability matrix.

| Requirement ID | Requirement | Rule ID(s) | Normative source | Schema/field | Module contract | Invariant | Vector(s) | Release gate | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| APS-COMPLETE-000 | Capture and audit live baseline | Pending | `PRODUCT-COMPLETION-INSTRUCTIONS.md`, `EXECUTION-PLAN.md` | N/A | N/A | N/A | N/A | P0 | In progress | `completion-evidence/baseline-audit.md` |
| APS-COMPLETE-100 | Repair state, orbit, reachability, and operational semantics | Pending | `SEMANTIC-CLOSURE-SPECIFICATION.md` sections 1-7 | Required | `StateModel`, `RecoveryEngine`, `Diagnostics` | Required | Required | P1 | Open blocker | `completion-evidence/unresolved-language-inventory.md` |
| APS-COMPLETE-200 | Lock identifiers, transitions, branching, topology, and averaging | Pending | `SEMANTIC-CLOSURE-SPECIFICATION.md` sections 3, 4, 8, 9 | Required | `RealmEncoder`, `TransitionRegistry`, `TopologyGenerator` | Required | Required | P2 | Open blocker | Reference assets verified in package preflight |
| APS-COMPLETE-300 | Complete axiom, generation, emission, diagnostic, and rule semantics | Pending | `SEMANTIC-CLOSURE-SPECIFICATION.md` sections 10-12 | Required | `AxiomEvaluator`, `GenerationPlanner`, `ArtifactEmitter`, `Diagnostics` | Required | Required | P3 | Open blocker | `completion-evidence/symbol-inventory.json` |
| APS-COMPLETE-400 | Build versioned schemas, canonical data, and examples | Pending | `MACHINE-READABLE-PRODUCT-REQUIREMENTS.md` | Required | All public records | Required | Required | P4 | Not started | Missing `schemas/`, `canonical-data/`, `examples/` |
| APS-COMPLETE-500 | Build exhaustive conformance corpus | Pending | `CONFORMANCE-CORPUS-REQUIREMENTS.md` | Required | All modules | Required | Required | P5 | Not started | Downstream conformance check fails; no canonical corpus exists |
| APS-COMPLETE-600 | Reconcile contracts, invariants, acceptance, and downstream handoff | Pending | `PRODUCT-COMPLETION-INSTRUCTIONS.md` workstream G | Required | All nine contracts | Required | Required | P6 | Not started | Current contracts still include stale semantic terms |
| APS-COMPLETE-700 | Harden governance, security, and naming controls | Pending | `SECURITY-AND-AUTOMATION-HARDENING.md` | Required | Governance scripts/workflows | Required | Required | P7 | Not started | Workflows use `REPORT_ONLY`, mutable actions, and non-neutral filenames |
| APS-COMPLETE-800 | Complete lifecycle, legal, citation, support, and documentation | Pending | `DOCUMENTATION-LEGAL-AND-DISTRIBUTION.md`, `RELEASE-GOVERNANCE-AND-LIFECYCLE.md` | Required | Release/documentation surfaces | Required | Required | P8 | Not started | Required root product files absent |
| APS-COMPLETE-900 | Build reproducible release candidate and execute recursive audit | Pending | `VERIFICATION-AND-SELF-AUDIT-PROTOCOL.md` | Required | All release surfaces | Required | Required | P9/P10 | Not started | Requires previous workstreams |

## Completeness checks

- Total package workstream requirements: 10
- Requirements mapped to rule IDs: 0
- Requirements mapped to schemas: Pending schema creation
- Requirements mapped to contracts: Seed mapping only
- Requirements mapped to invariants: Pending invariant rewrite
- Requirements mapped to vectors: Pending corpus creation
- Requirements mapped to release gates: 10
- Orphan rules: Not yet audited
- Orphan schema fields: Schemas absent
- Orphan vectors: Corpus absent
- Open gaps: All semantic/product workstreams after Phase 0
