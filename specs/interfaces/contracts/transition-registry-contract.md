# TransitionRegistry Contract — implementation contract

## Purpose

The `TransitionRegistry` module resolves and applies state transitions deterministically. It operates exclusively on normalized states and preserves the locked core/control semantics through every transition.

## Canonical responsibility

The `TransitionRegistry` module is the single authority for:

- resolving which transitions are available for a given normalized state
- applying a selected transition to produce a new normalized state
- preserving the rule that ordinary transitions operate on the core and then re-derive the control bit

## Required inputs

- A normalized `AshState`
- A transition identifier or transition request

## Required outputs

- A new normalized `AshState` (the result of applying the transition)
- Transition diagnostics when resolution or application fails

## Required behaviors

### Deterministic resolution
- Transition resolution must be deterministic — the same state and transition identifier always resolve to the same outcome
- The set of available transitions for a given state must be deterministic

### Normalized-state requirement
- Transitions must only be applied to normalized states
- If a non-normalized state is provided, the registry must fail with a diagnostic
- The registry must not attempt normalization itself — that is the responsibility of `StateModel`

### Core/control preservation
- Ordinary transitions operate on the 8-bit stabilizing core
- After modifying the core, the control bit must be re-derived using the locked parity formula
- The transition must not directly mutate the control bit as an independent coordinate
- The result of a transition must be a valid normalized state

## Required diagnostics

- If transition resolution fails (e.g., unknown identifier, inapplicable transition), produce a diagnostic conforming to `diagnostic-schema.md`
- Rule IDs must conform to `rule-id-taxonomy.md`

## Invariants

1. Transition resolution is deterministic
2. Transition application produces a normalized state
3. The control bit is always re-derived after core modification
4. No direct mutation of the control bit during ordinary transitions

## Prohibited shortcuts

- Must not apply transitions to unnormalized states
- Must not directly mutate the control bit outside of re-derivation
- Must not skip re-derivation after core modification
- Must not silently drop a failed transition

## Relation to other contracts and specifications

- `state-model-contract.md` — provides normalized states consumed by TransitionRegistry
- `transition-system.pseudo.md` — transition semantics
- `ash-state-space.pseudo.md` — canonical state definition
- `control-bit-derivation.pseudo.md` — locked parity formula for re-derivation
- `diagnostics-module-contract.md` — schema and taxonomy conformance requirements
