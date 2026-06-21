# Design Philosophy

## Primary principle

The ASH Pattern System must be specified in terms of **semantic invariants**, not implementation accidents.

## Governing ideas

### 1. State before platform

The ASH state model is the root layer.
Platform behavior, tooling, and materialization must be downstream of that state model.

### 2. Semantics before syntax

The repository defines what operations mean.
It does not define the syntax a language must use to express them.

### 3. Planning before side effects

The engine must first produce an abstract, inspectable generation plan.
Only then may a downstream adapter materialize files, modules, services, views, or packages.

### 4. Full-state semantics, not arbitrary mutation

All 9 coordinates participate in the canonical state model.
Ordinary transitions operate on the full 9-bit state via XOR-by-codeword.

Participating in the state model is distinct from being flipped by a transition: every canonical codeword has weight zero in the ninth coordinate, so XOR-by-codeword transitions leave `b8` unchanged. This is a structural property of the canonical code, not a coordinate-derivation rule — all nine coordinates remain equal participants in state representation, realm identity, and averaging. See [`codeword-set.pseudo.md`](../specs/core/codeword-set.pseudo.md).

### 5. Stabilization is part of the model

The full 9-bit state is not just a convenient storage layout.
It is the stabilizing algebraic substrate of the ASH state model.

This stabilization is formalized by the idempotent averaging operator (`T² = T`); see [`averaging-operator-semantics.pseudo.md`](../specs/algorithms/averaging-operator-semantics.pseudo.md).

### 6. Determinism matters

Equal inputs must produce equal semantic outputs for:

- normalization
- realm identity
- transition application
- topology expansion
- axiom diagnosis
- generation planning

### 7. Explanation matters

The engine should expose diagnostics that explain:

- why a state is valid or invalid
- why a transition is allowed or rejected
- why an axiom passes or fails
- why a plan is acceptable or unstable

### 8. Implementations are replaceable

No single language implementation should become the identity of the engine.
The engine must be portable by design.

## Design test

A design decision is aligned only if it preserves the semantic model while leaving room for multiple correct implementations.
