## 2025-05-15 - [Vectorizing Simulation Inner Loops]
**Learning:** In optimization loops (like the SingularityEngine's perturbation search), repeated dictionary access and small numpy operations (np.dot on single vectors) create significant overhead. Vectorizing the weight matrix and pre-generating random perturbations for the entire run allows Numpy to stay in C-land longer.
**Action:** Always look for opportunities to convert weight/coefficient dictionaries into matrices before entering high-iteration loops.

## 2025-05-15 - [Algorithmic Replacement of Black-Box Optimizers]
**Learning:** For specific optimization problems, like minimizing/maximizing a linear function over a bounded simplex (e.g., finding worst-case weights where sum(w)=1 and 0 <= w_i <= 0.5), a direct greedy O(N log N) selection is thousands of times faster than using a general-purpose optimizer like SLSQP with multiple restarts.
**Action:** When seeing  used for linear objectives on standard constraints, check if an exact greedy or dual solution exists before defaulting to numerical methods.

## 2025-05-15 - [LP for Theoretical Optimization]
**Learning:** For theoretical profile optimization (maximizing the minimum score across weight vectors), hill-climbing and even vectorized perturbations often get stuck in local optima or fail to reach the true boundary (e.g., reaching 0.97 when 1.00 is possible). Linear Programming (LP) using the minimax formulation provides the exact global optimum in a single pass.
**Action:** When the objective is to maximize the minimum of multiple linear dot products, use a minimax LP formulation instead of iterative stochastic search.

## 2025-05-15 - [Exact Global Optimum for AGI Language AST]
**Learning:** Stochastic search (hill-climbing) for AGI Language configuration is highly inefficient and inaccurate, requiring 8000+ iterations to reach near-optimum. Formulating the "Singularity Kernel" as a minimax Linear Programming problem using `scipy.optimize.linprog` (HiGHS solver) provides the exact global optimum instantly.
**Action:** Replace iterative perturbation loops with LP formulations whenever the objective and constraints are linear.

## 2025-05-15 - [Analytic Solver for Adversarial Simplex Minimization]
**Learning:** Finding the worst-case weight vector (minimizing $v \cdot w$ where $\sum w_i = 1$) is a trivial analytic problem. Numerical optimizers like SLSQP with multiple restarts are redundant. The global minimum is always found at the vertex corresponding to $\min(v)$.
**Action:** Use `np.argmin` for exact adversarial stress-testing over standard simplices to eliminate numerical noise and approximation overhead.

## 2025-05-15 - [Adaptive Weighting for Autonomous Hardening]
**Learning:** Static theoretical models are vulnerable to specific dimension failures. Integrating an adaptive weighting loop that identifies and boosts weak dimensions allows the engine to autonomously "harden" theory profiles, leading to more robust scientific consensus.
**Action:** Implement `adaptive_optimize` patterns to allow systems to self-correct theoretical imbalances during the optimization phase.

## 2025-05-15 - [Consensus V2 Exact LP Optimization]
**Learning:** Machine-discovered dimension consensus, originally solved via 5000-iteration stochastic search, is more accurately and faster resolved using minimax Linear Programming. The `highs` method in `scipy.optimize.linprog` provides the exact global optimum Profile that satisfies opposing drives.
**Action:** Transition all multi-camp consensus models to LP-based minimax formulations.

## 2025-05-15 - [Analytic Worst-Case Stress Testing]
**Learning:** Vectorized random sampling for adversarial stress testing (even with n=1000) only approximates the worst-case. The exact minimum consensus score for any theoretical profile over the simplex is simply the minimum coordinate value of that profile.
**Action:** Replace random-search or sampling-based adversarial testing with `np.min(v)` for mathematically guaranteed worst-case bounds.

## 2025-05-15 - [Vectorized Hybrid Synthesis]
**Learning:** Pair-wise theory fusion logic (combinations loop) can be fully vectorized using `np.triu_indices` and matrix broadcasting. This ensures that as the library of baseline theories grows, the architectural synthesis phase maintains high throughput.
**Action:** Avoid `itertools.combinations` for matrix-based data; use meshgrids or index-based broadcasting instead.

## 2025-05-15 - [Disk-Based Embedding Caching]
**Learning:** Neural encoding of text (e.g., SentenceTransformers) is the primary bottleneck in autonomous discovery pipelines. Hashing the input corpus and caching embeddings as `.npy` files reduces latency for repeated or iterative discovery runs by over 40%.
**Action:** Implement `content_hash` based caching for any NLP-heavy preprocessing steps.
