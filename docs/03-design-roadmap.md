# Design Roadmap

## Goal

Move from a corrected semantic baseline to implementation-ready handoff materials without collapsing the design into any single language or platform.

## Sequence

### Phase 1 — lock the semantic foundation

Complete and stabilize:

- ASH state-space specification
- realm identity specification
- transition semantics
- topology expansion semantics
- axiom evaluation semantics
- generation-planning semantics

### Phase 2 — lock the implementation contracts

Define the exact capabilities that any implementation must expose, including:

- state normalization
- control derivation
- transition application
- topology generation
- axiom diagnostics
- generation planning
- artifact materialization boundary

### Phase 3 — define invariant-based verification requirements

Describe what downstream test suites must prove, including:

- deterministic normalization
- deterministic realm encoding
- no uncontrolled mutation of the control dimension
- deterministic transition outcomes
- deterministic topology expansion
- stable axiom diagnostics
- stable generation-plan structure

### Phase 4 — create platform build handoff packages

For each target implementation repo, the coding agent should receive:

- this repository
- target platform constraints
- target language constraints
- runtime constraints
- packaging constraints
- performance constraints if applicable

## Immediate next design step

The next design step is to treat the files in `specs/` and `governance/` as the canonical handoff baseline for the first implementation repository.
