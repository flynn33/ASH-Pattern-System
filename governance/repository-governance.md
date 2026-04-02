# Repository Governance

## Repository role

This repository is the canonical semantic definition of the ASH Engine.
It is not a language implementation repository.

## Governance rules

### 1. Language neutrality

No programming language may be described as the canonical identity of the engine in this repository.

### 2. Platform neutrality

No operating system, runtime family, or device category may be described as the canonical platform identity of the engine in this repository.

### 3. Spec-first rule

Changes that affect semantics must be made in the specification documents first.
Implementation repositories must follow the specifications, not redefine them.

### 4. Pseudocode rule

When algorithmic examples are needed, use pseudocode unless a target-specific handoff explicitly requires implementation syntax.

### 5. Semantic clarity rule

A document is only complete if a downstream coding agent can determine:

- what the model means
- what invariants must hold
- what boundary separates planning from materialization
- what behaviors are prohibited

### 6. Fresh-repo rule

This repository stands on its own as a fresh baseline.
It should not depend on explanation through older implementation layouts.

## Admission rule for future files

A new file belongs in this repository only if it strengthens the semantic source of truth.
If it mainly expresses one platform's build, runtime, or packaging concerns, it belongs in a downstream implementation repository instead.
