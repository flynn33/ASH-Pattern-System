# Product Semantic Closure Math Note

## What changed

The state admissibility, diagnostics, classification, recoverability, recovery/fallback, branching, and state-space specifications were aligned to the 1.0 release-candidate semantic closure. The update separates malformed input, well-formed realm identity, pairwise reachability, and operational health under explicit context.

## Why

The previous wording mixed structural validity with operational health and described some well-formed states as unreachable from selected reference states. In the locked canonical model, every nine-bit state is a realm, every realm belongs to exactly one codeword orbit, and reachability is a pairwise relation determined by codeword-difference membership.

## Baseline preservation statement

The full `F2^9` state space, all 512 realms, the exact 16-member canonical codeword set, XOR-by-codeword transitions, and the `b8` invariance of canonical transitions are preserved. The change does not alter the locked codeword members, bit order, realm indexing, orbit partition, or transition operation.
