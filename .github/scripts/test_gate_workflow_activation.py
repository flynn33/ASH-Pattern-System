"""Adversarial activation/hardening tests; existing policy cases remain intact."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from gate_integrity_selftest import ROOT, assert_workflow_hardening
from gate_integrity_check import evaluate


class WorkflowActivationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "governance", self.root / "governance")
        shutil.copytree(ROOT / ".github", self.root / ".github")
        self.manifest = self.root / "governance/workflow-activation.json"
        self.workflow = self.root / ".github/workflows/no-ai-attribution.yml"

    def alter(self, change):
        document = json.loads(self.manifest.read_text())
        change(document)
        self.manifest.write_text(json.dumps(document), encoding="utf-8")

    def test_current_active_inventory_is_hardened(self):
        assert_workflow_hardening(self.root)

    def test_missing_active_workflow_rejected(self):
        self.workflow.unlink()
        with self.assertRaises(AssertionError):
            assert_workflow_hardening(self.root)

    def test_extra_and_yaml_workflow_rejected(self):
        for name in ("extra.yml", "extra.yaml"):
            added = self.workflow.parent / name
            added.write_text("name: Extra\n", encoding="utf-8")
            with self.assertRaises(AssertionError):
                assert_workflow_hardening(self.root)
            added.unlink()

    def test_required_attribution_workflow_cannot_be_undeclared(self):
        self.alter(lambda data: data.update(active_workflows=[]))
        self.workflow.unlink()
        with self.assertRaises(AssertionError):
            assert_workflow_hardening(self.root)

    def test_duplicate_overlapping_and_unsafe_inventory_rejected(self):
        original = self.manifest.read_text()
        mutations = (
            lambda data: data["active_workflows"].append("no-ai-attribution.yml"),
            lambda data: data["active_workflows"].append("../escape.yml"),
            lambda data: data["retired_workflows"].append(copy.deepcopy(data["retired_workflows"][0])),
            lambda data: data["active_workflows"].append(data["retired_workflows"][0]["workflow"]),
            lambda data: data.update(active_workflows="no-ai-attribution.yml"),
            lambda data: data.update(schema_version="2.0"),
        )
        for mutation in mutations:
            self.manifest.write_text(original, encoding="utf-8")
            self.alter(mutation)
            with self.assertRaises(AssertionError):
                assert_workflow_hardening(self.root)

    def test_retirement_requires_exact_commit_and_retained_script(self):
        original = self.manifest.read_text()
        for field, value in (("retirement_commit", "short"), ("script", ".github/scripts/missing.py")):
            self.manifest.write_text(original, encoding="utf-8")
            self.alter(lambda data: data["retired_workflows"][0].update({field: value}))
            with self.assertRaises(AssertionError):
                assert_workflow_hardening(self.root)

    def test_unpinned_action_and_failure_bypasses_rejected(self):
        original = self.workflow.read_text()
        for text in (original.replace("@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0", "@main"),
                     original + "\n- uses: actions/checkout@main\n",
                     original + "\ncontinue-on-error: true\n", original + '\nREPORT_ONLY: "1"\n'):
            self.workflow.write_text(text, encoding="utf-8")
            with self.assertRaises(AssertionError):
                assert_workflow_hardening(self.root)

    def test_reactivated_gate_retains_trusted_base_requirements(self):
        gate = self.workflow.parent / "gate-integrity.yml"
        self.alter(lambda data: (data["active_workflows"].append("gate-integrity.yml"),
                   data.update(retired_workflows=[entry for entry in data["retired_workflows"] if entry["workflow"] != "gate-integrity.yml"])))
        gate.write_text("pull_request_target:\ncontents: read\npull-requests: read\ngithub.event.pull_request.base.sha\ngate_integrity_check.py\n", encoding="utf-8")
        assert_workflow_hardening(self.root)
        for token in ("pull_request_target:", "contents: read", "pull-requests: read", "github.event.pull_request.base.sha", "gate_integrity_check.py"):
            original = gate.read_text()
            gate.write_text(original.replace(token, "removed"), encoding="utf-8")
            with self.assertRaises(AssertionError):
                assert_workflow_hardening(self.root)
            gate.write_text(original, encoding="utf-8")

    def test_activation_manifest_stays_protected_and_mixed_changes_rejected(self):
        records = [{"filename": "governance/workflow-activation.json", "status": "modified"}]
        self.assertFalse(evaluate(records, set(), "release/rc2", "1" * 40, []).ok)
        records.append({"filename": "tools/product/aps_product.py", "status": "modified"})
        reviews = [{"user": {"login": "flynn33"}, "state": "APPROVED", "commit_id": "1" * 40}]
        self.assertFalse(evaluate(records, {"governance-change"}, "governance/activation", "1" * 40, reviews).ok)


if __name__ == "__main__":
    unittest.main()
