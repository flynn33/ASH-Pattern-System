# GitHub Governance Agents

This document defines the GitHub-native sentinel agent layer that guards the canonical ASH Pattern System repository against drift. The agents are implemented as GitHub Actions workflows under `.github/workflows/` and small Python scripts under `.github/scripts/`.

## Role

The agents are sentinels and gatekeepers, not canonical authorities.

- Agents detect deviations from already-documented canonical state.
- Agents may block commits, pushes, and pull requests at the CI boundary.
- Canonical truth remains in `specs/` and the governance documents.
- If an agent's output conflicts with the canonical specification, the specification wins and the agent must be corrected.

## Canonical file-type policy

The canonical ASH Pattern System repository may contain:

- Markdown (`.md`)
- JSON (`.json`) for manifest or configuration purposes only
- plain text (`.txt`)
- pseudocode files (`.pseudo.md`)
- GitHub Actions workflow YAML under `.github/workflows/`
- small governance and sentinel Python scripts under `.github/scripts/`
- product support tooling under `tools/product/`

The canonical repository may not contain platform, build, or runtime implementation code outside the governance and product-tooling allowlists.

## Agents

Eight agents/workflows are defined. Seven guard the canonical repository directly; one is a reusable workflow for downstream implementation repositories.

### 1. Alignment Agent

**Workflow:** `.github/workflows/alignment-agent.yml`
**Script:** `.github/scripts/alignment_check.py`
**Behavior:** blocking on hard boundary violations.
**Triggers:** every `push` and `pull_request` on any branch.

Checks:

- implementation code anywhere in the repo outside the explicit governance-agent allowlist
- build, package, or platform-tree files that do not belong in the canonical repository
- hierarchy-inversion language that incorrectly moves canonical authority from the specs to downstream implementation surfaces

### 2. Canonical Semantic Integrity Agent

**Workflow:** `.github/workflows/canonical-semantic-integrity-agent.yml`
**Script:** `.github/scripts/semantic_integrity_check.py`
**Behavior:** blocking on canonical-language and authority-boundary violations.
**Triggers:** every `push` and `pull_request` on any branch.

Checks:

- non-canonical math-language reintroduction in active canonical files
- handoff-template authority inversion
- contradictory status language across README, roadmap, and coding-agent handoff surfaces

### 3. Math Integrity Agent

**Workflow:** `.github/workflows/math-integrity-agent.yml`
**Script:** `.github/scripts/math_integrity_check.py`
**Behavior:** blocking.
**Triggers:** every `push` and `pull_request` on any branch. Only activates when a math-critical path is in the changed set.

#### Protected math-critical paths

When any of the following files is in the changed set, the Math Integrity Agent enforces its full rule set:

- `specs/core/ash-state-space.pseudo.md`
- `specs/core/codeword-set.pseudo.md`
- `specs/core/realm-identity.pseudo.md`
- `specs/core/recoverability-semantics.pseudo.md`
- `specs/core/state-admissibility.pseudo.md`
- `specs/core/state-validity-diagnostics.pseudo.md`
- `specs/core/system-state-classification.pseudo.md`
- `specs/algorithms/averaging-operator-semantics.pseudo.md`
- `specs/algorithms/branching-semantics.pseudo.md`
- `specs/algorithms/codeword-transformation-semantics.pseudo.md`
- `specs/algorithms/containment-safe-failure-semantics.pseudo.md`
- `specs/algorithms/recovery-fallback-semantics.pseudo.md`
- `specs/algorithms/transition-system.pseudo.md`
- `specs/algorithms/topology-expansion.pseudo.md`
- `specs/algorithms/axiom-evaluation.pseudo.md`
- `specs/algorithms/generation-planning.pseudo.md`
- `specs/verification/invariant-spec.md`
- `specs/verification/conformance-categories.md`
- `specs/verification/implementation-acceptance.md`

#### Baseline-marker paths

The following subset is checked for continued presence of direct 9D baseline markers after any edit:

- `specs/core/ash-state-space.pseudo.md`
- `specs/core/codeword-set.pseudo.md`
- `specs/core/realm-identity.pseudo.md`
- `specs/algorithms/codeword-transformation-semantics.pseudo.md`
- `specs/algorithms/averaging-operator-semantics.pseudo.md`
- `specs/algorithms/branching-semantics.pseudo.md`

#### Why math changes require human review

The canonical ASH Pattern System math is a locked canonical baseline. The 9D state space, the specific codeword set `C ⊂ F2^9`, the averaging operator, and the branching topology carry cascade effects across admissibility, recovery, classification, verification, and downstream conformance.

#### Math-change note requirement

When any math-critical path is in the changed set, the Math Integrity Agent requires a math-change note in the same push or pull request:

- the note must live under `governance/math-change-notes/` and be a `.md` file other than `README.md`
- the note must contain exactly these three headings: `## What changed`, `## Why`, `## Baseline preservation statement`
- the note must be committed in the same push or pull request as the math-critical edit

#### PR human-review gating

When the triggering event is a pull request and the PR payload is available, at least one of the following labels must be present on the PR:

- `math-reviewed`
- `human-reviewed`
- `baseline-approved`

### 4. Downstream Conformance Agent

**Workflow:** `.github/workflows/downstream-conformance-agent.yml`
**Script:** `.github/scripts/downstream_conformance_check.py`
**Behavior:** reusable workflow for downstream implementation repositories.
**Triggers:** `workflow_call` only.

The agent validates the six canonical downstream conformance artifacts defined in `handoff-templates/common-downstream-handoff-requirements.md`:

1. Module mapping
2. Verification plan/report
3. Diagnostics conformance
4. Materialization boundary
5. Deviation log
6. Acceptance judgment

### 5. No AI Attribution Agent

**Workflow:** `.github/workflows/no-ai-attribution.yml`
**Script:** `.github/scripts/no_attribution_check.py`
**Behavior:** blocking.
**Triggers:** every `push` and `pull_request` on any branch.

Checks:

- AI-attribution markers in commit messages
- AI-associated author or committer identities
- AI-attribution markers in changed file content
- prohibited attribution tokens in branch and tag names
- prohibited attribution tokens in non-grandfathered changed paths

### 6. Gate Integrity Agent

**Workflow:** `.github/workflows/gate-integrity.yml`
**Script:** `.github/scripts/gate_integrity_check.py`
**Self-test:** `.github/scripts/gate_integrity_selftest.py`
**Behavior:** blocking.
**Triggers:** `pull_request_target` for opened, reopened, synchronize, ready-for-review, label, and unlabel events.

Checks:

- product pull requests do not add, edit, delete, or rename protected governance paths
- historical protected-path touches inside a pull-request branch are detected even if later reverted
- governance pull requests are isolated to the governance allowlist
- governance pull requests use a `governance/` branch and the `governance-change` label
- owner approval is present on the current head commit
- API, pagination, payload, or policy errors fail closed

### 7. Wiki Maintenance Agent

**Workflow:** `.github/workflows/wiki-maintenance-agent.yml`
**Script:** `.github/scripts/wiki_maintenance_check.py`
**Behavior:** blocking on hard violations; drift notices remain warnings.
**Triggers:** every `push` and `pull_request` on any branch.

Checks:

- required wiki pages exist and are non-empty
- `wiki/Home.md` and `wiki/_Sidebar.md` contain links to required canonical wiki pages
- internal wiki links resolve
- drift signal when canonical docs/specs/governance/agent surfaces change without a wiki update
- required Wiki sync check on pull requests and wiki publication on `push` to `main`

### 8. Docs Maintenance Agent

**Workflow:** `.github/workflows/docs-maintenance-agent.yml`
**Script:** `.github/scripts/docs_maintenance_check.py`
**Behavior:** blocking on hard violations; drift notices remain warnings.
**Triggers:** every `push` and `pull_request` on any branch.

Checks:

- required canonical docs/governance/handoff files exist and are non-empty
- required headings remain present in key canonical documents
- README baseline markers and repository-map path references remain valid
- internal markdown links across README/docs/governance/handoff/wiki resolve
- drift signal when canonical docs/specs change without a README update

## Rollout state

Critical sentinel workflows run blocking in protected-branch operation. `REPORT_ONLY` is retained only as a local diagnostic switch inside the Python helpers.

- `REPORT_ONLY="1"` prints full findings but exits successfully
- `REPORT_ONLY="0"` makes the workflow blocking

Protected branch rulesets must require the blocking sentinel checks, Gate Integrity, CODEOWNER review, latest-push approval, and no bypass actors before product completion branches are created.
