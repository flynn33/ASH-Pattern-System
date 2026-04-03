# StateModel Contract — implementation contract

## Purpose

The `StateModel` module is the foundational implementation module for the ASH Pattern System. It owns the canonical state representation, normalization, validity diagnostics, system-state classification, and recoverability classification.

## Canonical responsibility

The `StateModel` module is the single authority for:

- representing ASH states as 9-coordinate binary vectors over F2
- normalizing candidate states into valid normalized form
- classifying core admissibility against the locked [8,4,4] codeword set
- deriving the control bit using the locked parity formula
- producing state-validity diagnostics
- classifying system states into the 7 canonical classes
- classifying recoverability for each system-state class
- applying the corrected-core derivation rule

## Required inputs

- A candidate ASH state (raw 9-element vector or structured `AshState`)

## Required outputs

- Normalized `AshState` (when normalization succeeds)
- `StateValidityDiagnostic` record (for any candidate state)
- `SystemStateClass` classification
- `RecoveryCategory` classification

## Required behaviors

### Normalization
- Extract the 8-bit core and observed control bit from the candidate state
- Classify core admissibility using the locked normative 16-codeword set
- If `ADMISSIBLE`: derive control from `extracted_core` using the locked parity formula (`b0 XOR b1 XOR ... XOR b7`)
- If `INADMISSIBLE_CORRECTABLE`: correct to nearest codeword, then derive control from `corrected_core` (corrected-core derivation rule)
- If `INADMISSIBLE_DETECTABLE` or `INADMISSIBLE_UNRECOVERABLE`: normalization fails with diagnostic
- Return normalized state or diagnostic failure

### Control-bit derivation
- Use the locked parity formula: `derive_control_bit(core) = b0 XOR b1 XOR b2 XOR b3 XOR b4 XOR b5 XOR b6 XOR b7`
- For admissible normalized cores, the derived control bit is always `0`
- Must not substitute a different formula

### Admissibility classification
- Use the locked normative 16-codeword set from `core-admissibility.pseudo.md`
- Classification is by Hamming distance: 0=ADMISSIBLE, 1=CORRECTABLE, 2=DETECTABLE, >=3=UNRECOVERABLE
- Must not substitute a different codeword set

### System-state classification
- Map admissibility + control-derivation + runtime context to one of: STABLE, UNSTABLE, CORRECTABLE, DEGRADED, CONTAINED, FAILED, SAFE_HALT
- Classification must be deterministic and total

### Recoverability classification
- Map each system-state class to its recovery category: NO_ACTION, RE_DERIVE_CONTROL, CORRECT_AND_RE_DERIVE, FALLBACK_REQUIRED, CONTAINMENT_REQUIRED, ESCALATION_REQUIRED, TERMINAL_NO_RECOVERY

## Required diagnostics

- Every normalization attempt must produce a `StateValidityDiagnostic` conforming to `diagnostic-schema.md`
- Rule IDs must conform to `rule-id-taxonomy.md` (`ASH-STATE` family)
- Diagnostics must never be silently omitted

## Invariants

1. Normalization is deterministic
2. Equal 8-bit cores produce equal derived control bits
3. State validity can be explained diagnostically
4. The corrected-core derivation rule is applied for all correctable states
5. Classification is total — every state maps to exactly one class

## Prohibited shortcuts

- Must not treat the 9th coordinate as an ordinary peer bit
- Must not derive control from a raw inadmissible core when correction applies
- Must not skip admissibility classification before normalization
- Must not silently accept an inadmissible core as valid
- Must not invent alternative algebraic definitions

## Relation to other contracts and specifications

- `ash-state-space.pseudo.md` — canonical state definition
- `control-bit-derivation.pseudo.md` — locked parity formula
- `core-admissibility.pseudo.md` — locked 16-codeword set
- `state-validity-diagnostics.pseudo.md` — diagnostic record definition
- `system-state-classification.pseudo.md` — classification logic
- `recoverability-semantics.pseudo.md` — recovery category mapping
- `recovery-engine-contract.md` — consumes classification and diagnostics from StateModel
- `diagnostics-module-contract.md` — schema and taxonomy conformance requirements
