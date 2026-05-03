import json
import os
import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import warnings; warnings.filterwarnings('ignore')

def run_pipeline(abstracts_path, n_dims=8, cache_dir=".cache"):
    print(f"Loading abstracts from {abstracts_path}...")
    with open(abstracts_path, 'r') as f:
        abstracts = json.load(f)

    # ⚡ Performance Boost: Embedding Caching
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Create a unique hash for the current set of abstracts
    content_hash = hashlib.md5(json.dumps(abstracts, sort_keys=True).encode()).hexdigest()
    cache_path = os.path.join(cache_dir, f"embeddings_{content_hash}.npy")

    if os.path.exists(cache_path):
        print(f"Loading cached embeddings from {cache_path}...")
        embeddings = np.load(cache_path)
    else:
        print("Encoding abstracts (this may take a moment)...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(abstracts)
        np.save(cache_path, embeddings)
        print(f"Embeddings cached to {cache_path}")

    print(f"Discovering {n_dims} orthogonal axes of tension...")
    pca = PCA(n_components=n_dims)
    projections = pca.fit_transform(embeddings)

    # Normalize projections to [0, 1] for the Epistemological Engine
    p_min = projections.min(axis=0)
    p_max = projections.max(axis=0)
    # Avoid division by zero
    p_range = np.where(p_max - p_min == 0, 1, p_max - p_min)
    v_normalized = (projections - p_min) / p_range

    # 8-dimensional space discovered autonomously
    dimensions = [f"PC{i+1}" for i in range(n_dims)]

    # Map back to theories
    theories = {}
    for i, abstract in enumerate(abstracts):
        name = "_".join(abstract.split()[:3]).replace(".", "").replace(",", "")
        theories[name] = v_normalized[i].tolist()

    results = {
        "dimensions": dimensions,
        "theories": theories,
        "variance_explained": pca.explained_variance_ratio_.tolist()
    }

    with open('discovered_engine_v2.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("Pipeline complete. discovered_engine_v2.json written.")
    return results

if __name__ == "__main__":
    run_pipeline('mock_abstracts.json')
