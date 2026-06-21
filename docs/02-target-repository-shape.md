# Target Repository Shape

## Canonical structure

```text
ash-pattern-system/
├── README.md
├── VERSION
├── product-manifest.json
├── CHANGELOG.md
├── PRODUCT-STATUS.md
├── PUBLIC-SPECIFICATION-API.md
├── RELEASE-NOTES.md
├── RELEASE-PROCESS.md
├── COMPATIBILITY.md
├── DEPRECATION-POLICY.md
├── MIGRATION-GUIDE.md
├── LICENSE.md
├── NOTICE.md
├── SECURITY.md
├── SUPPORT.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CITATION.cff
├── schemas/
│   └── 1.0/
├── canonical-data/
│   └── 1.0/
├── conformance/
│   └── 1.0/
├── examples/
│   ├── valid/
│   └── invalid/
├── tools/
│   └── product/
├── docs/
│   ├── 00-repository-purpose.md
│   ├── 01-design-philosophy.md
│   ├── 02-target-repository-shape.md
│   └── 03-design-roadmap.md
├── specs/
│   ├── core/
│   │   ├── ash-state-space.pseudo.md
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
│   ├── README.md
│   ├── Home.md
│   ├── _Sidebar.md
│   ├── _Footer.md
│   ├── Getting-Started.md
│   ├── Canonical-Math-Baseline.md
│   ├── Specification-Layers.md
│   ├── Recovery-and-Safety-Semantics.md
│   ├── Contracts-and-Verification.md
│   ├── Governance-and-Agents.md
│   ├── Downstream-Handoff-Guide.md
│   ├── Wiki-Maintenance-Playbook.md
│   └── Glossary.md
├── completion-evidence/
│   ├── protected-surface-baseline.json
│   └── governance/
│       ├── gate-integrity-hardening-request.md
│       ├── local-verification.md
│       ├── owner-server-side-steps.md
│       ├── pinned-actions.md
│       └── server-ruleset-evidence-2026-06-21.md
├── .github/
│   ├── CODEOWNERS
│   ├── rulesets/
│   │   └── main-release-platform-protection.md
│   ├── workflows/
│   │   ├── alignment-agent.yml
│   │   ├── canonical-semantic-integrity-agent.yml
│   │   ├── math-integrity-agent.yml
│   │   ├── downstream-conformance-agent.yml
│   │   ├── no-ai-attribution.yml
│   │   ├── gate-integrity.yml
│   │   ├── wiki-maintenance-agent.yml
│   │   └── docs-maintenance-agent.yml
│   └── scripts/
│       ├── _common.py
│       ├── alignment_check.py
│       ├── semantic_integrity_check.py
│       ├── math_integrity_check.py
│       ├── downstream_conformance_check.py
│       ├── no_attribution_check.py
│       ├── gate_integrity_check.py
│       ├── gate_integrity_selftest.py
│       ├── wiki_maintenance_check.py
│       └── docs_maintenance_check.py
└── governance/
    ├── repository-governance.md
    ├── ai-coding-handoff.md
    ├── github-agents-governance.md
    └── math-change-notes/
        ├── README.md
        └── 2026-05-02-self-contained-canonical-language.md
```

## Structural rules

### `docs/`

Contains explanatory and planning documents that describe the repository as a self-contained canonical baseline.

### Root lifecycle files

Contain the product version, manifest, public specification API, release notes, changelog, compatibility policy, migration guidance, license, notice, support, security, contribution, conduct, and citation surfaces for APS as a specification product.

### `schemas/`

Contains versioned JSON Schema entry points for public APS records.

### `canonical-data/`

Contains deterministic versioned codewords, realms, orbits, transitions, fallback policy definitions, rule registry, mathematical properties, and normative artifact index.

### `conformance/`

Contains versioned implementation-neutral vectors and corpus metadata for downstream validation.

### `examples/`

Contains valid and invalid schema examples used by product validation.

### `tools/product/`

Contains standard-library product generation, validation, conformance, and release-archive tooling. This is product support tooling, not a platform implementation tree.

### `specs/core/`

Contains the canonical model of the ASH state itself.
This is the highest-priority semantic layer.

### `specs/algorithms/`

Contains algorithmic semantics expressed in platform-neutral pseudocode and prose.

### `specs/registries/`

Contains canonical registries that govern deterministic policy-driven behavior.

### `specs/verification/`

Contains invariant specifications, conformance categories, and implementation acceptance criteria for downstream verification.

### `specs/interfaces/`

Contains contracts, diagnostic schemas, and rule taxonomies that downstream implementations must satisfy.

### `handoff-templates/`

Contains downstream handoff templates that define required structure, deliverables, and proof-of-conformance inputs for implementation repositories.

### `wiki/`

Contains the version-controlled source for GitHub Wiki pages. Wiki content summarizes canonical semantics and governance and must stay aligned with canonical repository files.

### `.github/`

Contains sentinel workflow definitions and governance scripts that enforce repository boundary, semantic integrity, math integrity, attribution policy, gate integrity (protected-surface and governance-PR controls), and documentation/wiki upkeep, alongside `CODEOWNERS` and the branch-protection ruleset under `rulesets/`.

### `governance/`

Contains repository rules, coding-agent handoff rules, and math-change note requirements.

### `completion-evidence/`

Contains the protected-surface baseline and dated governance verification evidence (local verification, owner server-side steps, pinned actions, and recorded ruleset evidence) that support the gate-integrity controls.

## Exclusions from this repository shape

This repository shape intentionally excludes canonical dependence on:

- `src/`
- `include/`
- `tests/`
- build-system files
- runtime package manifests
- platform-specific CI assumptions

Those may exist later in implementation repositories.
They are not the identity of this repository.
