import numpy as np
import json
from scipy.optimize import minimize
from boss_fights import get_boss_fight
import paper_generator as pg
import warnings; warnings.filterwarnings('ignore')

class SingularityEngine:
    def __init__(self, data):
        self.dims = data['dimensions']
        self.weights = data['weights']
        # ⚡ Optimization: Pre-convert weights to a matrix for vectorized dot products
        self.weight_matrix = np.array(list(self.weights.values()))
        self.TP = data['theories']

    def q(self, v, w):
        # Kept for backward compatibility if needed, but not used in optimized loop
        return float(np.dot(w, np.clip(v, 0, 1)))

    def consensus_score(self, v):
        # ⚡ Optimization: Vectorized calculation of all scores at once
        # v is expected to be clipped to [0, 1] by the caller (optimize loop)
        return np.min(np.dot(self.weight_matrix, v))

    def optimize(self, iterations=10000):
        # Start from the best existing theory
        best_existing = None
        best_existing_score = -1
        for name, v in self.TP.items():
            # Ensure input is clipped for consistency
            score = self.consensus_score(np.clip(v, 0, 1))
            if score > best_existing_score:
                best_existing_score = score
                best_existing = name

        v_best = self.TP[best_existing].copy()
        best_score = best_existing_score

        # ⚡ Optimization: Pre-generate all perturbations at once
        num_dims = len(self.dims)
        perturbations = np.random.randn(iterations, num_dims) * 0.015

        for i in range(iterations):
            v_try = np.clip(v_best + perturbations[i], 0, 1)
            score = self.consensus_score(v_try)
            if score > best_score:
                best_score = score
                v_best = v_try.copy()

        return v_best, best_score, best_existing

    def generate_report(self, v_best, best_score, best_existing, title):
        results = {
            "dimensions": self.dims,
            "v_best": v_best.tolist(),
            "best_score": best_score,
            "best_existing": best_existing,
            "diagnostics": [
                f"Singularity reached with consensus score {best_score:.4f}.",
                f"Best baseline: {best_existing}.",
                "Resolved tension between primary opposing weight vectors.",
                "Mathematically derived optimal theoretical profile."
            ]
        }

        report_name = f"{title.lower().replace(' ', '_')}_results.json"
        with open(report_name, 'w') as f:
            json.dump(results, f, indent=4)

        tex_name = f"{title.lower().replace(' ', '_')}_preprint.tex"
        pg.generate_latex(report_name, tex_name)
        return tex_name

if __name__ == "__main__":
    import sys
    cartridge_name = sys.argv[1] if len(sys.argv) > 1 else "TOE"
    data = get_boss_fight(cartridge_name)

    if data:
        engine = SingularityEngine(data)
        v_best, best_score, best_existing = engine.optimize()
        print(f"Cartridge: {cartridge_name}")
        print(f"Singularity Score: {best_score:.4f}")

        tex_file = engine.generate_report(v_best, best_score, best_existing, f"{cartridge_name} Resolution")
        print(f"Preprint generated: {tex_file}")
    else:
        print("Invalid cartridge.")
