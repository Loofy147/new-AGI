"""
episteme
=======
Unified Epistemological Engine v2.
Theoretical deadlock resolution through manifold consensus.
"""
from .embed       import EmbedResult, LSAEmbedder
from .consensus   import ConsensusResult, StressResult, lp_manifold_consensus, stress_test
from .cartridge   import Cartridge, CartridgeResult, resolve
from .isomorphism import IsomorphismResult, cross_domain_correlations, rank_bridges
from .report      import generate_text_report, generate_latex
from .export      import EpistemeEncoder, export_json
from .discovery   import ArXivFetcher, TheoryDiscoverer
from .engine      import SingularityEngine

__version__ = "2.1.0"
__all__ = [
    "Cartridge",
    "CartridgeResult",
    "resolve",
    "cross_domain_correlations",
    "rank_bridges",
    "generate_text_report",
    "generate_latex",
    "export_json",
    "ArXivFetcher",
    "TheoryDiscoverer",
    "SingularityEngine",
]
