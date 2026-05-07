"""
episteme.paper_generator
========================
Generates a complete LaTeX preprint from SingularityEngine results.
"""
import episteme as ep
from episteme.report import generate_latex
import os

def generate_preprint(engine, output_path="results/unified_preprint.tex"):
    """
    Synthesizes the unified preprint from the engine's resolved cartridges.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    latex_content = generate_latex(engine.results)
    with open(output_path, "w") as f:
        f.write(latex_content)
    return output_path

if __name__ == "__main__":
    # Test generation with benchmarks
    engine = ep.SingularityEngine()
    for name in ep.list_benchmarks():
        c = ep.get_benchmark_cartridge(name)
        engine.cartridges.append(c)
    engine.run()
    path = generate_preprint(engine)
    print(f"Preprint generated at: {path}")
