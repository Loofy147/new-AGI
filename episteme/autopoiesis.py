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
    """
    v_opt = last_result.consensus.v_opt
    weak_dims = v_opt < threshold

    if not np.any(weak_dims):
        return current_weights

    new_weights_dict = {}
    for party, w in current_weights.items():
        wn = w.copy()
        for i in range(len(wn)):
            if weak_dims[i]:
                # If dimension is weak, increase its importance
                if wn[i] == 0:
                    wn[i] = 0.05
                else:
                    wn[i] *= (1.0 + learning_rate)

        # Re-normalize
        wn /= (wn.sum() + 1e-9)
        new_weights_dict[party] = wn

    return new_weights_dict
