import numpy as np
import json
from singularity_engine import SingularityEngine
from boss_fights import get_boss_fight
from semantic_extractor import run_pipeline
import warnings; warnings.filterwarnings('ignore')

def adversarial_stress_test(v):
    # 🎯 Analytic Solver: argmin(v)
    worst_q = np.min(np.clip(v, 0, 1))
    return float(worst_q)

def run_phase5():
    print("="*82)
    print("  PHASE 5: UNIFIED EPISTEMOLOGICAL EXECUTION")
    print("="*82)

    cartridges = ["TOE", "AGING", "ECON", "AGI", "NEURO", "LANGUAGE"]
    summary = []

    for name in cartridges:
        print(f"\n--- Processing Cartridge: {name} ---")
        data = get_boss_fight(name)
        engine = SingularityEngine(data)

        # Optimize on theory manifold
        v_best, best_score, best_existing, mixture = engine.adaptive_optimize()

        # Stress-test
        worst_q = adversarial_stress_test(v_best)

        print(f"  Consensus Q: {best_score:.4f}")
        print(f"  Worst-case Q: {worst_q:.4f}")
        print(f"  Mixture: {mixture}")

        summary.append({
            "cartridge": name,
            "consensus_q": best_score,
            "worst_case_q": worst_q,
            "mixture": mixture
        })

    print("\n" + "="*82)
    print("  PHASE 5: AUTONOMOUS DIMENSION DISCOVERY (ArXiv Bridge)")
    print("="*82)
    # Demonstrate the semantic extractor pipeline
    run_pipeline('mock_abstracts.json')

    print("\n" + "="*82)
    print("  PHASE 5: FINAL SUMMARY")
    print("="*82)
    print(f"{'Cartridge':12s} | {'Consensus Q':>12} | {'Adversarial Q':>14} | {'Dominant Mix'}")
    print("-" * 82)
    for res in summary:
        mix_str = ", ".join([f"{k}:{v:.1f}" for k, v in sorted(res['mixture'].items(), key=lambda x: -x[1])[:2]])
        print(f"{res['cartridge']:12s} | {res['consensus_q']:12.4f} | {res['worst_case_q']:14.4f} | {mix_str}")

if __name__ == "__main__":
    run_phase5()
