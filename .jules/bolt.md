## 2025-05-15 - [Vectorizing Simulation Inner Loops]
**Learning:** In optimization loops (like the SingularityEngine's perturbation search), repeated dictionary access and small numpy operations (np.dot on single vectors) create significant overhead. Vectorizing the weight matrix and pre-generating random perturbations for the entire run allows Numpy to stay in C-land longer.
**Action:** Always look for opportunities to convert weight/coefficient dictionaries into matrices before entering high-iteration loops.

## 2025-05-15 - [Algorithmic Replacement of Black-Box Optimizers]
**Learning:** For specific optimization problems, like minimizing/maximizing a linear function over a bounded simplex (e.g., finding worst-case weights where sum(w)=1 and 0 <= w_i <= 0.5), a direct greedy O(N log N) selection is thousands of times faster than using a general-purpose optimizer like SLSQP with multiple restarts.
**Action:** When seeing  used for linear objectives on standard constraints, check if an exact greedy or dual solution exists before defaulting to numerical methods.
