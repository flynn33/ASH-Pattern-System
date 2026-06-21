import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.product import aps_product


class CanonicalMathTests(unittest.TestCase):
    def test_codewords_are_closed_rank_four_and_preserve_b8(self):
        codewords = aps_product.canonical_codewords()
        self.assertEqual(16, len(codewords))
        self.assertEqual("000000000", codewords[0])
        self.assertEqual(16, len(set(codewords)))
        self.assertEqual(4, aps_product.gf2_rank([aps_product.bits(value) for value in codewords]))
        for left in codewords:
            self.assertEqual("0", left[-1])
            for right in codewords:
                self.assertIn(aps_product.xor_signature(left, right), codewords)

    def test_orbits_partition_all_512_states(self):
        data = aps_product.canonical_math_data()
        realms = data["realms"]["realms"]
        orbits = data["orbits"]["orbits"]
        self.assertEqual(512, len(realms))
        self.assertEqual(32, len(orbits))
        self.assertEqual(512, len({item["realm_id"] for item in realms}))
        members = []
        for orbit in orbits:
            self.assertEqual(16, orbit["member_count"])
            member_signatures = [member["state_signature"] for member in orbit["members"]]
            self.assertEqual(orbit["representative_signature"], min(member_signatures))
            members.extend(member_signatures)
        self.assertEqual(512, len(members))
        self.assertEqual(512, len(set(members)))


class ProductOutputTests(unittest.TestCase):
    def test_topology_depth_two_is_deterministic(self):
        result = aps_product.topology_result(2)
        self.assertEqual(13, result["total_nodes"])
        self.assertEqual(9, result["leaf_count"])
        self.assertEqual("APS-NODE-R", result["nodes"][0]["node_id"])
        self.assertEqual("APS-NODE-R.C.C", result["leaves"][0]["node_id"])
        self.assertEqual("APS-NODE-R.N.N", result["leaves"][-1]["node_id"])

    def test_canonical_json_is_stable_and_hashable(self):
        first = {"b": [2, 1], "a": {"d": True, "c": None}}
        second = {"a": {"c": None, "d": True}, "b": [2, 1]}
        self.assertEqual(aps_product.canonical_json(first), aps_product.canonical_json(second))
        self.assertEqual(64, len(aps_product.sha256_text(aps_product.canonical_json(first))))

    def test_build_and_verify_product_tree(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            aps_product.build_product_tree(root, source_commit="0" * 40)
            report = aps_product.verify_product_tree(root)
            self.assertEqual([], report["errors"])
            self.assertEqual("1.0.0-rc.1", json.loads((root / "product-manifest.json").read_text())["version"])
            self.assertTrue((root / "canonical-data/1.0/codewords.json").is_file())
            self.assertTrue((root / "conformance/1.0/manifest.json").is_file())
            self.assertTrue((root / "schemas/1.0/ash-state.schema.json").is_file())
            self.assertTrue((root / "LICENSE.md").is_file())

    def test_conformance_layout_matches_product_package(self):
        required_vector_files = {
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
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            aps_product.build_product_tree(root, source_commit="0" * 40)
            corpus = root / "conformance/1.0"
            for name in required_vector_files:
                with self.subTest(vector=name):
                    self.assertTrue((corpus / "vectors" / name).is_file())
            self.assertTrue((corpus / "invalid").is_dir())
            manifest = json.loads((corpus / "manifest.json").read_text())
            manifest_paths = {entry["path"] for entry in manifest["vectors"]}
            for name in required_vector_files:
                self.assertIn(f"vectors/{name}", manifest_paths)
            self.assertIn("invalid/manifest.json", manifest_paths)

    def test_generated_product_tree_contains_no_blocked_language(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            aps_product.build_product_tree(root, source_commit="0" * 40)
            self.assertEqual([], aps_product.assert_no_placeholders(root))

    def test_repeated_product_generation_keeps_manifest_hashes_stable(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            aps_product.build_product_tree(root, source_commit="0" * 40)
            aps_product.build_product_tree(root, source_commit="0" * 40)
            manifest = json.loads((root / "conformance/1.0/manifest.json").read_text())
            manifest_paths = {entry["path"] for entry in manifest["vectors"]}
            self.assertNotIn("SHA256SUMS", manifest_paths)
            for entry in manifest["vectors"]:
                path = root / "conformance/1.0" / entry["path"]
                self.assertEqual(entry["sha256"], aps_product.sha256_file(path))

    def test_release_manifest_includes_archive_and_file_inventory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "source"
            output = Path(tmpdir) / "release"
            root.mkdir()
            aps_product.build_product_tree(root, source_commit="0" * 40)
            staging = output / "staging"
            aps_product.copy_release_inputs(root, staging)
            archive_result = aps_product.build_release_archive(staging, output / "aps.zip")
            manifest = aps_product.release_manifest(staging, archive_result, source_commit="0" * 40)
            self.assertEqual("ASH Pattern System", manifest["product_name"])
            self.assertEqual("1.0.0-rc.1", manifest["version"])
            self.assertEqual(archive_result["sha256"], manifest["archive_sha256"])
            self.assertIn("VERSION", {entry["path"] for entry in manifest["files"]})
            self.assertGreater(manifest["included_file_count"], 10)

    def test_normative_index_excludes_release_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "release").mkdir()
            (root / "release" / "artifact.zip").write_text("not indexed\n", encoding="utf-8")
            aps_product.build_product_tree(root, source_commit="0" * 40)
            index = json.loads((root / "canonical-data/1.0/normative-artifact-index.json").read_text())
            indexed_paths = {entry["path"] for entry in index["artifacts"]}
            self.assertNotIn("release/artifact.zip", indexed_paths)

    def test_schema_validation_rejects_valid_example_with_unknown_field(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            aps_product.build_product_tree(root, source_commit="0" * 40)
            example_path = root / "examples/valid/ash-state-minimal.json"
            example = json.loads(example_path.read_text(encoding="utf-8"))
            example["unexpected"] = True
            example_path.write_text(json.dumps(example), encoding="utf-8")

            errors = aps_product.validate_schema_surfaces(root)

            self.assertTrue(any("unexpected" in error for error in errors), errors)

    def test_schema_validation_rejects_invalid_source_commit_format(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            aps_product.build_product_tree(root, source_commit="not-a-commit")

            errors = aps_product.validate_schema_surfaces(root)

            self.assertTrue(any("source_commit" in error for error in errors), errors)

    def test_traceability_validation_requires_all_rule_ids(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            aps_product.build_product_tree(root, source_commit="0" * 40)
            evidence = root / "completion-evidence"
            evidence.mkdir()
            (evidence / "traceability-matrix.md").write_text(
                "# Traceability Matrix\n\n`ASH-STATE-001`\n",
                encoding="utf-8",
            )

            errors = aps_product.validate_traceability_surfaces(root)

            self.assertTrue(any("ASH-SECURITY-001" in error for error in errors), errors)

    def test_release_archive_cli_uses_explicit_source_commit_and_cleans_work_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "source"
            output = Path(tmpdir) / "release"
            source_commit = "2" * 40
            root.mkdir()
            aps_product.build_product_tree(root, source_commit=source_commit)

            result = subprocess.run(
                [
                    sys.executable,
                    str(Path("tools/product/build_release_archive.py")),
                    "--root",
                    str(root),
                    "--output",
                    str(output),
                    "--source-commit",
                    source_commit,
                    "--verify",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            self.assertEqual(0, result.returncode, result.stdout)
            self.assertFalse((output / "staging").exists())
            self.assertFalse((output / "ash-pattern-system-1.0.0-rc.1.second.zip").exists())
            manifest = json.loads((output / "release-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(source_commit, manifest["source_commit"])
            with zipfile.ZipFile(output / "ash-pattern-system-1.0.0-rc.1.zip") as archive:
                archived_manifest = json.loads(archive.read("product-manifest.json"))
            self.assertEqual(source_commit, archived_manifest["source_commit"])

    def test_release_archive_cli_stamps_staged_product_manifest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "source"
            output = Path(tmpdir) / "release"
            release_commit = "3" * 40
            stale_commit = "4" * 40
            root.mkdir()
            aps_product.build_product_tree(root, source_commit=stale_commit)

            result = subprocess.run(
                [
                    sys.executable,
                    str(Path("tools/product/build_release_archive.py")),
                    "--root",
                    str(root),
                    "--output",
                    str(output),
                    "--source-commit",
                    release_commit,
                    "--verify",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            self.assertEqual(0, result.returncode, result.stdout)
            self.assertEqual(stale_commit, json.loads((root / "product-manifest.json").read_text())["source_commit"])
            with zipfile.ZipFile(output / "ash-pattern-system-1.0.0-rc.1.zip") as archive:
                archived_manifest = json.loads(archive.read("product-manifest.json"))
            self.assertEqual(release_commit, archived_manifest["source_commit"])

    def test_release_readiness_rejects_root_manifest_release_mismatch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "source"
            output = root / "release"
            release_commit = "3" * 40
            stale_commit = "4" * 40
            root.mkdir()
            aps_product.build_product_tree(root, source_commit=stale_commit)

            result = subprocess.run(
                [
                    sys.executable,
                    str(Path("tools/product/build_release_archive.py")),
                    "--root",
                    str(root),
                    "--output",
                    str(output),
                    "--source-commit",
                    release_commit,
                    "--verify",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            self.assertEqual(0, result.returncode, result.stdout)
            errors = aps_product.validate_release_outputs(root, release_commit)
            self.assertTrue(
                any("root product-manifest.json source_commit does not match release-manifest.json" in error for error in errors),
                errors,
            )

    def test_required_command_entrypoints_support_self_test(self):
        commands = [
            "generate_canonical_data.py",
            "verify_canonical_data.py",
            "generate_conformance_corpus.py",
            "verify_conformance_corpus.py",
            "validate_schemas.py",
            "validate_rule_registry.py",
            "validate_traceability.py",
            "build_release_archive.py",
            "verify_release_archive.py",
            "release_readiness.py",
        ]
        for command in commands:
            with self.subTest(command=command):
                result = subprocess.run(
                    [sys.executable, str(Path("tools/product") / command), "--self-test"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                self.assertEqual(0, result.returncode, result.stdout)


if __name__ == "__main__":
    unittest.main()
