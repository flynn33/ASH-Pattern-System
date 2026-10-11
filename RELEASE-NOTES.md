# APS 1.0.0-rc.2 Release Notes

This corrective prerelease reconciles diagnostic and containment artifacts that previously disagreed with their normative requirements. Diagnostic vectors now contain explanations of their actual conditions, structured details, occurrence metadata, schema version, and identities covering all nine semantic fields. Machine schemas validate the complete inner diagnostic and serialized containment/halt snapshots. New causal-chain and occurrence vectors require complete field comparisons and explicit phase validation.

A confirmed breach while contained records the breach, enters terminal SAFE_HALT, preserves the full diagnostic chain, and freezes it before returning. A denied unauthorized operation that did not cross the boundary remains CONTAINED and records its denial. Further calls after halt return the original snapshot without transitions or diagnostic mutation.

The state space, fixed codewords, orbits, XOR transitions, b8 preservation, exact averaging, branching, operational-context predicates, five axiom predicates, and fallback policies/order retain their existing definitions. Diagnostic IDs and affected corpus bytes change. Follow `MIGRATION-GUIDE.md` and bind the complete successor artifacts to their exact source commit. The rc.1 commit remains immutable.
