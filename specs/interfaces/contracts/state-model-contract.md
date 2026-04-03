# StateModel Contract — temporary bridge contract (R2 baseline)

> **TEMPORARY BRIDGE CONTRACT — Pending R3 Rebuild**
>
> This contract has been rewritten as a **temporary bridge** aligned to the R2 full-9D research baseline. It replaces the previous 8+1-era contract that mandated the parity formula, 16-codeword set, and corrected-core derivation.
>
> This is **not the final authoritative contract**. The full contract rebuild occurs in R3. This bridge provides interim guidance for understanding the StateModel module's responsibility within the restored 9D model.

## Purpose

The `StateModel` module is the foundational implementation module for the ASH Pattern System. It owns the canonical state representation, normalization, validity diagnostics, system-state classification, and recoverability classification.

## Canonical responsibility (R2 baseline)

The `StateModel` module is responsible for:

- Representing ASH states as **full 9-bit vectors in F2^9**
- Classifying state admissibility using the codeword-orbit structure defined in `specs/core/state-admissibility.pseudo.md`
- Producing state-validity diagnostics as defined in `specs/core/state-validity-diagnostics.pseudo.md`
- Classifying system states into the 7 canonical classes as defined in `specs/core/system-state-classification.pseudo.md`
- Classifying recoverability as defined in `specs/core/recoverability-semantics.pseudo.md`
- Grounding transformation semantics in the canonical codeword set defined in `specs/core/codeword-set.pseudo.md`

## Required behaviors (R2 baseline)

- States are full 9-bit vectors — not decomposed into an 8-bit core plus a derived 9th bit
- Normalization operates on the full 9-bit state using codeword-based correction
- Admissibility is determined by codeword-orbit membership, not by an 8-bit sub-code
- Diagnostics use the full-state diagnostic record (no extracted_core, no control_derivation_status)
- XOR-by-codeword is the canonical transformation mechanism

## What this bridge contract does NOT mandate

This bridge contract does **not** mandate any of the following superseded 8+1 requirements:

- The parity formula (`b0 XOR b1 XOR ... XOR b7`) as canonical control-bit derivation
- The [8,4,4] extended Hamming code 16-codeword set as canonical admissibility law
- Extracted-core / corrected-core / derived-control handling as canonical implementation behavior
- The corrected-core derivation rule

Those requirements belonged to the superseded 8+1 formalization and are no longer authoritative.

## Relation to other specifications

- `specs/core/ash-state-space.pseudo.md` — canonical F2^9 state definition
- `specs/core/codeword-set.pseudo.md` — canonical codeword structure
- `specs/core/state-admissibility.pseudo.md` — full 9-bit admissibility
- `specs/core/state-validity-diagnostics.pseudo.md` — full 9D diagnostic model
- `specs/core/system-state-classification.pseudo.md` — system-state classes
- `specs/core/recoverability-semantics.pseudo.md` — recovery categories
