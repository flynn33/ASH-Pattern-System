# Diagnostic Schema — canonical specification (1.0.0-rc.3)

## Shared record and transport envelope

Every diagnostic uses this record, including standalone assessments and every step of recovery, fallback, containment, and safe halt. In-memory parent/root references project to the IDs below; they do not replace the required serialized fields.

```text
TYPE DiagnosticEnvelope
    schema_version             : String ("1.0")
    diagnostic_id              : String
    diagnostic_kind            : DiagnosticKind
    severity                   : Severity
    stage                      : Stage
    disposition                : Disposition
    subject_reference          : String
    parent_diagnostic_id       : String or NONE
    chain_root_diagnostic_id   : String
    sequence_number            : Integer >= 1
    rule_ids                   : nonempty List of RuleID
    summary                    : nonempty one-line String
    notes                      : nonempty List of nonempty explanatory String
    details                    : Object (empty object permitted)
    occurrence_metadata        : Object or NONE
END TYPE
```

`schemas/1.0/diagnostic-envelope.schema.json` validates the transport envelope `{schema_version, product_version, id, data}`. Its `data` is exactly the record above, `id = data.diagnostic_id`, and both schema versions are `1.0`. Conformance `expected_output` is the inner record. A consumer must compare every applicable field; the wrapper is a projection, not a reason to omit record fields. Schema validation checks shape. Semantic validation additionally checks identity and chain integrity.

## Vocabulary

Diagnostic kinds are `INPUT_VALIDATION`, `STATE_ASSESSMENT`, `CLASSIFICATION`, `TRANSITION`, `TOPOLOGY`, `AXIOM`, `GENERATION_PLAN`, `EMISSION`, `RECOVERY`, `FALLBACK`, `CONTAINMENT`, `SAFE_HALT`, `SCHEMA_VALIDATION`, and `CONFORMANCE`. The earlier `STATE_VALIDITY` spelling remains accepted as a deprecated assessment kind. Its spelling is preserved in identity; alias acceptance does not rewrite a record.

Severities are `INFO`, `WARNING`, `ERROR`, and `CRITICAL`; severity reflects impact. Dispositions are `RECORDED`, `RESOLVED`, `PENDING`, `BLOCKED`, `ESCALATED`, and `TERMINAL`. `RECORDED` reports an observation or action, `PENDING` awaits resolution, and `TERMINAL` freezes the chain.

Stages express either a safety phase or an operation label. The explicit safety phase mapping is:

| Phase | Accepted stages |
|---|---|
| 0: detection | `DETECTION`, `PARSE` |
| 1: assessment/classification | `CLASSIFICATION`, `ASSESS`, `CLASSIFY` |
| 2: recovery/fallback | `RECOVERY`, `RECOVER`, `FALLBACK` |
| 3: containment | `ESCALATION`, `CONTAIN` |
| 4: terminal halt | `TERMINAL`, `HALT` |

`TRANSFORM`, `PLAN`, `EVALUATE`, `EMIT`, `VALIDATE`, and `VERIFY` are operation labels with no total ordering. Their enum ordinals must never determine escalation order. An operation record carries the latest preceding safety phase for subsequent checks.

## Chain integrity and safety

1. A root has null parent, sequence 1, and its own ID as chain root. Standalone records may use any supported stage.
2. A child references its immediate predecessor, shares the root ID, and has predecessor sequence plus one. Every referenced record must be available. Cycles, orphans, skipped sequences, and inconsistent roots are invalid. A semantic ID can repeat for repeated identical conditions; chain occurrence is distinguished by parent and sequence, not by changing semantic content.
3. Safety phases cannot decrease. Entering phase 3 requires a preceding effective phase 1 or 2. Entering phase 4 requires phase 2 or 3. Same-phase 3 management records use kind `CONTAINMENT` and may describe a denied operation (`BLOCKED`), an observation (`RECORDED`), awaiting resolution (`PENDING`), escalation (`ESCALATED`), or an externally directed resolution decision (`RESOLVED`); they do not resume ordinary operations. A `TERMINAL` disposition freezes the resulting record regardless of kind.
4. After phase 3, ordinary operation-label records are prohibited. After stage `HALT` or `TERMINAL`, kind `SAFE_HALT`, or disposition `TERMINAL`, all children are prohibited. Rejected calls after halt return the preserved frozen snapshot and do not append diagnostics.
5. Every actual recovery/escalation step emits a meaningful diagnostic. Do not silently skip, suppress, defer, or batch steps. The complete chain remains observable.
6. Severity follows `INFO < WARNING < ERROR < CRITICAL` and does not decrease within a causal escalation chain, preserving the recovery contract's severity invariant. Externally directed resolution decisions retain this chain's severity floor; a separately authorized resumption does not rewrite its diagnostic history.

## Explanation, details, and occurrence metadata

Summary identifies the condition in one line. Each note explains a condition, action, or disposition; a filler string added solely to satisfy cardinality is nonconformant. `details` holds structured semantic facts such as candidate state, policy, restricted operations, or breach evidence. It is required even when `{}` suffices. Rule IDs follow `rule-id-taxonomy.md`, in evaluation order.

The machine schema requires nonblank subject, summary, and note strings, and a summary without line breaks. It rejects missing, empty, and whitespace-only explanations. Shape validation cannot establish whether an explanation is meaningful; that remains a semantic requirement. Identity and cross-record safety checks also remain separate from schema validation.

`occurrence_metadata` is required and may be null. When present it holds non-semantic timestamp, host, process, or transport facts. Times use strings. Diagnostic JSON values are null, Boolean, Unicode scalar strings, signed 64-bit integers, arrays, or objects with Unicode scalar string keys. Floating-point values and invalid Unicode surrogate strings are prohibited in these records; exact ratios may be represented by integer numerator/denominator objects. This bounds portable canonical serialization without changing mathematical averaging semantics.

## Semantic identity

The semantic payload consists of exactly these nine fields, with their recorded values: `diagnostic_kind`, `disposition`, `rule_ids`, `severity`, `stage`, `subject_reference`, `summary`, `notes`, `details`.

Serialize the payload as compact JSON encoded in UTF-8. Sort all object keys by Unicode scalar order; preserve array order; use lowercase `true`, `false`, `null`; decimal integer formatting without leading zeros. Escape quote, backslash, and controls U+0000 through U+001F using JSON escapes (short escapes for backspace, form feed, newline, carriage return, tab; lowercase hex for the others). Other valid Unicode scalars are emitted as UTF-8 without ASCII escaping. No whitespace is inserted between tokens. This is `json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)` over the permitted values.

`diagnostic_id = "APS-DIAG-" + uppercase(first 24 hexadecimal characters of SHA256(serialized_payload))`.

Schema version, parent/root IDs, sequence, and occurrence metadata are excluded. Changing semantic notes, details, subject, summary, rules, or other payload fields requires recomputing identity; validators reject stale or arbitrary IDs. Changing timestamp/host metadata preserves identity. Chain placement is validated independently. The rc.1 seven-field corpus omitted explanatory content from identity and emitted empty notes; rc.2 corrects that inconsistency, and the affected corpus IDs change.

## Related contracts

`state-validity-diagnostics.pseudo.md` defines assessment content; recovery/fallback and containment/safe-failure specifications define action content. `diagnostics-module-contract.md` requires complete schema and semantic validation. `rule-id-taxonomy.md` governs rule identifiers. No downstream implementation may invent a conflicting envelope or infer operational health without its required context.
