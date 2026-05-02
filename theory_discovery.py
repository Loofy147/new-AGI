import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import warnings; warnings.filterwarnings('ignore')

def discover_theories(abstracts_path, axes_path):
    """
    Maps specific papers (theories) to the discovered PCA axes.
    """
    with open(abstracts_path, 'r') as f:
        abstracts = json.load(f)

    with open(axes_path, 'r') as f:
        axes_data = json.load(f)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(abstracts)

    # Reconstruct PCA object
    pca = PCA(n_components=len(axes_data['variance_ratio']))
    pca.components_ = np.array(axes_data['components'])
    pca.mean_ = np.mean(embeddings, axis=0) # Approximation of the original mean

    # Project embeddings into PCA space
    projections = pca.transform(embeddings)

    # Normalize projections to [0, 1] for the engine
    # We use min-max scaling per dimension across all samples
    v_min = projections.min(axis=0)
    v_max = projections.max(axis=0)
    v_normalized = (projections - v_min) / (v_max - v_min)

    theories = {}
    for i, abstract in enumerate(abstracts):
        # Use first 3 words as name
        name = "_".join(abstract.split()[:3]).replace(".", "").replace(",", "")
        theories[name] = v_normalized[i].tolist()

    return theories

if __name__ == "__main__":
    theories = discover_theories('mock_abstracts.json', 'discovered_axes.json')
    with open('discovered_theories.json', 'w') as f:
        json.dump(theories, f, indent=4)
    print(f"Discovered {len(theories)} theories and saved to discovered_theories.json")

    # Print sample
    sample_key = list(theories.keys())[0]
    print(f"Sample Theory '{sample_key}': {theories[sample_key][:4]}...")
