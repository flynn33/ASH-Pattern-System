# Mobile Implementation Handoff Template

## Target class

**Mobile application** — a native or cross-platform mobile application implementing the ASH Pattern System.

## Canonical-authority boundary

The canonical agnostic repository is the semantic authority. This template constrains the downstream mobile repository structure, required deliverables, and proof-of-conformance inputs. It does not override canonical semantics, prescribe a specific programming language, or mandate a specific mobile framework.

## Required sections in downstream repository

### 1. Target environment
Document the specific mobile target:
- Platform(s) (e.g., iOS, Android, cross-platform)
- Minimum OS version requirements
- Runtime environment
- App lifecycle model (foreground, background, suspended)
- Native UI framework (if applicable)
- Concurrency / threading model

### 2. Semantic-module mapping
Map each of the 9 canonical semantic modules to concrete mobile implementation modules. See `common-downstream-handoff-requirements.md` for the full module list.

### 3. Invariant / conformance verification inputs
Document how the mobile implementation will verify conformance:
- Test framework and tooling
- Coverage of all 5 conformance categories
- How invariants are tested on mobile (device, simulator, CI)
- Any mobile-specific verification considerations

### 4. Diagnostics integration
Document how diagnostics will be surfaced in the mobile context:
- Diagnostic output format and destination (on-device logs, remote telemetry, debug UI)
- Schema and taxonomy conformance
- Chain integrity under mobile app lifecycle constraints (backgrounding, termination)

### 5. Materialization-boundary expectations
Document how the planner/emitter boundary is respected:
- Where planning occurs in the mobile application lifecycle
- Where materialization occurs (local storage, network emission, UI rendering)
- How the boundary is enforced given mobile resource constraints

### 6. Packaging / build / deployment decisions
Document target-specific decisions:
- Build system and toolchain
- Dependency management
- App store packaging and distribution
- Over-the-air update strategy (if applicable)
- Configuration management

### 7. Performance / resource constraints
Document mobile-specific constraints:
- Memory budget (constrained compared to desktop/service)
- Battery impact requirements
- Startup time and responsiveness requirements
- Storage constraints (on-device limits)
- Network bandwidth / offline operation requirements
- Thermal / CPU throttling considerations

### 8. Caveat / deviation tracking
Maintain a deviation log for any departures from canonical semantics. See `common-downstream-handoff-requirements.md` for tracking requirements.

### 9. Proof-of-conformance deliverables
Produce all deliverables listed in `common-downstream-handoff-requirements.md` before the mobile implementation is considered implementation-ready.
