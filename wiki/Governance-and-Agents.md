# Governance and Agents

This page summarizes repository governance and the sentinel agents that protect canonical integrity.

## Governance Scope

Primary governance documents live under `governance/`.

There are eight agents: seven guard the canonical repository directly, and one (Downstream Conformance) is a reusable downstream workflow.

## Active GitHub Agents

| Agent | Workflow | Purpose |
|---|---|---|
| Alignment Agent | `.github/workflows/alignment-agent.yml` | Blocks implementation-code drift in canonical repo |
| Canonical Semantic Integrity Agent | `.github/workflows/canonical-semantic-integrity-agent.yml` | Blocks non-canonical math-language reintroduction and semantic authority inversion |
| Math Integrity Agent | `.github/workflows/math-integrity-agent.yml` | Protects locked 9D math-critical paths |
| Downstream Conformance Agent | `.github/workflows/downstream-conformance-agent.yml` | Reusable `workflow_call` workflow consumed by downstream repos to validate handoff deliverables and conformance; not a push/PR gate on the canonical repo |
| Attribution Policy Agent | protected attribution workflow | Rejects prohibited attribution markers in commits/authors/files |
| Gate Integrity Agent | `.github/workflows/gate-integrity.yml` | Enforces protected-surface protection, governance-PR isolation, owner approval, and fail-closed gate checks |
| Wiki Maintenance Agent | `.github/workflows/wiki-maintenance-agent.yml` | Maintains wiki completeness, structure, and drift checks |
| Docs Maintenance Agent | `.github/workflows/docs-maintenance-agent.yml` | Maintains README/docs/governance quality and reference integrity |

## Agent Roles

- Agents are gatekeepers, not semantic authorities.
- Canonical truth remains in `specs/` plus governance documents.
- Agent output that conflicts with canonical specs must be corrected in agent logic.

## Workflow Mode

Sentinels run blocking by default (the `REPORT_ONLY` default is `0`, so findings are enforced). `REPORT_ONLY` is a local diagnostic switch read by `.github/scripts/_common.py`: when set to `1`, scripts emit findings without blocking. It is exposed as an env var by only some workflows, and the `no-ai-attribution`, `gate-integrity`, and `downstream-conformance` workflows do not honor it.
