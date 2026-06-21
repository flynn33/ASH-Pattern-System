# Canonical Verification Report

## Scope

This report records the repository-local verification commands for the APS 1.0 release-candidate conformance surfaces.

## Commands

| Command | Result |
|---|---|
| `python3 tools/product/verify_canonical_data.py` | PASS |
| `python3 tools/product/verify_conformance_corpus.py` | PASS |
| `python3 tools/product/validate_schemas.py` | PASS |
| `python3 tools/product/validate_rule_registry.py` | PASS |
| `python3 tools/product/validate_traceability.py` | PASS |
| `python3 -m unittest discover -s tools/product/tests -v` | PASS |

## Coverage

The conformance corpus covers all 512 states, 16 codewords, 32 orbits, 8,192 transformations, compact reachability proof records, exact averaging vectors, topology vectors, diagnostic vectors, axiom vectors, generation-plan vectors, recovery vectors, fallback vectors, containment vectors, and safe-halt vectors.

## Result

The canonical conformance corpus verifies against the current product schemas and rule registry.
