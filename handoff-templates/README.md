# Handoff Templates

## Purpose

This directory contains **downstream build handoff templates** for the ASH Pattern System.

Each template defines what a downstream implementation repository must contain, how it must map to the canonical specifications, and what proof-of-conformance deliverables it must produce — without prescribing a specific programming language, framework, or implementation stack.

## Authority model

The **canonical agnostic repository** remains the semantic authority. Handoff templates constrain downstream repository structure, required deliverables, and proof-of-conformance inputs. They do not override canonical semantics.

Downstream implementations must satisfy:
1. The canonical specifications in `specs/`
2. The contract layer in `specs/interfaces/`
3. The verification layer in `specs/verification/`
4. The handoff requirements defined here

## Contents

| File | Description |
|---|---|
| `common-downstream-handoff-requirements.md` | Universal requirements every downstream handoff must satisfy |
| `desktop-implementation-handoff-template.md` | Template for desktop target class |
| `mobile-implementation-handoff-template.md` | Template for mobile target class |
| `service-implementation-handoff-template.md` | Template for service/backend target class |

## Usage

A coding agent building a downstream implementation should:

1. Read the canonical specifications, contracts, and verification requirements first
2. Read `common-downstream-handoff-requirements.md` for universal handoff expectations
3. Read the appropriate target-class template for the implementation target
4. Use the template to structure the downstream repository, plan deliverables, and track conformance
