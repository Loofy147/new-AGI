import json
import os
import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import warnings; warnings.filterwarnings('ignore')

def discover_theories(abstracts_path, axes_path, cache_dir=".cache"):
    """
    Maps specific papers (theories) to the discovered PCA axes.
    """
    with open(abstracts_path, 'r') as f:
        abstracts = json.load(f)

    with open(axes_path, 'r') as f:
        axes_data = json.load(f)

    # ⚡ Performance Boost: Embedding Caching
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    content_hash = hashlib.md5(json.dumps(abstracts, sort_keys=True).encode()).hexdigest()
    cache_path = os.path.join(cache_dir, f"embeddings_{content_hash}.npy")

    if os.path.exists(cache_path):
        print(f"Loading cached embeddings from {cache_path}...")
        embeddings = np.load(cache_path)
    else:
        print("Encoding abstracts...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(abstracts)
        np.save(cache_path, embeddings)

    # Reconstruct PCA object
    pca = PCA(n_components=len(axes_data['variance_ratio']))
    pca.components_ = np.array(axes_data['components'])
    pca.mean_ = np.mean(embeddings, axis=0) # Approximation of the original mean

    # Project embeddings into PCA space
    projections = pca.transform(embeddings)

    # Normalize projections to [0, 1] for the engine
    v_min = projections.min(axis=0)
    v_max = projections.max(axis=0)
    v_range = np.where(v_max - v_min == 0, 1, v_max - v_min)
    v_normalized = (projections - v_min) / v_range

    theories = {}
    for i, abstract in enumerate(abstracts):
        name = "_".join(abstract.split()[:3]).replace(".", "").replace(",", "")
        theories[name] = v_normalized[i].tolist()

    return theories

if __name__ == "__main__":
    if os.path.exists('mock_abstracts.json') and os.path.exists('discovered_axes.json'):
        theories = discover_theories('mock_abstracts.json', 'discovered_axes.json')
        with open('discovered_theories.json', 'w') as f:
            json.dump(theories, f, indent=4)
        print(f"Discovered {len(theories)} theories and saved to discovered_theories.json")
