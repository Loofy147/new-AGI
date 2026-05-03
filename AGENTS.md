# Epistemological Engine Agent Directives

## Coding Conventions
- **Modular Library**: Core logic resides in the `episteme` package. Use its high-level APIs (`TheoryCartridge`, `lp_manifold`, etc.) for all theoretical analysis.
- **Vectorization First**: Avoid loops for linear algebra. Use `numpy` matrix multiplication (`@`) and broadcasting.
- **Precision Logic**: Use exact solvers (`scipy.optimize.linprog` with `method='highs'`) for global consensus.
- **Robustness**: Always implement O(1) analytic adversarial solvers for linear objectives over a simplex.

## Mathematical Principles
- **The Theory Manifold**: Constrain consensus solutions to the convex hull of existing theories (mixtures) to ensure theoretical realism.
- **Q-Score Framework**: Theoretical quality is measured by minimax consensus across antagonistic weight scenarios.
- **Semantic Extraction**: Dimensions are derived via LSA (TF-IDF + Truncated SVD) for reproducibility and local execution.

## Execution
- `unified_engine.py`: Entry point for full cross-domain Singularity execution.
- `results/`: Output directory for JSON results and LaTeX preprints.
- `episteme/`: Reusable library package for epistemological analysis.

## Project Hierarchy
- `episteme/`: Core library (Consensus, Robustness, Embedding, Isomorphism).
- `unified_engine.py`: Integrated execution script.
- `paper_generator.py`: LaTeX synthesis logic.
