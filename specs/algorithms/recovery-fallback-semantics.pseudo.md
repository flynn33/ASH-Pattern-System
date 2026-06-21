# Recovery and Fallback Semantics — canonical specification (1.0 release candidate)

## Purpose

This specification defines deterministic correction, fallback replacement, containment escalation, and diagnostic requirements.

Correction and fallback are separate operations:

- correction applies one canonical codeword inside the current orbit;
- fallback replacement is an authorized policy action that may replace the state across orbits;
- containment escalation does not replace state.

## Correction attempt flow

`APPLY_CORRECTION` is permitted only for `CORRECTABLE` assessments.

```text
FUNCTION apply_correction(assessment: StateAssessment) -> RecoveryResult
    REQUIRE assessment.class == CORRECTABLE
    REQUIRE assessment.selected_target is not NONE
    REQUIRE assessment.correction_codeword_id is not NONE

    current = assessment.state
    target = assessment.selected_target
    delta = current.state_signature ⊕ target.state_signature

    IF delta ∉ C THEN
        RETURN recovery_failure("correction codeword is not canonical")
    END IF

    corrected = transform_state(current, delta)

    IF corrected.state_signature != target.state_signature THEN
        RETURN recovery_failure("correction target mismatch")
    END IF

    RETURN RecoveryResult(
        recovery_category = APPLY_CORRECTION,
        outcome = RECOVERED,
        original_state = current,
        target_state = target,
        codeword_id = codeword_id(delta),
        diagnostic_chain = correction_diagnostics(assessment, corrected)
    )
END FUNCTION
```

The correction result must record current state, target state, codeword ID, policy decision, pre-diagnostic, post-diagnostic, and outcome.

## Target-resolution flow

`TARGET_RESOLUTION_REQUIRED` is not a mutation category. The implementation must wait for a validated policy or context change that selects one target, or classify the condition as degraded if candidates become invalid.

## Fallback selection flow

Fallback selection applies to `FALLBACK_REQUIRED`.

```text
FUNCTION select_fallback(assessment: StateAssessment, instance: FallbackPolicyInstance) -> RecoveryResult
    IF instance is invalid THEN
        RETURN containment_escalation("fallback policy instance invalid")
    END IF

    candidates = evaluate_fallback_candidates(assessment, instance)

    IF candidates is empty THEN
        RETURN containment_escalation("no fallback candidate available")
    END IF

    selected = first_candidate_by_policy_order(candidates)
    reassessment = assess_state(selected.state, assessment.operational_context)

    IF reassessment.class not in [STABLE, CORRECTABLE, UNSTABLE] THEN
        RETURN containment_escalation("fallback candidate failed immediate reassessment")
    END IF

    RETURN RecoveryResult(
        recovery_category = FALLBACK_REQUIRED,
        outcome = RECOVERED_VIA_FALLBACK_REPLACEMENT,
        original_state = assessment.state,
        replacement_state = selected.state,
        fallback_policy_id = selected.policy_id,
        diagnostic_chain = fallback_diagnostics(assessment, selected, reassessment)
    )
END FUNCTION
```

A cross-orbit replacement must be labeled `RECOVERED_VIA_FALLBACK_REPLACEMENT`. It must never be presented as XOR-by-codeword motion.

## Canonical fallback definitions

The canonical fallback-policy definition registry contains:

| Policy ID | Name | Selection order |
|---|---|---|
| `FALLBACK-STATE-001` | Declared Known-Good | configured rank, then realm ID |
| `FALLBACK-STATE-002` | Last Verified Stable | highest verification sequence, then realm ID |
| `FALLBACK-STATE-999` | Containment Escalation | no replacement |

Concrete candidate states and evidence are supplied by downstream policy instances. APS validates the instance and selection rule; it does not invent domain-safe states.

## Recovery result

```text
TYPE RecoveryResult
    recovery_category       : RecoveryCategory
    outcome                 : RecoveryOutcome
    original_state          : AshState
    target_state            : AshState or NONE
    replacement_state       : AshState or NONE
    codeword_id             : String or NONE
    fallback_policy_id      : String or NONE
    diagnostic_chain        : List of DiagnosticEnvelope
END TYPE

ENUM RecoveryOutcome
    RECOVERED
    RECOVERED_VIA_FALLBACK_REPLACEMENT
    TARGET_RESOLUTION_BLOCKED
    RECOVERY_FAILED
    ESCALATE_TO_CONTAINMENT
    NOT_APPLICABLE
END ENUM
```

## No silent recovery

Every correction, fallback replacement, containment escalation, failed attempt, and blocked action must produce a diagnostic chain. No state mutation may occur without an explicit result record.

## Prohibition on heuristic selection

When a validated policy is absent, the system must escalate to containment. It must not use random, nearest-neighbor, most-common, recently seen, or undocumented selection.

## Relation to other specifications

- **system-state-classification.pseudo.md** — provides `StateAssessment`.
- **recoverability-semantics.pseudo.md** — maps classes to recovery categories.
- **containment-safe-failure-semantics.pseudo.md** — handles containment and safe halt.
- **state-validity-diagnostics.pseudo.md** — provides diagnostic envelopes.
- **codeword-set.pseudo.md** — provides the codeword structure used for correction.
- **fallback-policy-registry.md** — defines fallback policy definitions and instance requirements.
