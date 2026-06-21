# Reproducibility Report

## Commands

| Command | Result |
|---|---|
| `python3 tools/product/build_release_archive.py --verify` | PASS |
| `python3 tools/product/verify_release_archive.py --archive release/ash-pattern-system-1.0.0-rc.1.zip` | PASS |

## Release artifacts

| Artifact | SHA-256 |
|---|---|
| `release/ash-pattern-system-1.0.0-rc.1.zip` | `e75d67fe9127f3fdf432a18136cbf1dededcfcf6e35eaf826a93972f9c9777a0` |
| `release/release-manifest.json` | `0cb402a48d76fffba96479471d85db221279fa32185bbbbbc66e91b3d340649a` |
| `release/SHA256SUMS` | `e44a93068e2e16e1744c4784ebfd2e7f02ba704c1cc463940dd8b615bef2852e` |

## Result

The archive was built twice by `--verify` with identical SHA-256 output, then extracted and verified offline.
