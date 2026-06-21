# Desktop Implementation Handoff Template

## Target class

**Desktop application** — a native or cross-platform desktop application implementing the ASH Pattern System.

## Canonical-authority boundary

The canonical agnostic repository is the semantic authority. This template constrains the downstream desktop repository structure, required deliverables, and proof-of-conformance inputs. It does not override canonical semantics, prescribe a specific programming language, or mandate a specific desktop framework.

## Required sections in downstream repository

### 1. Target environment
Document the specific desktop target:
- Operating system(s)
- Runtime environment
- Windowing / UI framework (if applicable)
- File system access model
- Concurrency / threading model

### 2. Semantic-module mapping
Map each of the 9 canonical semantic modules to concrete desktop implementation modules. See `common-downstream-handoff-requirements.md` for the full module list.

### 3. Invariant / conformance verification inputs
Document how the desktop implementation will verify conformance:
- Test framework and tooling
- Coverage of all 5 conformance categories
- How invariants are tested in the desktop environment
- Any desktop-specific verification considerations

### 4. Diagnostics integration
Document how diagnostics will be surfaced in the desktop context:
- Diagnostic output format and destination (log files, UI, telemetry)
- Schema and taxonomy conformance
- Chain integrity in the desktop execution model

### 5. Materialization-boundary expectations
Document how the planner/emitter boundary is respected:
- Where planning occurs in the desktop application lifecycle
- Where materialization occurs, including file emission and UI rendering
- How the boundary is enforced architecturally

### 6. Packaging / build / deployment decisions
Document target-specific decisions:
- Build system and toolchain
- Dependency management
- Installer / distribution format
- Update / versioning strategy
- Configuration management

### 7. Performance / resource constraints
Document desktop-specific constraints:
- Memory budget
- Startup time requirements
- Responsiveness requirements
- Storage constraints
- Offline / disconnected operation requirements (if applicable)

### 8. Caveat / deviation tracking
Maintain a deviation log for any departures from canonical semantics. See `common-downstream-handoff-requirements.md` for tracking requirements.

### 9. Proof-of-conformance deliverables
Produce all deliverables listed in `common-downstream-handoff-requirements.md` before the desktop implementation is considered implementation-ready.
