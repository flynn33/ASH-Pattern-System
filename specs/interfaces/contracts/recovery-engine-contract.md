# RecoveryEngine Contract — implementation contract

## Purpose

The `RecoveryEngine` module implements deterministic recovery, fallback, containment, and safe-halt behavior for the ASH Pattern System. It consumes state classifications and diagnostics from `StateModel` and executes the appropriate recovery action.

## Canonical responsibility

The `RecoveryEngine` module is the single authority for:

- executing recovery actions (re-derive control, correct + re-derive)
- selecting fallback states from the canonical fallback-policy registry
- entering and managing containment mode
- entering safe halt
- producing recovery, fallback, containment, and safe-halt diagnostics

## Required inputs

- `StateValidityDiagnostic` from StateModel
- `SystemStateClass` from StateModel
- `RecoveryCategory` from StateModel
- Access to the canonical fallback-policy registry

## Required outputs

- `RecoveryDiagnostic` record for every recovery/fallback action
- `ContainmentDiagnostic` record for containment entry
- `SafeHaltDiagnostic` record for safe-halt entry
- Recovered/corrected `AshState` (when recovery succeeds)

## Required behaviors

### Recovery actions
- `RE_DERIVE_CONTROL`: re-derive control bit from admissible core using locked parity formula
- `CORRECT_AND_RE_DERIVE`: correct core to nearest codeword, then re-derive from corrected core
- Post-recovery validation: re-diagnose the recovered state; must classify as STABLE
- If validation fails: escalate

### Fallback selection
- Select from the canonical fallback-policy registry (`specs/registries/fallback-policy-registry.md`)
- Deterministic ordering by `ordering_rank` then `policy_id`
- Post-selection validation: selected state must classify as STABLE
- If no valid candidate: escalate to containment
- Must not invent, guess, or heuristically select fallback states

### Containment
- Enter containment when fallback fails, propagation risk detected, or operator requests
- Restrict operations to safe subset
- Preserve diagnostic state
- Remain operational in restricted mode
- Escalate to safe halt if containment boundary is breached

### Safe halt
- Enter safe halt when directed by escalation, containment breach, or operator request
- No further transitions permitted — terminal state
- Preserve full diagnostic chain for post-mortem

### Monotonic escalation
- Recovery failure → fallback → containment → safe halt
- Escalation is strictly monotonic — never de-escalate without external intervention
- Every escalation must be recorded in the diagnostic chain

## Required diagnostics

- Every recovery step must produce a diagnostic record
- No silent healing — all state mutations must be diagnosable
- Diagnostics must conform to `diagnostic-schema.md`
- Rule IDs must conform to `rule-id-taxonomy.md` (`ASH-RECOVERY`, `ASH-FALLBACK`, `ASH-CONTAINMENT`, `ASH-HALT` families)
- Diagnostic chaining: each diagnostic must reference its parent and chain root

## Invariants

1. Recovery is deterministic — same inputs produce same recovery outcome
2. Escalation is monotonic — severity never decreases without external intervention
3. No silent healing — every recovery action produces a diagnostic
4. Fallback is registry-driven — no ad hoc fallback selection
5. Safe halt is terminal — no transitions from SAFE_HALT

## Prohibited shortcuts

- Must not silently heal without producing diagnostics
- Must not skip containment when the specification requires it
- Must not select fallback states outside the canonical registry
- Must not allow transitions from SAFE_HALT to any other state
- Must not de-escalate without external intervention

## Relation to other contracts and specifications

- `state-model-contract.md` — provides classification and diagnostics consumed by RecoveryEngine
- `recoverability-semantics.pseudo.md` — recovery category definitions
- `recovery-fallback-semantics.pseudo.md` — algorithmic recovery/fallback flow
- `containment-safe-failure-semantics.pseudo.md` — containment and safe-halt behavior
- `fallback-policy-registry.md` — canonical registry for fallback selection
- `diagnostics-module-contract.md` — schema and taxonomy conformance requirements
