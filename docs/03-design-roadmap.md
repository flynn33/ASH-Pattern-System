# Design Roadmap

## Goal

Keep every repository surface aligned to the ASH Model source of truth so that the canonical repository, its governance agents, its wiki, and its downstream handoff material all describe the same math and semantics.

## Research math realignment sequence

### 1. Source grounding

The baseline comes from the ASH Model source materials captured in this repository's canonical specs:

- full state space `F2^9`
- fixed 16-member codeword set `C ⊂ F2^9`
- XOR-by-codeword transition semantics
- averaging operator with `T² = T`
- first-class branching semantics

`specs/core/codeword-set.pseudo.md` is the main source-grounding bridge: it traces the canonical codeword set back to the ASH Model simulation vectors and research-paper statements.

### 2. Core and algorithm alignment

The core and algorithm specifications must remain direct expressions of the source-of-truth math:

- `specs/core/*`
- `specs/algorithms/*`
- `specs/registries/*`

No alternate foundational state model may be introduced in these files.

### 3. Contract and verification alignment

The downstream-facing proof layer must match the same baseline exactly:

- `specs/interfaces/*`
- `specs/verification/*`

Contracts, diagnostics, taxonomy, and acceptance language must all preserve the same canonical state and transition semantics.

### 4. Governance and agent alignment

Repository governance, GitHub agents, and maintenance checks must enforce the current baseline rather than narrate older repository history:

- `governance/*`
- `.github/workflows/*`
- `.github/scripts/*`

### 5. Downstream delivery alignment

Secondary delivery surfaces must stay subordinate to the canonical specs while remaining useful:

- `handoff-templates/*`
- `wiki/*`

These files should summarize, enforce, or operationalize the canonical baseline without redefining it.

## Main-repository closeout

The main repository remains the canonical baseline and stays in maintenance mode.

Future work in this repository is limited to:

- source-grounded semantic corrections
- clarity improvements across docs, governance, and wiki
- stronger contract and verification alignment
- GitHub agent and maintenance-rule improvements

Platform implementations, build outputs, and runtime packaging remain downstream concerns.
