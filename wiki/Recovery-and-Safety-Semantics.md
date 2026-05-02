# Recovery and Safety Semantics

The ASH Pattern System is resilient because it defines deterministic behavior for recovery, fallback, containment, and terminal halt.

## Canonical System-State Classes

| Class | Meaning | Action category |
|---|---|---|
| `STABLE` | Healthy valid state | `NO_ACTION` |
| `UNSTABLE` | Transformation-compatible, needs normalization | `NORMALIZE_STATE` |
| `CORRECTABLE` | Known correction path exists | `APPLY_CORRECTION` |
| `DEGRADED` | Incompatible or ambiguous correction | `FALLBACK_REQUIRED` |
| `CONTAINED` | Restricted mode to prevent propagation | `CONTAINMENT_REQUIRED` |
| `FAILED` | No automated recovery path | `ESCALATION_REQUIRED` |
| `SAFE_HALT` | Intentional terminal state | `TERMINAL_NO_RECOVERY` |

## Deterministic Escalation Flow

```mermaid
flowchart LR
    A[State diagnostic] --> B{Class}
    B -->|STABLE| C[No action]
    B -->|UNSTABLE or CORRECTABLE| D[Normalize or correct]
    B -->|DEGRADED| E[Fallback selection]
    E -->|No valid fallback| F[Containment]
    F -->|Containment breach or halt policy| G[Safe halt]
    B -->|FAILED| H[Escalate to authority]
    H --> G
```

## Required Recovery Properties

1. Deterministic class-to-recovery mapping.
2. No silent healing.
3. Fallback only through canonical registry policy ordering.
4. Monotonic escalation.
5. SAFE_HALT is terminal and non-reversible.

## Diagnostic Chain Requirement

Every stage must emit diagnostics conforming to:

- Shared envelope (`specs/interfaces/diagnostic-schema.md`)
- Canonical rule-ID taxonomy (`specs/interfaces/rule-id-taxonomy.md`)

## References

- `specs/core/state-validity-diagnostics.pseudo.md`
- `specs/core/system-state-classification.pseudo.md`
- `specs/core/recoverability-semantics.pseudo.md`
- `specs/algorithms/recovery-fallback-semantics.pseudo.md`
- `specs/algorithms/containment-safe-failure-semantics.pseudo.md`
