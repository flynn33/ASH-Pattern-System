# Service Implementation Handoff Template

## Target class

**Service / backend** — a server-side service, API, or backend system implementing the ASH Pattern System.

## Canonical-authority boundary

The canonical agnostic repository is the semantic authority. This template constrains the downstream service repository structure, required deliverables, and proof-of-conformance inputs. It does not override canonical semantics, prescribe a specific programming language, or mandate a specific service framework.

## Required sections in downstream repository

### 1. Target environment
Document the specific service target:
- Runtime environment (container, serverless, VM, bare metal)
- Hosting model (cloud provider, self-hosted, edge)
- API surface (REST, gRPC, WebSocket, message queue)
- Concurrency / scaling model (horizontal, vertical, auto-scaling)
- Network / isolation model

### 2. Semantic-module mapping
Map each of the 9 canonical semantic modules to concrete service implementation modules. See `common-downstream-handoff-requirements.md` for the full module list.

### 3. Invariant / conformance verification inputs
Document how the service implementation will verify conformance:
- Test framework and tooling
- Coverage of all 5 conformance categories
- How invariants are tested in the service environment (unit, integration, end-to-end)
- Any service-specific verification considerations (distributed systems, eventual consistency)

### 4. Diagnostics integration
Document how diagnostics will be surfaced in the service context:
- Diagnostic output format and destination (structured logs, observability platform, metrics)
- Schema and taxonomy conformance
- Chain integrity in distributed / multi-instance service environments
- Diagnostic correlation across service boundaries (if applicable)

### 5. Materialization-boundary expectations
Document how the planner/emitter boundary is respected:
- Where planning occurs in the service request lifecycle
- Where materialization occurs (response emission, file generation, downstream service calls)
- How the boundary is enforced in a concurrent / multi-tenant service environment

### 6. Packaging / build / deployment decisions
Document target-specific decisions:
- Build system and toolchain
- Dependency management
- Container / image format (if applicable)
- Deployment pipeline (CI/CD, blue-green, canary)
- Configuration management (environment variables, config services)
- Secret management

### 7. Performance / resource constraints
Document service-specific constraints:
- Latency requirements (p50, p99)
- Throughput requirements (requests per second, concurrent connections)
- Memory and CPU budgets
- Storage requirements
- Scaling boundaries (horizontal, vertical limits)
- Cold-start considerations (if serverless)

### 8. Caveat / deviation tracking
Maintain a deviation log for any departures from canonical semantics. See `common-downstream-handoff-requirements.md` for tracking requirements.

### 9. Proof-of-conformance deliverables
Produce all deliverables listed in `common-downstream-handoff-requirements.md` before the service implementation is considered implementation-ready.
