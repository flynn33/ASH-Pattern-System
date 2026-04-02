# Transition System — agnostic specification

## Purpose

The transition system defines how an ASH state evolves while preserving the corrected distinction between:

- the 8-bit stabilizing core
- the derived control/parity dimension

## Transition model

A transition acts primarily on the **core state**.
After the transition is applied, the control dimension is re-derived.

## Canonical transition record

```text
TYPE TransitionDefinition
    transition_id: String
    display_name: String
    description: String
    core_transform: Function
    applicability_rule: Function
END TYPE
```

## Canonical transition registry

```text
TYPE TransitionRegistry
    ordered_transitions: List<TransitionDefinition>
END TYPE
```

## Application rule

1. normalize input state
2. check applicability of requested transition
3. apply the transition to the 8-bit core
4. re-derive the control bit from the transformed core
5. return normalized transformed state

## Pseudocode

```text
FUNCTION apply_transition(state: AshState, transition: TransitionDefinition) -> AshState
    normalized = normalize_state(state)

    IF transition.applicability_rule(normalized) == false THEN
        RAISE TransitionNotApplicable
    END IF

    transformed_core = transition.core_transform(normalized.core_bits)
    result = make_state(transformed_core)
    RETURN result
END FUNCTION
```

```text
FUNCTION apply_transition_chain(state: AshState, transitions: List<TransitionDefinition>) -> AshState
    current = normalize_state(state)
    FOR each transition IN transitions
        current = apply_transition(current, transition)
    END FOR
    RETURN current
END FUNCTION
```

## Key rule

The transition definition may not treat the 9th coordinate as an unrestricted peer bit under ordinary evolution.
The control bit must be obtained by derivation unless the engine later defines a special class of meta-transition with explicit justification.

## Required invariants

1. equal input state + equal transition => equal output state
2. transitions operate on normalized states
3. control bit is re-derived after core transformation
4. failed applicability checks return explainable diagnostics
