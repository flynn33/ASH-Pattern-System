# State Admissibility — canonical specification (1.0 release candidate)

## Purpose

This specification separates structural state validity from operational health.

An ASH candidate has three distinct evaluation layers:

1. input well-formedness;
2. canonical orbit identity and pairwise reachability;
3. operational assessment under an explicit context.

The canonical state space remains `F2^9`. Every well-formed nine-bit value is a realm. No well-formed state is outside the orbit partition.

## Candidate input status

```text
ENUM InputStatus
    WELL_FORMED
    MALFORMED
END ENUM
```

`WELL_FORMED` means the candidate is exactly nine binary values in `b0` through `b8` order.

`MALFORMED` means the candidate cannot be represented as an ASH state without losing information. Malformed input is an input-validation failure, not an invalid realm.

## Canonical state record

```text
TYPE AshState
    bits            : Vector[9] over F2
    state_signature : String matching ^[01]{9}$
    realm_index     : Integer 0..511
    realm_id        : String matching ^APS-REALM-[0-9]{3}$
    orbit_id        : String matching ^APS-ORBIT-[0-9]{2}$
END TYPE
```

For integer conversion, `b0` is the most significant bit and `b8` is the least significant bit:

```text
state_index = sum(bi * 2^(8-i)) for i = 0..8
realm_id = "APS-REALM-" + zero_pad(state_index, 3)
```

## Orbit identity

For every well-formed state `x`:

```text
Orbit(x) = { x ⊕ c : c ∈ C }
```

The canonical codeword set `C` is a subgroup. Its orbits partition all 512 states into 32 disjoint orbits of 16 members each.

The canonical orbit representative is the lexicographically smallest state signature in the orbit. Orbit representatives are sorted lexicographically and assigned:

```text
APS-ORBIT-00 through APS-ORBIT-31
```

## Pairwise reachability

Reachability is a relation between two well-formed states, not an intrinsic property of one state.

```text
reachable(source, target) iff (source ⊕ target) ∈ C
```

Equivalent rule:

```text
reachable(source, target) iff orbit_id(source) == orbit_id(target)
```

If reachable, the unique one-step codeword is:

```text
delta = source ⊕ target
```

## Admissibility statuses

```text
ENUM AdmissibilityStatus
    WELL_FORMED_REALM
    MALFORMED_INPUT
END ENUM
```

`WELL_FORMED_REALM` means the candidate is a valid element of `F2^9`, has one realm ID, and has one orbit ID.

`MALFORMED_INPUT` means parsing failed before a state existed.

## Reachability statuses

```text
ENUM ReachabilityStatus
    REACHABLE
    NOT_REACHABLE
    MALFORMED_INPUT
END ENUM
```

`NOT_REACHABLE` means two well-formed states belong to different orbits. It does not mean either state is invalid.

## Structural normalization

Structural normalization only parses and canonicalizes representation:

1. parse the candidate;
2. verify exactly nine binary values;
3. emit canonical bit-vector, signature, realm, and orbit fields;
4. preserve every bit.

Structural normalization never changes a realm, selects an operational target, applies a codeword, or performs fallback.

## Pseudocode

```text
FUNCTION normalize_state(candidate) -> NormalizedInput
    IF candidate is not exactly nine binary values THEN
        RETURN {
            input_status: MALFORMED,
            diagnostic_kind: INPUT_VALIDATION,
            state: NONE
        }
    END IF

    state_signature = canonical_nine_bit_signature(candidate)
    state_index = binary_to_integer(state_signature)
    orbit = compute_orbit_identity(state_signature, C)

    RETURN {
        input_status: WELL_FORMED,
        state: AshState(
            bits = candidate bits in b0..b8 order,
            state_signature = state_signature,
            realm_index = state_index,
            realm_id = "APS-REALM-" + zero_pad(state_index, 3),
            orbit_id = orbit.orbit_id
        )
    }
END FUNCTION
```

```text
FUNCTION classify_state_admissibility(candidate, codeword_set C) -> AdmissibilityStatus
    normalized = normalize_state(candidate)

    IF normalized.input_status == MALFORMED THEN
        RETURN MALFORMED_INPUT
    END IF

    RETURN WELL_FORMED_REALM
END FUNCTION
```

```text
FUNCTION evaluate_reachability(source_candidate, target_candidate, codeword_set C) -> ReachabilityResult
    source = normalize_state(source_candidate)
    target = normalize_state(target_candidate)

    IF source.input_status == MALFORMED OR target.input_status == MALFORMED THEN
        RETURN { status: MALFORMED_INPUT, delta_codeword_id: NONE }
    END IF

    delta = source.state.state_signature ⊕ target.state.state_signature

    IF delta ∈ C THEN
        RETURN {
            status: REACHABLE,
            delta_signature: delta,
            codeword_id: codeword_id(delta)
        }
    END IF

    RETURN { status: NOT_REACHABLE, delta_signature: delta, codeword_id: NONE }
END FUNCTION
```

## Relation to operational health

Operational health is not determined by state membership in `F2^9`. A well-formed state becomes `STABLE`, `UNSTABLE`, `CORRECTABLE`, `DEGRADED`, `CONTAINED`, `FAILED`, or `SAFE_HALT` only through `StateAssessment` under a validated `OperationalContext`.

## Invariants

1. Every well-formed nine-bit vector maps to one realm ID.
2. Every well-formed nine-bit vector maps to one orbit ID.
3. The 32 orbits are disjoint and cover all 512 states.
4. Pairwise reachability is exact codeword-difference membership.
5. Structural normalization is realm-preserving.
6. Malformed input is reported before realm, orbit, or reachability evaluation.

## Relation to other specifications

- **codeword-set.pseudo.md** — defines the codeword set `C`.
- **ash-state-space.pseudo.md** — defines the `F2^9` state space.
- **state-validity-diagnostics.pseudo.md** — emits normalized-input and reachability diagnostics.
- **system-state-classification.pseudo.md** — defines operational assessment under context.
- **recoverability-semantics.pseudo.md** — maps operational classes to recovery categories.
