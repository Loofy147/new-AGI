import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from scipy.optimize import linprog

# ⚡ Bolt: Using modern NumPy Generator for thread-safe and faster RNG
_RNG = np.random.default_rng()

def q(v, w):
    """Linear quality score: dot product of weight vector and profile."""
    return float(np.dot(w, np.clip(v, 0, 1)))

def q_worst_greedy(v):
    """Exact: min of linear q(v,w) over simplex = min_i(v_i). O(1)."""
    return float(np.min(np.clip(v, 0, 1)))

def q_best_greedy(v):
    """Exact: max of linear q(v,w) over simplex = max_i(v_i). O(1)."""
    return float(np.max(np.clip(v, 0, 1)))

def lp_manifold(V_matrix, names, W_mat):
    """
    Exact LP: max t  s.t.  W_j·(T·λ)>=t ∀j,  Σλ=1, λ>=0
    Constrained to convex hull of actual theories (mixtures).
    V_matrix: (N, D) matrix of theory profiles.
    names: List of theory names.
    W_mat: (M, D) matrix of weight personas.
    """
    T = V_matrix.T  # (D, N)
    N = len(names)
    nw = W_mat.shape[0]

    # Objective: minimize -t
    c = np.zeros(N + 1)
    c[-1] = -1.0

    # Inequality constraints: -(W @ T) @ lambda + t <= 0
    Au = np.zeros((nw, N + 1))
    Au[:, :N] = -(W_mat @ T)
    Au[:, -1] = 1.0

    # Equality constraint: sum(lambda) = 1
    Ae = np.zeros((1, N + 1))
    Ae[0, :N] = 1.0

    res = linprog(c, A_ub=Au, b_ub=np.zeros(nw),
                  A_eq=Ae, b_eq=np.array([1.0]),
                  bounds=[(0, None)] * N + [(0, None)],
                  method='highs')

    if not res.success:
        return None, 0.0, {}

    lam = np.clip(res.x[:N], 0, None)
    total_lam = lam.sum()
    if total_lam > 0:
        lam /= total_lam

    v_opt = T @ lam
    t_opt = float(res.x[-1])
    mixture = {names[i]: float(lam[i]) for i in range(N) if lam[i] > 0.005}

    return v_opt, t_opt, mixture

def stress_vectorized(V_matrix, names, n_scenarios=1000):
    """Matrix-wide robustness evaluation."""
    V = np.clip(V_matrix, 0, 1)  # (N, D)
    N, D = V.shape

    # ⚡ Bolt: Using generator for faster Dirichlet sampling
    adv = _RNG.dirichlet(np.ones(D) * 0.4, n_scenarios)  # (n, D)
    scores = adv @ V.T                                   # (n, N)

    worst_stoch = np.percentile(scores, 1, axis=0)
    worst_exact = np.min(V, axis=1)
    means = np.mean(scores, axis=0)
    fragility = np.max(V, axis=1) - worst_exact

    return {
        names[i]: {
            'worst_stoch': float(worst_stoch[i]),
            'worst_exact': float(worst_exact[i]),
            'mean':        float(means[i]),
            'fragility':   float(fragility[i]),
        } for i in range(N)
    }

def embed_corpus(texts, n_dims=8):
    """Latent Semantic Analysis embedding."""
    vec = TfidfVectorizer(
        ngram_range=(1, 2), min_df=1, max_df=0.95,
        sublinear_tf=True, strip_accents='unicode'
    )
    X = vec.fit_transform(texts)

    svd = TruncatedSVD(
        n_components=min(n_dims, X.shape[1] - 1, X.shape[0] - 1),
        random_state=42
    )
    proj = svd.fit_transform(X)

    scaler = MinMaxScaler()
    v_norm = scaler.fit_transform(proj)

    if v_norm.shape[1] < n_dims:
        pad = np.zeros((v_norm.shape[0], n_dims - v_norm.shape[1]))
        v_norm = np.hstack([v_norm, pad])

    var_ratio = svd.explained_variance_ratio_
    return v_norm, var_ratio
