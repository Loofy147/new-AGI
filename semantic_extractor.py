import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import warnings; warnings.filterwarnings('ignore')

def run_pipeline(abstracts_path, n_dims=8):
    print(f"Loading abstracts from {abstracts_path}...")
    with open(abstracts_path, 'r') as f:
        abstracts = json.load(f)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(abstracts)

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
