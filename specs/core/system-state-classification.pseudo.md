# System-State Classification — canonical specification (1.0 release candidate)

## Purpose

This specification defines operational state classes for a well-formed ASH state under a validated operational context.

Classification is not a property of a state in isolation. It requires a `StateAssessment` that includes structural state, orbit identity, operational context, candidate stable targets, policy decision, and runtime mode.

Malformed input does not receive a system-state class. It receives an input-validation diagnostic and a blocked assessment.

## Operational context

```text
TYPE OperationalContext
    context_id                 : String
    context_version            : String
    allowed_stable_states      : List of StateSignature
    preferred_state            : StateSignature or NONE
    fallback_policy_instance   : FallbackPolicyInstance
    propagation_risk_policy    : PropagationRiskPolicy
    containment_policy         : ContainmentPolicy
    halt_policy                : HaltPolicy
    registry_versions          : RegistryVersionSet
END TYPE
```

The context must validate before classification. Empty stable sets, incompatible registry versions, contradictory policies, or missing fallback instances fail closed.

## State assessment

```text
TYPE StateAssessment
    state                   : AshState
    operational_context_id  : String
    candidate_targets       : List of AshState
    selected_target         : AshState or NONE
    correction_codeword_id  : String or NONE
    runtime_mode            : RuntimeMode
    class                   : SystemStateClass
    diagnostics             : List of DiagnosticReference
END TYPE
```

## Canonical state classes

```text
ENUM SystemStateClass
    STABLE
    UNSTABLE
    CORRECTABLE
    DEGRADED
    CONTAINED
    FAILED
    SAFE_HALT
END ENUM
```

### STABLE

- State is well formed.
- State is in `allowed_stable_states`.
- Runtime mode is not contained, failed, or halted.

### UNSTABLE

- State is well formed.
- State is not stable.
- One or more same-orbit stable candidates exist.
- Policy cannot select exactly one target.
- No automatic mutation is permitted.

### CORRECTABLE

- State is well formed.
- State is not stable.
- A unique policy-selected stable target exists in the same orbit.
- `current ⊕ target` is in `C` and names the correction codeword.

### DEGRADED

- State is well formed.
- No same-orbit stable target is available, or a correction attempt failed validation.
- Fallback policy must decide whether an authorized replacement or containment escalation is available.

### CONTAINED

- Containment mode has been deliberately entered.
- Only policy-declared restricted operations are allowed.
- Entry and resolution attempts are diagnosed.

### FAILED

- Automated correction and fallback are unavailable or exhausted.
- Normal operations are prohibited.
- The process may remain running only to preserve diagnostics and await external authority.

### SAFE_HALT

- Deliberate terminal state.
- No transition, recovery mutation, fallback, or de-escalation is permitted.
- Diagnostic chain is frozen and exportable.

## Pseudocode

```text
FUNCTION classify_system_state(normalized: NormalizedInput, context: OperationalContext, runtime: RuntimeMode) -> StateAssessment
    IF normalized.input_status == MALFORMED THEN
        RETURN blocked_assessment("malformed input has no system-state class")
    END IF

    validated_context = validate_operational_context(context)
    IF validated_context is invalid THEN
        RETURN blocked_assessment("invalid operational context")
    END IF

    IF runtime.is_in_safe_halt THEN
        RETURN assessment(class = SAFE_HALT)
    END IF

    IF runtime.is_in_containment THEN
        RETURN assessment(class = CONTAINED)
    END IF

    current = normalized.state

    IF current.state_signature IN validated_context.allowed_stable_states THEN
        RETURN assessment(class = STABLE)
    END IF

    same_orbit_targets = [
        target FOR target IN validated_context.allowed_stable_states
        WHERE evaluate_reachability(current, target, C).status == REACHABLE
    ]

    IF same_orbit_targets is empty THEN
        RETURN assessment(class = DEGRADED)
    END IF

    selected = apply_target_policy(current, same_orbit_targets, validated_context)

    IF selected is NONE THEN
        RETURN assessment(class = UNSTABLE, candidate_targets = same_orbit_targets)
    END IF

    delta = current.state_signature ⊕ selected.state_signature
    IF delta ∈ C THEN
        RETURN assessment(
            class = CORRECTABLE,
            selected_target = selected,
            correction_codeword_id = codeword_id(delta)
        )
    END IF

    RETURN assessment(class = DEGRADED)
END FUNCTION
```

## Invariants

1. Classification is total for well-formed states under valid context and runtime mode.
2. Classes are non-overlapping.
3. Structural normalization never changes the class by mutating the state.
4. `CORRECTABLE` always names one same-orbit target and one codeword.
5. Cross-orbit fallback is never classified as a codeword transition.
6. `SAFE_HALT` is terminal inside APS semantics.

## Relation to other specifications

- **state-validity-diagnostics.pseudo.md** — provides structural diagnostics.
- **state-admissibility.pseudo.md** — defines reachability and orbit identity.
- **recoverability-semantics.pseudo.md** — maps classes to recovery categories.
- **recovery-fallback-semantics.pseudo.md** — defines correction and fallback behavior.
- **containment-safe-failure-semantics.pseudo.md** — defines containment and safe halt.
