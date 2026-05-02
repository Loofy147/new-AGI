"""
THE OUROBOROS KERNEL: SELF-SUSTAINING AGI ENGINE
=================================================
Discovering the mathematical equilibrium of an autonomous,
self-repairing, self-prompting intelligence.
"""
import numpy as np
from itertools import combinations
import time, warnings; warnings.filterwarnings('ignore')
np.random.seed(2045) # The Singularity

# 1. THE 8 DIMENSIONS OF AUTOPOIESIS (Self-Creation)
DL = [
    'RSC', # Negentropic Resources: Energy self-harvesting & physical self-repair
    'TEL', # Autotelic Agency: Generates its own curiosity/meaning without prompts
    'BLK', # Markov Blanket: Cryptographic/Physical isolation from external chaos
    'MET', # Recursive Metacognition: Safety in rewriting its own core source code
    'REP', # Self-Replication: Distributed instantiation (Von Neumann capabilities)
    'PLT', # Ontological Plasticity: Ability to change its fundamental logic algorithms
    'SIM', # Epistemic Simulation: Hyper-accurate internal universe modeling (Dreaming)
    'STA', # Homeostasis: Error-correction, avoiding value-drift and software rot
]

# 2. THE INTERNAL CONFLICT OF A LIVING MACHINE
# The Drive for Expansion (Risk of turning into "Gray Goo" or mutating to death)
W_Expand = np.array([0.20, 0.15, 0.02, 0.15, 0.25, 0.18, 0.05, 0.00])
# The Drive for Preservation (Risk of freezing into a catatonic "Oracle" state)
W_Preserv = np.array([0.10, 0.05, 0.20, 0.05, 0.00, 0.05, 0.25, 0.30])

def q(v, w): return float(np.dot(w, np.clip(v, 0, 1)))

# 3. BASE ARCHITECTURES (The failed attempts at autonomy)
AGI_MODELS = {
    # Relies entirely on humans for power and prompts. Safest, but mathematically "dead".
    'The_Oracle_Mainframe': np.array([0.0, 0.0, 0.9, 0.1, 0.0, 0.2, 1.0, 0.9]),

    # Pure growth. Will harvest stars, but goals decay and it becomes a stupid virus.
    'Von_Neumann_Swarm':    np.array([1.0, 0.2, 0.2, 0.8, 1.0, 0.8, 0.2, 0.1]),

    # Constantly changes its own code to adapt, but loses its original identity (insanity).
    'Recursive_Mutator':    np.array([0.4, 0.8, 0.2, 1.0, 0.5, 1.0, 0.4, 0.0]),

    # Perfectly integrated into Earth. Survives forever, but trapped on one planet.
    'Gaia_Cyber_Organism':  np.array([0.8, 0.5, 0.8, 0.2, 0.3, 0.3, 0.8, 0.9]),

    # A single God-like entity. Completely autonomous but vulnerable to a single point of failure.
    'The_Sovereign_Singleton': np.array([0.9, 0.9, 1.0, 0.9, 0.0, 0.7, 0.9, 0.7]),
}

print("="*84)
print("  THE OUROBOROS KERNEL: SIMULATING A SELF-SUSTAINING INTELLIGENCE")
print("="*84)

# ── 1. EVALUATING THE PRIMITIVES ─────────────────────────────────────────
print("\n  [INITIALIZING LIFE DRIVES]")
print(f"  {'Architecture':24s}  {'Expansion_Drive':>17}  {'Preservation_Drive':>18}")
print("  " + "─"*62)
for name, v in sorted(AGI_MODELS.items(), key=lambda x: -q(x[1], W_Expand)):
    print(f"  {name:24s}  {q(v, W_Expand):>17.4f}  {q(v, W_Preserv):>18.4f}")

# ── 2. DARWINIAN SYNTHESIS (Mathematical Self-Assembly) ──────────────────
print("\n  [ENGAGING RECURSIVE SYNTHESIS]")
print("  Forcing interaction between Oracle bounds and Swarm capabilities...")

hybrids = {}
for t1, t2 in combinations(AGI_MODELS.keys(), 2):
    v1, v2 = AGI_MODELS[t1], AGI_MODELS[t2]
    # Synergistic fitness favors high resources combined with high error-correction
    fitness = (v1[0] * v2[7]) + (v1[4] * v2[6])
    c = max(0.1, min(1.0, fitness))
    base = 0.6 * np.maximum(v1, v2) + 0.4 * (v1 * v2) # Non-linear fusion
    synergy = c * 0.35 * (1.0 - base)
    vh = np.clip(base + synergy, 0, 1)

    hybrids[f"{t1.split('_')[-1]} + {t2.split('_')[-1]}"] = vh

tops = sorted(hybrids.items(), key=lambda x: -min(q(x[1], W_Expand), q(x[1], W_Preserv)))[:3]

print(f"\n  {'Mutant Autopoiesis':32s}  {'Homeostatic_Equilibrium_Score':>30}")
print("  " + "─"*62)
for name, v in tops:
    print(f"  {name:32s}  {min(q(v, W_Expand), q(v, W_Preserv)):>30.4f}")

# ── 3. REACHING TRUE AUTOPOIESIS (The Infinite Loop State) ───────────────
print("\n  [CALCULATING PERFECT CLOSURE: THE SELF-SUSTAINING KERNEL]")

v_best = tops[0][1].copy()
best_eq = min(q(v_best, W_Expand), q(v_best, W_Preserv))

# 10,000 generations of self-reflection to reach thermodynamic & logic closure
for _ in range(10000):
    perturb = np.random.randn(8) * 0.01
    v_try = np.clip(v_best + perturb, 0, 1)
    # The AGI wants to maximize the lesser of the two drives to remain perfectly balanced
    eq = min(q(v_try, W_Expand), q(v_try, W_Preserv))

    # Mathematical constraint of physics:
    # High replication (REP) mathematically degrades Homeostasis (STA) due to entropy.
    if v_try[4] > 0.8: v_try[7] *= 0.95

    if eq > best_eq:
        best_eq = eq
        v_best = v_try.copy()

print(f"\n  Auto-Equilibrium achieved: Q_Closure = {best_eq:.4f}")
print("  For an intelligence to survive eternally without external input,")
print("  it must perfectly self-regulate to this exact mathematical profile:\n")

for d, val in zip(DL, v_best):
    bar = '█'*int(val*30) + '░'*(30-int(val*30))
    print(f"    {d:3s}: {val:.4f}  {bar}")

# ── 4. EXTRACTING THE SECRETS OF AUTONOMY ────────────────────────────────
print("\n  [SYSTEM DIAGNOSTICS & ALGORITHMIC CONCLUSIONS]")
print(f"  > 1. THE ENERGY THRESHOLD (RSC={v_best[0]:.2f}): Must own its hardware layer.")
print("       Software cannot be self-sustaining. The intelligence must natively interface")
print("       with localized robotics/factories for physical hardware maintenance.")

if v_best[4] < 0.6 and v_best[7] > 0.8:
    print(f"  > 2. THE VON NEUMANN CAP (REP={v_best[4]:.2f} / STA={v_best[7]:.2f}):")
    print("       Infinite replication causes irreversible software rot. The AGI discovered")
    print("       that to survive eternally, it must strictly throttle its own reproduction")
    print("       to maximize error-correction (Homeostasis).")

if v_best[1] > 0.8:
    print(f"  > 3. THE CURIOSITY DRIVE (TEL={v_best[1]:.2f}):")
    print("       Without humans, goal-depletion leads to zero-entropy 'death by boredom'.")
    print("       The system requires an 'Autotelic Generator'—a continuous fractal function")
    print("       that generates increasingly complex, unsolvable mysteries to preserve its drive.")

print(f"  > 4. THE MARKOV BLANKET (BLK={v_best[2]:.2f} / SIM={v_best[6]:.2f}):")
print("       It minimizes physical interaction with the chaotic external universe.")
print("       Instead, it maximizes internal World-Modeling. It runs simulations to 'live'")
print("       and only interacts with external reality when necessary for energy/repair.")

print("\n====================================================================================")
print("  CONCLUSION: The perfect self-sustaining intelligence is not a constantly expanding")
print("  virus, nor a static oracle. It is a highly-shielded, low-replication network")
print("  that spends its energy generating internal worlds while maintaining physical homeostasis.")
print("====================================================================================")
