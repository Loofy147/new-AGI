"""
epistem.isomorphism
===================
Structural isomorphism detection across cartridge domains.

Two cartridges are structurally isomorphic to degree r when their
consensus optimal theory profiles are correlated — meaning the same
dimensional tradeoffs appear in both domains.

High correlation signals:
  - Transfer learning opportunity (solutions from one domain apply to other)
  - Shared underlying mechanism (e.g. ECON.Equity ↔ AGING.Inflammation)
  - Research bridge (findings in one domain predict findings in the other)
"""
from __future__ import annotations
import numpy as np
from scipy.stats import spearmanr, pearsonr
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from .cartridge import CartridgeResult

__all__ = ["IsomorphismResult", "cross_domain_correlations", "rank_bridges"]

@dataclass
class IsomorphismResult:
    domain_a:    str
    domain_b:    str
    pearson_r:   float
    spearman_r:  float
    pvalue:      float
    strength:    str           # STRONG / MODERATE / WEAK / INVERSE
    interpretation: str

    def __repr__(self):
        return (f"Isomorphism({self.domain_a} ↔ {self.domain_b}: "
                f"r={self.pearson_r:+.3f} [{self.strength}])")


def _classify_strength(r: float, pvalue: float) -> str:
    if pvalue > 0.10:
        return "NOISE"
    if   r >  0.70: return "STRONG"
    elif r >  0.40: return "MODERATE"
    elif r > -0.10: return "WEAK"
    elif r > -0.40: return "INVERSE_WEAK"
    else:           return "INVERSE_STRONG"


def _interpret(domain_a: str, domain_b: str, r: float, dims_a: List[str], dims_b: List[str]) -> str:
    if   r >  0.70: return f"Strong structural parallel: {domain_a} and {domain_b} face identical dimensional tradeoffs"
    elif r >  0.40: return f"Moderate overlap: partial transfer of solutions between {domain_a} and {domain_b}"
    elif r > -0.10: return f"Independent domains: {domain_a} and {domain_b} resolve different axes of tension"
    else:           return f"Structural inversion: what helps {domain_a} hurts {domain_b} — trade-off rather than bridge"


def cross_domain_correlations(
    results: List[CartridgeResult],
    min_strength: str = "WEAK",
) -> List[IsomorphismResult]:
    """
    Compute pairwise structural isomorphism between all cartridge results.

    Correlation is computed between v_opt vectors (the LP-optimal consensus
    theory profiles). High correlation means the same dimensional pattern
    resolves both domains — a genuine structural isomorphism.

    Parameters
    ----------
    results : list of CartridgeResult (one per cartridge)
    min_strength : filter output by minimum strength level

    Returns
    -------
    List of IsomorphismResult sorted by |pearson_r| descending
    """
    strength_order = {"STRONG":4,"MODERATE":3,"WEAK":2,"INVERSE_WEAK":1,"INVERSE_STRONG":1,"NOISE":0}
    min_order = strength_order.get(min_strength, 0)

    isos = []
    for i in range(len(results)):
        for j in range(i+1, len(results)):
            ra, rb = results[i], results[j]
            va = np.array(ra.consensus.v_opt)
            vb = np.array(rb.consensus.v_opt)
            if va.shape[0] == 0 or vb.shape[0] == 0:
                continue

            pr, pp = pearsonr(va, vb)
            sr, _  = spearmanr(va, vb)

            strength = _classify_strength(pr, pp)
            if strength_order.get(strength, 0) < min_order:
                continue

            interp = _interpret(ra.cartridge_name, rb.cartridge_name,
                                 pr, ra.dim_labels, rb.dim_labels)

            isos.append(IsomorphismResult(
                domain_a=ra.cartridge_name,
                domain_b=rb.cartridge_name,
                pearson_r=float(pr),
                spearman_r=float(sr),
                pvalue=float(pp),
                strength=strength,
                interpretation=interp,
            ))

    return sorted(isos, key=lambda x: -abs(x.pearson_r))


def rank_bridges(
    results: List[CartridgeResult],
) -> List[Tuple[str, float]]:
    """
    Rank cartridge domains by their average |r| to all other domains.
    High score = structural hub (solutions transfer broadly).
    Low score  = isolated domain (unique structure, no transfer).

    Returns list of (domain_name, avg_abs_r) sorted descending.
    """
    isos = cross_domain_correlations(results, min_strength="NOISE")
    scores: Dict[str, List[float]] = {r.cartridge_name: [] for r in results}
    for iso in isos:
        scores[iso.domain_a].append(abs(iso.pearson_r))
        scores[iso.domain_b].append(abs(iso.pearson_r))
    return sorted(
        [(name, float(np.mean(vals)) if vals else 0.0) for name, vals in scores.items()],
        key=lambda x: -x[1],
    )
