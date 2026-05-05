"""
episteme.engine
===============
High-level orchestration for multi-domain theoretical resolution.
"""
from __future__ import annotations
import numpy as np
from typing import List, Dict, Optional, Any
from .cartridge import Cartridge, CartridgeResult, resolve
from .isomorphism import cross_domain_correlations, IsomorphismResult
from .report import generate_text_report, generate_latex
from .export import export_json
from .embed import LSAEmbedder, NumericEmbedder
from .autopoiesis import evolved_weights

class SingularityEngine:
    """
    Orchestrates the full Episteme pipeline across multiple domains.
    """
    def __init__(self, n_dims: int = 8, use_sbert: bool = False):
        self.embedder = LSAEmbedder(n_dims=n_dims, use_sbert=use_sbert)
        self.cartridges: List[Cartridge] = []
        self.results: List[CartridgeResult] = []
        self.isomorphisms: List[IsomorphismResult] = []

    def add_cartridge(self, name: str, corpus: List[tuple[str, str]], weights: Dict[str, np.ndarray], dim_labels: Optional[List[str]] = None):
        c = Cartridge(name=name, corpus=corpus, weights=weights, embedder=self.embedder, dim_labels=dim_labels)
        self.cartridges.append(c)

    def run(self, fit_globally: bool = True):
        """Runs resolution for all cartridges."""
        # Only fit if not a numeric embedder and fitting requested
        if fit_globally and not isinstance(self.embedder, NumericEmbedder):
            global_corpus = []
            for c in self.cartridges:
                global_corpus.extend(c.corpus)
            if global_corpus:
                try:
                    self.embedder.fit(global_corpus)
                except Exception as e:
                    print(f"  Warning: Global embedding fit failed ({e}). Using local fallback.")

        self.results = []
        for c in self.cartridges:
            res = resolve(c)
            self.results.append(res)

        self.isomorphisms = cross_domain_correlations(self.results)
        return self.results

    def run_autopoietic(self, cycles: int = 3, fit_globally: bool = True):
        """
        Runs resolution iteratively, evolving party weights to address weaknesses.
        """
        print(f"Starting Autopoietic Singularity ({cycles} cycles)...")
        for i in range(cycles):
            print(f"  Cycle {i+1}/{cycles}...")
            self.run(fit_globally=(fit_globally and i == 0))

            if i < cycles - 1:
                for idx, res in enumerate(self.results):
                    c = self.cartridges[idx]
                    c.weights = evolved_weights(c.weights, res)

        return self.results

    def get_report(self) -> str:
        return generate_text_report(self.results)

    def export(self, report_path: str = "results/unified_report.txt",
               latex_path: str = "results/unified_preprint.tex",
               json_path: str = "results/unified_results.json") -> Dict[str, str]:

        import os
        for path in [report_path, latex_path, json_path]:
            os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None

        with open(report_path, 'w') as f:
            f.write(self.get_report())

        with open(latex_path, 'w') as f:
            f.write(generate_latex(self.results))

        export_json(self.results, json_path)

        return {"report": report_path, "latex": latex_path, "json": json_path}
