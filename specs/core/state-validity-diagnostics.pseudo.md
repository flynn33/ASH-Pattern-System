# State-Validity Diagnostics — canonical specification (1.0 release candidate)

## Purpose

This specification defines the diagnostic model for candidate input, structural state validity, orbit identity, pairwise reachability, and operational assessment boundaries.

Diagnostics must distinguish:

- malformed input;
- well-formed ASH realms;
- orbit identity;
- pairwise reachability;
- context-bound operational health.

## Diagnostic envelope

Every diagnostic record is emitted inside a versioned envelope:

```text
TYPE DiagnosticEnvelope
    schema_version             : String
    diagnostic_id              : String
    diagnostic_kind            : DiagnosticKind
    severity                   : DiagnosticSeverity
    stage                      : String
    disposition                : DiagnosticDisposition
    subject_reference          : String
    parent_diagnostic_id       : String or NONE
    chain_root_diagnostic_id   : String
    sequence_number            : Integer >= 1
    rule_ids                   : List of RuleID
    summary                    : String
    notes                      : List of String
    details                    : Object
    occurrence_metadata        : Object or NONE
END TYPE
```

`diagnostic_id` is the SHA-256 digest of the canonical semantic payload. Occurrence metadata such as timestamp, host, process, or transport data is excluded from this identity.

## Diagnostic kinds

```text
ENUM DiagnosticKind
    INPUT_VALIDATION
    STATE_ASSESSMENT
    CLASSIFICATION
    TRANSITION
    TOPOLOGY
    AXIOM
    GENERATION_PLAN
    EMISSION
    RECOVERY
    FALLBACK
    CONTAINMENT
    SAFE_HALT
    SCHEMA_VALIDATION
    CONFORMANCE
END ENUM
```

## State validity diagnostic

```text
TYPE StateValidityDiagnostic
    input_status            : InputStatus
    raw_candidate_reference : String
    state                   : AshState or NONE
    orbit_id                : String or NONE
    orbit_representative    : String or NONE
    admissibility_status    : AdmissibilityStatus
    reachability            : ReachabilityResult or NONE
    operational_context_id  : String or NONE
    state_assessment        : StateAssessment or NONE
    rule_ids                : List of RuleID
END TYPE
```

### `input_status`

`WELL_FORMED` or `MALFORMED`.

### `state`

Present only when the candidate is a well-formed nine-bit vector.

### `orbit_id` and `orbit_representative`

Present for every well-formed state. Absent for malformed input.

### `admissibility_status`

`WELL_FORMED_REALM` for every well-formed state, `MALFORMED_INPUT` otherwise.

### `reachability`

Present only when the diagnostic evaluates a source/target pair. Reachability is never inferred from a single state.

### `state_assessment`

Present only when a validated `OperationalContext` is supplied. Without context, diagnostics may report structural facts but may not claim operational health.

## Pseudocode

```text
FUNCTION diagnose_state(candidate, codeword_set C, operational_context or NONE) -> StateValidityDiagnostic
    normalized = normalize_state(candidate)
    diagnostic = new StateValidityDiagnostic()
    diagnostic.rule_ids = ["ASH-INPUT-001", "ASH-STATE-001"]

    IF normalized.input_status == MALFORMED THEN
        diagnostic.input_status = MALFORMED
        diagnostic.raw_candidate_reference = safe_raw_candidate_reference(candidate)
        diagnostic.state = NONE
        diagnostic.orbit_id = NONE
        diagnostic.orbit_representative = NONE
        diagnostic.admissibility_status = MALFORMED_INPUT
        diagnostic.state_assessment = NONE
        RETURN diagnostic
    END IF

    diagnostic.input_status = WELL_FORMED
    diagnostic.state = normalized.state
    diagnostic.orbit_id = normalized.state.orbit_id
    diagnostic.orbit_representative = orbit_representative(normalized.state.orbit_id)
    diagnostic.admissibility_status = WELL_FORMED_REALM

    IF operational_context is NONE THEN
        diagnostic.operational_context_id = NONE
        diagnostic.state_assessment = NONE
        RETURN diagnostic
    END IF

    validated_context = validate_operational_context(operational_context)
    IF validated_context is invalid THEN
        diagnostic.operational_context_id = NONE
        diagnostic.state_assessment = blocked_assessment("invalid operational context")
        RETURN diagnostic
    END IF

    diagnostic.operational_context_id = validated_context.context_id
    diagnostic.state_assessment = assess_state(normalized.state, validated_context)
    RETURN diagnostic
END FUNCTION
```

```text
FUNCTION diagnose_reachability(source_candidate, target_candidate, codeword_set C) -> DiagnosticEnvelope
    result = evaluate_reachability(source_candidate, target_candidate, C)
    RETURN diagnostic_envelope(
        diagnostic_kind = TRANSITION,
        subject_reference = reachability_subject(source_candidate, target_candidate),
        details = result
    )
END FUNCTION
```

## Completeness requirement

Every downstream implementation must emit a diagnostic for any candidate input. The diagnostic may block state assessment when input or context is invalid, but it must not be empty, partial, or silent.

Malformed input must preserve the raw candidate through a safe reference or escaped representation. It must not be coerced into `Vector[9]`.

## Relation to other specifications

- **ash-state-space.pseudo.md** — defines `F2^9` and `AshState`.
- **state-admissibility.pseudo.md** — defines well-formedness, orbit identity, and pairwise reachability.
- **codeword-set.pseudo.md** — defines canonical codeword membership.
- **system-state-classification.pseudo.md** — consumes diagnostics plus operational context.
- **recoverability-semantics.pseudo.md** — consumes operational classes.
