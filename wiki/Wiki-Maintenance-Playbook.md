# Wiki Maintenance Playbook

This playbook defines how wiki content is maintained as part of canonical repository upkeep.

## Canonical Wiki Source

The `wiki/` directory in the main repository is the source-controlled canonical wiki content set.

## Required Wiki Pages

- `Home.md`
- `_Sidebar.md`
- `Getting-Started.md`
- `Canonical-Math-Baseline.md`
- `Specification-Layers.md`
- `Recovery-and-Safety-Semantics.md`
- `Contracts-and-Verification.md`
- `Governance-and-Agents.md`
- `Downstream-Handoff-Guide.md`
- `Glossary.md`
- `Wiki-Maintenance-Playbook.md`

## Update Triggers

Update wiki pages when any of these change materially:

- `README.md`
- `docs/*.md`
- `specs/**/*.md`
- `governance/*.md`
- `.github/workflows/*.yml`
- `.github/scripts/*.py`

## Maintenance Workflow

1. Update canonical source docs/specs first.
2. Update affected wiki pages in `wiki/`.
3. Verify internal wiki links resolve.
4. Ensure `Home.md` and `_Sidebar.md` include all required pages.
5. Run `python3 .github/scripts/wiki_maintenance_check.py`.

## CI Guardrail

`Wiki Maintenance Agent` enforces page presence, heading health, internal link integrity, and change-drift signaling when canonical docs change without wiki updates.

On `push` to `main`, if `wiki/` changed, the workflow also syncs the `wiki/` directory into the GitHub Wiki repository (`<repo>.wiki.git`).
