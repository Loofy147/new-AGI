"""
episteme.benchmarks
===================
Standardized theoretical resolution benchmarks (Boss Fights).
"""
from __future__ import annotations
import numpy as np
from typing import Dict, List, Optional
from .cartridge import Cartridge
from .embed import NumericEmbedder

# 1. PHYSICS (TOE)
TOE_DATA = {
    "labels": ["IND", "DIS", "SYM", "TES", "ELE", "GRA", "HOL", "DET"],
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
    "labels": ["GEN", "ENT", "EPI", "SEN", "MET", "AUT", "TEL", "INF"],
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
    "labels": ["LIB", "INT", "LAB", "MON", "EQU", "EFF", "DEB", "VAL"],
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

# 4. CONSCIOUSNESS
NEURO_DATA = {
    "labels": ["G","C","S","A","H","V","P","T"],
    "weights": {
        "Corpus": np.array([0.18,0.20,0.18,0.16,0.12,0.08,0.05,0.03]),
        "Survey": np.array([0.0266,0.0789,0.1312,0.1355,0.0902,0.2044,0.1432,0.1900])
    },
    "theories": {
        "PP":           np.array([0.9493,0.9200,0.9380,0.9050,0.9000,0.8800,0.8600,0.8400]),
        "GWT":          np.array([0.9352,0.9100,0.9200,0.9000,0.8800,0.8200,0.8800,0.8800]),
        "IIT":          np.array([0.9053,0.8900,0.9600,0.8200,0.9200,0.8400,0.8000,0.7800]),
        "HOT":          np.array([0.8530,0.8200,0.9000,0.8000,0.9400,0.7600,0.8500,0.8800]),
    }
}

# 5. AGI LANGUAGE
LANGUAGE_DATA = {
    "labels": ['EXE', 'SMD', 'VER', 'DIF', 'CON', 'MEM', 'SYM', 'SYN'],
    "weights": {
        "Scale_Engineers": np.array([0.25, 0.05, 0.05, 0.25, 0.20, 0.05, 0.05, 0.10]),
        "Alignment_Lab":   np.array([0.05, 0.15, 0.25, 0.05, 0.05, 0.20, 0.20, 0.05])
    },
    "theories": {
        'Python+PyTorch': np.array([0.3, 0.8, 0.1, 0.9, 0.4, 0.3, 0.2, 1.0]),
        'Rust':           np.array([0.9, 0.3, 0.7, 0.1, 0.8, 1.0, 0.2, 0.5]),
        'Mojo':           np.array([0.9, 0.5, 0.3, 0.9, 0.8, 0.7, 0.2, 0.9]),
        'Lean/Coq':       np.array([0.2, 0.2, 1.0, 0.0, 0.2, 1.0, 0.9, 0.2]),
    }
}

def get_benchmark_cartridge(name: str) -> Optional[Cartridge]:
    registry = {
        "TOE": TOE_DATA,
        "AGING": AGING_DATA,
        "ECON": ECON_DATA,
        "NEURO": NEURO_DATA,
        "LANGUAGE": LANGUAGE_DATA,
    }
    data = registry.get(name)
    if not data: return None

    embedder = NumericEmbedder(data["theories"])
    corpus = [(n, "Pre-computed benchmark theory") for n in data["theories"]]

    return Cartridge(
        name=name,
        corpus=corpus,
        weights=data["weights"],
        dim_labels=data["labels"],
        embedder=embedder
    )

def list_benchmarks() -> List[str]:
    return ["TOE", "AGING", "ECON", "NEURO", "LANGUAGE"]
