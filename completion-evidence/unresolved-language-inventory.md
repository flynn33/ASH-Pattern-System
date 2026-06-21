# Unresolved Language Inventory

Generated during Phase 0 baseline capture. Each hit requires disposition during semantic closure.

- `governance/ai-coding-handoff.md:68` — - guess foundational math that lacks explicit canonical definition
- `governance/math-change-notes/2026-05-02-self-contained-canonical-language.md:7` — - Removed stale decomposition and closure wording that implied unresolved codeword semantics or special derived-coordinate handling.
- `governance/repository-governance.md:33` — ### 7. No placeholder semantics
- `governance/repository-governance.md:35` — Canonical documents must not rely on guessed values, implicit defaults, or unresolved placeholders when describing normative behavior.
- `handoff-templates/desktop-implementation-handoff-template.md:40` — - Where materialization occurs (file emission, UI rendering, etc.)
- `specs/algorithms/branching-semantics.pseudo.md:63` — This specification establishes branching as a canonical first-class capability and defines its relationship to the rest of the canonical system. Specific tree construction strategies remain implementation-defined unless a future canonical specification standardizes them explicitly.
- `specs/algorithms/containment-safe-failure-semantics.pseudo.md:57` — The determination of propagation risk is a policy decision. If no propagation-risk policy is defined, the system must not assume safety — it must escalate to containment rather than guess.
- `specs/algorithms/recovery-fallback-semantics.pseudo.md:154` — ## Prohibition on heuristic guessing
- `specs/algorithms/recovery-fallback-semantics.pseudo.md:156` — When canonical policy is absent, the system must not guess. It must escalate to containment.
- `specs/core/ash-state-space.pseudo.md:93` — - **Codeword-orbit membership** — whether a state is reachable from known valid states via codeword transformations
- `specs/core/state-admissibility.pseudo.md:30` —     TRANSFORMATION_COMPATIBLE    -- state is reachable via codeword orbit from a known valid state
- `specs/core/state-admissibility.pseudo.md:31` —     TRANSFORMATION_INCOMPATIBLE  -- state is not reachable via any codeword orbit from known valid states
- `specs/core/state-admissibility.pseudo.md:42` — The state is reachable from a known valid state via one or more codeword transformations. It is within the codeword orbit structure and can participate in normal transformation operations.
- `specs/core/state-admissibility.pseudo.md:46` — The state is a well-formed 9-bit vector but is not reachable from any known valid state via codeword transformations. It lies outside the codeword orbit structure and cannot be reached or departed from using canonical transformations alone.
- `specs/core/state-admissibility.pseudo.md:72` —     IF state is a recognized valid state THEN
- `specs/core/state-validity-diagnostics.pseudo.md:62` —     INCOMPATIBLE     -- state is outside all known codeword orbits
- `specs/core/state-validity-diagnostics.pseudo.md:99` — - whether the orbit contains known valid states
- `specs/interfaces/contracts/artifact-emitter-contract.md:11` — - materializing a generation plan into target-specific artifacts (files, modules, services, etc.)
- `specs/interfaces/contracts/artifact-emitter-contract.md:22` — - Materialized artifacts (files, modules, services, etc.)
- `specs/interfaces/contracts/artifact-emitter-contract.md:39` — - If the plan is incomplete or ambiguous, the emitter must fail with a diagnostic rather than guess
- `specs/interfaces/contracts/recovery-engine-contract.md:46` — - Must not invent, guess, or heuristically select fallback states
- `specs/registries/fallback-policy-registry.md:15` — The fallback-policy registry is a locked design decision. It is not optional, not future, and not a placeholder.
- `specs/registries/fallback-policy-registry.md:145` — 4. The system must not invent, guess, or heuristically select a fallback state outside the registry.
- `wiki/Specification-Layers.md:48` — When semantics change, update spec layers first, then contracts/verification as needed, then refresh docs/wiki summaries.
