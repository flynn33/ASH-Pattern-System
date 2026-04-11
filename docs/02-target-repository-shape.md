# Target Repository Shape

## Canonical structure

```text
ash-pattern-system/
├── README.md
├── docs/
│   ├── 00-repository-purpose.md
│   ├── 01-design-philosophy.md
│   ├── 02-target-repository-shape.md
│   └── 03-design-roadmap.md
├── specs/
│   ├── core/
│   │   ├── ash-state-space.pseudo.md
│   │   ├── control-bit-derivation.pseudo.md
│   │   ├── core-admissibility.pseudo.md
│   │   ├── codeword-set.pseudo.md
│   │   ├── state-admissibility.pseudo.md
│   │   ├── state-validity-diagnostics.pseudo.md
│   │   ├── system-state-classification.pseudo.md
│   │   ├── recoverability-semantics.pseudo.md
│   │   └── realm-identity.pseudo.md
│   ├── algorithms/
│   │   ├── codeword-transformation-semantics.pseudo.md
│   │   ├── averaging-operator-semantics.pseudo.md
│   │   ├── branching-semantics.pseudo.md
│   │   ├── transition-system.pseudo.md
│   │   ├── topology-expansion.pseudo.md
│   │   ├── axiom-evaluation.pseudo.md
│   │   ├── generation-planning.pseudo.md
│   │   ├── recovery-fallback-semantics.pseudo.md
│   │   └── containment-safe-failure-semantics.pseudo.md
│   ├── registries/
│   │   └── fallback-policy-registry.md
│   ├── verification/
│   │   ├── invariant-spec.md
│   │   ├── conformance-categories.md
│   │   └── implementation-acceptance.md
│   └── interfaces/
│       ├── semantic-contracts.md
│       ├── diagnostic-schema.md
│       ├── rule-id-taxonomy.md
│       └── contracts/
│           ├── state-model-contract.md
│           ├── recovery-engine-contract.md
│           ├── realm-encoder-contract.md
│           ├── transition-registry-contract.md
│           ├── topology-generator-contract.md
│           ├── axiom-evaluator-contract.md
│           ├── generation-planner-contract.md
│           ├── artifact-emitter-contract.md
│           └── diagnostics-module-contract.md
├── handoff-templates/
│   ├── README.md
│   ├── common-downstream-handoff-requirements.md
│   ├── desktop-implementation-handoff-template.md
│   ├── mobile-implementation-handoff-template.md
│   └── service-implementation-handoff-template.md
├── wiki/
│   ├── Home.md
│   ├── _Sidebar.md
│   ├── Getting-Started.md
│   ├── Canonical-Math-Baseline.md
│   ├── Specification-Layers.md
│   ├── Recovery-and-Safety-Semantics.md
│   ├── Contracts-and-Verification.md
│   ├── Governance-and-Agents.md
│   ├── Downstream-Handoff-Guide.md
│   ├── Wiki-Maintenance-Playbook.md
│   └── Glossary.md
├── .github/
│   ├── workflows/
│   │   ├── alignment-agent.yml
│   │   ├── canonical-semantic-integrity-agent.yml
│   │   ├── math-integrity-agent.yml
│   │   ├── downstream-conformance-agent.yml
│   │   ├── no-ai-attribution.yml
│   │   ├── wiki-maintenance-agent.yml
│   │   └── docs-maintenance-agent.yml
│   └── scripts/
│       ├── _common.py
│       ├── alignment_check.py
│       ├── semantic_integrity_check.py
│       ├── math_integrity_check.py
│       ├── downstream_conformance_check.py
│       ├── wiki_maintenance_check.py
│       └── docs_maintenance_check.py
└── governance/
    ├── repository-governance.md
    ├── ai-coding-handoff.md
    └── github-agents-governance.md
```

## Structural rules

### `docs/`
Contains explanatory and planning documents.
These explain intent, philosophy, and sequencing.

### `specs/core/`
Contains the canonical model of the ASH state itself.
This is the highest-priority semantic layer.

### `specs/algorithms/`
Contains algorithmic semantics expressed in platform-neutral pseudocode and prose.

### `specs/registries/`
Contains canonical registries that govern deterministic policy-driven behavior (e.g., fallback selection).

### `specs/verification/`
Contains invariant specifications, conformance categories, and implementation acceptance criteria for downstream verification.

### `specs/interfaces/`
Contains contracts, diagnostic schemas, and rule taxonomies that downstream implementations must satisfy.

### `handoff-templates/`
Contains downstream build handoff templates that define what each target-class implementation repository must contain. Templates define structure, required deliverables, and proof-of-conformance inputs — not implementation code.

### `wiki/`
Contains the version-controlled source for GitHub Wiki pages. Wiki content summarizes canonical semantics and governance and must stay aligned with repository source-of-truth files.

### `.github/`
Contains sentinel workflow definitions and governance scripts that enforce canonical boundary, semantic integrity, math integrity, attribution policy, and documentation/wiki upkeep.

### `governance/`
Contains repository rules and handoff rules for coding agents.

## Exclusions from this repository shape

This repository shape intentionally excludes canonical dependence on:

- `src/`
- `include/`
- `tests/`
- `examples/`
- build-system files
- runtime package manifests
- platform-specific CI assumptions

Those may exist later in implementation repositories.
They are not the identity of this repository.
