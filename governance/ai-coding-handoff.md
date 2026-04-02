# AI Coding Handoff

## Purpose

This document tells a coding agent how to use this repository when building a target implementation.

## Handoff rule

Treat this repository as the semantic authority.
Do not infer core semantics from convenience, local idiom, or language defaults.

## Required coding-agent workflow

1. read `README.md`
2. read all files in `docs/`
3. read all files in `specs/core/`
4. read all files in `specs/algorithms/`
5. read `specs/interfaces/semantic-contracts.md`
6. read `governance/repository-governance.md`
7. only then begin target-specific design and implementation planning

## What the coding agent must preserve

The coding agent must preserve:

- the ASH state space as **F2^9**
- the special role of the first 8 coordinates as the stabilizing algebraic core
- the special role of the 9th coordinate as a derived control/parity dimension
- deterministic normalization
- deterministic realm identity
- deterministic transition behavior
- deterministic topology expansion
- full axiom diagnostics
- explicit separation between generation planning and materialization

## What the coding agent must not do

The coding agent must not:

- reinterpret the 9th coordinate as a normal peer bit for ordinary transitions
- silently collapse the core/control distinction
- make one platform's file structure into the engine's identity
- replace semantic planning with direct side effects
- treat convenience behavior as canonical if the specs do not say so

## Required delivery shape for implementation repos

A downstream implementation handoff should include, at minimum:

- mapping from spec modules to implementation modules
- invariant-based test plan
- materialization boundary design
- diagnostics design
- target-runtime constraints
- packaging and build decisions for that target repo
