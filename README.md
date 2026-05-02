# ASH Pattern System

This repository is the platform-neutral specification baseline for the ASH Pattern System, grounded in the ASH Model's full 9-bit state space `F2^9`.

## Scope

The repository defines:

- the canonical ASH state space and codeword set `C ⊂ F2^9`
- XOR-by-codeword transitions, averaging behavior, branching, topology expansion, and realm identity
- state admissibility, diagnostics, classification, recoverability, fallback, containment, and safe halt
- contracts, schema, taxonomy, and verification requirements for conformant implementations

The repository does not contain:

- delivery scaffolding that is not part of the canonical specification
- GitHub agent governance packages or workflow automation
- platform-specific implementation code
- legacy pre-remediation specifications

## Canonical baseline

- State space: `F2^9` with 512 states.
- Transformations: `x' = x ⊕ c` for `c ∈ C`.
- Codeword set: fixed 16-member `[9, 4, 4]` code defined in `specs/core/codeword-set.pseudo.md`.
- Recovery and safety behavior is defined on full 9-bit states.

## Repository map

- `docs/00-repository-purpose.md` — repository role and boundaries
- `docs/01-design-philosophy.md` — governing design principles
- `governance/repository-governance.md` — repository rules for current canonical content
- `specs/core/` — state, codeword, diagnostic, classification, recovery, and identity specifications
- `specs/algorithms/` — transformation, averaging, branching, recovery, containment, topology, and planning semantics
- `specs/registries/` — canonical fallback policy registry
- `specs/interfaces/` — contracts, diagnostic schema, and rule-ID taxonomy
- `specs/verification/` — invariants, conformance categories, and acceptance requirements

## Repository rule

If an implementation disagrees with this repository, the specification here wins. The math and semantics in this repository must remain aligned with the ASH Model baseline.
