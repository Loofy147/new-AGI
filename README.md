# Epistemological Engine V3: The Unified Collapse

A system for autonomous cross-domain scientific discovery, mathematical theory resolution, and formal paper generation.

## Features
- **Unified Singularity Engine**: Resolves six major theoretical domains (Physics, Aging, Economics, AGI, Consciousness, Autopoiesis) as a single mathematical object.
- **Manifold-Constrained LP**: Uses Linear Programming to find consensus theoretical profiles within the convex hull of existing research, ensuring mathematical validity.
- **Data-Driven Grounding**: Integrated **ArXiv Bridge** uses NLP (SentenceTransformers) and PCA to derive theoretical dimensions from live scientific abstracts.
- **Isomorphism Mapping**: Identifies structural parallels between disparate fields (e.g., AGI compiler scaling/verification vs Neuroscience predictive/structural tensions).
- **Exact Adversarial Verification**: O(1) greedy analytic solver for robustness testing and fragility analysis.

## Repository Structure
- `unified_engine.py`: The primary entry point. Executes the unified pipeline and generates results.
- `paper_generator.py`: Results-to-LaTeX compiler for scientific preprints.
- `results/`: Directory containing machine-computed results (`.json`) and LaTeX preprints (`.tex`).
- `data/`: Static corpora and training data.
- `legacy/`: Archive of Phase 4 and Phase 5 developmental scripts and legacy domain engines.

## Usage
To execute the unified epistemological collapse:
```bash
python3 unified_engine.py
```
This will fetch live data, compute consensus mixtures across all domains, map isomorphisms, and generate a unified preprint in `results/unified_preprint.tex`.

## Dependencies
- `numpy`, `scipy`, `scikit-learn`
- `sentence-transformers`
- `huggingface_hub` (for embedding models)
