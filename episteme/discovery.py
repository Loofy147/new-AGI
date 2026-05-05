"""
episteme.discovery
==================
Automated theory discovery via external library (ArXiv) fetching.
"""
from __future__ import annotations
import urllib.request
import xml.etree.ElementTree as ET
import time
import os
import json
import hashlib
from typing import List, Optional, Tuple
from .embed import LSAEmbedder

class ArXivFetcher:
    """
    Fetches scientific abstracts from ArXiv API with local caching.
    """
    def __init__(self, cache_dir: str = "arxiv_cache", delay: int = 3):
        self.cache_dir = cache_dir
        self.delay = delay
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _get_cache_path(self, query: str) -> str:
        h = hashlib.md5(query.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{h}.json")

    def fetch(self, query: str, max_results: int = 50) -> List[str]:
        """Fetch abstracts for a query, using cache if available."""
        cache_path = self._get_cache_path(query)
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)

        base_url = 'http://export.arxiv.org/api/query?'
        search_query = f'all:{query.replace(" ", "+")}'

        abstracts = []
        start = 0
        batch_size = 50

        while len(abstracts) < max_results:
            url = f'{base_url}search_query={search_query}&start={start}&max_results={batch_size}'
            try:
                with urllib.request.urlopen(url) as response:
                    content = response.read()

                root = ET.fromstring(content)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                entries = root.findall('atom:entry', ns)
                if not entries: break

                for entry in entries:
                    summary = entry.find('atom:summary', ns)
                    if summary is not None:
                        abstracts.append(summary.text.strip().replace('\n', ' '))

                if len(abstracts) >= max_results: break

                start += batch_size
                time.sleep(self.delay)
            except Exception as e:
                print(f"ArXiv Fetch Error: {e}")
                break

        if abstracts:
            with open(cache_path, 'w') as f:
                json.dump(abstracts, f)

        return abstracts[:max_results]

class TheoryDiscoverer:
    """
    Maps raw text (abstracts) into theory profiles using LSA.
    """
    def __init__(self, embedder: Optional[LSAEmbedder] = None):
        self.embedder = embedder or LSAEmbedder(n_dims=8)

    def discover(self, abstracts: List[str], domain_name: str = "Discovered") -> List[Tuple[str, str]]:
        """
        Processes abstracts into (name, text) pairs for Cartridge.
        Auto-generates names from the first few words of the abstract.
        """
        corpus = []
        for i, abs_text in enumerate(abstracts):
            # Clean name: first 3 words, alphanumeric
            words = [w for w in abs_text.split() if w.isalnum()]
            name_seed = "_".join(words[:3]) if len(words) >= 3 else f"Theory_{i}"
            name = f"{domain_name}_{name_seed}_{i}"
            corpus.append((name, abs_text))
        return corpus
