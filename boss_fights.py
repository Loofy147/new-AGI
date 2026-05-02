import numpy as np

# 1. THEORY OF EVERYTHING (PHYSICS)
TOE_DATA = {
    "dimensions": ["IND", "DIS", "SYM", "TES", "ELE", "GRA", "HOL", "DET"],
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
    "dimensions": ["GEN", "ENT", "EPI", "SEN", "MET", "AUT", "TEL", "INF"],
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
    "dimensions": ["LIB", "INT", "LAB", "MON", "EQU", "EFF", "DEB", "VAL"],
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

# ⚡ Expansion: 4. AUTOPOIETIC AGI (Ouroboros Integration)
AGI_DATA = {
    "dimensions": ["RSC", "TEL", "BLK", "MET", "REP", "PLT", "SIM", "STA"],
    "weights": {
        "Expansionists":  np.array([0.20, 0.15, 0.02, 0.15, 0.25, 0.18, 0.05, 0.00]),
        "Preservationists": np.array([0.10, 0.05, 0.20, 0.05, 0.00, 0.05, 0.25, 0.30])
    },
    "theories": {
        "Oracle_Mainframe": np.array([0.0, 0.0, 0.9, 0.1, 0.0, 0.2, 1.0, 0.9]),
        "Von_Neumann_Swarm": np.array([1.0, 0.2, 0.2, 0.8, 1.0, 0.8, 0.2, 0.1]),
        "Recursive_Mutator": np.array([0.4, 0.8, 0.2, 1.0, 0.5, 1.0, 0.4, 0.0]),
        "Gaia_Cyber_Organism": np.array([0.8, 0.5, 0.8, 0.2, 0.3, 0.3, 0.8, 0.9])
    }
}

# ⚡ Expansion: 5. CONSCIOUSNESS (Neuroscience)
NEURO_DATA = {
    "dimensions": [
        "IIT", # Integrated Information
        "GWT", # Global Workspace
        "HOT", # Higher Order Thought
        "PAS", # Panpsychism (Fundamental property)
        "EMB", # Embodiment / Sensorimotor
        "QUA", # Qualia / Subjective experience
        "SYN", # Synchronization / Gamma bands
        "PRE", # Predictive Processing
    ],
    "weights": {
        "Materialists": np.array([0.20, 0.25, 0.15, 0.00, 0.10, 0.05, 0.15, 0.10]),
        "Idealists":     np.array([0.05, 0.00, 0.05, 0.40, 0.05, 0.30, 0.05, 0.10])
    },
    "theories": {
        "Integrated_Info": np.array([1.0, 0.2, 0.3, 0.8, 0.1, 0.9, 0.6, 0.4]),
        "Global_Workspace": np.array([0.3, 1.0, 0.8, 0.1, 0.4, 0.3, 0.7, 0.9]),
        "Panpsychism":      np.array([0.1, 0.0, 0.1, 1.0, 0.1, 1.0, 0.1, 0.1]),
        "Predictive_Mind":  np.array([0.4, 0.6, 0.4, 0.2, 0.8, 0.5, 0.5, 1.0])
    }
}

def get_boss_fight(name):
    if name == "TOE": return TOE_DATA
    if name == "AGING": return AGING_DATA
    if name == "ECON": return ECON_DATA
    if name == "AGI": return AGI_DATA
    if name == "NEURO": return NEURO_DATA
    return None
