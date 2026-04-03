# Recoverability Semantics — agnostic specification

## Purpose

This specification defines the **recoverability layer** of the ASH Pattern System.

Recoverability determines the deterministic mapping from each system-state class to the **allowed recovery category**. It answers: given the current system-state classification, what category of recovery action is permitted, required, or forbidden?

This layer exists because resilient software must not improvise recovery. Every recovery decision must be traceable to a classification, and every classification must map to exactly one recovery category.

## Recovery categories

```text
ENUM RecoveryCategory
    NO_ACTION
    RE_DERIVE_CONTROL
    CORRECT_AND_RE_DERIVE
    FALLBACK_REQUIRED
    CONTAINMENT_REQUIRED
    ESCALATION_REQUIRED
    TERMINAL_NO_RECOVERY
END ENUM
```

### NO_ACTION

- **Applies to**: `STABLE`
- **Meaning**: The system is healthy. No recovery action is needed.
- **Preconditions**: Core is admissible and control bit matches derivation.
- **Postconditions**: System remains in normal operation.

### RE_DERIVE_CONTROL

- **Applies to**: `UNSTABLE`
- **Meaning**: The core is admissible but the control bit is inconsistent. Recovery consists of re-deriving the control bit from the admissible core.
- **Preconditions**: Core admissibility is `ADMISSIBLE`. Input is well-formed.
- **Postconditions**: After re-derivation, the state must classify as `STABLE`. If it does not, the recovery has failed and escalation to `CORRECTABLE` or `DEGRADED` classification is required.
- **Blocked when**: Input is malformed or implementation nonconformance prevents derivation.

### CORRECT_AND_RE_DERIVE

- **Applies to**: `CORRECTABLE`
- **Meaning**: The core is inadmissible but within correctable distance of a valid codeword. Recovery consists of correcting the core to the nearest codeword, then re-deriving the control bit from the **corrected admissible core**.
- **Preconditions**: Core admissibility is `INADMISSIBLE_CORRECTABLE`. Correction function is available. Derivation formula is available.
- **Postconditions**: After correction and re-derivation, the state must classify as `STABLE`. If it does not, the recovery has failed and escalation is required.
- **Blocked when**: Input is malformed or implementation nonconformance prevents correction or derivation.
- **Corrected-core derivation rule**: The expected control dimension is always derived from the corrected admissible core, not from the raw inadmissible core.

### FALLBACK_REQUIRED

- **Applies to**: `DEGRADED`
- **Meaning**: The core is inadmissible and correction is ambiguous. The system must select a known-good fallback state from the fallback-policy registry.
- **Preconditions**: Core admissibility is `INADMISSIBLE_DETECTABLE`. Fallback-policy registry is available and contains at least one candidate.
- **Postconditions**: After fallback, the system must re-classify. If the fallback state is `STABLE`, recovery succeeds. If not, escalation to containment is required.
- **Blocked when**: No fallback-policy registry is available, or the registry contains no candidates. In this case, the system must escalate to containment.
- **Prohibition**: The system must not guess a fallback state. Selection must be deterministic and policy-driven.

### CONTAINMENT_REQUIRED

- **Applies to**: `CONTAINED`
- **Meaning**: The system must restrict operations to prevent error propagation. Containment is a holding state, not a resolution.
- **Preconditions**: Fallback has failed or is unavailable, or propagation risk is detected, or operator/policy has requested containment.
- **Postconditions**: The system operates in a restricted mode. Awaits external decision (operator, policy, or supervisor).
- **Escalation**: If the containment boundary is breached, the system must escalate to `SAFE_HALT`.

### ESCALATION_REQUIRED

- **Applies to**: `FAILED`
- **Meaning**: The core is inadmissible beyond reliable correction. No automated recovery path exists. The system must escalate to an external authority.
- **Preconditions**: Core admissibility is `INADMISSIBLE_UNRECOVERABLE`.
- **Postconditions**: The system remains in `FAILED` state until an external authority resolves the condition. Diagnostic state must be preserved for the authority.
- **Escalation**: The external authority may direct the system to enter `SAFE_HALT`, attempt a full state reset, or take other action outside the scope of the ASH recovery semantics.

### TERMINAL_NO_RECOVERY

- **Applies to**: `SAFE_HALT`
- **Meaning**: The system has already halted in a known-safe terminal state. No further transitions are permitted and no recovery action is pending.
- **Preconditions**: The system has already entered `SAFE_HALT` (via escalation from `FAILED`, containment breach, or explicit operator/policy halt).
- **Postconditions**: The system remains halted. Full diagnostic state is preserved for post-mortem. No further state transitions or recovery actions occur.
- **Finality**: This is the only recovery category that represents a completed terminal state. Unlike other categories, it does not prescribe an action to take — it confirms that the system is already in its final state.

## Deterministic mapping

```text
FUNCTION classify_recoverability(state_class: SystemStateClass) -> RecoveryCategory
    SWITCH state_class
        CASE STABLE:                RETURN NO_ACTION
        CASE UNSTABLE:              RETURN RE_DERIVE_CONTROL
        CASE CORRECTABLE:           RETURN CORRECT_AND_RE_DERIVE
        CASE DEGRADED:              RETURN FALLBACK_REQUIRED
        CASE CONTAINED:             RETURN CONTAINMENT_REQUIRED
        CASE FAILED:                RETURN ESCALATION_REQUIRED
        CASE SAFE_HALT:             RETURN TERMINAL_NO_RECOVERY
    END SWITCH
END FUNCTION
```

This mapping is:
- **Total** — every system-state class has a recovery category
- **Injective** — each class maps to exactly one category
- **Deterministic** — the same class always produces the same category

## Blocked recovery conditions

Recovery may be blocked when required resources are not available:

| Recovery Category | Blocked When | Fallback Behavior |
|---|---|---|
| `RE_DERIVE_CONTROL` | Malformed input or implementation nonconformance | Normalization is `BLOCKED`; system cannot recover |
| `CORRECT_AND_RE_DERIVE` | Malformed input or implementation nonconformance | Normalization is `BLOCKED`; system cannot recover |
| `FALLBACK_REQUIRED` | No fallback-policy registry, or registry is empty | Escalate to `CONTAINMENT_REQUIRED` |
| `CONTAINMENT_REQUIRED` | Containment boundary breached | Escalate to `TERMINAL_NO_RECOVERY` |
| `ESCALATION_REQUIRED` | No external authority reachable | Escalate to `TERMINAL_NO_RECOVERY` |

## Invariants

1. **Determinism** — the same system-state class always maps to the same recovery category.
2. **Completeness** — every system-state class has a defined recovery category.
3. **Monotonic escalation** — blocked recovery always escalates to a more severe category, never to a less severe one.
4. **No silent recovery** — every recovery action must produce a diagnostic record explaining what was done and why.
5. **Finality** — `TERMINAL_NO_RECOVERY` represents a completed terminal state; no further recovery action exists or is pending within the ASH recovery semantics.

## Relation to other specifications

- **system-state-classification.pseudo.md** — provides the `SystemStateClass` that is mapped to a recovery category
- **recovery-fallback-semantics.pseudo.md** — implements the algorithmic details of correction, fallback, and escalation
- **containment-safe-failure-semantics.pseudo.md** — implements containment and safe-halt behavior
- **state-validity-diagnostics.pseudo.md** — provides the diagnostic record that informs classification and recovery
- **control-bit-derivation.pseudo.md** — provides the derivation function used in `RE_DERIVE_CONTROL` and `CORRECT_AND_RE_DERIVE`
- **core-admissibility.pseudo.md** — provides the correction function used in `CORRECT_AND_RE_DERIVE`
