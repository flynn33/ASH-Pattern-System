# Governance and Agents

This page summarizes repository governance and the sentinel agents that protect canonical integrity.

## Governance Scope

Primary governance documents:

- `governance/repository-governance.md`
- `governance/ai-coding-handoff.md`
- `governance/github-agents-governance.md`

## Active GitHub Agents

| Agent | Workflow | Purpose |
|---|---|---|
| Alignment Agent | `.github/workflows/alignment-agent.yml` | Blocks implementation-code drift in canonical repo |
| Canonical Semantic Integrity Agent | `.github/workflows/canonical-semantic-integrity-agent.yml` | Blocks non-canonical math-language reintroduction and semantic authority inversion |
| Math Integrity Agent | `.github/workflows/math-integrity-agent.yml` | Protects locked 9D math-critical paths |
| Downstream Conformance Agent | `.github/workflows/downstream-conformance-agent.yml` | Reusable downstream artifact/conformance validation |
| No AI Attribution Agent | `.github/workflows/no-ai-attribution.yml` | Rejects AI-attribution markers in commits/authors/files |
| Wiki Maintenance Agent | `.github/workflows/wiki-maintenance-agent.yml` | Maintains wiki completeness, structure, and drift checks |
| Docs Maintenance Agent | `.github/workflows/docs-maintenance-agent.yml` | Maintains README/docs/governance quality and reference integrity |

## Agent Roles

- Agents are gatekeepers, not semantic authorities.
- Canonical truth remains in `specs/` plus governance documents.
- Agent output that conflicts with canonical specs must be corrected in agent logic.

## Workflow Mode

Sentinel workflows respect the `REPORT_ONLY` environment variable in each workflow file. Report-only mode emits findings without blocking; blocking mode enforces them.
