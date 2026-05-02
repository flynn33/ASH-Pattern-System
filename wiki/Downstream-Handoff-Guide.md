# Downstream Handoff Guide

The canonical repository provides template-driven handoff guidance for downstream implementation repositories.

## Required Downstream Deliverables

Each downstream repository should deliver:

1. Module mapping document
2. Verification report
3. Diagnostics conformance report
4. Materialization boundary report
5. Deviation log
6. Acceptance judgment

## Template Sources

- `handoff-templates/common-downstream-handoff-requirements.md`
- `handoff-templates/desktop-implementation-handoff-template.md`
- `handoff-templates/mobile-implementation-handoff-template.md`
- `handoff-templates/service-implementation-handoff-template.md`

## Handoff Principles

1. Templates define structure and evidence, not platform technology choices.
2. Templates do not override canonical semantic specs.
3. Conformance evidence must map to canonical invariants and contracts.
4. Deviation logs are mandatory when behavior diverges from canonical baselines.

## Downstream Conformance Check

Downstream repos can call the reusable workflow:

- `.github/workflows/downstream-conformance-agent.yml`

This verifies required artifacts and acceptance judgment language.
