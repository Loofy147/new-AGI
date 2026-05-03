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

# 4. AUTOPOIETIC AGI
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

# 5. CONSCIOUSNESS (Expanded Phase 4 Set)
NEURO_DATA = {
    "dimensions": ["G","C","S","A","H","V","P","T"],
    "weights": {
        "Corpus": np.array([0.18,0.20,0.18,0.16,0.12,0.08,0.05,0.03]),
        "Survey": np.array([0.0266,0.0789,0.1312,0.1355,0.0902,0.2044,0.1432,0.1900])
    },
    "theories": {
        "PP":           np.array([0.9493,0.9200,0.9380,0.9050,0.9000,0.8800,0.8600,0.8400]),
        "GWT":          np.array([0.9352,0.9100,0.9200,0.9000,0.8800,0.8200,0.8800,0.8800]),
        "IIT":          np.array([0.9053,0.8900,0.9600,0.8200,0.9200,0.8400,0.8000,0.7800]),
        "HOT":          np.array([0.8530,0.8200,0.9000,0.8000,0.9400,0.7600,0.8500,0.8800]),
        "IRT_Latent":   np.array([0.8600,0.9200,0.8600,0.9900,0.8000,0.7500,0.7000,0.5500]),
        "Thermo_Phase": np.array([0.9400,0.8700,0.9200,0.8500,0.8200,0.8600,0.6500,0.6800]),
        "ECC_Attn":     np.array([0.8500,0.8900,0.8700,0.8700,0.7500,0.7800,0.6500,0.5200]),
        "GameFreeWill": np.array([0.8200,0.8400,0.8200,0.9000,0.8700,0.7400,0.7100,0.5700]),
        "ImmuneSelf":   np.array([0.7800,0.7500,0.8000,0.8200,0.8500,0.7000,0.6700,0.6200]),
        "4WAY_Grand":   np.array([1.000, 0.979, 0.996, 1.000, 0.953, 0.933, 0.906, 0.882]),
    }
}

# 6. AGI LANGUAGE
LANGUAGE_DATA = {
    "dimensions": ['EXE', 'SMD', 'VER', 'DIF', 'CON', 'MEM', 'SYM', 'SYN'],
    "weights": {
        "Scale_Engineers": np.array([0.25, 0.05, 0.05, 0.25, 0.20, 0.05, 0.05, 0.10]),
        "Alignment_Lab":   np.array([0.05, 0.15, 0.25, 0.05, 0.05, 0.20, 0.20, 0.05])
    },
    "theories": {
        'Python+PyTorch': np.array([0.3, 0.8, 0.1, 0.9, 0.4, 0.3, 0.2, 1.0]),
        'Rust':           np.array([0.9, 0.3, 0.7, 0.1, 0.8, 1.0, 0.2, 0.5]),
        'Mojo':           np.array([0.9, 0.5, 0.3, 0.9, 0.8, 0.7, 0.2, 0.9]),
        'Lisp/Clojure':   np.array([0.4, 1.0, 0.2, 0.3, 0.6, 0.5, 0.8, 0.8]),
        'Julia':          np.array([0.8, 0.8, 0.2, 0.8, 0.7, 0.4, 0.4, 0.8]),
        'Lean/Coq':       np.array([0.2, 0.2, 1.0, 0.0, 0.2, 1.0, 0.9, 0.2]),
        'Erlang/Elixir':  np.array([0.6, 0.5, 0.3, 0.1, 1.0, 0.8, 0.3, 0.7]),
        'CUDA_C++':       np.array([1.0, 0.1, 0.1, 0.5, 0.9, 0.2, 0.1, 0.3]),
    }
}

def get_boss_fight(name):
    if name == "TOE": return TOE_DATA
    if name == "AGING": return AGING_DATA
    if name == "ECON": return ECON_DATA
    if name == "AGI": return AGI_DATA
    if name == "NEURO": return NEURO_DATA
    if name == "LANGUAGE": return LANGUAGE_DATA
    return None
