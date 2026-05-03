# Episteme: Epistemological Engine

A library for finding minimax consensus among competing theoretical frameworks and evaluating their robustness.

## Features
- **LP Manifold Consensus**: Exact Linear Programming solver for finding optimal theoretical mixtures constrained to the convex hull of existing theories.
- **Analytic Adversarial Stress Testing**: O(1) greedy solvers and vectorized Dirichlet scenario testing for theoretical fragility.
- **Semantic Domain Embedding**: LSA-based embedding (TF-IDF + SVD) for extracting latent dimensions from scientific corpora.
- **Cross-Domain Isomorphism Mapping**: Statistical identification of structural similarities across disparate fields.

## Core Primitives
- `episteme.lp_manifold`: Finds the consensus singularity.
- `episteme.stress_vectorized`: Measures robustness across antagonistic weight scenarios.
- `episteme.TheoryCartridge`: Managed object for domain-specific analysis.
