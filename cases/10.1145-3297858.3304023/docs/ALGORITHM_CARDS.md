# Algorithm Cards

This file replaces formula cards for this algorithm paper. Numerical scripts
must point to these cards before using a method.

## ALG001: Qubit Mapping Problem

- Source: Problem Analysis section.
- Status: source_verified.

Given a circuit and a coupling graph, find:

- an initial logical-to-physical mapping;
- inserted SWAPs that update the mapping during execution;
- a final hardware-compliant circuit.

Objectives:

- reduce additional gates, especially SWAP-induced CNOTs;
- control circuit depth;
- scale to irregular NISQ coupling graphs.

## ALG002: Distance Matrix

- Source: Preprocessing section.
- Status: implemented.

Compute all-pairs shortest paths on the physical coupling graph. Each coupling
edge has distance 1. `D[i][j]` is the minimum number of SWAPs required to move a
logical qubit from physical qubit `Qi` to `Qj`.

## ALG003: Circuit DAG and Front Layer

- Source: Preprocessing section and Fig. 4.
- Status: implemented.

Only two-qubit gates define routing dependencies. A gate enters the front layer
when all previous two-qubit gates touching either of its qubits have executed.

## ALG004: Candidate SWAPs

- Source: Algorithm 1 and Section IV-C.
- Status: implemented.

If no front-layer gate is executable, consider only physical coupling edges
touching a physical qubit currently holding a logical qubit used by the front
layer. This is the paper's key search-space reduction.

## ALG005: Basic Heuristic

- Source: Eq. 1.
- Status: implemented.

```text
H_basic = sum_{gate in F} D[pi(gate.q1)][pi(gate.q2)]
```

Smaller values mean front-layer qubit pairs are closer on the hardware graph.

## ALG006: Look-Ahead Extended Set

- Source: Section IV-D.
- Status: implemented.

Collect nearby successor gates after the front layer into an extended set `E`.
The cost adds a weighted, normalized distance term over `E`.

## ALG007: Decay Heuristic

- Source: Eq. 2 and Section IV-E.
- Status: implemented.

```text
H = max(decay(swap.q1), decay(swap.q2))
    * ( average distance over F + W * average distance over E )
```

Recently used physical qubits receive a larger decay value, encouraging
non-overlapping SWAPs and exposing a gate-count/depth trade-off.

## ALG008: Reverse Traversal Initial Mapping

- Source: Fig. 5 and Section IV-C.
- Status: implemented.

Run SABRE forward from a temporary mapping, then run the reverse circuit from
the final mapping. The reverse final mapping becomes the improved initial
mapping for the final forward traversal.

## ALG009: Metrics

- Source: Evaluation section.
- Status: implemented.

The pilot records:

- original two-qubit gate count;
- inserted SWAP count;
- additional CNOT-equivalent gate count (`3 * swaps`);
- output depth with SWAP duration 3;
- runtime;
- final hardware-compliance check.
