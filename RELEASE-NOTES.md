# APS 1.0.0-rc.3 Release Notes

This corrective prerelease closes machine-schema acceptance of whitespace-only explanations and multiline summaries. Such fields were already semantically invalid. Full diagnostic and safety-record schemas now enforce the shape constraints directly; semantic checks still prove identity, chain continuity, causal phases, and required explanatory meaning.

PUBLIC-SPECIFICATION-API.md records precise normative precedence for older conflicting state, recovery, realm, topology, fallback, and rule-taxonomy clauses. The selected current core/algorithm/data contracts already defined these behaviors before this correction. The old source commits and historical evidence remain immutable.

The rc.2 diagnostic IDs and complete semantic expected records are unchanged. The state space, fixed codewords, bit order, orbits, realms, XOR, averaging, structural topology, operational-context predicates, five axiom predicates, and fallback definition data are unchanged. Regenerated product-version metadata and artifact checksums identify rc.3. Acquire the exact new source commit and follow MIGRATION-GUIDE.md.
