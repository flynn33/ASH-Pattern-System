# Repository Governance

## Repository role

This repository is the current canonical specification of the ASH Pattern System. It exists to describe the system's math, semantics, contracts, and verification requirements without tying them to a platform implementation.

## Governance rules

### 1. ASH Model alignment

All canonical math and state semantics in this repository must stay aligned with the ASH Model baseline.

### 2. Spec-first rule

Changes that affect semantics must be made in the specification documents first. Implementations follow the specifications; they do not redefine them.

### 3. Platform neutrality

No programming language, operating system, runtime family, device category, or toolchain may be described as the canonical identity of the system.

### 4. Current-baseline rule

This repository carries the current canonical baseline only. Legacy formulations and explanatory packaging that exists only to discuss older repository states do not belong here.

### 5. Pseudocode rule

When algorithmic examples are needed, use pseudocode or specification prose. Platform syntax belongs in implementation repositories.

### 6. Admission rule for future files

A new file belongs in this repository only if it strengthens the current semantic source of truth or enforces it operationally. Governance agents, wiki source pages, and downstream handoff templates are allowed when they remain aligned with the canonical math and semantics.

### 7. No placeholder semantics

Canonical documents must not rely on guessed values, implicit defaults, or unresolved placeholders when describing normative behavior.

## Repository boundary

This repository may contain:

- Markdown specifications and governance
- pseudocode specifications
- GitHub workflows and small governance scripts that enforce canonical integrity
- wiki source pages and downstream handoff templates aligned to the canonical baseline
- small supporting text or JSON artifacts that clarify canonical semantics

This repository must not contain:

- platform-specific source code
- build or delivery scaffolding that is not part of the ASH Pattern System itself
- historical pre-remediation specifications retained only for comparison

## Main-repository closeout

This repository remains the canonical baseline and stays implementation-free.

- Main remains aligned to the ASH Model source of truth.
- Main may include governance agents, wiki material, and handoff templates when they reinforce the canonical baseline rather than replace it.
- Main must not be used to host platform builds, runtime packages, emitted artifacts, or implementation-specific source trees.
- Future edits are limited to canonical corrections, clearer source grounding, contract and verification upkeep, and enforcement improvements.
