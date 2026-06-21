# Diagnostics Conformance

## Scope

APS diagnostics are governed by `specs/interfaces/diagnostic-schema.md`, `specs/interfaces/rule-id-taxonomy.md`, and `schemas/1.0/diagnostic-envelope.schema.json`.

## Required properties

- Each diagnostic has a stable diagnostic kind, severity, stage, disposition, subject reference, rule ID list, summary, and deterministic semantic identity.
- Diagnostic chains preserve root, parent, and sequence relationships.
- Rule IDs resolve through `canonical-data/1.0/rule-registry.json`.
- Occurrence metadata does not alter semantic diagnostic identity.

## Evidence

| Evidence | Purpose |
|---|---|
| `conformance/1.0/vectors/diagnostics.jsonl` | Positive diagnostic envelope and chain vectors |
| `conformance/1.0/invalid/undeclared-rule-id.json` | Invalid rule-reference case |
| `tools/product/validate_rule_registry.py` | Rule registry validation |
| `tools/product/validate_schemas.py` | Schema and example validation |

## Result

The canonical diagnostic surfaces are schema-bound and covered by conformance vectors.
