import numpy as np
from scipy.stats import spearmanr

def find_isomorphisms(optimal_vectors, threshold=0.6):
    """Identifies structural similarities between optimal domain profiles."""
    isomorphisms = []
    domain_list = list(optimal_vectors.keys())

    for i in range(len(domain_list)):
        for j in range(i + 1, len(domain_list)):
            d1, d2 = domain_list[i], domain_list[j]
            r, _ = spearmanr(optimal_vectors[d1], optimal_vectors[d2])
            isomorphisms.append({
                "pair": [d1, d2],
                "score": float(r),
                "significant": bool(abs(r) > threshold)
            })

    return isomorphisms
