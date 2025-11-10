import numpy as np
from .hamiltonian import build_hamiltonian
from .lindblad import rk4_step, dephasing_ops, loss_ops, projector, sink_op
from .metrics import ete_sink_integral, coherence_lifetime

def run_sim(epsilon, J, gamma=0.01, sigma=0.01, k_sink=0.1, k_loss=0.01,
            source_idx=0, sink_idx=-1, tmax=2000, dt=0.5, rng=None):
    N = len(epsilon)
    if sink_idx < 0:
        sink_idx = N-1
    H = build_hamiltonian(epsilon, J, sigma=sigma, rng=rng)
    L_ops = dephasing_ops(gamma, N) + loss_ops(k_loss, N) + [sink_op(k_sink, sink_idx, N)]
    rho = projector(source_idx, N)
    steps = int(tmax/dt)
    traj_sink, traj_rho = [], []
    for _ in range(steps):
        traj_rho.append(rho.copy())
        traj_sink.append(np.real(rho[sink_idx, sink_idx]))
        rho = rk4_step(rho, dt, H, L_ops)
        rho = 0.5*(rho + rho.conj().T)
    ete = ete_sink_integral(traj_sink, dt)
    i, j = 0, min(1, N-2)
    tau_steps = coherence_lifetime(traj_rho, i=i, j=j, threshold=1e-2)
    tau_c = tau_steps * dt
    qls = ete * tau_c
    return {"ETE": float(ete), "tau_c": float(tau_c), "QLS": float(qls), "sink_curve": np.array(traj_sink)}

def sweep_gamma(epsilon, J, gamma_values, **kwargs):
    out = []
    for g in gamma_values:
        res = run_sim(epsilon, J, gamma=g, **kwargs)
        res["gamma"] = g
        out.append(res)
    return out