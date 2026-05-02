import numpy as np

# 1. THEORY OF EVERYTHING (PHYSICS)
TOE_DATA = {
    "dimensions": [
        "IND", # Background Independence (Dynamic space-time)
        "DIS", # Discreteness (Quantized space-time)
        "SYM", # Super-symmetry (Higher dimensional balance)
        "TES", # Testability (Experimental proximity)
        "ELE", # Mathematical Elegance / Rigor
        "GRA", # Gravity-Quantum Unification
        "HOL", # Holographic/Twistor Geometric fit
        "DET", # Determinism (Classical-Quantum bridge)
    ],
    "weights": {
        "Fundamentalists": np.array([0.25, 0.20, 0.05, 0.05, 0.20, 0.20, 0.05, 0.00]),
        "Phenomenologists": np.array([0.05, 0.05, 0.15, 0.30, 0.05, 0.10, 0.15, 0.15])
    },
    "theories": {
        "String_Theory":     np.array([0.4, 0.1, 1.0, 0.1, 0.9, 0.9, 0.8, 0.2]),
        "Loop_Quantum_Grav": np.array([1.0, 1.0, 0.2, 0.2, 0.7, 0.9, 0.3, 0.4]),
        "Wolfram_Physics":   np.array([0.8, 1.0, 0.1, 0.3, 0.6, 0.6, 0.4, 1.0]),
        "Twistor_Theory":    np.array([0.7, 0.4, 0.3, 0.2, 1.0, 0.5, 1.0, 0.6])
    }
}

# 2. BIOLOGICAL AGING
AGING_DATA = {
    "dimensions": [
        "GEN", # Programmed Genetics (Death program)
        "ENT", # Entropic Damage (Wear and tear)
        "EPI", # Epigenetic Drift (Information loss)
        "SEN", # Cellular Senescence (Zombie cells)
        "MET", # Metabolic Rate / IGF-1
        "AUT", # Autophagy / Repair Capacity
        "TEL", # Telomere Attrition
        "INF", # Inflammaging (Systemic decay)
    ],
    "weights": {
        "Programmers": np.array([0.30, 0.05, 0.25, 0.05, 0.10, 0.10, 0.15, 0.00]),
        "Accumulators": np.array([0.05, 0.30, 0.05, 0.20, 0.10, 0.10, 0.00, 0.20])
    },
    "theories": {
        "Genetic_Clock":    np.array([1.0, 0.2, 0.8, 0.4, 0.6, 0.5, 0.9, 0.3]),
        "DNA_Damage":       np.array([0.3, 1.0, 0.4, 0.6, 0.5, 0.7, 0.3, 0.5]),
        "Epigenetic_Shift": np.array([0.8, 0.5, 1.0, 0.4, 0.3, 0.4, 0.2, 0.6]),
        "Senescence_Model": np.array([0.4, 0.6, 0.5, 1.0, 0.4, 0.3, 0.4, 1.0])
    }
}

# 3. MACROECONOMICS
ECON_DATA = {
    "dimensions": [
        "LIB", # Individual Liberty (Austrian)
        "INT", # State Intervention (Keynesian)
        "LAB", # Labor/Class Struggle (Marxist)
        "MON", # Monetary Expansion (MMT/Friedman)
        "EQU", # Wealth Equality
        "EFF", # Market Efficiency
        "DEB", # Debt Tolerance
        "VAL", # Objective Theory of Value
    ],
    "weights": {
        "Individualists": np.array([0.40, 0.00, 0.00, 0.10, 0.00, 0.40, 0.00, 0.10]),
        "Collectivists":  np.array([0.00, 0.30, 0.30, 0.00, 0.30, 0.00, 0.10, 0.00])
    },
    "theories": {
        "Austrian_School": np.array([1.0, 0.0, 0.1, 0.0, 0.1, 0.9, 0.0, 0.8]),
        "Keynesianism":    np.array([0.4, 1.0, 0.3, 0.7, 0.5, 0.6, 0.8, 0.2]),
        "Marxism":         np.array([0.1, 0.8, 1.0, 0.1, 1.0, 0.2, 0.4, 1.0]),
        "MMT":             np.array([0.3, 0.9, 0.4, 1.0, 0.6, 0.4, 1.0, 0.1])
    }
}

def get_boss_fight(name):
    if name == "TOE": return TOE_DATA
    if name == "AGING": return AGING_DATA
    if name == "ECON": return ECON_DATA
    return None
