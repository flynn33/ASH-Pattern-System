# System-State Classification — agnostic specification

## Purpose

This specification defines the **canonical system-state classes** for the ASH Pattern System.

The ASH Pattern System is a framework for self-healing, self-correcting, safe-failure, and fallback software. At its core, the system must be able to classify any state into a behavioral category that deterministically maps to the correct system response — whether that is normal operation, correction, fallback, containment, or safe halt.

System-state classification sits above state-validity diagnostics. Where diagnostics answer "what is the condition of this state?", classification answers "what should the system do about it?"

## Classification criteria

A system-state class is determined by evaluating two conditions from the state-validity diagnostic:

1. **Core admissibility** — is the 8-bit stabilizing core a valid codeword, correctable, detectable, or unrecoverable?
2. **Control-derivation status** — does the observed control bit match the expected derived value?

Additional conditions arise from runtime context:

3. **Containment status** — has the system entered containment mode?
4. **Halt status** — has the system entered safe halt?

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

The system is in normal operating condition.

- Core admissibility: `ADMISSIBLE`
- Control derivation: `MATCH`
- No recovery action required
- All transitions proceed normally

### UNSTABLE

The system has a valid core but an inconsistent control dimension.

- Core admissibility: `ADMISSIBLE`
- Control derivation: `MISMATCH` or `UNABLE_TO_DERIVE`
- Recovery: re-derive control bit from the admissible core
- The system should not proceed with normal transitions until control is re-derived
- This is a recoverable condition that does not require fallback

### CORRECTABLE

The system has an inadmissible core that is within correctable distance of a valid codeword.

- Core admissibility: `INADMISSIBLE_CORRECTABLE`
- Control derivation: any (will be re-derived after correction)
- Recovery: correct core to nearest codeword, then re-derive control from the **corrected admissible core**
- The corrected-core derivation rule applies: expected control semantics are defined on the corrected core, not the raw inadmissible core
- This is a recoverable condition that does not require fallback

### DEGRADED

The system has an inadmissible core where the error is detected but correction is ambiguous.

- Core admissibility: `INADMISSIBLE_DETECTABLE`
- Control derivation: not meaningful (core is not correctable)
- Recovery: **fallback required** — the system must select a known-good state from the fallback-policy registry
- Deterministic correction is not possible; the system must not guess
- If fallback fails or is unavailable, the system must escalate to containment

### CONTAINED

The system has entered containment mode to prevent error propagation.

- Entry conditions:
  - DEGRADED state where fallback is unavailable or has failed
  - Propagation risk detected during recovery
  - Explicit containment request from operator or policy
- Behavior: operations are restricted to a safe subset; the system does not attempt further correction
- The system remains operational but in a restricted mode
- Awaits operator/policy decision for resolution
- Containment may escalate to SAFE_HALT if the containment boundary is breached

### FAILED

The system has an inadmissible core beyond reliable correction, and no automated recovery path exists.

- Core admissibility: `INADMISSIBLE_UNRECOVERABLE`
- Control derivation: not meaningful
- Recovery: **escalation required** — no automated recovery; the system must escalate to an external authority (operator, supervisor, or upstream system)
- The system is still running but in an unrecoverable error state
- FAILED is distinct from SAFE_HALT: FAILED means the system has detected an unrecoverable condition but has not yet halted
- The system must produce diagnostic state for escalation
- FAILED may transition to SAFE_HALT if escalation determines that halt is appropriate

### SAFE_HALT

The system has deliberately halted in a known-safe terminal state.

- Entry conditions:
  - FAILED state where escalation determines halt is appropriate
  - Containment breach (CONTAINED state where the containment boundary is violated)
  - Explicit halt request from operator or policy
- Behavior: **no further transitions are permitted**
- The system preserves its full diagnostic state for post-mortem analysis
- SAFE_HALT is an intentional terminal action, not just an error condition
- SAFE_HALT is the only system-state class from which no recovery path exists by design

## Deterministic class-to-action mapping

Every system-state class maps deterministically to exactly one action category:

| System-State Class | Action Category | Description |
|---|---|---|
| `STABLE` | `NO_ACTION` | Normal operation; no recovery needed |
| `UNSTABLE` | `RE_DERIVE_CONTROL` | Re-derive control bit from admissible core |
| `CORRECTABLE` | `CORRECT_AND_RE_DERIVE` | Correct core to nearest codeword, then re-derive control |
| `DEGRADED` | `FALLBACK_REQUIRED` | Select known-good state from fallback-policy registry |
| `CONTAINED` | `CONTAINMENT_REQUIRED` | Restrict operations; await operator/policy decision |
| `FAILED` | `ESCALATION_REQUIRED` | Escalate to external authority; no automated recovery |
| `SAFE_HALT` | `TERMINAL_NO_RECOVERY` | Already halted in known-safe terminal state; no further transitions or recovery actions |

This mapping is:
- **Total** — every possible system-state class has exactly one action category
- **Deterministic** — the same class always maps to the same action
- **Monotonic in severity** — action severity increases with classification severity

## Pseudocode

```text
FUNCTION classify_system_state(diagnostic: StateValidityDiagnostic, context: SystemContext) -> SystemStateClass

    -- Check terminal states first
    IF context.is_in_safe_halt THEN
        RETURN SAFE_HALT
    END IF

    IF context.is_in_containment THEN
        RETURN CONTAINED
    END IF

    -- Classify from diagnostic conditions
    SWITCH diagnostic.admissibility_status
        CASE ADMISSIBLE:
            IF diagnostic.control_derivation_status == MATCH THEN
                RETURN STABLE
            ELSE
                RETURN UNSTABLE
            END IF

        CASE INADMISSIBLE_CORRECTABLE:
            RETURN CORRECTABLE

        CASE INADMISSIBLE_DETECTABLE:
            RETURN DEGRADED

        CASE INADMISSIBLE_UNRECOVERABLE:
            RETURN FAILED
    END SWITCH
END FUNCTION
```

## Invariants

1. **Completeness** — every possible combination of admissibility status, control-derivation status, and runtime context maps to exactly one system-state class.
2. **Determinism** — the same inputs always produce the same classification.
3. **Monotonic severity** — STABLE < UNSTABLE < CORRECTABLE < DEGRADED < CONTAINED < FAILED < SAFE_HALT in severity ordering.
4. **No silent classification** — classification must always be accompanied by a diagnostic record.
5. **Terminal finality** — SAFE_HALT is a terminal state; once entered, no transition to any other class is permitted.
6. **Containment monotonicity** — once CONTAINED, the system may only transition to SAFE_HALT (escalation), never back to a lower-severity class without explicit operator intervention.

## Relation to other specifications

- **state-validity-diagnostics.pseudo.md** — provides the `StateValidityDiagnostic` record that feeds classification
- **core-admissibility.pseudo.md** — provides the `AdmissibilityStatus` used in classification criteria
- **control-bit-derivation.pseudo.md** — provides the derivation status used in classification criteria
- **recoverability-semantics.pseudo.md** — maps each class to its recovery category
- **recovery-fallback-semantics.pseudo.md** — defines the algorithmic recovery and fallback flows
- **containment-safe-failure-semantics.pseudo.md** — defines containment and safe-halt behavior
- **ash-state-space.pseudo.md** — defines the state structure being classified
