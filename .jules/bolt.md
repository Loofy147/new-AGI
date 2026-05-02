## 2025-05-15 - [Vectorizing Simulation Inner Loops]
**Learning:** In optimization loops (like the SingularityEngine's perturbation search), repeated dictionary access and small numpy operations (np.dot on single vectors) create significant overhead. Vectorizing the weight matrix and pre-generating random perturbations for the entire run allows Numpy to stay in C-land longer.
**Action:** Always look for opportunities to convert weight/coefficient dictionaries into matrices before entering high-iteration loops.
