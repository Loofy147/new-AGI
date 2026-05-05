"""
episteme.engine
===============
High-level orchestration for multi-domain theoretical resolution.
"""
from __future__ import annotations
import numpy as np
from typing import List, Dict, Optional
from .cartridge import Cartridge, CartridgeResult, resolve
from .isomorphism import cross_domain_correlations, IsomorphismResult
from .report import generate_text_report, generate_latex
from .export import export_json
from .embed import LSAEmbedder

class SingularityEngine:
    """
    Orchestrates the full Episteme pipeline across multiple domains.
    """
    def __init__(self, n_dims: int = 8, use_sbert: bool = False):
        self.embedder = LSAEmbedder(n_dims=n_dims, use_sbert=use_sbert)
        self.cartridges: List[Cartridge] = []
        self.results: List[CartridgeResult] = []
        self.isomorphisms: List[IsomorphismResult] = []

    def add_cartridge(self, name: str, corpus: List[tuple[str, str]], weights: Dict[str, np.ndarray]):
        c = Cartridge(name=name, corpus=corpus, weights=weights, embedder=self.embedder)
        self.cartridges.append(c)

    def run(self, fit_globally: bool = True):
        """Runs resolution for all cartridges."""
        if fit_globally:
            # Fit embedder on all corpora combined for consistent latent space
            global_corpus = []
            for c in self.cartridges:
                global_corpus.extend(c.corpus)
            self.embedder.fit(global_corpus)

        self.results = []
        for c in self.cartridges:
            res = resolve(c)
            self.results.append(res)

        self.isomorphisms = cross_domain_correlations(self.results)
        return self.results

    def get_report(self) -> str:
        return generate_text_report(self.results)

    def export(self, report_path: str = "results/unified_report.txt",
               latex_path: str = "results/unified_preprint.tex",
               json_path: str = "results/unified_results.json"):

        import os
        for path in [report_path, latex_path, json_path]:
            os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None

        # Text
        with open(report_path, 'w') as f:
            f.write(self.get_report())

        # LaTeX
        with open(latex_path, 'w') as f:
            f.write(generate_latex(self.results))

        # JSON
        export_json(self.results, json_path)

        return {"report": report_path, "latex": latex_path, "json": json_path}
