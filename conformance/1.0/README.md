# APS 1.0 Conformance Corpus

This directory contains deterministic implementation-neutral vectors for APS 1.0 release qualification.

Compare every declared expected field. Diagnostic expected_output is the complete inner record; the versioned schema transport wraps it as data and repeats its diagnostic_id as id. Required notes explain conditions, details hold semantic facts, and occurrence_metadata may be null. diagnostic-chains.jsonl additionally qualifies modern/legacy safety chains, containment management, operation-phase carry, and occurrence-invariant identity.

Containment vectors declare initial mode and actual boundary/prevention/propagation evidence. A confirmed breach completes at frozen terminal SAFE_HALT; a prevented unauthorized attempt stays CONTAINED. After halt, calls return the preserved frozen snapshot without appending diagnostics.
