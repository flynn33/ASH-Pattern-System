# Downstream Handoff Guide

The canonical repository provides template-driven handoff guidance for downstream implementation repositories.

For the canonical conformance model these deliverables prove against, see [Contracts and Verification](Contracts-and-Verification); for the sentinels that gate the canonical repository and the reusable downstream conformance workflow, see [Governance and Agents](Governance-and-Agents).

## Required Downstream Deliverables

Each downstream repository should deliver:

1. Module mapping document
2. Verification report
3. Diagnostics conformance report
4. Materialization-boundary report
5. Deviation log
6. Acceptance judgment

## Template Sources

Templates cover three target classes — desktop, mobile, and service — plus the common requirements file shared by all of them:

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

This verifies required artifacts and the acceptance judgment, which must be one of `CONFORMANT`, `CONFORMANT WITH CAVEATS`, or `NON-CONFORMANT` — the three valid judgments enumerated in [Contracts and Verification](Contracts-and-Verification) (there is no partial conformance).
