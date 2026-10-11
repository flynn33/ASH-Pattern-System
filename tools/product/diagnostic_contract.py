"""Canonical diagnostic shape, semantic identity, and causal safety validation."""
from __future__ import annotations

import hashlib
import json
from typing import Any

KINDS = ("INPUT_VALIDATION", "STATE_ASSESSMENT", "CLASSIFICATION", "TRANSITION",
         "TOPOLOGY", "AXIOM", "GENERATION_PLAN", "EMISSION", "RECOVERY", "FALLBACK",
         "CONTAINMENT", "SAFE_HALT", "SCHEMA_VALIDATION", "CONFORMANCE", "STATE_VALIDITY")
SEVERITIES = ("INFO", "WARNING", "ERROR", "CRITICAL")
DISPOSITIONS = ("RECORDED", "RESOLVED", "PENDING", "BLOCKED", "ESCALATED", "TERMINAL")
SAFETY_PHASES = {"DETECTION": 0, "PARSE": 0, "CLASSIFICATION": 1, "ASSESS": 1,
                 "CLASSIFY": 1, "RECOVERY": 2, "RECOVER": 2, "FALLBACK": 2,
                 "ESCALATION": 3, "CONTAIN": 3, "TERMINAL": 4, "HALT": 4}
OPERATION_STAGES = ("TRANSFORM", "PLAN", "EVALUATE", "EMIT", "VALIDATE", "VERIFY")
IDENTITY_FIELDS = ("diagnostic_kind", "disposition", "rule_ids", "severity", "stage",
                   "subject_reference", "summary", "notes", "details")
ID_PATTERN = "^APS-DIAG-[0-9A-F]{24}$"
RULE_PATTERN = "^ASH-(?:INPUT|STATE|CODEWORD|ORBIT|REALM|TRANSITION|TOPOLOGY|AXIOM|CLASSIFICATION|RECOVERY|FALLBACK|CONTAINMENT|HALT|GENERATION|EMISSION|DIAGNOSTIC|CONFORMANCE|RELEASE|SECURITY|ADMISSIBILITY)(?:-[A-Z]+)*-[0-9]{3}$"


def record_schema() -> dict[str, Any]:
    text = {"type": "string", "minLength": 1}
    diagnostic_id = {"type": "string", "pattern": ID_PATTERN}
    properties = {
        "schema_version": {"type": "string", "const": "1.0"},
        "diagnostic_id": diagnostic_id,
        "diagnostic_kind": {"type": "string", "enum": list(KINDS)},
        "severity": {"type": "string", "enum": list(SEVERITIES)},
        "stage": {"type": "string", "enum": list(SAFETY_PHASES) + list(OPERATION_STAGES)},
        "disposition": {"type": "string", "enum": list(DISPOSITIONS)},
        "subject_reference": text,
        "parent_diagnostic_id": {"type": ["string", "null"], "pattern": ID_PATTERN},
        "chain_root_diagnostic_id": diagnostic_id,
        "sequence_number": {"type": "integer", "minimum": 1},
        "rule_ids": {"type": "array", "minItems": 1, "items": {"type": "string", "pattern": RULE_PATTERN}},
        "summary": text,
        "notes": {"type": "array", "minItems": 1, "items": text},
        "details": {"type": "object"},
        "occurrence_metadata": {"type": ["object", "null"]},
    }
    return {"type": "object", "additionalProperties": False, "properties": properties,
            "required": list(properties)}


def value_errors(value: Any, location: str) -> list[str]:
    """Reject nonportable numeric and Unicode values before canonical serialization."""
    if value is None or isinstance(value, bool):
        return []
    if isinstance(value, int):
        return [] if -(2**63) <= value < 2**63 else [f"{location}: integer outside signed 64-bit range"]
    if isinstance(value, str):
        return [] if all(not 0xD800 <= ord(char) <= 0xDFFF for char in value) else [f"{location}: invalid Unicode scalar"]
    if isinstance(value, list):
        return [error for index, item in enumerate(value) for error in value_errors(item, f"{location}[{index}]")]
    if isinstance(value, dict):
        errors = []
        for key, item in value.items():
            if not isinstance(key, str):
                errors.append(f"{location}: object key must be a string")
            else:
                errors.extend(value_errors(key, f"{location}.key"))
                errors.extend(value_errors(item, f"{location}.{key}"))
        return errors
    return [f"{location}: unsupported diagnostic JSON value"]


def semantic_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {key: record[key] for key in IDENTITY_FIELDS}


def identity(record: dict[str, Any]) -> str:
    payload = semantic_payload(record)
    errors = value_errors(payload, "payload")
    if errors:
        raise ValueError("; ".join(errors))
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    return "APS-DIAG-" + hashlib.sha256(encoded).hexdigest()[:24].upper()


def make_record(payload: dict[str, Any], parent: dict[str, Any] | None = None,
                occurrence_metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    diagnostic_id = identity(payload)
    return {**semantic_payload(payload), "schema_version": "1.0", "diagnostic_id": diagnostic_id,
            "parent_diagnostic_id": parent["diagnostic_id"] if parent else None,
            "chain_root_diagnostic_id": parent["chain_root_diagnostic_id"] if parent else diagnostic_id,
            "sequence_number": parent["sequence_number"] + 1 if parent else 1,
            "occurrence_metadata": occurrence_metadata}


def wrapper(record: dict[str, Any], product_version: str) -> dict[str, Any]:
    return {"schema_version": "1.0", "product_version": product_version,
            "id": record["diagnostic_id"], "data": record}


def record_errors(record: dict[str, Any]) -> list[str]:
    # Import at the boundary to share the product's schema validator without an
    # import-time cycle: aps_product also uses this module to construct schemas.
    from tools.product.aps_product import validate_instance
    errors = validate_instance(record, record_schema(), "diagnostic")
    if errors:
        return errors
    errors.extend(value_errors(record, "diagnostic"))
    if any(key not in record for key in IDENTITY_FIELDS):
        return errors + ["diagnostic: missing semantic identity field"]
    for key in ("subject_reference", "summary"):
        if not isinstance(record[key], str) or not record[key].strip():
            errors.append(f"diagnostic.{key}: empty explanatory value")
    if isinstance(record["summary"], str) and any(char in record["summary"] for char in "\r\n"):
        errors.append("diagnostic.summary: must be one line")
    if not isinstance(record["notes"], list) or not record["notes"] or any(
            not isinstance(note, str) or not note.strip() for note in record["notes"]):
        errors.append("diagnostic.notes: nonempty explanatory notes required")
    try:
        if identity(record) != record.get("diagnostic_id"):
            errors.append("diagnostic.diagnostic_id: stale or invalid semantic identity")
    except (ValueError, TypeError, KeyError) as exc:
        errors.append(f"diagnostic.diagnostic_id: cannot serialize semantic payload: {exc}")
    return errors


def chain_errors(records: list[dict[str, Any]]) -> list[str]:
    if not records:
        return ["diagnostic chain: empty chain"]
    errors = []
    if any(not isinstance(record, dict) for record in records):
        return ["diagnostic chain: records must be objects"]
    root = records[0]
    if root.get("parent_diagnostic_id") is not None or root.get("sequence_number") != 1:
        errors.append("diagnostic chain: root must have null parent and sequence 1")
    root_id = root.get("diagnostic_id")
    previous_phase = None
    for index, record in enumerate(records):
        errors.extend(record_errors(record))
        if record.get("chain_root_diagnostic_id") != root_id:
            errors.append(f"diagnostic chain[{index}]: inconsistent root")
        phase = SAFETY_PHASES.get(record.get("stage"))
        if index:
            parent = records[index - 1]
            if record.get("severity") in SEVERITIES and parent.get("severity") in SEVERITIES:
                if SEVERITIES.index(record["severity"]) < SEVERITIES.index(parent["severity"]):
                    errors.append(f"diagnostic chain[{index}]: severity decreases within causal chain")
            if record.get("parent_diagnostic_id") != parent.get("diagnostic_id"):
                errors.append(f"diagnostic chain[{index}]: missing immediate predecessor")
            if record.get("sequence_number") != index + 1:
                errors.append(f"diagnostic chain[{index}]: skipped or cyclic sequence")
            if (parent.get("stage") in ("TERMINAL", "HALT") or parent.get("diagnostic_kind") == "SAFE_HALT"
                    or parent.get("disposition") == "TERMINAL"):
                errors.append(f"diagnostic chain[{index}]: terminal parent forbids children")
            if phase is None and previous_phase is not None and previous_phase >= 3:
                errors.append(f"diagnostic chain[{index}]: ordinary operation after containment")
            if phase is not None and previous_phase is not None and phase < previous_phase:
                errors.append(f"diagnostic chain[{index}]: backwards safety phase")
            if phase == 3 and previous_phase != 3 and previous_phase not in (1, 2):
                errors.append(f"diagnostic chain[{index}]: containment requires assessment or recovery")
            if phase == 3 and previous_phase == 3 and record.get("diagnostic_kind") != "CONTAINMENT":
                errors.append(f"diagnostic chain[{index}]: same-phase containment management requires CONTAINMENT kind")
            if phase == 4 and previous_phase not in (2, 3):
                errors.append(f"diagnostic chain[{index}]: halt requires recovery or containment")
        if phase is not None:
            previous_phase = phase
    return errors


def containment_outcome(inputs: dict[str, Any]) -> dict[str, Any]:
    """Outcome of the specified safety observation, never an implicit breach guess."""
    mode = inputs.get("initial_mode")
    if mode == "CONTAINED":
        breach = inputs.get("boundary_breached")
        prevented = inputs.get("attempt_prevented")
        propagated = inputs.get("propagation_observed")
        if not all(isinstance(value, bool) for value in (breach, prevented, propagated)):
            raise ValueError("containment observation requires Boolean boundary, prevention, and propagation evidence")
        if breach != propagated or (breach and prevented):
            raise ValueError("containment evidence is inconsistent")
    if mode == "SAFE_HALT":
        return {"mode": "SAFE_HALT", "terminal": True, "transitions_allowed": False,
                "diagnostics_preserved": True, "diagnostics_frozen": True, "chain_append_count": 0,
                "expected_failure": "TERMINAL_NO_RECOVERY"}
    if mode == "CONTAINED" and inputs.get("boundary_breached") is True:
        return {"mode": "SAFE_HALT", "terminal": True, "transitions_allowed": False,
                "diagnostics_preserved": True, "diagnostics_frozen": True, "chain_append_count": 2,
                "breach_confirmed": True}
    if mode == "CONTAINED" and inputs.get("boundary_breached") is False and inputs.get("attempt_prevented") is True:
        return {"mode": "CONTAINED", "restricted_operations_only": True, "terminal": False,
                "transitions_allowed": False, "diagnostics_preserved": True,
                "diagnostics_frozen": False, "chain_append_count": 1, "breach_confirmed": False}
    if mode == "DEGRADED" and inputs.get("risk") == "PROPAGATION_BLOCKED":
        return {"mode": "CONTAINED", "restricted_operations_only": True, "terminal": False,
                "diagnostics_preserved": True, "diagnostics_frozen": False, "chain_append_count": 1}
    raise ValueError("containment vector requires explicit containment/halt preconditions and boundary evidence")
