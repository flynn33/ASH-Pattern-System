# Recovery and Fallback Semantics — agnostic specification

## Purpose

This specification defines the **algorithmic semantics of deterministic recovery and fallback selection** for the ASH Pattern System.

The ASH Pattern System is designed for self-healing, self-correcting, safe-failure, and fallback software. This file specifies how recovery actions are carried out once a system-state classification and recoverability category have been determined.

Every recovery action must be:

- **Deterministic** — the same inputs produce the same recovery outcome
- **Diagnosable** — every step emits diagnostic information explaining what was done and why
- **Policy-driven** — fallback selection is governed by a canonical policy registry, not by heuristic guessing

## Correction attempt flow

When the recovery category is `CORRECT_AND_RE_DERIVE` (for `CORRECTABLE` states) or `RE_DERIVE_CONTROL` (for `UNSTABLE` states), the system attempts deterministic correction.

```text
FUNCTION attempt_recovery(diagnostic: StateValidityDiagnostic, state_class: SystemStateClass) -> RecoveryResult
    result = new RecoveryResult()
    result.original_diagnostic = diagnostic
    result.recovery_category = classify_recoverability(state_class)
    result.steps = []

    SWITCH result.recovery_category

        CASE RE_DERIVE_CONTROL:
            -- Core is admissible; only control bit needs re-derivation
            IF NOT derivation_formula_is_locked() THEN
                result.outcome = BLOCKED
                result.reason = "Derivation formula not locked"
                result.steps.append(step("re-derive-control", BLOCKED, "derivation formula unavailable"))
                RETURN result
            END IF

            new_control = derive_control_bit(diagnostic.extracted_core)
            result.corrected_state = AshState(core_bits = diagnostic.extracted_core, control_bit = new_control)
            result.steps.append(step("re-derive-control", COMPLETED, "control re-derived from admissible core"))
            result.outcome = RECOVERED

        CASE CORRECT_AND_RE_DERIVE:
            -- Core is inadmissible but correctable
            IF NOT admissibility_law_is_locked() THEN
                result.outcome = BLOCKED
                result.reason = "Admissibility law not locked"
                result.steps.append(step("correct-core", BLOCKED, "codeword set unavailable"))
                RETURN result
            END IF

            corrected_core = correct_to_nearest_codeword(diagnostic.extracted_core)
            result.steps.append(step("correct-core", COMPLETED,
                "core corrected from " + diagnostic.extracted_core + " to " + corrected_core))

            IF NOT derivation_formula_is_locked() THEN
                result.outcome = BLOCKED
                result.reason = "Derivation formula not locked after core correction"
                result.steps.append(step("re-derive-control", BLOCKED, "derivation formula unavailable"))
                RETURN result
            END IF

            -- Corrected-core derivation rule: derive from corrected core
            new_control = derive_control_bit(corrected_core)
            result.corrected_state = AshState(core_bits = corrected_core, control_bit = new_control)
            result.steps.append(step("re-derive-control", COMPLETED,
                "control derived from corrected admissible core"))
            result.outcome = RECOVERED

        CASE FALLBACK_REQUIRED:
            result = select_fallback(diagnostic, result)
            RETURN result

        OTHERWISE:
            -- NO_ACTION, CONTAINMENT_REQUIRED, ESCALATION_REQUIRED, TERMINAL_NO_RECOVERY
            -- These are handled by other specifications
            result.outcome = NOT_APPLICABLE
            result.reason = "Recovery category handled by another specification"
            RETURN result

    END SWITCH

    -- Validate recovered state
    IF result.outcome == RECOVERED THEN
        validation = diagnose_state(result.corrected_state)
        result.steps.append(step("validate-recovery", COMPLETED,
            "post-recovery validation: " + validation.recoverability_status))

        IF validation.recoverability_status != STABLE THEN
            result.outcome = RECOVERY_FAILED
            result.reason = "Recovered state did not classify as STABLE"
            result.steps.append(step("validate-recovery", FAILED,
                "post-recovery state classified as " + validation.recoverability_status))
        END IF
    END IF

    RETURN result
END FUNCTION
```

## Fallback selection flow

When the recovery category is `FALLBACK_REQUIRED` (for `DEGRADED` states), the system must select a known-good state from the fallback-policy registry.

Fallback selection operates against the **canonical fallback-policy registry** (see future `specs/registries/fallback-policy-registry.md`). Ordering is deterministic and fully specified by policy identifiers.

```text
FUNCTION select_fallback(diagnostic: StateValidityDiagnostic, result: RecoveryResult) -> RecoveryResult

    IF NOT fallback_registry_is_available() THEN
        result.outcome = ESCALATE_TO_CONTAINMENT
        result.reason = "No fallback-policy registry available"
        result.steps.append(step("select-fallback", BLOCKED, "fallback registry unavailable"))
        RETURN result
    END IF

    candidates = fallback_registry.get_candidates_for(diagnostic)

    IF candidates is empty THEN
        result.outcome = ESCALATE_TO_CONTAINMENT
        result.reason = "Fallback registry contains no candidates for this state"
        result.steps.append(step("select-fallback", BLOCKED, "no fallback candidates"))
        RETURN result
    END IF

    -- Deterministic ordering: candidates are ordered by policy identifier
    -- The first candidate in policy order is selected
    selected = candidates.first_by_policy_order()

    result.corrected_state = selected.state
    result.fallback_policy_id = selected.policy_id
    result.steps.append(step("select-fallback", COMPLETED,
        "fallback selected: policy=" + selected.policy_id))
    result.outcome = RECOVERED_VIA_FALLBACK

    -- Validate fallback state
    validation = diagnose_state(result.corrected_state)
    result.steps.append(step("validate-fallback", COMPLETED,
        "post-fallback validation: " + validation.recoverability_status))

    IF validation.recoverability_status != STABLE THEN
        result.outcome = ESCALATE_TO_CONTAINMENT
        result.reason = "Fallback state did not classify as STABLE"
        result.steps.append(step("validate-fallback", FAILED,
            "fallback state classified as " + validation.recoverability_status + "; escalating"))
    END IF

    RETURN result
END FUNCTION
```

## Fallback escalation behavior

When fallback fails, the system must escalate:

1. **Primary fallback fails** — the selected fallback state does not classify as `STABLE` after validation
2. **No candidates** — the fallback-policy registry has no candidates for the current state
3. **Registry unavailable** — no fallback-policy registry is configured

In all three cases, the system escalates to `CONTAINMENT_REQUIRED`. The escalation must be recorded in the diagnostic with the reason for escalation.

Escalation is always monotonic in severity: fallback failure never leads to a less severe action than containment.

## Deterministic ordering rules

Fallback selection must obey these ordering rules:

1. **Policy-identifier ordering** — candidates are ordered by their canonical policy identifier, not by recency, frequency, or heuristic score.
2. **Stability preference** — among candidates with the same policy priority, prefer the candidate whose post-selection diagnostic is most likely to classify as `STABLE`.
3. **No randomness** — fallback selection must never involve randomness, shuffling, or probabilistic choice.
4. **No heuristic guessing** — if canonical policy is absent, the system must not guess. It must escalate to containment.

## Prohibition on heuristic guessing

When the canonical fallback-policy registry is absent, empty, or does not contain a candidate for the current state, the system **must not**:

- Invent a fallback state from convenience or local defaults
- Select a "closest" state by heuristic distance
- Use a previously seen state as a fallback without policy backing
- Silently continue in the current degraded state

The system must escalate to containment and produce a diagnostic explaining why fallback was not possible.

## No silent healing

All recovery actions must be diagnosable. The system must not silently mutate its own state without producing an explainable diagnostic record.

Every recovery step must record:

- The action taken
- The input state
- The output state (if recovery succeeded)
- The reason for the action
- Which specification rules were applied

## Minimum diagnostic content for recovery and fallback actions

Every recovery or fallback action must produce a diagnostic record containing at minimum:

```text
TYPE RecoveryDiagnostic
    recovery_category        : RecoveryCategory
    original_state_class     : SystemStateClass
    original_diagnostic      : StateValidityDiagnostic
    steps                    : List of RecoveryStep
    outcome                  : RecoveryOutcome
    corrected_state          : AshState or NONE
    fallback_policy_id       : String or NONE
    reason                   : String
    rule_ids                 : List of String
END TYPE

TYPE RecoveryStep
    action                   : String
    status                   : COMPLETED | BLOCKED | FAILED
    detail                   : String
END TYPE

ENUM RecoveryOutcome
    RECOVERED
    RECOVERED_VIA_FALLBACK
    BLOCKED
    RECOVERY_FAILED
    ESCALATE_TO_CONTAINMENT
    NOT_APPLICABLE
END ENUM
```

## Relation to other specifications

- **system-state-classification.pseudo.md** — provides the `SystemStateClass` that determines recovery category
- **recoverability-semantics.pseudo.md** — provides the `RecoveryCategory` mapping
- **containment-safe-failure-semantics.pseudo.md** — handles escalation when recovery/fallback fails
- **state-validity-diagnostics.pseudo.md** — provides pre-recovery diagnostics and post-recovery validation
- **core-admissibility.pseudo.md** — provides `correct_to_nearest_codeword` for core correction
- **control-bit-derivation.pseudo.md** — provides `derive_control_bit` for control re-derivation

---

## Unresolved closure item — fallback-policy registry

> **STATUS: FUTURE SPECIFICATION REQUIRED**

The fallback-policy registry (`specs/registries/fallback-policy-registry.md`) has not yet been defined. Until it is:

1. Implementations must structure their code so the fallback registry is a replaceable component.
2. Implementations must report `fallback-registry-unavailable` in diagnostics when no registry is configured.
3. Implementations must escalate to containment when the registry is absent.
4. Implementations must not invent a fallback registry or hardcode fallback states.
