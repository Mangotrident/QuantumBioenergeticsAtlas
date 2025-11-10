import numpy as np
from qle.simulate import sweep_gamma

def test_enaqt_bell():
    N = 6
    epsilon = np.zeros(N)
    J = np.zeros((N,N))
    for i in range(N-1):
        J[i,i+1] = J[i+1,i] = 0.03
    gammas = np.linspace(0.0, 0.05, 11)
    res = sweep_gamma(epsilon, J, gammas, sigma=0.01, k_sink=0.1, k_loss=0.01)
    etes = [r["ETE"] for r in res]
    m = int(np.argmax(etes))
    assert m not in (0, len(etes)-1)
if __name__ == "__main__":
    test_enaqt_bell()
    print("OK")