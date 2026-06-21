# Canonical Math Baseline

This page summarizes the canonical research-aligned math baseline used by the ASH Pattern System.

## Core Definitions

| Concept | Canonical definition |
|---|---|
| State space | `F2^9` (full 9-bit binary space, 512 states) |
| State vector | `(b0..b8)` with each `bi in F2` |
| Canonical transform | `x' = x XOR c`, `c in C subset F2^9` |
| Codeword set size | 16 members |
| Code parameters | `[9, 4, 4]` doubly-even linear code |
| Averaging operator | `T f(x) = (1/|C|) Σ_{c ∈ C} f(x ⊕ c)` |
| Averaging property | `T^2 = T` (idempotent projection) |
| Branching status | First-class canonical capability |

## Codeword Set Overview

The canonical codeword set `C` is fully closed and fixed.

- Size: 16 codewords
- Construction: XOR-closure of 4 independent generators (the spec lists 6 basis-reference vectors; rank 4, since `g5 = g1 ⊕ g6`)
- Weight distribution: `{0: 1, 4: 14, 8: 1}`
- Orbit count: `512 / 16 = 32`
- Ninth coordinate: every codeword has `b8 = 0` (weight 0 in the ninth coordinate) — a structural property of the code, not a derived/parity bit; all nine coordinates remain equal participants, so invariant #2 ("no coordinate is foundationally privileged") still holds

Branching is a first-class canonical capability: the canonical topology is a structural, full ordered ternary tree of nodes and paths. The core tree does not by itself mutate ASH states or apply codeword transitions; assigning states to branches is optional profile behavior (a `BranchStateAssignmentProfile`) in which every edge must name an explicit canonical transition (`specs/algorithms/branching-semantics.pseudo.md`).

Reference: `specs/core/codeword-set.pseudo.md`

## Critical Invariants

1. Full 9-coordinate processing is required.
2. No coordinate is foundationally privileged.
3. Transforms are deterministic and pure.
4. Same codeword applied twice returns original state.
5. The codeword set is fixed and non-extensible.

## Boundary Rule

Canonical processing uses the full 9-bit model throughout. No alternate foundational decomposition may replace the `F2^9` baseline.

## Related Pages

- [Specification Layers](Specification-Layers)
- [Recovery and Safety Semantics](Recovery-and-Safety-Semantics)
- [Contracts and Verification](Contracts-and-Verification)
