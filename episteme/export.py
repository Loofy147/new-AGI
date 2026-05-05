"""
episteme.export
===============
JSON serialization with custom NumPy-aware encoding.
"""
from __future__ import annotations
import json
import numpy as np
from typing import Any

class EpistemeEncoder(json.JSONEncoder):
    """Handles NumPy arrays, types and Python booleans for JSON export."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, (np.int64, np.int32, np.integer)):
            return int(obj)
        if isinstance(obj, (np.float64, np.float32, np.floating)):
            return float(obj)
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)

def export_json(data: Any, path: str = "results/unified_results.json") -> str:
    """Export data to JSON using EpistemeEncoder."""
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, cls=EpistemeEncoder)
    return path
