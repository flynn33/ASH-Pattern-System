# Release Process

From a clean checkout, run `python3 tools/product/verify_canonical_data.py`, `python3 tools/product/verify_conformance_corpus.py`, `python3 tools/product/build_release_archive.py --source-commit <release-source-commit> --verify`, `python3 tools/product/verify_release_archive.py --archive release/ash-pattern-system-1.0.0-rc.1.zip`, and `python3 tools/product/release_readiness.py --strict --offline --source-commit <release-source-commit>` before publishing.
