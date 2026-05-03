# Epistemological Engine Agent Directives

## Coding Conventions
- **Vectorization First**: Avoid loops for linear algebra. Use `numpy` matrix multiplication (`@`) and broadcasting.
- **Precision Logic**: Use exact solvers (`scipy.optimize.linprog` with `method='highs'`) for global consensus rather than stochastic hill-climbing.
- **Robustness**: Always implement O(1) analytic adversarial solvers for linear objectives over a simplex.

## Mathematical Principles
- **The Theory Manifold**: Never optimize into the raw hypercube $[0,1]^N$. Always constrain solutions to the convex hull of existing theories (mixtures) to ensure physical/theoretical realism.
- **Q-Score Framework**: Theoretical quality is measured by the minimax consensus across antagonistic weighting scenarios.
- **Semantic Extraction**: Dimensions must be derived from principal components of scientific text embeddings, not manual estimates.

## Execution
- The unified pipeline is found in `unified_engine.py`.
- Results are stored in `results/`.
- Large model weights (e.g., MiniLM) are handled via `sentence-transformers`.

## Project Hierarchy
- `unified_engine.py`: Entry point for all future theoretical work.
- `paper_generator.py`: Central logic for paper synthesis.
- `arxiv_bridge_v3.py`: Shared utility for ArXiv data ingestion.
