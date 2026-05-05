"""
episteme.autopoiesis
====================
Self-optimizing weight evolution for autopoietic consensus.
"""
from __future__ import annotations
import numpy as np
from typing import Dict, List, Tuple
from .cartridge import CartridgeResult

def evolved_weights(
    current_weights: Dict[str, np.ndarray],
    last_result: CartridgeResult,
    learning_rate: float = 0.20,
    threshold: float = 0.80
) -> Dict[str, np.ndarray]:
    """
    Evolve persona weights based on detected weaknesses in the consensus profile.
    If a dimension in v_opt is below threshold, stakeholders increase their
    sensitivity (weight) to that dimension.

    Optimized: Vectorized implementation across all parties and dimensions.
    """
    v_opt = last_result.consensus.v_opt
    weak_dims = v_opt < threshold

    if not np.any(weak_dims):
        return current_weights

    party_names = list(current_weights.keys())
    W = np.array([current_weights[p] for p in party_names]) # (M, D)

    # weak_dims is (D,), W is (M, D)
    # NumPy broadcasting handles the dimension-wise application

    zeros_mask = (W == 0) & weak_dims
    scale_mask = (W != 0) & weak_dims

    W[zeros_mask] = 0.05
    W[scale_mask] *= (1.0 + learning_rate)

    # Re-normalize each party's weight vector
    W /= (W.sum(axis=1, keepdims=True) + 1e-9)

    return {party_names[i]: W[i] for i in range(len(party_names))}
