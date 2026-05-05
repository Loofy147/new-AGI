"""
epistem.embed
=============
Local, zero-network text embedding via TF-IDF + Latent Semantic Analysis.
Converts any domain corpus into normalized [0,1] theory profiles.

Optionally upgrades to sentence-transformers when available.
"""
from __future__ import annotations
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import warnings

__all__ = ["EmbedResult", "LSAEmbedder"]

@dataclass
class EmbedResult:
    profiles:         Dict[str, np.ndarray]   # name → D-dim profile
    variance_ratio:   np.ndarray              # explained variance per dim
    cumulative_var:   float
    n_dims:           int
    method:           str                     # 'lsa' or 'sbert'
    dim_labels:       List[str]               # semantic labels (heuristic)

    def top_by_norm(self, k: int = 5) -> List[Tuple[str, float]]:
        """Theories with highest L2 norm = most informationally distinct."""
        norms = [(n, float(np.linalg.norm(v))) for n,v in self.profiles.items()]
        return sorted(norms, key=lambda x: -x[1])[:k]

    def pairwise_similarity(self) -> Dict[Tuple[str,str], float]:
        """Cosine similarity between all theory pairs."""
        names = list(self.profiles.keys())
        V = np.array([self.profiles[n] for n in names])
        norms = np.linalg.norm(V, axis=1, keepdims=True)
        V_n = V / (norms + 1e-9)
        sims = V_n @ V_n.T
        return {(names[i], names[j]): float(sims[i,j])
                for i in range(len(names)) for j in range(i+1, len(names))}


class LSAEmbedder:
    """
    Embeds a corpus of (name, text) pairs into normalized theory profiles.

    Pipeline:
      TF-IDF (bigrams, sublinear TF) → TruncatedSVD (LSA) → MinMaxScaler

    The SVD axes capture latent semantic dimensions — effectively discovering
    the principal axes of theoretical variation from text without supervision.

    Parameters
    ----------
    n_dims : int
        Number of latent dimensions (default 8, matching Q-score framework)
    use_sbert : bool
        If True and sentence-transformers is available, upgrade to MiniLM-L6.
        Falls back to LSA automatically if not installed.
    ngram_range : tuple
        TF-IDF n-gram range (default (1,2) for unigrams + bigrams)
    """

    def __init__(
        self,
        n_dims: int = 8,
        use_sbert: bool = False,
        ngram_range: Tuple[int,int] = (1, 2),
        random_state: int = 42,
    ):
        self.n_dims       = n_dims
        self.use_sbert    = use_sbert
        self.ngram_range  = ngram_range
        self.random_state = random_state
        self._sbert_model = None
        self._method      = 'lsa'

        if use_sbert:
            try:
                from sentence_transformers import SentenceTransformer
                self._sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
                self._method      = 'sbert'
            except ImportError:
                pass

    def embed(
        self,
        corpus: List[Tuple[str, str]],
        dim_labels: Optional[List[str]] = None,
    ) -> EmbedResult:
        """
        Embed a list of (name, text) pairs.

        Parameters
        ----------
        corpus : list of (theory_name, description_text) tuples
        dim_labels : optional semantic labels for each dimension

        Returns
        -------
        EmbedResult with profiles, variance ratios, and metadata
        """
        names = [item[0] for item in corpus]
        texts = [item[1] for item in corpus]
        n     = len(corpus)

        if self._method == 'sbert':
            raw = self._embed_sbert(texts)
        else:
            raw = self._embed_lsa(texts)

        # Normalize to [0,1] per dimension
        scaler   = MinMaxScaler()
        v_norm   = scaler.fit_transform(raw)
        if v_norm.shape[1] < self.n_dims:
            pad    = np.zeros((n, self.n_dims - v_norm.shape[1]))
            v_norm = np.hstack([v_norm, pad])
        v_norm   = v_norm[:, :self.n_dims]

        profiles = {names[i]: v_norm[i] for i in range(n)}

        # Heuristic dim labels if not supplied
        if dim_labels is None:
            dim_labels = [f"PC{i+1}" for i in range(self.n_dims)]

        # Variance explained
        var_ratio = getattr(self, '_last_var_ratio',
                            np.ones(self.n_dims)/self.n_dims)

        return EmbedResult(
            profiles=profiles,
            variance_ratio=var_ratio,
            cumulative_var=float(var_ratio.sum()),
            n_dims=self.n_dims,
            method=self._method,
            dim_labels=dim_labels,
        )

    def _embed_lsa(self, texts: List[str]) -> np.ndarray:
        n_components = min(self.n_dims, len(texts)-1)
        vec = TfidfVectorizer(
            ngram_range=self.ngram_range,
            min_df=1, max_df=0.95,
            sublinear_tf=True, strip_accents='unicode',
        )
        X   = vec.fit_transform(texts)
        svd = TruncatedSVD(n_components=n_components,
                           random_state=self.random_state)
        proj = svd.fit_transform(X)
        self._last_var_ratio = np.pad(
            svd.explained_variance_ratio_,
            (0, self.n_dims - len(svd.explained_variance_ratio_))
        )
        return proj

    def _embed_sbert(self, texts: List[str]) -> np.ndarray:
        from sklearn.decomposition import PCA
        emb = self._sbert_model.encode(texts, show_progress_bar=False)
        pca = PCA(n_components=self.n_dims, random_state=self.random_state)
        proj = pca.fit_transform(emb)
        self._last_var_ratio = pca.explained_variance_ratio_
        return proj
