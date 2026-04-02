# Realm Identity — agnostic specification

## Purpose

Realm identity is the stable semantic encoding of an ASH state.
It provides a deterministic identifier for a normalized state.

## Inputs

Realm identity is derived from a **normalized** ASH state.

That means realm encoding always operates on:

- stabilized 8-bit core
- derived control bit

## Realm record

```text
TYPE RealmIdentity
    core_signature: String
    control_signature: String
    combined_id: String
END TYPE
```

## Semantic rule

The same normalized ASH state must always yield the same realm identity.
Different normalized states must yield different realm identities unless the engine deliberately defines an equivalence relation that merges them.

## Pseudocode

```text
FUNCTION encode_realm_identity(state: AshState) -> RealmIdentity
    normalized = normalize_state(state)

    realm.core_signature = encode_core_signature(normalized.core_bits)
    realm.control_signature = encode_control_signature(normalized.control_bit)
    realm.combined_id = combine_realm_parts(
        realm.core_signature,
        realm.control_signature
    )

    RETURN realm
END FUNCTION
```

## Notes

This specification intentionally leaves the external string format open.
A downstream implementation may use different formatting conventions so long as the mapping remains deterministic and semantically faithful.

## Required invariants

1. equal normalized states yield equal realm identities
2. realm identity is computed from normalized state, not raw input shape
3. the control dimension is represented explicitly in the realm identity model
