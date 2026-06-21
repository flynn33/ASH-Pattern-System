# Getting Started

Use this sequence to understand the repository from canonical intent to downstream conformance.

## Recommended Reading Order

1. [Home](Home)
2. [Canonical Math Baseline](Canonical-Math-Baseline)
3. [Specification Layers](Specification-Layers)
4. [Recovery and Safety Semantics](Recovery-and-Safety-Semantics)
5. [Contracts and Verification](Contracts-and-Verification)
6. [Governance and Agents](Governance-and-Agents)
7. [Downstream Handoff Guide](Downstream-Handoff-Guide)

## Fast Orientation

| Question | Canonical answer |
|---|---|
| What is this repository? | A platform-neutral canonical specification repository for ASH. |
| Is this an implementation repo? | No. Implementation code belongs in downstream repos. |
| What state model is canonical? | Full `F2^9`, 512-state space. |
| What transformation is canonical? | XOR-by-codeword with `C subset F2^9`. |
| Where does the math come from? | The canonical specifications and enumerations in this repository. |
| What proves downstream conformance? | Invariants + category coverage (all five conformance categories) + contract satisfaction + diagnostic completeness, yielding an acceptance judgment of CONFORMANT / CONFORMANT WITH CAVEATS / NON-CONFORMANT. |

## What To Read In The Repository

- Purpose and design stance:
  - `README.md`
  - `docs/00-repository-purpose.md`
  - `docs/01-design-philosophy.md`
  - `docs/02-target-repository-shape.md`
  - `docs/03-design-roadmap.md`
- Canonical semantics:
  - `specs/core/*.md`
  - `specs/algorithms/*.md`
- Implementation contract layer:
  - `specs/interfaces/semantic-contracts.md`
  - `specs/interfaces/contracts/*.md`
- Verification layer:
  - `specs/verification/*.md`
- Governance and sentinels:
  - `governance/*.md`
  - `.github/workflows/*.yml`
  - `.github/scripts/*.py`

## Contributor Rule

If downstream implementation behavior conflicts with canonical specs, canonical specs win.
