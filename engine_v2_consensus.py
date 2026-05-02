import json
import numpy as np
from scipy.optimize import minimize
import warnings; warnings.filterwarnings('ignore')

def run_consensus_v2(data_path):
    print(f"Loading discovered theories from {data_path}...")
    with open(data_path, 'r') as f:
        data = json.load(f)

    dims = data['dimensions']
    TP = data['theories']

    # In V2, we don't have human-defined weights.
    # We simulate two opposing "Expert Camps" based on PCA variance.
    # Camp A: Weights first 4 dimensions (High variance/Structural)
    # Camp B: Weights last 4 dimensions (Nuance/Secondary)
    W_A = np.array([0.25, 0.25, 0.2, 0.2, 0.1, 0.0, 0.0, 0.0])
    W_B = np.array([0.0, 0.0, 0.0, 0.1, 0.2, 0.2, 0.25, 0.25])

    def q(v, w): return float(np.dot(w, np.clip(v, 0, 1)))
    def consensus_score(v): return min(q(v, W_A), q(v, W_B))

    # Find best existing theory
    best_existing = None
    best_existing_score = -1
    for name, v in TP.items():
        score = consensus_score(v)
        if score > best_existing_score:
            best_existing_score = score
            best_existing = name

    print(f"Best existing theory in latent space: {best_existing} (Q={best_existing_score:.4f})")

    # Optimization for the Singularity Theory
    v_start = np.array(TP[best_existing])
    v_best = v_start.copy()
    best_cons = best_existing_score

    for _ in range(5000):
        perturb = np.random.randn(8) * 0.015
        v_try = np.clip(v_best + perturb, 0, 1)
        cs = consensus_score(v_try)
        if cs > best_cons:
            best_cons = cs
            v_best = v_try.copy()

    print(f"Optimized Singularity Theory Q: {best_cons:.4f}")

    results = {
        "dimensions": dims,
        "best_existing_theory": best_existing,
        "best_existing_score": best_existing_score,
        "singularity_profile": v_best.tolist(),
        "singularity_score": best_cons
    }

    with open('consensus_v2_results.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("consensus_v2_results.json written.")

    # Visual Profile
    print("\nSingularity Profile for Machine-Discovered Dimensions:")
    for d, val in zip(dims, v_best):
        bar = '█'*int(val*30) + '░'*(30-int(val*30))
        print(f"  {d}: {val:.4f} {bar}")

if __name__ == "__main__":
    run_consensus_v2('discovered_engine_v2.json')
