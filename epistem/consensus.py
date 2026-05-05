"""
epistem.consensus
=================
Exact theoretical consensus via Linear Programming and adversarial stress testing.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import linprog
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

__all__ = ["ConsensusResult", "StressResult", "lp_manifold_consensus", "stress_test"]

@dataclass
class ConsensusResult:
    v_opt:        np.ndarray              # Pareto-optimal theory profile
    consensus_Q:  float                   # Minimax satisfaction score
    mixture:      Dict[str, float]        # theory_name -> lambda weight
    party_scores: Dict[str, float]        # party_name -> score
    tension:      float                   # Std dev of party scores (disagreement)
    deadlock:     bool                    # True if tension > threshold

@dataclass
class StressResult:
    worst_stoch: float   # 1st percentile score in random weight scenarios
    worst_exact: float   # Global minimum possible score (greedy O(1))
    mean:        float   # Average score
    fragility:   float   # Max - Min gap (vulnerability to weight shifts)


def lp_manifold_consensus(
    theories: Dict[str, np.ndarray],
    weight_matrix: np.ndarray,
    party_names: List[str],
) -> ConsensusResult:
    """
    Find the optimal theory mixture v* = sum(lambda_i * v_i) that maximizes
    the minimum score across all parties.

    Constrained to the convex hull of existing theories.
    """
    names = list(theories.keys())
    V = np.array([theories[n] for n in names]) # (N, D)
    N, D = V.shape
    M = weight_matrix.shape[0] # Number of parties

    # Objective: maximize t => minimize -t
    # x = [lambda_1, ..., lambda_N, t]
    c = np.zeros(N + 1)
    c[-1] = -1.0

    # Inequality constraints: W_j * (V^T * lambda) >= t  =>  -(W_j * V^T) * lambda + t <= 0
    # W is (M, D), V is (N, D) => W @ V.T is (M, N)
    Au = np.zeros((M, N + 1))
    Au[:, :N] = -(weight_matrix @ V.T)
    Au[:, -1] = 1.0
    bu = np.zeros(M)

    # Equality constraint: sum(lambda) = 1
    Ae = np.zeros((1, N + 1))
    Ae[0, :N] = 1.0
    be = np.array([1.0])

    # Bounds: lambda >= 0, t >= 0
    bounds = [(0, 1.0)] * N + [(0, None)]

    res = linprog(c, A_ub=Au, b_ub=bu, A_eq=Ae, b_eq=be, bounds=bounds, method='highs')

    if not res.success:
        raise ValueError(f"LP failed to converge: {res.message}")

    lam = res.x[:N]
    t_opt = float(res.x[-1])
    v_opt = V.T @ lam

    mixture = {names[i]: float(lam[i]) for i in range(N) if lam[i] > 1e-4}

    # Calculate party scores
    scores = weight_matrix @ v_opt
    party_scores = {party_names[i]: float(scores[i]) for i in range(M)}

    tension = float(np.std(scores))
    deadlock = tension > 0.08 # Heuristic threshold

    return ConsensusResult(
        v_opt=v_opt,
        consensus_Q=t_opt,
        mixture=mixture,
        party_scores=party_scores,
        tension=tension,
        deadlock=deadlock,
    )


def stress_test(
    theories: Dict[str, np.ndarray],
    weight_matrix: Optional[np.ndarray] = None,
    n_scenarios: int = 1000,
    alpha: float = 0.4,
) -> Dict[str, StressResult]:
    """
    Evaluate the robustness of each theory against adversarial weight shifts.
    """
    names = list(theories.keys())
    V = np.array([theories[n] for n in names]) # (N, D)
    N, D = V.shape

    rng = np.random.default_rng(42)
    # Adversarial weight scenarios (Dirichlet distribution on simplex)
    scenarios = rng.dirichlet(np.ones(D) * alpha, n_scenarios) # (S, D)

    # scores: (S, N) = (S, D) @ (D, N)
    scores = scenarios @ V.T

    worst_stoch = np.percentile(scores, 1, axis=0)
    # worst_exact: min(v_i) for a profile on the simplex
    worst_exact = np.min(V, axis=1)
    means = np.mean(scores, axis=0)
    # fragility: max(v_i) - min(v_i)
    fragility = np.max(V, axis=1) - worst_exact

    results = {}
    for i in range(N):
        results[names[i]] = StressResult(
            worst_stoch=float(worst_stoch[i]),
            worst_exact=float(worst_exact[i]),
            mean=float(means[i]),
            fragility=float(fragility[i]),
        )
    return results
