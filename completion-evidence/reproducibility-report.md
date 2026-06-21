# Reproducibility Report

## Commands

| Command | Result |
|---|---|
| `python3 tools/product/build_release_archive.py --source-commit 639e0cfe8b1c276e03cd3351e04311fc845936d1 --verify` | PASS |
| `python3 tools/product/verify_release_archive.py --archive release/ash-pattern-system-1.0.0-rc.1.zip` | PASS |

## Release artifacts

| Artifact | SHA-256 |
|---|---|
| `release/ash-pattern-system-1.0.0-rc.1.zip` | `23be577f886760f8d8fef5dbaf9b483c07a002baf6dc0373a2b04961ea811e15` |
| `release/release-manifest.json` | `8b51290e2fa5cf90e207e613a5fe99a2e12cbc9fd3fa4e5168e767ebadf6a6b8` |
| `release/SHA256SUMS` | `b98545ad5cb7fd0018c29e1a141dc0af4de28bbfd8637d884a663664713e4b3a` |

## Result

The archive was built twice by `--verify` with identical SHA-256 output, then extracted and verified offline.
