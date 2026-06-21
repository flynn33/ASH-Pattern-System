#!/usr/bin/env python3
"""Command-line entry points for APS product tooling."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from tools.product import aps_product


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def current_commit(root: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def self_test(name: str) -> int:
    with tempfile.TemporaryDirectory(prefix=f"aps-{name}-") as tmpdir:
        root = Path(tmpdir)
        aps_product.build_product_tree(root, source_commit="0" * 40)
        report = aps_product.verify_product_tree(root)
        if report["errors"]:
            print(f"{name}: SELF-TEST FAIL")
            for error in report["errors"]:
                print(f"- {error}")
            return 1
    print(f"{name}: SELF-TEST PASS")
    return 0


def generate_canonical_data(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("generate-canonical-data")
    aps_product.build_schemas(args.root)
    data = aps_product.build_canonical_data(args.root)
    aps_product.build_examples(args.root)
    aps_product.write_json(
        args.root / "canonical-data" / aps_product.CANONICAL_DATA_VERSION / "mathematical-properties.json",
        data["mathematical-properties"],
    )
    print("Canonical data generated.")
    return 0


def verify_canonical_data(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("verify-canonical-data")
    report = aps_product.verify_product_tree(args.root)
    if report["errors"]:
        print("Canonical data verification failed.")
        for error in report["errors"]:
            print(f"- {error}")
        return 1
    print("Canonical data verification passed.")
    return 0


def generate_conformance_corpus(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("generate-conformance-corpus")
    data = aps_product.canonical_math_data()
    aps_product.build_conformance_corpus(args.root, data)
    print("Conformance corpus generated.")
    return 0


def verify_conformance_corpus(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("verify-conformance-corpus")
    manifest = args.root / "conformance" / aps_product.CONFORMANCE_VERSION / "manifest.json"
    if not manifest.is_file():
        print("Conformance manifest is missing.")
        return 1
    data = json.loads(manifest.read_text(encoding="utf-8"))
    errors = []
    for entry in data.get("vectors", []):
        path = manifest.parent / entry["path"]
        if not path.is_file():
            errors.append(f"missing vector file: {entry['path']}")
        elif aps_product.sha256_file(path) != entry["sha256"]:
            errors.append(f"hash mismatch: {entry['path']}")
    if errors:
        print("Conformance corpus verification failed.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Conformance corpus verification passed.")
    return 0


def validate_schemas(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("validate-schemas")
    errors = aps_product.validate_schema_surfaces(args.root)
    if errors:
        print("Schema validation failed.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Schema validation passed.")
    return 0


def validate_rule_registry(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("validate-rule-registry")
    errors = aps_product.validate_rule_registry_surfaces(args.root)
    if errors:
        print("Rule registry validation failed.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Rule registry validation passed.")
    return 0


def validate_traceability(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("validate-traceability")
    errors = aps_product.validate_traceability_surfaces(args.root)
    if errors:
        print("Traceability validation failed.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Traceability validation passed.")
    return 0


def build_release_archive(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--output", type=Path, default=repo_root() / "release")
    parser.add_argument("--source-commit")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("build-release-archive")
    staging = args.output / "staging"
    second = args.output / "ash-pattern-system-1.0.0-rc.1.second.zip"
    source_commit = args.source_commit or current_commit(args.root)
    if not aps_product.HEX_SHA_RE.fullmatch(source_commit):
        print("source commit must be a full lowercase commit SHA")
        return 1
    try:
        aps_product.copy_release_inputs(args.root, staging)
        aps_product.stamp_product_manifest(staging, source_commit)
        archive = args.output / "ash-pattern-system-1.0.0-rc.1.zip"
        result = aps_product.build_release_archive(staging, archive)
        manifest = aps_product.release_manifest(staging, result, source_commit=source_commit)
        manifest_path = args.output / "release-manifest.json"
        aps_product.write_json(manifest_path, manifest)
        (args.output / "SHA256SUMS").write_text(
            f"{result['sha256']}  {archive.name}\n"
            f"{aps_product.sha256_file(manifest_path)}  {manifest_path.name}\n",
            encoding="utf-8",
        )
        if args.verify:
            second_result = aps_product.build_release_archive(staging, second)
            if result["sha256"] != second_result["sha256"]:
                print("Release archive is not reproducible.")
                return 1
    finally:
        if staging.exists():
            shutil.rmtree(staging)
        if second.exists():
            second.unlink()
    print(f"Release archive built: {archive}")
    return 0


def release_readiness(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--source-commit")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("release-readiness")
    if args.source_commit and not aps_product.HEX_SHA_RE.fullmatch(args.source_commit):
        print("source commit must be a full lowercase commit SHA")
        return 1
    errors = aps_product.release_readiness_errors(args.root, args.source_commit)
    if errors:
        print("Release readiness failed.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Release readiness passed.")
    return 0


def verify_release_archive(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test("verify-release-archive")
    if args.archive is None or not args.archive.is_file():
        print("Release archive path is missing.")
        return 1
    with tempfile.TemporaryDirectory(prefix="aps-release-verify-") as tmpdir:
        shutil.unpack_archive(str(args.archive), tmpdir)
        report = aps_product.verify_product_tree(Path(tmpdir))
        if report["errors"]:
            print("Release archive verification failed.")
            for error in report["errors"]:
                print(f"- {error}")
            return 1
    print("Release archive verification passed.")
    return 0


COMMANDS = {
    "generate_canonical_data": generate_canonical_data,
    "verify_canonical_data": verify_canonical_data,
    "generate_conformance_corpus": generate_conformance_corpus,
    "verify_conformance_corpus": verify_conformance_corpus,
    "validate_schemas": validate_schemas,
    "validate_rule_registry": validate_rule_registry,
    "validate_traceability": validate_traceability,
    "build_release_archive": build_release_archive,
    "verify_release_archive": verify_release_archive,
    "release_readiness": release_readiness,
}


def main(command: str, argv: list[str] | None = None) -> int:
    return COMMANDS[command](list(sys.argv[1:] if argv is None else argv))
