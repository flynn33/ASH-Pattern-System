# Codeword Set — canonical specification (Research Baseline)

## Purpose

This specification defines the canonical **codeword set** `C ⊂ F2^9` for the ASH Pattern System.

The codeword set is the algebraic structure that governs all state transformations, orbit structure, averaging behavior, and branching topology in the ASH model. Every transformation `x' = x ⊕ c` uses a codeword from this set.

## What the codeword set is

The codeword set `C` is a subset of `F2^9` — a collection of 9-bit binary vectors that define the allowed XOR transformations on the state space.

- `C ⊂ F2^9`
- Each codeword `c ∈ C` is a full 9-bit vector
- The set defines the orbit structure: for any state `x`, the orbit of `x` under `C` is `{ x ⊕ c : c ∈ C }`
- The averaging operator `T f(x) = (1/|C|) Σ_{c∈C} f(x ⊕ c)` is defined over this set

## Research-baseline grounding

The ASH research materials (ashcosmology.net, published papers and preprints) describe the codeword structure in terms of:

- A set of **generating transformations** that produce the codeword set
- Published **example codewords** that illustrate the transformation structure
- The algebraic relationship between the codeword structure and adinkra / graph-theoretic constructs in the research baseline

### Observable properties of published examples

Some published example codewords have their 9th coordinate set to `0`. This is an observable structural property of those specific codewords. It does **not** mandate that all codewords must have `b8 = 0`, nor does it justify promoting the 9th coordinate to a derived parity/control role.

### Exact codeword enumeration

> **STATUS: PENDING RESEARCH CLOSURE**

The exact exhaustive enumeration of all codewords in `C` for the canonical ASH model has not been fully formalized in this repository from the research baseline. The research materials provide generating structures and example sets, but the complete canonical enumeration requires careful extraction from the published sources.

Until this closure item is resolved:

1. Implementations must treat the codeword set as a defined-by-research input, not an implementation choice
2. Implementations must not invent codewords not supported by the research baseline
3. Implementations must structure code so the codeword set is a single replaceable point of definition
4. The generating structure from the research materials should be used to derive the complete set where published

## Downstream treatment of unspecified codewords

Downstream implementations must not:

- Invent codewords not grounded in the research baseline
- Extend the codeword set beyond what the research materials justify
- Treat the codeword set as an open parameter that implementations may choose freely
- Assume any specific algebraic closure (e.g., a linear code) unless the research baseline explicitly establishes it

## Relation to other specifications

- **codeword-transformation-semantics.pseudo.md** — defines `x' = x ⊕ c` using codewords from this set
- **averaging-operator-semantics.pseudo.md** — defines `T` as a sum over codeword transformations
- **branching-semantics.pseudo.md** — branching topology is governed by the codeword structure
- **state-admissibility.pseudo.md** — admissibility is defined relative to the codeword orbit structure
- **ash-state-space.pseudo.md** — defines the F2^9 state space in which codewords operate
- **transition-system.pseudo.md** — transitions use codeword transformations

## Invariants

1. **Research grounding**: the codeword set must be grounded in published research materials, not invented
2. **9-bit completeness**: codewords are full 9-bit vectors in F2^9
3. **No 8+1 decomposition**: codewords are not decomposed into 8-bit components plus a derived 9th bit at the foundational level
4. **Determinism**: the codeword set is fixed for a given ASH model configuration — it does not vary at runtime
