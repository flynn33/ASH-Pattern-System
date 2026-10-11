# Migration Guide

Downstream implementations should bind to versioned schemas, canonical data, and conformance corpus paths for each APS release.

For 1.0.0-rc.3, read the normative reconciliation in PUBLIC-SPECIFICATION-API.md. The existing core/algorithm/data behavior and rc.2 semantic diagnostic IDs remain unchanged. Blank explanations and multiline summaries were already semantically invalid; the machine schemas now reject them too. Bind regenerated product-version fields, checksums, schemas, and corpus to the new exact commit. Earlier module/invariant/registry clauses listed by the reconciliation are superseded only for those stated conflicts.

For 1.0.0-rc.2, acquire the exact tagged/integrated source commit in a new cache. Retain earlier commit caches and qualification evidence as immutable historical inputs. Rebind schema, corpus, index, and provenance together; do not rewrite rc.1 expected files in place.

Diagnostic builders must supply meaningful nonempty notes, required details (possibly `{}`), and occurrence metadata (possibly null), then compute the nine-field semantic identity specified in `specs/interfaces/diagnostic-schema.md`. The fourteen affected root-vector IDs change. Persisted rc.1 diagnostic IDs must remain identified as rc.1; they are not valid rc.2 identities. Recompute only when migrating the complete semantic record, preserving its old provenance separately. Serialize all record fields under the versioned transport wrapper and validate both schema and identity. Parent/root IDs and sequence describe causal placement separately from semantic identity.

Use the explicit safety-phase table for modern and retained legacy stage spellings. Operation labels have no invented total order. Qualify the new diagnostic chain/occurrence vectors in addition to standalone diagnostics. Confirmed containment breach must preserve a breach record and terminal halt record before returning SAFE_HALT. A prevented unauthorized write remains CONTAINED, preserves restrictions, and records its denial. Subsequent mutation/recovery calls after halt return the frozen snapshot without adding diagnostics.
