# Recoverability Semantics — canonical specification (1.0 release candidate)

## Purpose

This specification defines the deterministic mapping from each operational system-state class to the allowed recovery category.

Structural normalization is not a recovery category. It occurs before operational classification and preserves realm identity.

## Recovery categories

```text
ENUM RecoveryCategory
    NO_ACTION
    TARGET_RESOLUTION_REQUIRED
    APPLY_CORRECTION
    FALLBACK_REQUIRED
    CONTAINMENT_ACTIVE
    EXTERNAL_ESCALATION_REQUIRED
    TERMINAL_NO_RECOVERY
END ENUM
```

### NO_ACTION

- **Applies to**: `STABLE`
- **Meaning**: The state is allowed by the active context. No recovery action is needed.

### TARGET_RESOLUTION_REQUIRED

- **Applies to**: `UNSTABLE`
- **Meaning**: Same-orbit stable candidates exist, but policy cannot select exactly one target. No mutation is allowed until policy or context resolves the ambiguity.

### APPLY_CORRECTION

- **Applies to**: `CORRECTABLE`
- **Meaning**: Apply the single codeword `current ⊕ target` to reach the selected same-orbit stable target.

### FALLBACK_REQUIRED

- **Applies to**: `DEGRADED`
- **Meaning**: No same-orbit correction is currently available. A validated fallback policy instance must select an authorized replacement or escalate to containment.

### CONTAINMENT_ACTIVE

- **Applies to**: `CONTAINED`
- **Meaning**: Restricted operations are active while diagnostics and external resolution proceed.

### EXTERNAL_ESCALATION_REQUIRED

- **Applies to**: `FAILED`
- **Meaning**: Automated correction and fallback are unavailable or exhausted. External authority is required.

### TERMINAL_NO_RECOVERY

- **Applies to**: `SAFE_HALT`
- **Meaning**: The process is in a terminal no-mutation state.

## Deterministic mapping

```text
FUNCTION classify_recoverability(state_class: SystemStateClass) -> RecoveryCategory
    SWITCH state_class
        CASE STABLE:      RETURN NO_ACTION
        CASE UNSTABLE:    RETURN TARGET_RESOLUTION_REQUIRED
        CASE CORRECTABLE: RETURN APPLY_CORRECTION
        CASE DEGRADED:    RETURN FALLBACK_REQUIRED
        CASE CONTAINED:   RETURN CONTAINMENT_ACTIVE
        CASE FAILED:      RETURN EXTERNAL_ESCALATION_REQUIRED
        CASE SAFE_HALT:   RETURN TERMINAL_NO_RECOVERY
    END SWITCH
END FUNCTION
```

## Blocked recovery conditions

| Recovery Category | Blocked When | Escalation |
|---|---|---|
| `TARGET_RESOLUTION_REQUIRED` | Policy still cannot select one target | remain `UNSTABLE` or enter `DEGRADED` if context invalidates candidates |
| `APPLY_CORRECTION` | Target mismatch, codeword mismatch, or post-check failure | `FALLBACK_REQUIRED` |
| `FALLBACK_REQUIRED` | No valid policy instance or no valid candidate | containment escalation |
| `CONTAINMENT_ACTIVE` | Containment boundary breached | `TERMINAL_NO_RECOVERY` |
| `EXTERNAL_ESCALATION_REQUIRED` | External authority unavailable | `TERMINAL_NO_RECOVERY` |

## Invariants

1. Every system-state class maps to exactly one recovery category.
2. Blocked recovery never silently succeeds.
3. Correction and fallback are distinct actions.
4. Cross-orbit replacement is fallback, not canonical codeword motion.
5. Escalation is monotonic unless an external authority records a policy-permitted resolution.
6. `TERMINAL_NO_RECOVERY` is final inside APS semantics.

## Relation to other specifications

- **system-state-classification.pseudo.md** — provides the operational class.
- **recovery-fallback-semantics.pseudo.md** — implements correction and fallback.
- **containment-safe-failure-semantics.pseudo.md** — implements containment and safe halt behavior.
- **state-validity-diagnostics.pseudo.md** — provides diagnostic inputs.
- **codeword-set.pseudo.md** — defines the codeword structure used for correction.
