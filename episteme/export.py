import json
import os
import numpy as np

class EpistemeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        return super().default(obj)

def export_json(results_all, output_path="results/unified_results.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
    with open(output_path, 'w') as f:
        json.dump(results_all, f, indent=4, cls=EpistemeEncoder)
    return output_path

def generate_latex_preprint(data_path, output_path):
    if not os.path.exists(data_path):
        return f"Error: {data_path} not found."

    with open(data_path, 'r') as f:
        results = json.load(f)

    isomorphisms = results.get("isomorphisms", [])
    domains = {k: v for k, v in results.items() if k != "isomorphisms"}

    latex = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{margin=1in}

\title{The Unified Epistemological Engine v2: Cross-Domain Manifold Consensus}
\author{Episteme Framework Core}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
This paper presents exact manifold-constrained consensus results for six theoretical domains. Using Latent Semantic Analysis (LSA) on specialized corpora, we identify optimal theoretical mixtures that resolve structural deadlocks between antagonistic expert camps.
\end{abstract}

\section{Methodology}
Dimensions are derived from a global LSA projection of domain corpora. Consensus is solved via exact Linear Programming constrained to the theory manifold (convex hull of existing theories).

\section{Results: Consensus Q Scores}
\begin{table}[h]
\centering
\begin{tabular}{lccl}
\toprule
Domain & Q-Score & Primary Mixture & Most Robust Theory \\
\midrule
"""
    for domain, res in domains.items():
        q = res['q_score']
        mix = res['mixture']
        sorted_mix = sorted(mix.items(), key=lambda x: -x[1])
        mix_str = ", ".join([f"{k} ({v:.2f})" for k, v in sorted_mix[:2]])

        robust = res['robustness']
        most_robust = min(robust.items(), key=lambda x: x[1]['fragility'])[0]

        latex += f"{domain.replace('_', ' ')} & {q:.3f} & {mix_str} & {most_robust} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\end{table}

\section{Cross-Domain Isomorphisms}
Correlation analysis reveals structural similarities across domain-optimal vectors:
\begin{itemize}
"""
    for iso in sorted(isomorphisms, key=lambda x: -abs(x['score'])):
        d1, d2 = iso['pair']
        latex += f"\\item {d1} $\\leftrightarrow$ {d2}: $r={iso['score']:+.3f}$\n"

    latex += r"""\end{itemize}

\section{Theory-Level Robustness (Top 15)}
\begin{table}[h]
\centering
\begin{tabular}{lcccc}
\toprule
Theory & Worst-case Q & Mean Q & Fragility \\
\midrule
"""
    all_robust = []
    for domain, res in domains.items():
        for name, r in res['robustness'].items():
            all_robust.append((name, r))

    all_robust.sort(key=lambda x: -x[1]['mean'])

    for name, r in all_robust[:15]:
        latex += f"{name.replace('_', ' ')} & {r['worst_exact']:.3f} & {r['mean']:.3f} & {r['fragility']:.3f} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\end{table}

\end{document}
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
    with open(output_path, 'w') as f:
        f.write(latex)
    return output_path
