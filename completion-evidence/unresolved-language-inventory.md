# Unresolved Language Inventory

## Scan

Command:

```text
rg -n -i "TODO|TBD|FIXME|PLACEHOLDER|UNRESOLVED|pending research|future specification|not yet defined|implementation-defined|known valid state|recognized valid state|outside all known codeword orbits|guess|approximately|as needed|etc\." README.md docs governance handoff-templates specs wiki
```

## Findings

| Path | Line | Match | Initial disposition |
|---|---:|---|---|
| `governance/ai-coding-handoff.md` | 68 | `guess` | Prohibition language; review after neutral rename |
| `governance/math-change-notes/2026-05-02-self-contained-canonical-language.md` | 7 | `unresolved` | Historical note; likely acceptable as provenance |
| `wiki/Specification-Layers.md` | 48 | `as needed` | Informative wiki language; review during wiki alignment |
| `governance/repository-governance.md` | 33 | `placeholder` | Heading prohibits placeholder semantics; likely acceptable |
| `governance/repository-governance.md` | 35 | `guessed`, `unresolved`, `placeholders` | Prohibition language; likely acceptable |
| `specs/interfaces/contracts/recovery-engine-contract.md` | 46 | `guess` | Prohibition language; likely acceptable after semantic rewrite |
| `specs/interfaces/contracts/artifact-emitter-contract.md` | 11 | `etc.` | Normative-ish list; replace with closed wording |
| `specs/interfaces/contracts/artifact-emitter-contract.md` | 22 | `etc.` | Normative-ish list; replace with closed wording |
| `specs/interfaces/contracts/artifact-emitter-contract.md` | 39 | `guess` | Prohibition language; likely acceptable |
| `handoff-templates/desktop-implementation-handoff-template.md` | 40 | `etc.` | Template language; replace or bound |
| `specs/core/state-validity-diagnostics.pseudo.md` | 62 | `outside all known codeword orbits` | Blocker; contradicts closed orbit partition |
| `specs/core/state-validity-diagnostics.pseudo.md` | 99 | `known valid states` | Blocker; undefined operational concept |
| `specs/registries/fallback-policy-registry.md` | 15 | `future`, `placeholder` | Prohibition/positioning language; review |
| `specs/registries/fallback-policy-registry.md` | 145 | `guess` | Prohibition language; likely acceptable |
| `specs/core/state-admissibility.pseudo.md` | 30 | `known valid states` | Blocker; undefined operational concept |
| `specs/core/state-admissibility.pseudo.md` | 31 | `known valid states` | Blocker; contradicts closed orbit partition |
| `specs/core/state-admissibility.pseudo.md` | 42 | `known valid state` | Blocker; undefined operational concept |
| `specs/core/state-admissibility.pseudo.md` | 46 | `known valid state` | Blocker; contradicts closed orbit partition |
| `specs/core/state-admissibility.pseudo.md` | 72 | `recognized valid state` | Blocker; undefined operational concept |
| `specs/algorithms/containment-safe-failure-semantics.pseudo.md` | 57 | `guess` | Prohibition language; likely acceptable |
| `specs/core/ash-state-space.pseudo.md` | 93 | `known valid states` | Blocker; undefined operational concept |
| `specs/algorithms/branching-semantics.pseudo.md` | 63 | `implementation-defined`, `future canonical specification` | Blocker; topology must be closed for 1.0 |
| `specs/algorithms/recovery-fallback-semantics.pseudo.md` | 154 | `guessing` | Prohibition heading; likely acceptable |
| `specs/algorithms/recovery-fallback-semantics.pseudo.md` | 156 | `guess` | Prohibition language; likely acceptable |

## Baseline conclusion

The scan confirms the package audit: active normative files still contain undefined known-valid terminology and implementation-defined branching behavior. These are Phase 1 and Phase 2 blockers.
