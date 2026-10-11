# Diagnostic and containment consistency correction

## What changed

Correct the directly related diagnostic prose, vocabulary, identity payload, machine schemas, generator, examples, and conformance expectations. Required notes now explain actual conditions; details and occurrence metadata project in full. Explicit safety phases replace an unsupported enum order. Confirmed breaches finish in terminal SAFE_HALT; successfully prevented attempts remain CONTAINED.

## Why

The earlier corpus emitted empty notes despite the normative requirement for meaningful explanatory content, used a seven-field digest that omitted semantic explanations, and ended its breach operation at FAILED despite the mandatory safe-halt contract. Machine schemas did not validate these record fields. The correction is versioned as 1.0.0-rc.2, with independent regression assertions and complete field comparison.

## Baseline preservation statement

The full nine-bit F2^9 state space, all 512 states, the fixed sixteen codewords, thirty-two orbits, XOR-by-codeword transitions, b8 preservation, exact averaging, branching semantics, operational-context classification predicates, five axiom predicates, and fallback registry policies/order are unchanged. The original 7bb68bf3377b18c74d4b0ace6a561371e446bbee commit remains immutable. No platform implementation is added here.
