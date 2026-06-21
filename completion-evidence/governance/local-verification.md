# Local Governance Verification

## Environment

- Repository: `flynn33/ASH-Pattern-System`
- Local path: `/users/jim/github/asp`
- Branch: `governance/gate-integrity-hardening`
- Base SHA: `e123f5d7fdbb381179971f721a3292c31eb1cbc2`

## Commands

```text
python3 -m py_compile .github/scripts/*.py
python3 .github/scripts/gate_integrity_selftest.py
python3 .github/scripts/no_attribution_check.py
git diff --check
REPORT_ONLY=0 python3 .github/scripts/alignment_check.py
REPORT_ONLY=0 python3 .github/scripts/semantic_integrity_check.py
REPORT_ONLY=0 python3 .github/scripts/docs_maintenance_check.py
REPORT_ONLY=0 python3 .github/scripts/wiki_maintenance_check.py
REPORT_ONLY=0 python3 .github/scripts/math_integrity_check.py
python3 /users/jim/ai/codex/APS/aps-product-completion-governance-locked/tools/verify_protected_surface.py --policy /users/jim/ai/codex/APS/aps-product-completion-governance-locked/controls/protected-surface-policy.json --base-ref main --mode governance
rg -n "uses: .*@(v|main|master|HEAD|\$\{\{)" .github/workflows || true
python3 - <<'PY'
import subprocess
from importlib.machinery import SourceFileLoader
m = SourceFileLoader('no_attr', '.github/scripts/no_attribution_check.py').load_module()
tracked = subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()
untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], text=True).splitlines()
paths = set(tracked + untracked)
errors = []
m.check_paths(paths, errors)
m.check_file_content(paths, errors)
if errors:
    raise SystemExit("\\n".join(errors))
print(f"WORKTREE ATTRIBUTION SCAN: PASS ({len(paths)} changed paths scanned)")
PY
```

## Results

- Python compile: PASS
- Gate Integrity self-test: PASS
- Attribution commit-range check: PASS
- Whitespace check: PASS
- Alignment Agent: PASS
- Canonical Semantic Integrity Agent: PASS
- Docs Maintenance Agent: PASS
- Wiki Maintenance Agent: PASS
- Math Integrity Agent: PASS
- Protected surface verifier, governance mode: PASS
- Mutable active workflow `uses:` references: none found
- Working-tree attribution path/content scan: PASS, 21 changed paths scanned

## External Gates

- Trusted base-branch Gate Integrity cannot run on the bootstrap pull request until the workflow exists on protected `main`.
- Active branch/ruleset protection cannot be proven from local files. Authenticated GitHub settings evidence and owner confirmation are still required before product completion work can start.
