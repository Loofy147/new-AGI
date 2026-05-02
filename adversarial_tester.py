import numpy as np
from scipy.optimize import minimize
import json

def get_adversarial_w(v, n_samples=1000):
    """
    Finds the weight vector w (in the 8D simplex) that minimizes q(v, w).
    """
    v = np.clip(v, 0, 1)

    # Objective function to minimize: dot(w, v)
    def objective(w):
        return np.dot(w, v)

    # Constraints: sum(w) == 1, 0 <= w_i <= 1
    cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = [(0, 1) for _ in range(len(v))]

    best_w = None
    min_q = float('inf')

    # Random restarts for global optimization
    for _ in range(10):
        w0 = np.random.dirichlet(np.ones(len(v)))
        res = minimize(objective, w0, method='SLSQP', bounds=bounds, constraints=cons)
        if res.success and res.fun < min_q:
            min_q = res.fun
            best_w = res.x

    return min_q, best_w

def run_stress_test(theories, n_samples=1000):
    results = {}
    for name, v in theories.items():
        min_q, worst_w = get_adversarial_w(v, n_samples)
        results[name] = {
            "min_q": float(min_q),
            "worst_w": worst_w.tolist()
        }
    return results

if __name__ == "__main__":
    # Test with Ouroboros singularity profile if available
    try:
        with open('ouroboros_results.json', 'r') as f:
            data = json.load(f)
            v_best = data['v_best']
            name = "Ouroboros_Singularity"
            theories = {name: np.array(v_best)}
    except:
        # Fallback to a simple test case
        theories = {"Test_Theory": np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2])}

    stress_results = run_stress_test(theories)
    print("Stress Test Results:")
    for name, res in stress_results.items():
        print(f"  Theory: {name}")
        print(f"  Worst-case Q: {res['min_q']:.4f}")
        print(f"  Worst-case w: {[round(x, 3) for x in res['worst_w']]}")
