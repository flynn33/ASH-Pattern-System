# Glossary

## ASH State
A full 9-bit vector in `F2^9`.

## Codeword Set (C)
Canonical fixed 16-member subset of `F2^9` used for XOR transformations. `C` is a `[9, 4, 4]` doubly-even linear code and a subgroup of `(F2^9, ⊕)`: it contains the zero vector and is closed under XOR. It has `16 = 2^4` members and partitions `F2^9` into 32 orbits.

## XOR-by-Codeword
Canonical state motion rule: `x' = x XOR c`.

## Admissibility
Deterministic status assignment for a 9-bit state relative to codeword orbit structure.

## System-State Class
Operational class (`STABLE`, `UNSTABLE`, `CORRECTABLE`, `DEGRADED`, `CONTAINED`, `FAILED`, `SAFE_HALT`).

## Recovery Category
Deterministic action class selected from system-state class.

## Fallback Registry
Canonical policy registry that orders and validates fallback candidates.

## Containment
Restricted operation mode preventing propagation when recovery/fallback is insufficient.

## Safe Halt
Intentional terminal state with preserved diagnostic chain.

## Diagnostic Envelope
Shared schema for all diagnostic records across detection, recovery, escalation, and terminal stages.

## Rule ID Taxonomy
Canonical naming/governance format for diagnostic rule IDs.

## Materialization Boundary
Locked separation between planning (`GenerationPlanner`) and artifact materialization (`ArtifactEmitter`).

## Averaging Operator (T)
Canonical operator that averages a function over the codeword orbit: `T f(x) = (1/|C|) Σ_{c ∈ C} f(x ⊕ c)`. It is idempotent (`T² = T`), which is well-defined because `C` is a subgroup of `(F2^9, ⊕)`.

## Branching
First-class canonical capability of the system (specified in `specs/algorithms/branching-semantics.pseudo.md`).

## Realm Identity
A stable, deterministic semantic encoding of an ASH state, computed from the full 9-bit state. There is exactly one realm per `F2^9` vertex (512 realms); equal states yield equal realm identities (`specs/core/realm-identity.pseudo.md`).

## Orbit
A coset of `C` in `F2^9`. There are 32 orbits (`512 / 16`).

## Canonical Semantic Modules
The nine canonical semantic modules: `StateModel`, `RecoveryEngine`, `RealmEncoder`, `TransitionRegistry`, `TopologyGenerator`, `AxiomEvaluator`, `GenerationPlanner`, `ArtifactEmitter`, `Diagnostics`.

## Conformance Categories
Five required verification buckets for downstream acceptance: Algebraic/State Conformance; Recovery/Fallback/Containment Conformance; Diagnostics Conformance; Generation/Materialization-Boundary Conformance; Contract/Module Conformance. All five are required; see [Contracts and Verification](Contracts-and-Verification).
