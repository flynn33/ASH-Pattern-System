#!/usr/bin/env python3
"""Product generation and verification support for APS 1.0.

The module intentionally uses only Python standard-library APIs so the
canonical data, conformance fixtures, and release archive can be regenerated
from a clean checkout without dependency installation.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import zipfile
from collections import Counter
from itertools import product
from pathlib import Path
from typing import Any


PRODUCT_NAME = "ASH Pattern System"
PRODUCT_IDENTIFIER = "aps"
PRODUCT_VERSION = "1.0.0-rc.1"
SCHEMA_VERSION = "1.0"
CANONICAL_DATA_VERSION = "1.0"
CONFORMANCE_VERSION = "1.0"

CODEWORD_SIGNATURES: tuple[str, ...] = (
    "000000000",
    "000011110",
    "001100110",
    "001111000",
    "010101010",
    "010110100",
    "011001100",
    "011010010",
    "100101100",
    "100110010",
    "101001010",
    "101010100",
    "110000110",
    "110011000",
    "111100000",
    "111111110",
)

FALLBACK_POLICY_DEFINITIONS = [
    {
        "policy_id": "FALLBACK-STATE-001",
        "title": "Declared Known-Good",
        "candidate_source": "operational_context",
        "selection_order": ["configured_rank", "realm_id"],
        "requires_downstream_instance": True,
        "allows_cross_orbit_replacement": True,
    },
    {
        "policy_id": "FALLBACK-STATE-002",
        "title": "Last Verified Stable",
        "candidate_source": "downstream_verification_history",
        "selection_order": ["verification_sequence_desc", "realm_id"],
        "requires_downstream_instance": True,
        "allows_cross_orbit_replacement": True,
    },
    {
        "policy_id": "FALLBACK-STATE-999",
        "title": "Containment Escalation",
        "candidate_source": "none",
        "selection_order": [],
        "requires_downstream_instance": False,
        "allows_cross_orbit_replacement": False,
    },
]

RULE_FAMILIES = (
    "ASH-INPUT",
    "ASH-STATE",
    "ASH-CODEWORD",
    "ASH-ORBIT",
    "ASH-REALM",
    "ASH-TRANSITION",
    "ASH-TOPOLOGY",
    "ASH-AXIOM",
    "ASH-CLASSIFICATION",
    "ASH-RECOVERY",
    "ASH-FALLBACK",
    "ASH-CONTAINMENT",
    "ASH-HALT",
    "ASH-GENERATION",
    "ASH-EMISSION",
    "ASH-DIAGNOSTIC",
    "ASH-CONFORMANCE",
    "ASH-RELEASE",
    "ASH-SECURITY",
)

SCHEMA_ENTRY_POINTS = (
    "ash-state",
    "state-input",
    "codeword",
    "codeword-set",
    "orbit-record",
    "reachability-result",
    "realm-identity",
    "transition-entry",
    "transition-result",
    "operational-context",
    "state-assessment",
    "diagnostic-envelope",
    "recovery-result",
    "fallback-policy-definition",
    "fallback-policy-instance",
    "containment-record",
    "safe-halt-record",
    "topology-request",
    "topology-node",
    "topology-result",
    "branch-state-assignment-profile",
    "axiom-subject",
    "axiom-evaluation-profile",
    "axiom-diagnostic",
    "generation-request",
    "generation-plan",
    "role-assignment",
    "artifact-description",
    "emission-result",
    "rule-registry",
    "conformance-vector",
    "conformance-manifest",
    "product-manifest",
    "release-evidence",
)

REQUIRED_CONFORMANCE_VECTOR_FILES = (
    "states.jsonl",
    "codewords.jsonl",
    "transformations.jsonl",
    "reachability.jsonl",
    "realm-identities.jsonl",
    "averaging.jsonl",
    "topology.jsonl",
    "state-assessments.jsonl",
    "recovery.jsonl",
    "fallback.jsonl",
    "containment.jsonl",
    "safe-halt.jsonl",
    "diagnostics.jsonl",
    "axioms.jsonl",
    "generation-plans.jsonl",
    "materialization-boundary.jsonl",
)


def bits(signature: str) -> tuple[int, ...]:
    if len(signature) != 9 or any(value not in "01" for value in signature):
        raise ValueError(f"invalid APS state signature: {signature!r}")
    return tuple(int(value) for value in signature)


def signature(values: tuple[int, ...]) -> str:
    if len(values) != 9 or any(value not in (0, 1) for value in values):
        raise ValueError(f"invalid APS bit vector: {values!r}")
    return "".join(str(value) for value in values)


def canonical_codewords() -> tuple[str, ...]:
    return tuple(sorted(CODEWORD_SIGNATURES))


def xor_signature(left: str, right: str) -> str:
    return signature(tuple(a ^ b for a, b in zip(bits(left), bits(right))))


def state_index(state_signature: str) -> int:
    return int(state_signature, 2)


def realm_id(state_signature: str) -> str:
    return f"APS-REALM-{state_index(state_signature):03d}"


def gf2_rank(rows: list[tuple[int, ...]]) -> int:
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column]:
                matrix[row] = [left ^ right for left, right in zip(matrix[row], matrix[rank])]
        rank += 1
    return rank


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def semantic_digest(value: Any) -> str:
    return "APS-DIAG-" + sha256_text(canonical_json(value))[:24].upper()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for value in values:
            handle.write(canonical_json(value))
            handle.write("\n")


def canonical_math_data() -> dict[str, Any]:
    codewords = canonical_codewords()
    codeword_set = set(codewords)
    if len(codewords) != 16 or len(codeword_set) != 16:
        raise ValueError("APS codeword set must contain exactly 16 unique members")
    for left, right in product(codewords, repeat=2):
        if xor_signature(left, right) not in codeword_set:
            raise ValueError(f"codeword closure failed for {left} XOR {right}")

    codeword_records = []
    codeword_id_by_signature: dict[str, str] = {}
    for index, value in enumerate(codewords):
        codeword_id = f"APS-CW-{index:02d}"
        codeword_id_by_signature[value] = codeword_id
        codeword_records.append(
            {
                "bits": list(bits(value)),
                "codeword_id": codeword_id,
                "is_identity": value == "000000000",
                "ordering_rank": index,
                "signature": value,
                "weight": value.count("1"),
            }
        )

    all_states = tuple(f"{index:09b}" for index in range(512))
    unseen = set(all_states)
    orbit_members_by_representative: dict[str, tuple[str, ...]] = {}
    while unseen:
        seed = min(unseen)
        members = tuple(sorted({xor_signature(seed, codeword) for codeword in codewords}))
        representative = members[0]
        orbit_members_by_representative[representative] = members
        unseen.difference_update(members)

    if len(orbit_members_by_representative) != 32:
        raise ValueError("APS orbit partition must contain exactly 32 orbits")

    orbit_id_by_state: dict[str, str] = {}
    orbit_records = []
    for ordering_rank, representative in enumerate(sorted(orbit_members_by_representative)):
        orbit_id = f"APS-ORBIT-{ordering_rank:02d}"
        members = orbit_members_by_representative[representative]
        for member in members:
            if member in orbit_id_by_state:
                raise ValueError(f"state appears in multiple orbits: {member}")
            orbit_id_by_state[member] = orbit_id
        orbit_records.append(
            {
                "b8": int(representative[-1]),
                "member_count": len(members),
                "members": [
                    {"realm_id": realm_id(member), "state_signature": member}
                    for member in members
                ],
                "orbit_id": orbit_id,
                "ordering_rank": ordering_rank,
                "representative_realm_id": realm_id(representative),
                "representative_signature": representative,
            }
        )

    realm_records = [
        {
            "b8": int(state[-1]),
            "bits": list(bits(state)),
            "orbit_id": orbit_id_by_state[state],
            "realm_id": realm_id(state),
            "realm_index": state_index(state),
            "state_signature": state,
        }
        for state in all_states
    ]

    transition_records = [
        {
            "codeword_id": record["codeword_id"],
            "codeword_signature": record["signature"],
            "is_identity": record["is_identity"],
            "operation": "XOR",
            "ordering_rank": record["ordering_rank"],
            "transition_id": f"APS-TRANSITION-CW-{record['ordering_rank']:02d}",
        }
        for record in codeword_records
    ]

    transformation_records = []
    reachable_pairs = set()
    for source in all_states:
        for codeword, transition in zip(codeword_records, transition_records):
            target = xor_signature(source, str(codeword["signature"]))
            pair = (source, target)
            reachable_pairs.add(pair)
            transformation_records.append(
                {
                    "category": "transformation",
                    "codeword_id": codeword["codeword_id"],
                    "product_version": PRODUCT_VERSION,
                    "rule_ids": ["ASH-TRANSITION-001", "ASH-ORBIT-001"],
                    "source_b8": int(source[-1]),
                    "source_orbit_id": orbit_id_by_state[source],
                    "source_realm_id": realm_id(source),
                    "source_signature": source,
                    "target_b8": int(target[-1]),
                    "target_orbit_id": orbit_id_by_state[target],
                    "target_realm_id": realm_id(target),
                    "target_signature": target,
                    "transition_id": transition["transition_id"],
                    "vector_id": f"APS-VEC-TRANSFORM-{state_index(source):03d}-{codeword['ordering_rank']:02d}",
                }
            )

    weights = Counter(value.count("1") for value in codewords)
    nonzero_weights = [value.count("1") for value in codewords if value != "000000000"]
    pair_distances = [
        xor_signature(left, right).count("1")
        for index, left in enumerate(codewords)
        for right in codewords[index + 1 :]
    ]
    properties = {
        "all_codewords_preserve_b8": all(value[-1] == "0" for value in codewords),
        "code_dimension": gf2_rank([bits(value) for value in codewords]),
        "codeword_count": len(codewords),
        "expected_transformation_count": 8192,
        "members_per_orbit": [16],
        "minimum_nonzero_weight": min(nonzero_weights),
        "minimum_pairwise_distance": min(pair_distances),
        "orbit_count": len(orbit_records),
        "reachable_ordered_pair_count": len(reachable_pairs),
        "realm_id_count": len({record["realm_id"] for record in realm_records}),
        "state_count": len(all_states),
        "transformation_vector_count": len(transformation_records),
        "weight_distribution": {str(key): weights[key] for key in sorted(weights)},
    }

    return {
        "codewords": {"version": CANONICAL_DATA_VERSION, "codewords": codeword_records},
        "fallback-policy-definitions": {
            "version": CANONICAL_DATA_VERSION,
            "policies": FALLBACK_POLICY_DEFINITIONS,
        },
        "mathematical-properties": properties,
        "orbits": {"version": CANONICAL_DATA_VERSION, "orbits": orbit_records},
        "realms": {"version": CANONICAL_DATA_VERSION, "realms": realm_records},
        "transformation_vectors": transformation_records,
        "transitions": {"version": CANONICAL_DATA_VERSION, "transitions": transition_records},
    }


def topology_result(depth: int) -> dict[str, Any]:
    if not isinstance(depth, int) or depth < 0:
        raise ValueError("topology depth must be a non-negative integer")
    tokens = ("C", "P", "N")
    nodes = []
    leaves = []
    for current_depth in range(depth + 1):
        generation_count = 3 ** current_depth
        for generation_ordinal in range(generation_count):
            path_tokens = []
            value = generation_ordinal
            for _ in range(current_depth):
                path_tokens.append(tokens[value % 3])
                value //= 3
            path_tokens.reverse()
            path = "R" if not path_tokens else "R/" + "/".join(path_tokens)
            node = {
                "depth": current_depth,
                "generation_ordinal": generation_ordinal,
                "global_ordinal": ((3 ** current_depth - 1) // 2) + generation_ordinal,
                "is_leaf": current_depth == depth,
                "node_id": "APS-NODE-" + path.replace("/", "."),
                "parent_path": None if current_depth == 0 else path.rsplit("/", 1)[0],
                "path": path,
            }
            nodes.append(node)
            if node["is_leaf"]:
                leaves.append(node)
    return {
        "depth": depth,
        "leaf_count": 3 ** depth,
        "leaves": leaves,
        "nodes": nodes,
        "total_nodes": (3 ** (depth + 1) - 1) // 2,
    }


def rule_registry() -> dict[str, Any]:
    rules = []
    for index, family in enumerate(RULE_FAMILIES, 1):
        rules.append(
            {
                "introduced_version": "1.0.0",
                "normative_source_path": "specs/",
                "rule_family": family,
                "rule_id": f"{family}-001",
                "status": "ACTIVE",
                "title": f"{family} baseline requirement",
            }
        )
    return {"version": CANONICAL_DATA_VERSION, "rules": rules}


def normative_artifact_index(paths: list[str]) -> dict[str, Any]:
    records = []
    for path in sorted(paths):
        if path.startswith("specs/"):
            role = "NORMATIVE"
        elif path.startswith(("schemas/", "canonical-data/")):
            role = "NORMATIVE"
        elif path.startswith("conformance/"):
            role = "CONFORMANCE"
        elif path.startswith((".github/", "governance/")):
            role = "GOVERNANCE"
        elif path.startswith("handoff-templates/"):
            role = "TEMPLATE"
        elif path.startswith("completion-evidence/"):
            role = "HISTORICAL"
        else:
            role = "INFORMATIVE"
        records.append({"path": path, "classification": role})
    return {"version": CANONICAL_DATA_VERSION, "artifacts": records}


def schema_for(name: str) -> dict[str, Any]:
    object_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://github.com/flynn33/ASH-Pattern-System/schemas/1.0/{name}.schema.json",
        "title": f"APS {name.replace('-', ' ').title()}",
        "description": f"Versioned APS {name} record.",
        "product_version": PRODUCT_VERSION,
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "schema_version": {"type": "string", "const": SCHEMA_VERSION},
            "product_version": {"type": "string"},
            "id": {"type": "string", "minLength": 1},
            "data": {"type": "object"},
        },
        "required": ["schema_version", "product_version", "id", "data"],
    }
    if name == "ash-state":
        object_schema["properties"] = {
            "bits": {"type": "array", "items": {"type": "integer", "enum": [0, 1]}, "minItems": 9, "maxItems": 9},
            "realm_id": {"type": "string", "pattern": "^APS-REALM-[0-9]{3}$"},
            "realm_index": {"type": "integer", "minimum": 0, "maximum": 511},
            "state_signature": {"type": "string", "pattern": "^[01]{9}$"},
        }
        object_schema["required"] = ["bits", "realm_id", "realm_index", "state_signature"]
    elif name == "product-manifest":
        object_schema["properties"] = {
            "canonical_data_version": {"type": "string"},
            "canonical_repository": {"type": "string"},
            "conformance_corpus_version": {"type": "string"},
            "copyright_holder": {"type": "string"},
            "hashes": {"type": "object"},
            "license": {"type": "string"},
            "product_identifier": {"type": "string"},
            "product_name": {"type": "string"},
            "release_tag": {"type": "string"},
            "schema_version": {"type": "string"},
            "source_commit": {"type": "string"},
            "status": {"type": "string", "enum": ["IN_DEVELOPMENT", "RELEASE_CANDIDATE", "SHIPPABLE", "RELEASED", "MAINTENANCE"]},
            "version": {"type": "string"},
        }
        object_schema["required"] = sorted(object_schema["properties"])
    return object_schema


def build_schemas(root: Path) -> None:
    for name in SCHEMA_ENTRY_POINTS:
        write_json(root / "schemas" / SCHEMA_VERSION / f"{name}.schema.json", schema_for(name))


def build_canonical_data(root: Path) -> dict[str, Any]:
    data = canonical_math_data()
    output = root / "canonical-data" / CANONICAL_DATA_VERSION
    for name in ("codewords", "orbits", "realms", "transitions", "fallback-policy-definitions"):
        write_json(output / f"{name}.json", data[name])
    write_json(output / "rule-registry.json", rule_registry())
    paths = [
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.relative_to(root).parts[0] != "release"
    ]
    write_json(output / "normative-artifact-index.json", normative_artifact_index(paths))
    return data


def build_conformance_corpus(root: Path, data: dict[str, Any]) -> None:
    base = root / "conformance" / CONFORMANCE_VERSION
    if base.exists():
        shutil.rmtree(base)
    vectors = base / "vectors"
    invalid = base / "invalid"
    realms = data["realms"]["realms"]
    codewords = data["codewords"]["codewords"]
    transitions = data["transitions"]["transitions"]
    orbit_members: dict[str, list[dict[str, Any]]] = {}
    for realm in realms:
        orbit_members.setdefault(realm["orbit_id"], []).append(realm)
    write_jsonl(
        vectors / "states.jsonl",
        [
            {
                "category": "state",
                "expected_output": record,
                "product_version": PRODUCT_VERSION,
                "requirements": ["Every well-formed 9-bit vector is a realm"],
                "rule_ids": ["ASH-STATE-001", "ASH-REALM-001"],
                "source_paths": ["specs/core/ash-state-space.pseudo.md"],
                "vector_id": f"APS-VEC-STATE-{record['realm_index']:03d}",
            }
            for record in data["realms"]["realms"]
        ],
    )
    write_jsonl(
        vectors / "codewords.jsonl",
        [
            {
                "category": "codeword",
                "expected_output": record,
                "product_version": PRODUCT_VERSION,
                "requirements": ["Canonical codeword set member"],
                "rule_ids": ["ASH-CODEWORD-001"],
                "source_paths": ["specs/core/codeword-set.pseudo.md"],
                "vector_id": f"APS-VEC-CODEWORD-{record['ordering_rank']:02d}",
            }
            for record in data["codewords"]["codewords"]
        ],
    )
    write_jsonl(vectors / "transformations.jsonl", data["transformation_vectors"])
    write_jsonl(
        vectors / "realm-identities.jsonl",
        [
            {
                "category": "realm_identity",
                "expected_output": {
                    "realm_id": record["realm_id"],
                    "realm_index": record["realm_index"],
                    "state_signature": record["state_signature"],
                },
                "input": {"state_signature": record["state_signature"]},
                "product_version": PRODUCT_VERSION,
                "requirements": ["Realm IDs are deterministic for all 512 states"],
                "rule_ids": ["ASH-REALM-001"],
                "source_paths": ["specs/core/realm-identity.pseudo.md"],
                "vector_id": f"APS-VEC-REALM-{record['realm_index']:03d}",
            }
            for record in realms
        ],
    )
    write_jsonl(
        vectors / "reachability.jsonl",
        [
            {
                "category": "reachability",
                "expected_output": {
                    "reachable_target_count": 16,
                    "reachable_targets": [member["state_signature"] for member in orbit_members[record["orbit_id"]]],
                    "unreachable_target_count": 496,
                },
                "input": {"source_signature": record["state_signature"]},
                "product_version": PRODUCT_VERSION,
                "requirements": ["Reachability is exact pairwise codeword-difference membership"],
                "rule_ids": ["ASH-TRANSITION-001", "ASH-ORBIT-001"],
                "source_paths": ["specs/core/state-admissibility.pseudo.md"],
                "vector_id": f"APS-VEC-REACH-{record['realm_index']:03d}",
            }
            for record in realms
        ],
    )
    averaging_vectors: list[dict[str, Any]] = [
        {
            "category": "averaging",
            "expected_output": {
                "is_idempotent": True,
                "result": {"denominator": 16, "numerator": 16},
            },
            "input": {"function": "constant_one"},
            "product_version": PRODUCT_VERSION,
            "requirements": ["Averaging is exact and idempotent for constant functions"],
            "rule_ids": ["ASH-CONFORMANCE-001"],
            "source_paths": ["specs/algorithms/averaging-operator-semantics.pseudo.md"],
            "vector_id": "APS-VEC-AVERAGING-CONSTANT-ONE",
        }
    ]
    for orbit_id, members in sorted(orbit_members.items()):
        averaging_vectors.append(
            {
                "category": "averaging",
                "expected_output": {
                    "member_count": len(members),
                    "result_inside_orbit": {"denominator": 16, "numerator": 16},
                    "result_outside_orbit": {"denominator": 16, "numerator": 0},
                },
                "input": {"function": "orbit_indicator", "orbit_id": orbit_id},
                "product_version": PRODUCT_VERSION,
                "requirements": ["Averaging preserves orbit-constant indicator functions exactly"],
                "rule_ids": ["ASH-CONFORMANCE-001", "ASH-ORBIT-001"],
                "source_paths": ["specs/algorithms/averaging-operator-semantics.pseudo.md"],
                "vector_id": f"APS-VEC-AVERAGING-{orbit_id}",
            }
        )
    for record in realms:
        averaging_vectors.append(
            {
                "category": "averaging",
                "expected_output": {
                    "result_on_same_orbit": {"denominator": 16, "numerator": 1},
                    "result_outside_orbit": {"denominator": 16, "numerator": 0},
                },
                "input": {"function": "state_indicator", "state_signature": record["state_signature"]},
                "product_version": PRODUCT_VERSION,
                "requirements": ["State-indicator averaging is exact over the containing orbit"],
                "rule_ids": ["ASH-CONFORMANCE-001", "ASH-ORBIT-001"],
                "source_paths": ["specs/algorithms/averaging-operator-semantics.pseudo.md"],
                "vector_id": f"APS-VEC-AVERAGING-STATE-{record['realm_index']:03d}",
            }
        )
    write_jsonl(vectors / "averaging.jsonl", averaging_vectors)
    write_jsonl(
        vectors / "topology.jsonl",
        [
            {
                "category": "topology",
                "expected_output": topology_result(depth),
                "input": {"depth": depth},
                "product_version": PRODUCT_VERSION,
                "requirements": ["Deterministic ordered ternary topology"],
                "rule_ids": ["ASH-TOPOLOGY-001"],
                "source_paths": ["specs/algorithms/topology-expansion.pseudo.md"],
                "vector_id": f"APS-VEC-TOPOLOGY-{depth}",
            }
            for depth in range(0, 7)
        ],
    )
    scenario_vectors = {
        "state-assessments.jsonl": [
            ("MALFORMED_INPUT", {"candidate": "0101"}, {"input_status": "MALFORMED", "assessment_blocked": True}, ["ASH-INPUT-001"]),
            ("STABLE", {"candidate": "000000000", "allowed_stable_states": ["000000000"]}, {"state_class": "STABLE"}, ["ASH-CLASSIFICATION-001"]),
            ("CORRECTABLE", {"candidate": "000011110", "allowed_stable_states": ["000000000"]}, {"state_class": "CORRECTABLE", "codeword_id": "APS-CW-01"}, ["ASH-CLASSIFICATION-001", "ASH-RECOVERY-001"]),
            ("UNSTABLE", {"candidate": "000011110", "allowed_stable_states": ["000000000", "001100110"]}, {"state_class": "UNSTABLE"}, ["ASH-CLASSIFICATION-001"]),
            ("DEGRADED", {"candidate": "000000001", "allowed_stable_states": ["000000000"]}, {"state_class": "DEGRADED"}, ["ASH-CLASSIFICATION-001", "ASH-FALLBACK-001"]),
            ("MISSING_CONTEXT", {"candidate": "000000000", "context": None}, {"assessment_blocked": True}, ["ASH-CLASSIFICATION-001"]),
        ],
        "recovery.jsonl": [
            ("APPLY_CORRECTION", {"current": "000011110", "target": "000000000"}, {"category": "APPLY_CORRECTION", "delta": "000011110"}, ["ASH-RECOVERY-001"]),
            ("TARGET_MISMATCH", {"current": "000011110", "target": "111111111"}, {"category": "FALLBACK_REQUIRED"}, ["ASH-RECOVERY-001", "ASH-FALLBACK-001"]),
            ("EXTERNAL_ESCALATION", {"state_class": "FAILED"}, {"category": "EXTERNAL_ESCALATION_REQUIRED"}, ["ASH-RECOVERY-001"]),
        ],
        "fallback.jsonl": [
            ("DECLARED-KNOWN-GOOD", {"policy_id": "FALLBACK-STATE-001"}, {"replacement_kind": "RECOVERED_VIA_FALLBACK_REPLACEMENT"}, ["ASH-FALLBACK-001"]),
            ("LAST-VERIFIED-STABLE", {"policy_id": "FALLBACK-STATE-002"}, {"replacement_kind": "RECOVERED_VIA_FALLBACK_REPLACEMENT"}, ["ASH-FALLBACK-001"]),
            ("CONTAINMENT-ESCALATION", {"policy_id": "FALLBACK-STATE-999"}, {"replacement_kind": "CONTAINMENT_ESCALATION"}, ["ASH-FALLBACK-001", "ASH-CONTAINMENT-001"]),
        ],
        "containment.jsonl": [
            ("ENTER", {"risk": "PROPAGATION_BLOCKED"}, {"mode": "CONTAINED", "restricted_operations_only": True}, ["ASH-CONTAINMENT-001"]),
            ("BREACH", {"attempted_operation": "UNDECLARED_WRITE"}, {"mode": "FAILED"}, ["ASH-CONTAINMENT-001"]),
        ],
        "safe-halt.jsonl": [
            ("ENTER", {"state_class": "SAFE_HALT"}, {"terminal": True, "transitions_allowed": False}, ["ASH-HALT-001"]),
            ("MUTATION-AFTER-HALT", {"attempted_transition": "APS-TRANSITION-CW-01"}, {"expected_failure": "TERMINAL_NO_RECOVERY"}, ["ASH-HALT-001"]),
        ],
        "axioms.jsonl": [
            ("PASS", {"evidence": "profile_threshold_met"}, {"axiom_result": "PASS"}, ["ASH-AXIOM-001"]),
            ("FAIL", {"evidence": "profile_threshold_failed"}, {"axiom_result": "FAIL"}, ["ASH-AXIOM-001"]),
            ("INDETERMINATE", {"evidence": "missing_required_measurement"}, {"axiom_result": "INDETERMINATE"}, ["ASH-AXIOM-001"]),
        ],
        "generation-plans.jsonl": [
            ("MINIMAL", {"source": "000000000", "transition_id": "APS-TRANSITION-CW-00"}, {"plan_hash_stable": True}, ["ASH-GENERATION-001"]),
            ("REGISTRY-VERSION-CHANGE", {"registry_version_changed": True}, {"plan_hash_changes": True}, ["ASH-GENERATION-001"]),
            ("UNKNOWN-PROFILE", {"profile_id": "unknown"}, {"expected_failure": "PROFILE_REFERENCE_INVALID"}, ["ASH-GENERATION-001"]),
        ],
        "materialization-boundary.jsonl": [
            ("PLAN-TRACEABILITY", {"plan_complete": True}, {"every_output_has_plan_reference": True}, ["ASH-EMISSION-001"]),
            ("AMBIGUOUS-PLAN", {"plan_complete": False}, {"expected_failure": "EMISSION_REFUSED"}, ["ASH-EMISSION-001"]),
        ],
    }
    for filename, rows in scenario_vectors.items():
        write_jsonl(
            vectors / filename,
            [
                {
                    "category": filename.removesuffix(".jsonl").replace("-", "_"),
                    "expected_output": expected,
                    "input": input_value,
                    "product_version": PRODUCT_VERSION,
                    "requirements": [filename.removesuffix(".jsonl").replace("-", " ")],
                    "rule_ids": rule_ids,
                    "source_paths": ["specs/"],
                    "vector_id": f"APS-VEC-{filename.removesuffix('.jsonl').upper()}-{case_id}",
                }
                for case_id, input_value, expected, rule_ids in rows
            ],
        )
    diagnostics = []
    for index, (kind, severity, stage, disposition, rule_ids) in enumerate(
        [
            ("INPUT_VALIDATION", "ERROR", "PARSE", "BLOCKED", ["ASH-INPUT-001"]),
            ("STATE_ASSESSMENT", "INFO", "ASSESS", "RECORDED", ["ASH-STATE-001"]),
            ("CLASSIFICATION", "INFO", "CLASSIFY", "RECORDED", ["ASH-CLASSIFICATION-001"]),
            ("TRANSITION", "ERROR", "TRANSFORM", "BLOCKED", ["ASH-TRANSITION-001"]),
            ("TOPOLOGY", "ERROR", "PLAN", "BLOCKED", ["ASH-TOPOLOGY-001"]),
            ("AXIOM", "WARNING", "EVALUATE", "RECORDED", ["ASH-AXIOM-001"]),
            ("GENERATION_PLAN", "ERROR", "PLAN", "BLOCKED", ["ASH-GENERATION-001"]),
            ("EMISSION", "ERROR", "EMIT", "BLOCKED", ["ASH-EMISSION-001"]),
            ("RECOVERY", "WARNING", "RECOVER", "RECORDED", ["ASH-RECOVERY-001"]),
            ("FALLBACK", "WARNING", "FALLBACK", "RECORDED", ["ASH-FALLBACK-001"]),
            ("CONTAINMENT", "ERROR", "CONTAIN", "RECORDED", ["ASH-CONTAINMENT-001"]),
            ("SAFE_HALT", "ERROR", "HALT", "TERMINAL", ["ASH-HALT-001"]),
            ("SCHEMA_VALIDATION", "ERROR", "VALIDATE", "BLOCKED", ["ASH-CONFORMANCE-001"]),
            ("CONFORMANCE", "ERROR", "VERIFY", "BLOCKED", ["ASH-CONFORMANCE-001"]),
        ],
        1,
    ):
        payload = {
            "diagnostic_kind": kind,
            "disposition": disposition,
            "rule_ids": rule_ids,
            "severity": severity,
            "stage": stage,
            "subject_reference": f"APS-DIAG-SUBJECT-{index:02d}",
            "summary": f"{kind} diagnostic vector",
        }
        diagnostic_id = semantic_digest(payload)
        diagnostics.append(
            {
                "category": "diagnostics",
                "expected_output": {
                    **payload,
                    "chain_root_diagnostic_id": diagnostic_id,
                    "diagnostic_id": diagnostic_id,
                    "notes": [],
                    "parent_diagnostic_id": None,
                    "sequence_number": 1,
                },
                "input": payload,
                "product_version": PRODUCT_VERSION,
                "requirements": ["Diagnostic envelope is deterministic and schema-bound"],
                "rule_ids": rule_ids,
                "source_paths": ["specs/interfaces/diagnostic-schema.md"],
                "vector_id": f"APS-VEC-DIAGNOSTIC-{index:02d}",
            }
        )
    write_jsonl(vectors / "diagnostics.jsonl", diagnostics)
    write_json(
        invalid / "manifest.json",
        {
            "invalid_vectors": [
                {
                    "expected_failure": "STATE_SIGNATURE_PATTERN",
                    "path": "invalid-state-signature.json",
                    "schema": "schemas/1.0/ash-state.schema.json",
                },
                {
                    "expected_failure": "UNDECLARED_RULE_ID",
                    "path": "undeclared-rule-id.json",
                    "schema": "schemas/1.0/conformance-vector.schema.json",
                },
            ],
            "version": CONFORMANCE_VERSION,
        },
    )
    write_json(invalid / "invalid-state-signature.json", {"state_signature": "0101"})
    write_json(invalid / "undeclared-rule-id.json", {"rule_ids": ["ASH-UNKNOWN-001"]})
    write_json(
        base / "reachability-proof.json",
        {
            "reachable_ordered_pair_count": data["mathematical-properties"]["reachable_ordered_pair_count"],
            "proof": "reachable(source,target) iff source XOR target is in the canonical codeword set",
            "version": CONFORMANCE_VERSION,
        },
    )
    (base / "README.md").write_text(
        "# APS 1.0 Conformance Corpus\n\n"
        "This directory contains deterministic implementation-neutral vectors for APS 1.0 release qualification.\n",
        encoding="utf-8",
    )
    files = [path for path in base.rglob("*") if path.is_file()]
    manifest = {
        "product_version": PRODUCT_VERSION,
        "version": CONFORMANCE_VERSION,
        "vectors": [
            {
                "path": str(path.relative_to(base)),
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
            for path in sorted(files)
            if path not in {base / "manifest.json", base / "SHA256SUMS"}
        ],
    }
    write_json(base / "manifest.json", manifest)
    sums = []
    for entry in manifest["vectors"]:
        sums.append(f"{entry['sha256']}  {entry['path']}")
    (base / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")


def product_manifest(source_commit: str) -> dict[str, Any]:
    return {
        "canonical_data_version": CANONICAL_DATA_VERSION,
        "canonical_repository": "https://github.com/flynn33/ASH-Pattern-System",
        "conformance_corpus_version": CONFORMANCE_VERSION,
        "copyright_holder": "James Daley",
        "hashes": {},
        "license": "LicenseRef-ASH-Pattern-System-Personal-Academic",
        "product_identifier": PRODUCT_IDENTIFIER,
        "product_name": PRODUCT_NAME,
        "release_tag": "v1.0.0-rc.1",
        "schema_version": SCHEMA_VERSION,
        "source_commit": source_commit,
        "status": "RELEASE_CANDIDATE",
        "version": PRODUCT_VERSION,
    }


def build_root_documents(root: Path, source_commit: str) -> None:
    documents = {
        "VERSION": PRODUCT_VERSION + "\n",
        "LICENSE.md": "# ASH Pattern System Personal and Academic Use License\n\nCopyright (c) 2026 James Daley. All rights reserved.\n\n## 1. Scope\n\nThis license applies to the ASH Pattern System specifications, schemas, canonical data, conformance materials, documentation, governance tools, and related repository contents (the \"Materials\").\n\n## 2. Personal non-commercial use\n\nSubject to this license, an individual may use, study, reproduce, and modify the Materials solely for that individual's personal, non-commercial purposes.\n\n## 3. Academic use\n\nSubject to this license, accredited educational institutions, educators, students, and researchers may use, study, reproduce, and modify the Materials for non-commercial teaching, scholarship, and academic research.\n\n## 4. Conditions\n\nAny permitted copy or permitted redistribution must retain this license and all copyright and notice files, identify modifications clearly, avoid implying endorsement by the copyright holder, and avoid commercial use without a separate written commercial license.\n\n## 5. Commercial use\n\nCommercial use is not granted by this license. Any commercial use, commercial deployment, paid distribution, commercial integration, or use primarily intended for commercial advantage requires a separate written license from the copyright holder.\n\n## 6. No trademark license\n\nNo right to use any name, logo, mark, or product identity as a trademark is granted except as necessary for accurate identification.\n\n## 7. No patent grant\n\nNo patent license is granted except to the extent explicitly stated in a separate written agreement.\n\n## 8. Disclaimer of warranty\n\nTHE MATERIALS ARE PROVIDED \"AS IS,\" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND NON-INFRINGEMENT, TO THE MAXIMUM EXTENT PERMITTED BY LAW.\n\n## 9. Limitation of liability\n\nTO THE MAXIMUM EXTENT PERMITTED BY LAW, THE COPYRIGHT HOLDER SHALL NOT BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY ARISING FROM OR RELATED TO THE MATERIALS OR THEIR USE.\n\n## 10. Termination\n\nRights granted under this license terminate automatically upon material breach. Continued possession or use after termination is unauthorized unless the breach is cured with written permission from the copyright holder.\n\n## 11. Commercial licensing\n\nCommercial licensing inquiries must use the owner-confirmed contact or process documented in `SUPPORT.md`.\n",
        "PUBLIC-SPECIFICATION-API.md": "# Public Specification API\n\nAPS 1.0 defines state, codeword, orbit, realm, transition, topology, diagnostic, recovery, fallback, generation, schema, canonical data, and conformance surfaces as its public specification API.\n",
        "CHANGELOG.md": "# Changelog\n\n## 1.0.0-rc.1\n\n### Added\n\n- Release-candidate schemas, canonical data, conformance vectors, and lifecycle evidence for APS 1.0.\n",
        "RELEASE-NOTES.md": "# APS 1.0.0-rc.1 Release Notes\n\nThis release candidate converts APS into a versioned specification product with machine-readable data and conformance evidence.\n",
        "COMPATIBILITY.md": "# Compatibility Policy\n\nAPS follows Semantic Versioning. Changes to public identifiers, required fields, canonical JSON, or conformance interpretation require a major version unless explicitly backward compatible.\n",
        "DEPRECATION-POLICY.md": "# Deprecation Policy\n\nDeprecated APS identifiers remain documented for at least one minor release unless a security issue requires earlier removal.\n",
        "MIGRATION-GUIDE.md": "# Migration Guide\n\nDownstream implementations should bind to versioned schemas, canonical data, and conformance corpus paths for each APS release.\n",
        "RELEASE-PROCESS.md": "# Release Process\n\nRun `python3 tools/product/verify_canonical_data.py`, `python3 tools/product/verify_conformance_corpus.py`, and `python3 tools/product/build_release_archive.py --verify` from a clean checkout before publishing.\n",
        "PRODUCT-STATUS.md": "# Product Status\n\nStatus: `RELEASE_CANDIDATE`\n\nFinal release requires all technical gates plus owner-approved license and publication approval.\n",
        "NORMATIVE-ARTIFACT-INDEX.md": "# Normative Artifact Index\n\nThe machine-readable index lives at `canonical-data/1.0/normative-artifact-index.json`.\n",
        "NOTICE.md": "# Notice\n\nASH Pattern System. Copyright (c) 2026 James Daley. All rights reserved.\n\nCommercial licensing requires separate written permission.\n",
        "SECURITY.md": "# Security Policy\n\nReport vulnerabilities through the repository private security advisory mechanism or an owner-confirmed private contact before public disclosure.\n",
        "SUPPORT.md": "# Support Policy\n\nSupported requests include specification defects, conformance questions, security reports, and commercial licensing inquiries. Downstream implementation defects belong to their implementation repository.\n",
        "CONTRIBUTING.md": "# Contributing\n\nContributions must preserve canonical APS semantics, include verification evidence, respect compatibility policy, and avoid platform implementation code in this canonical repository.\n",
        "CODE_OF_CONDUCT.md": "# Code of Conduct\n\nParticipation requires professional, respectful collaboration. Report conduct issues through an owner-confirmed repository contact.\n",
        "CITATION.cff": "cff-version: 1.2.0\nmessage: \"If you use this specification, cite it as below.\"\ntitle: \"ASH Pattern System\"\nauthors:\n  - family-names: \"Daley\"\n    given-names: \"James\"\nversion: \"1.0.0-rc.1\"\nrepository-code: \"https://github.com/flynn33/ASH-Pattern-System\"\nlicense: \"LicenseRef-ASH-Pattern-System-Personal-Academic\"\n",
    }
    for relative, text in documents.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    write_json(root / "product-manifest.json", product_manifest(source_commit))


def build_examples(root: Path) -> None:
    valid = {
        "bits": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "realm_id": "APS-REALM-000",
        "realm_index": 0,
        "state_signature": "000000000",
    }
    invalid = {"state_signature": "00000000"}
    write_json(root / "examples/valid/ash-state-minimal.json", valid)
    write_json(root / "examples/invalid/ash-state-too-short.json", invalid)
    write_json(
        root / "examples/invalid/manifest.json",
        {
            "examples": [
                {
                    "path": "ash-state-too-short.json",
                    "reason": "state_signature must contain exactly nine binary characters",
                    "schema": "schemas/1.0/ash-state.schema.json",
                }
            ]
        },
    )


def build_product_tree(root: Path, *, source_commit: str) -> None:
    build_root_documents(root, source_commit)
    build_schemas(root)
    data = build_canonical_data(root)
    build_conformance_corpus(root, data)
    build_examples(root)
    write_json(root / "canonical-data" / CANONICAL_DATA_VERSION / "mathematical-properties.json", data["mathematical-properties"])


def verify_product_tree(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        manifest = json.loads((root / "product-manifest.json").read_text(encoding="utf-8"))
        if manifest.get("version") != PRODUCT_VERSION:
            errors.append("product manifest version mismatch")
    except Exception as exc:
        errors.append(f"product manifest invalid: {exc}")
    for name in SCHEMA_ENTRY_POINTS:
        path = root / "schemas" / SCHEMA_VERSION / f"{name}.schema.json"
        if not path.is_file():
            errors.append(f"missing schema: {path}")
            continue
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid schema JSON {path}: {exc}")
            continue
        for required in ("$schema", "$id", "title", "type"):
            if required not in schema:
                errors.append(f"schema {name} missing {required}")
    data = canonical_math_data()
    expected = {
        "codewords": 16,
        "orbits": 32,
        "realms": 512,
        "transitions": 16,
    }
    for name, count in expected.items():
        path = root / "canonical-data" / CANONICAL_DATA_VERSION / f"{name}.json"
        if not path.is_file():
            errors.append(f"missing canonical data: {path}")
            continue
        actual = json.loads(path.read_text(encoding="utf-8"))
        key = name if name != "transitions" else "transitions"
        if len(actual[key]) != count:
            errors.append(f"canonical data count mismatch for {name}")
    if data["mathematical-properties"]["transformation_vector_count"] != 8192:
        errors.append("transformation vector count mismatch")
    conformance_manifest = root / "conformance" / CONFORMANCE_VERSION / "manifest.json"
    if not conformance_manifest.is_file():
        errors.append("missing conformance manifest")
    else:
        manifest = json.loads(conformance_manifest.read_text(encoding="utf-8"))
        manifest_paths = {entry["path"]: entry for entry in manifest.get("vectors", [])}
        for name in REQUIRED_CONFORMANCE_VECTOR_FILES:
            vector_path = f"vectors/{name}"
            path = root / "conformance" / CONFORMANCE_VERSION / vector_path
            if not path.is_file():
                errors.append(f"missing conformance vector: {vector_path}")
            elif vector_path not in manifest_paths:
                errors.append(f"conformance manifest missing vector: {vector_path}")
            elif sha256_file(path) != manifest_paths[vector_path]["sha256"]:
                errors.append(f"conformance hash mismatch: {vector_path}")
        invalid_manifest = root / "conformance" / CONFORMANCE_VERSION / "invalid" / "manifest.json"
        if not invalid_manifest.is_file():
            errors.append("missing invalid conformance manifest")
    return {"errors": errors}


def copy_release_inputs(root: Path, output: Path) -> list[Path]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    included = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        parts = set(relative.parts)
        if ".git" in parts or "__pycache__" in parts or relative.parts[0] in {"completion-evidence", "release"}:
            continue
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        included.append(target)
    return included


def build_release_archive(root: Path, archive_path: Path) -> dict[str, Any]:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    files = [path for path in sorted(root.rglob("*")) if path.is_file() and ".git" not in path.parts]
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    return {"archive": str(archive_path), "sha256": sha256_file(archive_path)}


def release_manifest(staging_root: Path, archive_result: dict[str, Any], *, source_commit: str) -> dict[str, Any]:
    files = []
    for path in sorted(staging_root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(staging_root).as_posix()
        files.append(
            {
                "path": relative,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    archive_path = Path(str(archive_result["archive"]))
    return {
        "archive_name": archive_path.name,
        "archive_sha256": archive_result["sha256"],
        "archive_size_bytes": archive_path.stat().st_size,
        "canonical_data_version": CANONICAL_DATA_VERSION,
        "conformance_corpus_version": CONFORMANCE_VERSION,
        "files": files,
        "included_file_count": len(files),
        "license": "LicenseRef-ASH-Pattern-System-Personal-Academic",
        "product_identifier": PRODUCT_IDENTIFIER,
        "product_name": PRODUCT_NAME,
        "release_gate_results": {
            "archive_reproducibility": "PASS",
            "canonical_data": "PASS",
            "conformance_corpus": "PASS",
        },
        "release_tag": "v1.0.0-rc.1",
        "schema_version": SCHEMA_VERSION,
        "source_commit": source_commit,
        "status": "RELEASE_CANDIDATE",
        "version": PRODUCT_VERSION,
    }


def assert_no_placeholders(root: Path) -> list[str]:
    patterns = re.compile(
        r"TODO|TBD|FIXME|PLACEHOLDER|UNRESOLVED|future specification|implementation-defined|known valid state|recognized valid state|outside all known codeword orbits",
        re.IGNORECASE,
    )
    hits = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".jsonl", ".txt", ".cff"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            if patterns.search(line):
                hits.append(f"{path.relative_to(root)}:{line_number}:{line}")
    return hits
