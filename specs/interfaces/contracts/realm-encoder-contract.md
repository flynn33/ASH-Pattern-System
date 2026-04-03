# RealmEncoder Contract — implementation contract

## Purpose

The `RealmEncoder` module encodes realm identity from a normalized ASH state. It translates the algebraic state representation into a realm-level identity that preserves the semantic structure of the state model.

## Canonical responsibility

The `RealmEncoder` module is the single authority for:

- encoding realm identity from a normalized ASH state
- producing deterministic, reproducible realm encodings
- preserving the semantic distinction between core and control dimensions in the encoded output

## Required inputs

- A normalized `AshState` (must be valid — admissible core, correctly derived control bit)

## Required outputs

- A deterministic realm identity encoding

## Required behaviors

### Deterministic encoding
- The same normalized state must always produce the same realm encoding
- Encoding must be reproducible across platforms, implementations, and execution contexts

### Normalized-state requirement
- The encoder must only accept normalized states as input
- If an unnormalized or invalid state is provided, the encoder must fail with a diagnostic rather than silently produce a potentially incorrect encoding
- The encoder must not attempt normalization itself — that is the responsibility of `StateModel`

### Control semantics preservation
- The encoded output must preserve the semantic distinction between the 8-bit stabilizing core and the derived control dimension
- The encoding must not collapse the core/control distinction

## Required diagnostics

- If encoding fails (e.g., invalid input state), produce a diagnostic conforming to `diagnostic-schema.md`
- Rule IDs must conform to `rule-id-taxonomy.md`

## Invariants

1. Encoding is deterministic — equal inputs produce equal outputs
2. Encoding operates only on normalized states
3. The core/control semantic distinction is preserved in the encoding

## Prohibited shortcuts

- Must not encode from an unnormalized or invalid state
- Must not collapse the core/control distinction in the encoding
- Must not silently produce a default encoding when input is invalid

## Relation to other contracts and specifications

- `state-model-contract.md` — provides normalized states consumed by RealmEncoder
- `realm-identity.pseudo.md` — realm identity and encoding semantics
- `ash-state-space.pseudo.md` — canonical state definition
- `diagnostics-module-contract.md` — schema and taxonomy conformance requirements
