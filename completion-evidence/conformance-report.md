# Conformance Report

## Commands

| Command | Result |
|---|---|
| `python3 tools/product/generate_conformance_corpus.py` | PASS |
| `python3 tools/product/verify_conformance_corpus.py` | PASS |
| `python3 .github/scripts/downstream_conformance_check.py` | PASS |
| `python3 -m unittest discover -s tools/product/tests -v` | PASS |

## Corpus layout

The corpus exists under `conformance/1.0/` with:

- exhaustive state vectors;
- codeword vectors;
- transformation vectors;
- compact reachability records covering every source realm;
- realm identity vectors;
- exact averaging vectors;
- topology vectors;
- state assessment, recovery, fallback, containment, halt, diagnostic, axiom, generation, and materialization-boundary scenarios;
- invalid corpus metadata;
- manifest hashes and `SHA256SUMS`.
- top-level downstream handoff evidence files required by `handoff-templates/common-downstream-handoff-requirements.md`.

## Result

Conformance corpus verification passed. The repeated-generation regression test confirms corpus manifests remain stable after regeneration.
