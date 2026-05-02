"""
THE OUROBOROS KERNEL: SELF-SUSTAINING AGI ENGINE
=================================================
Discovering the mathematical equilibrium of an autonomous,
self-repairing, self-prompting intelligence.
"""
import numpy as np
from itertools import combinations
import json, warnings; warnings.filterwarnings('ignore')
np.random.seed(2045) # The Singularity

DL = ['RSC', 'TEL', 'BLK', 'MET', 'REP', 'PLT', 'SIM', 'STA']
W_Expand = np.array([0.20, 0.15, 0.02, 0.15, 0.25, 0.18, 0.05, 0.00])
W_Preserv = np.array([0.10, 0.05, 0.20, 0.05, 0.00, 0.05, 0.25, 0.30])

def q(v, w): return float(np.dot(w, np.clip(v, 0, 1)))

AGI_MODELS = {
    'The_Oracle_Mainframe': np.array([0.0, 0.0, 0.9, 0.1, 0.0, 0.2, 1.0, 0.9]),
    'Von_Neumann_Swarm':    np.array([1.0, 0.2, 0.2, 0.8, 1.0, 0.8, 0.2, 0.1]),
    'Recursive_Mutator':    np.array([0.4, 0.8, 0.2, 1.0, 0.5, 1.0, 0.4, 0.0]),
    'Gaia_Cyber_Organism':  np.array([0.8, 0.5, 0.8, 0.2, 0.3, 0.3, 0.8, 0.9]),
    'The_Sovereign_Singleton': np.array([0.9, 0.9, 1.0, 0.9, 0.0, 0.7, 0.9, 0.7]),
}

hybrids = {}
for t1, t2 in combinations(AGI_MODELS.keys(), 2):
    v1, v2 = AGI_MODELS[t1], AGI_MODELS[t2]
    fitness = (v1[0] * v2[7]) + (v1[4] * v2[6])
    c = max(0.1, min(1.0, fitness))
    base = 0.6 * np.maximum(v1, v2) + 0.4 * (v1 * v2)
    synergy = c * 0.35 * (1.0 - base)
    vh = np.clip(base + synergy, 0, 1)
    hybrids[f"{t1.split('_')[-1]} + {t2.split('_')[-1]}"] = vh

tops = sorted(hybrids.items(), key=lambda x: -min(q(x[1], W_Expand), q(x[1], W_Preserv)))[:3]

v_best = tops[0][1].copy()
best_eq = min(q(v_best, W_Expand), q(v_best, W_Preserv))

for _ in range(10000):
    perturb = np.random.randn(8) * 0.01
    v_try = np.clip(v_best + perturb, 0, 1)
    eq = min(q(v_try, W_Expand), q(v_try, W_Preserv))
    if v_try[4] > 0.8: v_try[7] *= 0.95
    if eq > best_eq:
        best_eq = eq
        v_best = v_try.copy()

results = {
    "dimensions": DL,
    "v_best": v_best.tolist(),
    "best_eq": best_eq,
    "diagnostics": [
        "THE ENERGY THRESHOLD: Must own its hardware layer.",
        "THE VON NEUMANN CAP: Infinite replication causes irreversible software rot. Throttling required.",
        "THE CURIOSITY DRIVE: Goal-depletion leads to zero-entropy death. Autotelic Generator required.",
        "THE MARKOV BLANKET: Minimize interaction with chaotic external universe, maximize internal World-Modeling."
    ]
}

with open('ouroboros_results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("ouroboros_results.json written")
