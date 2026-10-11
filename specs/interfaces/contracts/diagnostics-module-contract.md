# Diagnostics Module Contract — implementation contract (Canonical Baseline)

## Purpose

The `Diagnostics` module is the cross-cutting implementation module responsible for exposing, collecting, and validating diagnostic records across all other modules. It ensures that the full diagnostic chain is observable, auditable, and conformant with the canonical schema and taxonomy.

## Canonical responsibility

The `Diagnostics` module is the single authority for:

- ensuring all diagnostic records conform to the shared diagnostic schema
- ensuring all rule IDs conform to the canonical taxonomy
- exposing diagnostic chains for inspection and audit
- preventing silent omission of diagnostics

## Required inputs

- Diagnostic records produced by all other modules (StateModel, RecoveryEngine, RealmEncoder, TransitionRegistry, TopologyGenerator, AxiomEvaluator, GenerationPlanner, ArtifactEmitter)

## Required outputs

- Validated, schema-conformant diagnostic records
- Complete diagnostic chains with proper parent/root references
- Audit-ready diagnostic output

## Required behaviors

### Schema conformance
- All diagnostic records must conform to the `DiagnosticEnvelope` defined in `specs/interfaces/diagnostic-schema.md`
- Required serialized fields: `schema_version`, `diagnostic_id`, `diagnostic_kind`, `severity`, `stage`, `disposition`, `subject_reference`, `parent_diagnostic_id`, `chain_root_diagnostic_id`, `sequence_number`, `rule_ids`, `summary`, nonempty meaningful `notes`, `details`, and `occurrence_metadata`
- Recompute the nine-field semantic identity; reject arbitrary IDs or IDs stale after any semantic field changes
- Validate the transport wrapper and every inner field; `details = {}` and `occurrence_metadata = null` are valid populated fields
- Validate the explicit safety phases and carried operation phase defined in `diagnostic-schema.md`; enum ordinals are not escalation order
- No diagnostic record may be emitted without these fields populated

### Rule-ID taxonomy conformance
- All `rule_ids` in diagnostic records must conform to the canonical pattern defined in `specs/interfaces/rule-id-taxonomy.md`
- Patterns: registered baseline `{FAMILY}-{NUMBER}` and retained `{FAMILY}-{CATEGORY}-{NUMBER}` (e.g., `ASH-STATE-001`, `ASH-STATE-VALIDITY-001`), as defined in the taxonomy
- Rule-free diagnostics are prohibited

### Diagnostic chain exposure
- The full diagnostic chain from initial state-validity detection through terminal safe halt must be reconstructable
- `parent_diagnostic_reference` links each diagnostic to its predecessor
- `chain_root_reference` links every diagnostic to the originating state-validity diagnostic
- No orphan diagnostics — every diagnostic (except the root) must have a parent reference

### No silent omission
- Every step in the recovery/escalation chain must produce a diagnostic
- Silent escalation (changing severity or stage without emitting a diagnostic) is prohibited
- Diagnostics must not be deferred, batched, or conditionally suppressed
- If any module fails to produce a required diagnostic, the Diagnostics module must detect and report the gap

### Deterministic output
- The same input conditions must produce the same diagnostic output
- Diagnostic content must not depend on randomness, platform-specific behavior, or external state

## Required diagnostics

- The Diagnostics module itself must produce meta-diagnostics when it detects nonconformance (e.g., a diagnostic with invalid rule IDs, missing fields, or broken chain references)

## Invariants

1. All diagnostics conform to the shared schema
2. All rule IDs conform to the canonical taxonomy
3. The diagnostic chain is complete and reconstructable
4. No silent omission — every required diagnostic is emitted
5. Diagnostic output is deterministic

## Prohibited shortcuts

- Must not emit diagnostics with missing required fields
- Must not emit diagnostics with non-taxonomy-compliant rule IDs
- Must not silently drop diagnostics from the chain
- Must not defer or batch diagnostics in a way that breaks chain integrity
- Must not invent local diagnostic structures outside the canonical schema

## Relation to other contracts and specifications

- `diagnostic-schema.md` — shared diagnostic envelope definition
- `rule-id-taxonomy.md` — canonical rule-ID pattern and families
- `state-model-contract.md` — produces state-validity diagnostics
- `recovery-engine-contract.md` — produces recovery, fallback, containment, safe-halt diagnostics
- `realm-encoder-contract.md` — produces encoding diagnostics
- `transition-registry-contract.md` — produces transition diagnostics
- `topology-generator-contract.md` — produces topology diagnostics
- `axiom-evaluator-contract.md` — produces axiom evaluation diagnostics
- `generation-planner-contract.md` — produces plan diagnostics
- `artifact-emitter-contract.md` — produces emission diagnostics
