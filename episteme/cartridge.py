import numpy as np
from .core import embed_corpus, lp_manifold, stress_vectorized

class TheoryCartridge:
    def __init__(self, name, theories_data, weights_data):
        """
        theories_data: List of (name, text)
        weights_data: Dict of {persona: weight_vector}
        """
        self.name = name
        self.theory_names = [t[0] for t in theories_data]
        self.texts = [t[1] for t in theories_data]
        self.weights = np.array(list(weights_data.values()))
        self.personas = list(weights_data.keys())

        self.v_matrix = None
        self.var_explained = None
        self.results = {}

    def process(self, shared_v=None):
        """
        shared_v: Optional pre-computed embedding from a global space.
        """
        if shared_v is not None:
            self.v_matrix = shared_v
        else:
            self.v_matrix, self.var_explained = embed_corpus(self.texts)

        # ⚡ Bolt: Pass V_matrix and names directly to avoid redundant allocations
        v_opt, q_score, mixture = lp_manifold(self.v_matrix, self.theory_names, self.weights)
        robustness = stress_vectorized(self.v_matrix, self.theory_names)

        self.results = {
            "v_opt": v_opt,
            "q_score": q_score,
            "mixture": mixture,
            "robustness": robustness,
            "variance_explained": self.var_explained
        }
        return self.results
