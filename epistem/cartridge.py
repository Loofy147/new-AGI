"""
epistem.cartridge
=================
Domain plugin system. A Cartridge bundles:
  - corpus     : list of (name, text) theory descriptions
  - weights    : dict of party_name → weight_vector
  - dim_labels : semantic names for the 8 dimensions

resolve(cartridge) runs the full pipeline and returns a CartridgeResult.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from .embed   import LSAEmbedder, EmbedResult
from .consensus import (lp_manifold_consensus, stress_test,
                        ConsensusResult, StressResult)

__all__ = ["Cartridge", "CartridgeResult", "resolve"]

@dataclass
class Cartridge:
    """
    A domain plugin defining a theoretical deadlock resolution problem.

    Parameters
    ----------
    name : human-readable domain name
    corpus : list of (theory_name, description_text)
    weights : dict of party_name → np.ndarray weight vector (must sum to 1)
    dim_labels : semantic labels for the 8 LSA dimensions
    embedder : LSAEmbedder instance (shared across cartridges for efficiency)
    """
    name:       str
    corpus:     List[Tuple[str, str]]
    weights:    Dict[str, np.ndarray]
    dim_labels: List[str] = field(default_factory=lambda: [f"PC{i+1}" for i in range(8)])
    embedder:   Optional[LSAEmbedder] = None

    def __post_init__(self):
        # Validate weights
        for party, w in self.weights.items():
            s = w.sum()
            if abs(s - 1.0) > 1e-6:
                raise ValueError(
                    f"Cartridge '{self.name}': weight vector for '{party}' "
                    f"sums to {s:.4f}, not 1.0. Consensus LP requires normalised weights."
                )
        if self.embedder is None:
            self.embedder = LSAEmbedder(n_dims=8)

    @property
    def theory_names(self) -> List[str]:
        return [c[0] for c in self.corpus]

    @property
    def party_names(self) -> List[str]:
        return list(self.weights.keys())

    @property
    def weight_matrix(self) -> np.ndarray:
        return np.array(list(self.weights.values()))


@dataclass
class CartridgeResult:
    cartridge_name:  str
    embed_result:    EmbedResult
    consensus:       ConsensusResult
    stress:          Dict[str, StressResult]
    dim_labels:      List[str]

    # Derived convenience properties
    @property
    def consensus_Q(self) -> float:
        return self.consensus.consensus_Q

    @property
    def deadlock(self) -> bool:
        return self.consensus.deadlock

    @property
    def dominant_theory(self) -> Tuple[str, float]:
        if not self.consensus.mixture:
            return ("none", 0.0)
        return max(self.consensus.mixture.items(), key=lambda x: x[1])

    @property
    def most_robust(self) -> Tuple[str, float]:
        best = min(self.stress.items(), key=lambda x: x[1].fragility)
        return (best[0], best[1].fragility)

    @property
    def most_fragile(self) -> Tuple[str, float]:
        worst = max(self.stress.items(), key=lambda x: x[1].fragility)
        return (worst[0], worst[1].fragility)

    def summary(self) -> str:
        lines = [
            f"=== {self.cartridge_name} ===",
            f"  Consensus Q   : {self.consensus_Q:.4f}",
            f"  Tension (std) : {self.consensus.tension:.4f}",
            f"  Deadlock      : {'YES ⚠' if self.deadlock else 'no'}",
            f"  Dominant theory: {self.dominant_theory[0]} (λ={self.dominant_theory[1]:.3f})",
            f"  Most robust   : {self.most_robust[0]} (frag={self.most_robust[1]:.3f})",
            f"  Most fragile  : {self.most_fragile[0]} (frag={self.most_fragile[1]:.3f})",
            f"  Var explained : {self.embed_result.cumulative_var:.3f}",
            f"  Party scores:",
        ]
        for party, score in sorted(self.consensus.party_scores.items(), key=lambda x:-x[1]):
            lines.append(f"    {party:20s}: {score:.4f}")
        lines.append(f"  Mixture:")
        for theory, lam in sorted(self.consensus.mixture.items(), key=lambda x:-x[1]):
            lines.append(f"    λ={lam:.4f}  {theory}")
        return "\n".join(lines)


def resolve(
    cartridge: Cartridge,
    n_stress_scenarios: int = 1000,
    stress_alpha: float = 0.4,
) -> CartridgeResult:
    """
    Run the full resolution pipeline for one cartridge.

    Pipeline:
      1. LSA embed corpus → theory profiles
      2. LP manifold consensus → exact Pareto-optimal mixture
      3. Vectorised stress test → fragility scores

    Parameters
    ----------
    cartridge : Cartridge definition
    n_stress_scenarios : adversarial weight scenarios for stress test
    stress_alpha : Dirichlet concentration (lower = more extreme)

    Returns
    -------
    CartridgeResult with all computed fields
    """
    # Step 1: Embed
    embed_result = cartridge.embedder.embed(
        cartridge.corpus,
        dim_labels=cartridge.dim_labels,
    )

    # Step 2: LP consensus (exact, manifold-constrained)
    consensus = lp_manifold_consensus(
        theories=embed_result.profiles,
        weight_matrix=cartridge.weight_matrix,
        party_names=cartridge.party_names,
    )

    # Step 3: Stress test (vectorised)
    stress = stress_test(
        theories=embed_result.profiles,
        weight_matrix=cartridge.weight_matrix,
        n_scenarios=n_stress_scenarios,
        alpha=stress_alpha,
    )

    return CartridgeResult(
        cartridge_name=cartridge.name,
        embed_result=embed_result,
        consensus=consensus,
        stress=stress,
        dim_labels=cartridge.dim_labels,
    )
