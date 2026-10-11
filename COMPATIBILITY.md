# Compatibility Policy

APS follows Semantic Versioning. Changes to public identifiers, required fields, canonical JSON, or conformance interpretation require a major version unless explicitly backward compatible.

During the 1.0 release-candidate series, a corrective prerelease may reconcile contradictory pre-stable artifacts before the first stable release. Version 1.0.0-rc.2 is such a correction: diagnostic IDs change because the identity now includes mandatory explanatory notes and details, machine schemas enforce already-required fields, and completed containment breaches return the already-required terminal SAFE_HALT. These are migration-requiring corpus/serialization corrections, not a claim of byte compatibility with rc.1. The mathematical and operational-context baselines do not change. A downstream binding must name the exact source commit as well as the product version; namespace `1.0` alone does not distinguish prerelease artifacts.
