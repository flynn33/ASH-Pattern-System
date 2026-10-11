"""Independent assertions from the diagnostic and containment requirements.

Expected identities are derived with hashlib and explicit fields, not with the
generator's identity helper. Safety results are literal normative assertions.
"""
import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.product import aps_product, diagnostic_contract as contract


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "7bb68bf3377b18c74d4b0ace6a561371e446bbee"


def independent_record(stage="ASSESS", kind="STATE_ASSESSMENT", parent=None, disposition="RECORDED"):
    payload = {"diagnostic_kind": kind, "disposition": disposition, "rule_ids": ["ASH-STATE-001"],
               "severity": "ERROR", "stage": stage, "subject_reference": "subject-1",
               "summary": "Candidate observed", "notes": ["The nine-bit candidate was assessed using its declared context."], "details": {}}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    identifier = "APS-DIAG-" + hashlib.sha256(encoded).hexdigest()[:24].upper()
    return {**payload, "schema_version": "1.0", "diagnostic_id": identifier, "occurrence_metadata": None,
            "parent_diagnostic_id": parent["diagnostic_id"] if parent else None,
            "chain_root_diagnostic_id": parent["chain_root_diagnostic_id"] if parent else identifier,
            "sequence_number": parent["sequence_number"] + 1 if parent else 1}


def independent_chain(stages):
    chain = []
    for stage in stages:
        kind = "SAFE_HALT" if stage in ("HALT", "TERMINAL") else "CONTAINMENT" if stage in ("CONTAIN", "ESCALATION") else "STATE_ASSESSMENT"
        chain.append(independent_record(stage, kind, chain[-1] if chain else None,
                     "TERMINAL" if kind == "SAFE_HALT" else "RECORDED"))
    return chain


class DiagnosticRequirementsTests(unittest.TestCase):
    def test_identity_covers_exact_nine_semantic_fields(self):
        record = independent_record()
        self.assertEqual(record["diagnostic_id"], contract.identity(record))
        self.assertEqual([], contract.record_errors(record))
        for key, value in (("diagnostic_kind", "CLASSIFICATION"), ("disposition", "BLOCKED"),
                           ("rule_ids", ["ASH-RECOVERY-001"]), ("severity", "CRITICAL"), ("stage", "CLASSIFY"),
                           ("subject_reference", "different"), ("summary", "Changed condition"),
                           ("notes", ["Changed semantic explanation"]), ("details", {"state": "000000001"})):
            changed = copy.deepcopy(record)
            changed[key] = value
            with self.subTest(field=key):
                self.assertNotEqual(record["diagnostic_id"], contract.identity(changed))
                self.assertTrue(contract.record_errors(changed))

    def test_occurrence_and_chain_placement_do_not_change_identity(self):
        record = independent_record()
        record.update(occurrence_metadata={"timestamp": "2026-10-11T00:00:00Z", "host": "host-b", "process": 7},
                      parent_diagnostic_id="APS-DIAG-" + "1" * 24, chain_root_diagnostic_id="APS-DIAG-" + "2" * 24, sequence_number=99)
        self.assertEqual(record["diagnostic_id"], contract.identity(record))
        self.assertEqual([], contract.record_errors(record))

    def test_arbitrary_and_stale_ids_are_rejected(self):
        record = independent_record()
        record["diagnostic_id"] = "APS-DIAG-" + "0" * 24
        self.assertTrue(contract.record_errors(record))
        record["diagnostic_id"] = "arbitrary"
        self.assertTrue(contract.record_errors(record))

    def test_unknown_vocabulary_and_bad_rule_families_rejected(self):
        for field, value in (("stage", "UNKNOWN"), ("diagnostic_kind", "UNKNOWN"),
                             ("severity", "UNKNOWN"), ("disposition", "UNKNOWN"),
                             ("rule_ids", ["ASH-UNKNOWN-001"])):
            record = independent_record()
            record[field] = value
            record["diagnostic_id"] = contract.identity(record)
            self.assertTrue(contract.record_errors(record), field)

    def test_nonempty_meaningful_fields_required(self):
        for key, value in (("summary", ""), ("summary", "two\nlines"), ("notes", []), ("notes", [""]), ("notes", [" "])):
            record = independent_record()
            record[key] = value
            record["diagnostic_id"] = contract.identity(record)
            self.assertTrue(contract.record_errors(record), key)

    def test_root_and_child_projection_preserve_required_fields(self):
        root = independent_record()
        child = independent_record("RECOVER", "RECOVERY", root)
        child["occurrence_metadata"] = {"host": "é-host", "timestamp": "2026-10-11T00:00:00Z"}
        for record in (root, child):
            projection = {"schema_version": "1.0", "product_version": "1.0.0-rc.2", "id": record["diagnostic_id"], "data": record}
            self.assertEqual([], aps_product.validate_diagnostic_projection(projection))
            for key in ("schema_version", "details", "occurrence_metadata", "parent_diagnostic_id", "chain_root_diagnostic_id", "sequence_number"):
                invalid = copy.deepcopy(projection)
                del invalid["data"][key]
                self.assertTrue(aps_product.validate_diagnostic_projection(invalid), key)
        self.assertEqual([], contract.chain_errors([root, child]))

    def test_wrapper_identity_and_version_consistency_required(self):
        record = independent_record()
        projection = contract.wrapper(record, "1.0.0-rc.2")
        projection["id"] = "APS-DIAG-" + "0" * 24
        self.assertTrue(aps_product.validate_diagnostic_projection(projection))
        projection = contract.wrapper(record, "1.0.0-rc.2")
        projection["schema_version"] = "2.0"
        self.assertTrue(aps_product.validate_diagnostic_projection(projection))

    def test_modern_and_legacy_safety_phases(self):
        for stages in (("PARSE", "ASSESS", "CLASSIFY", "RECOVER", "CONTAIN", "HALT"),
                       ("DETECTION", "CLASSIFICATION", "RECOVERY", "ESCALATION", "TERMINAL")):
            self.assertEqual([], contract.chain_errors(independent_chain(stages)))

    def test_operation_labels_have_no_total_order_and_carry_phase(self):
        self.assertEqual([], contract.chain_errors(independent_chain(("CLASSIFY", "VERIFY", "PLAN", "EVALUATE", "RECOVER", "VALIDATE", "CONTAIN", "HALT"))))
        self.assertTrue(contract.chain_errors(independent_chain(("RECOVER", "PLAN", "ASSESS"))))
        self.assertTrue(contract.chain_errors(independent_chain(("CLASSIFY", "CONTAIN", "PLAN"))))

    def test_backward_and_skipped_safety_escalations_rejected(self):
        for stages in (("RECOVER", "ASSESS"), ("PARSE", "CONTAIN"), ("ASSESS", "HALT"), ("CONTAIN", "RECOVER")):
            self.assertTrue(contract.chain_errors(independent_chain(stages)), stages)

    def test_causal_severity_may_not_decrease(self):
        root = independent_record()
        child = independent_record("RECOVER", "RECOVERY", root)
        child["severity"] = "WARNING"
        child["diagnostic_id"] = contract.identity(child)
        self.assertTrue(contract.chain_errors([root, child]))

    def test_containment_management_stays_contained(self):
        chain = independent_chain(("ASSESS", "RECOVER", "CONTAIN"))
        for disposition in ("BLOCKED", "RECORDED", "PENDING", "ESCALATED", "RESOLVED"):
            child = independent_record("CONTAIN", "CONTAINMENT", chain[-1], disposition)
            self.assertEqual([], contract.chain_errors(chain + [child]), disposition)
        child = independent_record("CONTAIN", "RECOVERY", chain[-1])
        self.assertTrue(contract.chain_errors(chain + [child]))

    def test_terminal_rejects_every_child_regardless_label(self):
        for stage, kind, disposition in (("HALT", "SAFE_HALT", "TERMINAL"), ("RECOVER", "SAFE_HALT", "RECORDED"), ("RECOVER", "RECOVERY", "TERMINAL")):
            root = independent_record(stage, kind, disposition=disposition)
            for child_stage in ("PARSE", "ASSESS", "RECOVER", "CONTAIN", "HALT", "VERIFY"):
                self.assertTrue(contract.chain_errors([root, independent_record(child_stage, parent=root)]))

    def test_orphans_roots_sequences_and_cycles_rejected(self):
        chain = independent_chain(("ASSESS", "RECOVER", "CONTAIN"))
        for index, field, value in ((0, "parent_diagnostic_id", chain[-1]["diagnostic_id"]),
                                    (1, "parent_diagnostic_id", None), (1, "sequence_number", 5),
                                    (2, "chain_root_diagnostic_id", chain[1]["diagnostic_id"])):
            changed = copy.deepcopy(chain)
            changed[index][field] = value
            self.assertTrue(contract.chain_errors(changed))

    def test_portable_unicode_nested_integers_and_invalid_values(self):
        record = independent_record()
        record["details"] = {"é": [None, True, -(2**63), 2**63 - 1], "a": {"𐀀": "quote\" newline\n"}}
        expected = json.dumps({key: record[key] for key in ("diagnostic_kind", "disposition", "rule_ids", "severity", "stage", "subject_reference", "summary", "notes", "details")}, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        self.assertEqual("APS-DIAG-" + hashlib.sha256(expected.encode("utf-8")).hexdigest()[:24].upper(), contract.identity(record))
        for invalid in (1.5, float("nan"), 2**63, -(2**63) - 1, "\ud800", {1: "bad key"}):
            changed = copy.deepcopy(record)
            changed["details"] = {"value": invalid}
            with self.assertRaises(ValueError):
                contract.identity(changed)


class SafetyOutcomeRequirementsTests(unittest.TestCase):
    def test_confirmed_breach_finishes_at_frozen_terminal_halt(self):
        result = contract.containment_outcome({"initial_mode": "CONTAINED", "boundary_breached": True,
                 "attempt_prevented": False, "propagation_observed": True})
        self.assertEqual("SAFE_HALT", result["mode"])
        self.assertTrue(result["terminal"])
        self.assertFalse(result["transitions_allowed"])
        self.assertTrue(result["diagnostics_preserved"])
        self.assertTrue(result["diagnostics_frozen"])
        self.assertEqual(2, result["chain_append_count"])

    def test_prevented_write_remains_contained_with_one_denial_record(self):
        result = contract.containment_outcome({"initial_mode": "CONTAINED", "boundary_breached": False,
                 "attempt_prevented": True, "propagation_observed": False})
        self.assertEqual("CONTAINED", result["mode"])
        self.assertTrue(result["restricted_operations_only"])
        self.assertTrue(result["diagnostics_preserved"])
        self.assertFalse(result["terminal"])
        self.assertFalse(result["diagnostics_frozen"])
        self.assertEqual(1, result["chain_append_count"])

    def test_after_halt_rejection_never_appends_or_mutates(self):
        result = contract.containment_outcome({"initial_mode": "SAFE_HALT", "attempted_transition": "APS-TRANSITION-CW-01"})
        self.assertEqual("SAFE_HALT", result["mode"])
        self.assertEqual("TERMINAL_NO_RECOVERY", result["expected_failure"])
        self.assertEqual(0, result["chain_append_count"])
        self.assertTrue(result["diagnostics_frozen"])
        self.assertFalse(result["transitions_allowed"])

    def test_attempt_name_does_not_imply_breach(self):
        for inputs in ({"attempted_operation": "UNDECLARED_WRITE"},
                       {"initial_mode": "CONTAINED", "boundary_breached": True, "attempt_prevented": True, "propagation_observed": True},
                       {"initial_mode": "CONTAINED", "boundary_breached": True, "attempt_prevented": False, "propagation_observed": False}):
            with self.assertRaises(ValueError):
                contract.containment_outcome(inputs)

    def test_safety_snapshots_schema_validate_and_preserve_full_chain(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            aps_product.build_examples(root)
            for name in ("containment-record", "safe-halt-record"):
                record = json.loads((root / f"examples/valid/{name}.json").read_text())
                self.assertEqual([], aps_product.validate_diagnostic_projection(record, name))
                del record["data"]["full_diagnostic_chain"][1]
                self.assertTrue(aps_product.validate_diagnostic_projection(record, name))

    def test_corpus_all_declared_fields_checked_and_tampering_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            aps_product.build_conformance_corpus(root, aps_product.canonical_math_data())
            self.assertEqual([], aps_product.validate_conformance_semantics(root))
            path = root / "conformance/1.0/vectors/diagnostics.jsonl"
            rows = [json.loads(line) for line in path.read_text().splitlines()]
            rows[0]["expected_output"]["notes"] = []
            aps_product.write_jsonl(path, rows)
            errors = aps_product.validate_conformance_semantics(root)
            self.assertTrue(any("APS-VEC-DIAGNOSTIC-01" in error for error in errors))


class ImmutableBaselineRequirementsTests(unittest.TestCase):
    def test_product_regeneration_preserves_corrected_authoritative_release_docs(self):
        documents = ("COMPATIBILITY.md", "MIGRATION-GUIDE.md", "CHANGELOG.md", "RELEASE-NOTES.md", "RELEASE-PROCESS.md")
        expected = {name: (ROOT / name).read_bytes() for name in documents}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            aps_product.build_product_tree(root, source_commit="1" * 40)
            for name, contents in expected.items():
                self.assertEqual(contents, (root / name).read_bytes(), name)
            aps_product.build_product_tree(root, source_commit="1" * 40)
            for name, contents in expected.items():
                self.assertEqual(contents, (root / name).read_bytes(), name)

    def test_license_metadata_matches_existing_terms_without_reintroducing_removed_file(self):
        baseline_license = subprocess.check_output(["git", "show", f"{BASELINE}:LICENSE"], cwd=ROOT)
        self.assertEqual(baseline_license, (ROOT / "LICENSE").read_bytes())
        self.assertEqual("Apache-2.0", json.loads((ROOT / "product-manifest.json").read_text())["license"])
        self.assertIn('license: "Apache-2.0"', (ROOT / "CITATION.cff").read_text())
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            aps_product.build_root_documents(root, "1" * 40)
            self.assertEqual(baseline_license, (root / "LICENSE").read_bytes())
            self.assertEqual((ROOT / "NOTICE.md").read_bytes(), (root / "NOTICE.md").read_bytes())
            self.assertNotIn("Commercial licensing requires separate written permission", (root / "NOTICE.md").read_text())
            self.assertFalse((root / "LICENSE.md").exists())
            self.assertEqual("Apache-2.0", json.loads((root / "product-manifest.json").read_text())["license"])
            self.assertIn('license: "Apache-2.0"', (root / "CITATION.cff").read_text())
            archive = aps_product.build_release_archive(root, root / "license-fixture.zip")
            try:
                release = aps_product.release_manifest(root, archive, source_commit="1" * 40)
                self.assertEqual("Apache-2.0", release["license"])
                with zipfile.ZipFile(archive["archive"]) as package:
                    self.assertEqual((ROOT / "NOTICE.md").read_bytes(), package.read("NOTICE.md"))
                    self.assertEqual(baseline_license, package.read("LICENSE"))
                    self.assertNotIn("LICENSE.md", package.namelist())
            finally:
                Path(archive["archive"]).unlink()

    def test_locked_math_context_axioms_and_registry_bytes_preserved(self):
        paths = ["canonical-data/1.0/" + name + ".json" for name in
                 ("codewords", "orbits", "realms", "transitions", "fallback-policy-definitions", "mathematical-properties", "rule-registry")]
        paths += ["specs/core/ash-state-space.pseudo.md", "specs/core/codeword-set.pseudo.md",
                  "specs/core/state-admissibility.pseudo.md", "specs/core/system-state-classification.pseudo.md",
                  "specs/registries/fallback-policy-registry.md", "specs/algorithms/axiom-evaluation.pseudo.md",
                  "specs/algorithms/averaging-operator-semantics.pseudo.md", "specs/algorithms/branching-semantics.pseudo.md"]
        paths += ["release/ash-pattern-system-1.0.0-rc.1.zip", "release/release-manifest.json", "release/SHA256SUMS"]
        for relative in paths:
            baseline = subprocess.check_output(["git", "show", f"{BASELINE}:{relative}"], cwd=ROOT)
            self.assertEqual(baseline, (ROOT / relative).read_bytes(), relative)

    def test_all_8192_transitions_follow_independent_integer_xor(self):
        codewords = (0, 30, 102, 120, 170, 180, 204, 210, 300, 306, 330, 340, 390, 408, 480, 510)
        rows = [json.loads(line) for line in (ROOT / "conformance/1.0/vectors/transformations.jsonl").read_text().splitlines()]
        self.assertEqual(8192, len(rows))
        observed = set()
        for row in rows:
            source = int(row["source_signature"], 2)
            rank = int(row["codeword_id"].split("-")[-1])
            self.assertEqual(format(source ^ codewords[rank], "09b"), row["target_signature"])
            self.assertEqual(source & 1, int(row["target_signature"], 2) & 1)
            observed.add((source, rank))
        self.assertEqual({(source, rank) for source in range(512) for rank in range(16)}, observed)


if __name__ == "__main__":
    unittest.main()
