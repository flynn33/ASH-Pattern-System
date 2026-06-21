# Branching Semantics — canonical specification (1.0 release candidate)

## Purpose

This specification defines branching and topology as first-class canonical APS structure.

Branching is structural by default. It does not implicitly mutate ASH states and does not invent a default codeword mapping for tree edges.

## Canonical structural topology

The canonical topology is a full ordered ternary tree.

```text
root path: R
child order: continuation, positive, negative
path tokens: C, P, N
child path: parent_path + "/" + token
node ID: "APS-NODE-" + path with "/" replaced by "."
root depth: 0
```

Child token ordering is fixed:

```text
C -> 0
P -> 1
N -> 2
```

For a node at depth `d`, its generation ordinal is the base-3 value of its path tokens at that depth. The global ordinal is:

```text
global_ordinal = (3^d - 1) / 2 + generation_ordinal
```

Canonical output order is ascending `(depth, generation_ordinal)`.

At requested depth `d`:

```text
leaf_count  = 3^d
total_nodes = (3^(d+1) - 1) / 2
```

The topology result contains all nodes from depth `0` through `d`, plus an explicit leaf list.

## Topology request

```text
TYPE TopologyRequest
    requested_depth : Integer >= 0
    resource_limit  : TopologyResourceLimit or NONE
END TYPE
```

Semantic behavior is defined for every finite non-negative depth. An implementation may impose a documented resource limit. An over-limit request must fail before partial output and must emit requested depth, configured limit, projected node count, and projected leaf count.

## Topology node

```text
TYPE TopologyNode
    node_id            : String
    path               : String
    depth              : Integer >= 0
    generation_ordinal : Integer >= 0
    global_ordinal     : Integer >= 0
    parent_path        : String or NONE
    is_leaf            : Boolean
END TYPE
```

## Pseudocode

```text
FUNCTION expand_topology(request: TopologyRequest) -> TopologyResult
    IF request.requested_depth < 0 THEN
        RETURN diagnostic_failure(TOPOLOGY, "requested depth must be non-negative")
    END IF

    projected_nodes = (3^(request.requested_depth + 1) - 1) / 2
    projected_leaves = 3^request.requested_depth

    IF request.resource_limit exists AND projected_nodes > request.resource_limit.max_nodes THEN
        RETURN diagnostic_failure(
            TOPOLOGY,
            "topology request exceeds configured resource limit",
            requested_depth = request.requested_depth,
            projected_nodes = projected_nodes,
            projected_leaves = projected_leaves
        )
    END IF

    nodes = []
    FOR depth IN 0..request.requested_depth DO
        FOR generation_ordinal IN 0..(3^depth - 1) DO
            path = path_from_base3(depth, generation_ordinal, tokens = [C, P, N])
            nodes.append(topology_node(path, depth, generation_ordinal, request.requested_depth))
        END FOR
    END FOR

    RETURN TopologyResult(
        depth = request.requested_depth,
        total_nodes = projected_nodes,
        leaf_count = projected_leaves,
        nodes = nodes,
        leaves = [node IN nodes WHERE node.is_leaf]
    )
END FUNCTION
```

## Relation to states and codewords

The structural tree does not by itself apply codeword transitions.

If a downstream profile assigns ASH states to branches, every edge must explicitly name a canonical transition and satisfy the transition contract:

```text
edge.target_state = edge.source_state ⊕ transition.codeword_signature
```

This assignment belongs to a `BranchStateAssignmentProfile`. The core topology has no implicit state mutation.

## Invariants

1. Branching is first-class and canonical.
2. The structural tree is deterministic for a given depth.
3. Node IDs, paths, parent links, generation ordinals, and global ordinals are exact.
4. Output order is stable.
5. Negative depth and over-limit requests fail before partial output.
6. State assignment is optional profile behavior and must name explicit transitions.

## Relation to other specifications

- **topology-expansion.pseudo.md** — provides the topology expansion contract aligned to this structural tree.
- **codeword-set.pseudo.md** — defines transitions available to optional state-assignment profiles.
- **ash-state-space.pseudo.md** — defines the canonical `F2^9` state space.
- **codeword-transformation-semantics.pseudo.md** — defines edge transition validity when a profile assigns states.
