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

### 5. Stabilization is part of the model

The full 9-bit state is not just a convenient storage layout.
It is the stabilizing algebraic substrate of the ASH state model.

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
