import numpy as np

def build_hamiltonian(epsilon, J, sigma=0.0, rng=None):
    N = len(epsilon)
    if rng is None:
        rng = np.random.default_rng(0)
    eps = np.array(epsilon, dtype=float).copy()
    if sigma > 0:
        eps += rng.normal(0, sigma, size=N)
    H = np.array(J, dtype=float).copy()
    np.fill_diagonal(H, eps)
    H = 0.5*(H + H.T)  # ensure Hermitian
    return H