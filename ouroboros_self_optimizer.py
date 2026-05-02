import numpy as np
import json
import os

def self_tune_weights(history_path, current_weights):
    if not os.path.exists(history_path):
        return current_weights

    with open(history_path, 'r') as f:
        data = json.load(f)
        v_best = np.array(data['v_best'])

    weak_dims = v_best < 0.8
    if not np.any(weak_dims):
        return current_weights

    print(f"Self-Optimizing: Detected weaknesses in dimensions {np.where(weak_dims)[0]}")

    new_weights = current_weights.copy()
    for i in range(len(new_weights)):
        if weak_dims[i]:
            if new_weights[i] == 0:
                new_weights[i] = 0.05 # Give it a baseline weight if it was 0
            else:
                new_weights[i] *= 1.20 # Increase weight

    # Re-normalize
    new_weights /= np.sum(new_weights)
    return new_weights

if __name__ == "__main__":
    W_Expand = np.array([0.20, 0.15, 0.02, 0.15, 0.25, 0.18, 0.05, 0.00])
    # Assume previous run had low STA (dimension 7)
    with open('ouroboros_results.json', 'w') as f:
        json.dump({"v_best": [1.0, 0.9, 1.0, 0.9, 0.8, 0.9, 1.0, 0.7]}, f)

    updated_W = self_tune_weights('ouroboros_results.json', W_Expand)
    print(f"Original W: {W_Expand}")
    print(f"Self-Tuned W: {[round(x, 4) for x in updated_W]}")
