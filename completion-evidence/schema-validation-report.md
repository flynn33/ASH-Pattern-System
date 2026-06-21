# Schema Validation Report

## Commands

| Command | Result |
|---|---|
| `python3 tools/product/validate_schemas.py` | PASS |
| `python3 tools/product/verify_canonical_data.py` | PASS |
| `python3 -m unittest discover -s tools/product/tests -v` | PASS |

## Coverage

- Required schema entry points exist under `schemas/1.0/`.
- Schemas declare JSON Schema Draft 2020-12.
- Canonical data exists under `canonical-data/1.0/`.
- Valid and invalid examples exist under `examples/`.

## Result

Schema and canonical-data validation passed for the release-candidate product tree.
