"""Adversarial activation, hardening, and event tests; policy cases remain intact."""
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


import contextlib
import io
import os
import subprocess
from unittest.mock import patch

import no_attribution_check as sentinel


class AttributionEventTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="aps-attribution-")
        self.previous = Path.cwd()
        os.chdir(self.temporary.name)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Jim Daley")
        self.git("config", "user.email", "94642455+flynn33@users.noreply.github.com")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "tag.gpgsign", "false")
        Path("fixture.txt").write_text("Canonical source\n", encoding="utf-8")
        self.git("add", "fixture.txt")
        self.git("commit", "-m", "Initial canonical fixture")
        self.base = self.git("rev-parse", "HEAD")
        Path("fixture.txt").write_text("Canonical source candidate\n", encoding="utf-8")
        self.git("commit", "-am", "Update canonical fixture")
        self.head = self.git("rev-parse", "HEAD")
        self.git("tag", "-a", "v1.0.0-rc.2", "-m", "Canonical candidate")
        self.tag_object = self.git("rev-parse", "v1.0.0-rc.2")
        self.environment = patch.dict(os.environ, {
            "GITHUB_EVENT_NAME": "push", "GITHUB_REF_NAME": "v1.0.0-rc.2",
            "GITHUB_SHA": self.head, "GITHUB_EVENT_PATH": "",
        })
        self.environment.start()

    def tearDown(self):
        self.environment.stop()
        os.chdir(self.previous)
        self.temporary.cleanup()

    @staticmethod
    def git(*args):
        return subprocess.check_output(["git", *args], stderr=subprocess.STDOUT, text=True).strip()

    def event(self, **changes):
        return {"before": sentinel.ZERO_SHA, "after": self.head,
                "ref": "refs/tags/v1.0.0-rc.2", "created": True, "deleted": False,
                "commits": [], "head_commit": {"id": self.head}, **changes}

    def run_event(self, event):
        path = Path("event.json")
        path.write_text(json.dumps(event), encoding="utf-8")
        with patch.dict(os.environ, {"GITHUB_EVENT_PATH": str(path)}), contextlib.redirect_stdout(io.StringIO()) as output:
            result = sentinel.main()
        return result, output.getvalue()

    def test_normal_branch_range_is_unchanged(self):
        selector = sentinel.commit_selector("push", {"before": self.base, "after": self.head, "ref": "refs/heads/main"})
        self.assertEqual(f"{self.base}..{self.head}", selector)
        self.assertEqual([self.head], sentinel.commits(selector))

    def test_new_branch_requires_explicit_inventory(self):
        event = self.event(ref="refs/heads/release/candidate", commits=[{"id": self.head}])
        self.assertEqual([self.head], sentinel.commit_selector("push", event))

    def test_empty_new_branch_still_fails_closed(self):
        with self.assertRaises(sentinel.AttributionError):
            sentinel.commit_selector("push", self.event(ref="refs/heads/release/candidate"))

    def test_pull_request_range_is_unchanged(self):
        event = {"pull_request": {"base": {"sha": self.base}, "head": {"sha": self.head}}}
        self.assertEqual(f"{self.base}..{self.head}", sentinel.commit_selector("pull_request", event))

    def test_annotated_tag_with_commit_after_and_empty_inventory(self):
        event = self.event()
        self.assertEqual([self.head], sentinel.commit_selector("push", event))
        self.assertEqual({"fixture.txt"}, sentinel.changed_files([self.head]))
        self.assertEqual(0, self.run_event(event)[0])

    def test_annotated_tag_object_is_peeled_before_selection(self):
        event = self.event(after=self.tag_object)
        self.assertNotEqual(self.head, self.tag_object)
        self.assertEqual([self.head], sentinel.commit_selector("push", event))
        self.assertEqual(0, self.run_event(event)[0])

    def test_lightweight_tag_uses_same_target_checks(self):
        self.git("tag", "v1.0.0-lightweight")
        event = self.event(ref="refs/tags/v1.0.0-lightweight", head_commit=None)
        self.assertEqual([self.head], sentinel.commit_selector("push", event))
        self.assertEqual(0, self.run_event(event)[0])

    def test_wrong_tag_target_fails_closed(self):
        with self.assertRaises(sentinel.AttributionError):
            sentinel.commit_selector("push", self.event(after=self.base))

    def test_wrong_head_commit_fails_closed(self):
        with self.assertRaises(sentinel.AttributionError):
            sentinel.commit_selector("push", self.event(head_commit={"id": self.base}))

    def test_unavailable_tag_fails_closed(self):
        with self.assertRaises(sentinel.AttributionError):
            sentinel.commit_selector("push", self.event(ref="refs/tags/unavailable"))

    def test_deleted_tag_never_qualifies_publication(self):
        for changes in ({"deleted": True}, {"after": sentinel.ZERO_SHA}):
            with self.subTest(changes=changes), self.assertRaises(sentinel.AttributionError):
                sentinel.commit_selector("push", self.event(**changes))

    def test_non_sha_target_and_invalid_tag_ref_fail_closed(self):
        for changes in ({"after": "HEAD"}, {"after": "-1"}, {"ref": "refs/tags/invalid name"}):
            with self.subTest(changes=changes), self.assertRaises(sentinel.AttributionError):
                sentinel.commit_selector("push", self.event(**changes))

    def test_annotated_tag_metadata_is_checked(self):
        self.git("tag", "-a", "v1.0.0-prohibited", "-m", "Created using " + "Open" + "AI")
        event = self.event(ref="refs/tags/v1.0.0-prohibited")
        result, output = self.run_event(event)
        self.assertEqual(1, result)
        self.assertIn("annotated tag metadata", output)

    def test_target_commit_metadata_is_checked(self):
        Path("fixture.txt").write_text("Another fixture\n", encoding="utf-8")
        self.git("commit", "-am", "Created using " + "Open" + "AI")
        target = self.git("rev-parse", "HEAD")
        self.git("tag", "v1.0.0-target-check")
        result, output = self.run_event(self.event(after=target, ref="refs/tags/v1.0.0-target-check", head_commit={"id": target}))
        self.assertEqual(1, result)
        self.assertIn("commit metadata", output)

    def test_tag_name_is_checked(self):
        name = "v1.0.0-" + "ai"
        self.git("tag", name)
        with patch.dict(os.environ, {"GITHUB_REF_NAME": name}):
            result, output = self.run_event(self.event(ref="refs/tags/" + name))
        self.assertEqual(1, result)
        self.assertIn("ref name", output)

    def test_target_content_is_checked(self):
        Path("fixture.txt").write_text("Created using " + "Open" + "AI\n", encoding="utf-8")
        self.git("commit", "-am", "Change fixture contents")
        target = self.git("rev-parse", "HEAD")
        self.git("tag", "v1.0.0-content-check")
        result, output = self.run_event(self.event(after=target, ref="refs/tags/v1.0.0-content-check", head_commit={"id": target}))
        self.assertEqual(1, result)
        self.assertIn("file content", output)


if __name__ == "__main__":
    unittest.main()
