"""
episteme.embed
==============
Local, zero-network text embedding via TF-IDF + Latent Semantic Analysis.
Converts any domain corpus into normalized [0,1] theory profiles.

Supports global space fitting for cross-domain isomorphism consistency.
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

        # LSA State
        self._tfidf = TfidfVectorizer(
            ngram_range=self.ngram_range,
            min_df=1, max_df=0.95,
            sublinear_tf=True, strip_accents='unicode',
        )
        self._svd = TruncatedSVD(n_components=n_dims, random_state=random_state)
        self._scaler = MinMaxScaler()
        self._is_fitted = False

        if use_sbert:
            try:
                from sentence_transformers import SentenceTransformer
                self._sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
                self._method      = 'sbert'
            except ImportError:
                pass

    def fit(self, corpus: List[Tuple[str, str]]) -> LSAEmbedder:
        """Learns the latent semantic space from a global corpus."""
        texts = [item[1] for item in corpus]
        if self._method == 'sbert':
             from sklearn.decomposition import PCA
             emb = self._sbert_model.encode(texts, show_progress_bar=False)
             self._pca = PCA(n_components=self.n_dims, random_state=self.random_state)
             self._pca.fit(emb)
        else:
            X = self._tfidf.fit_transform(texts)
            # Adjust n_components if corpus is too small
            n_comp = min(self.n_dims, X.shape[1] - 1, X.shape[0] - 1)
            if n_comp < self.n_dims:
                self._svd = TruncatedSVD(n_components=n_comp, random_state=self.random_state)

            proj = self._svd.fit_transform(X)
            self._scaler.fit(proj)

        self._is_fitted = True
        return self

    def embed(
        self,
        corpus: List[Tuple[str, str]],
        dim_labels: Optional[List[str]] = None,
    ) -> EmbedResult:
        """Embed a list of (name, text) pairs."""
        names = [item[0] for item in corpus]
        texts = [item[1] for item in corpus]
        n     = len(corpus)

        if self._method == 'sbert':
            raw = self._embed_sbert(texts)
        else:
            raw = self._embed_lsa(texts)

        # Normalize to [0,1] per dimension
        v_norm = self._scaler.transform(raw) if self._is_fitted else MinMaxScaler().fit_transform(raw)

        # Ensure correct dimensionality
        if v_norm.shape[1] < self.n_dims:
            pad    = np.zeros((n, self.n_dims - v_norm.shape[1]))
            v_norm = np.hstack([v_norm, pad])
        v_norm   = v_norm[:, :self.n_dims]

        profiles = {names[i]: v_norm[i] for i in range(n)}

        if dim_labels is None:
            dim_labels = [f"PC{i+1}" for i in range(self.n_dims)]

        if self._method == 'sbert':
            var_ratio = self._pca.explained_variance_ratio_ if self._is_fitted else np.ones(self.n_dims)/self.n_dims
        else:
            var_ratio = self._svd.explained_variance_ratio_ if self._is_fitted else np.ones(self.n_dims)/self.n_dims

        return EmbedResult(
            profiles=profiles,
            variance_ratio=var_ratio,
            cumulative_var=float(var_ratio.sum()),
            n_dims=self.n_dims,
            method=self._method,
            dim_labels=dim_labels,
        )

    def _embed_lsa(self, texts: List[str]) -> np.ndarray:
        if self._is_fitted:
            X = self._tfidf.transform(texts)
            return self._svd.transform(X)

        # Local fallback
        X = self._tfidf.fit_transform(texts)
        n_comp = min(self.n_dims, X.shape[1] - 1, X.shape[0] - 1)
        svd = TruncatedSVD(n_components=n_comp, random_state=self.random_state)
        return svd.fit_transform(X)

    def _embed_sbert(self, texts: List[str]) -> np.ndarray:
        emb = self._sbert_model.encode(texts, show_progress_bar=False)
        if self._is_fitted:
            return self._pca.transform(emb)

        # Local fallback
        from sklearn.decomposition import PCA
        pca = PCA(n_components=min(self.n_dims, len(texts)), random_state=self.random_state)
        return pca.fit_transform(emb)

class NumericEmbedder(LSAEmbedder):
    """
    Embedder that bypasses text processing and returns pre-computed numeric profiles.
    Useful for benchmarks and legacy data.
    """
    def __init__(self, profiles: Dict[str, np.ndarray], n_dims: int = 8):
        super().__init__(n_dims=n_dims, use_sbert=False)
        self.profiles_data = profiles
        self._method = 'numeric'

    def embed(self, corpus: List[Tuple[str, str]], dim_labels: Optional[List[str]] = None) -> EmbedResult:
        # corpus names must match profiles_data keys
        profiles = {name: self.profiles_data[name] for name, _ in corpus}

        return EmbedResult(
            profiles=profiles,
            variance_ratio=np.ones(self.n_dims)/self.n_dims,
            cumulative_var=1.0,
            n_dims=self.n_dims,
            method=self._method,
            dim_labels=dim_labels or [f"Dim{i+1}" for i in range(self.n_dims)],
        )
