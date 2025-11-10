import numpy as np

def lindblad_rhs(rho, H, L_ops):
    i = 1j
    comm = H @ rho - rho @ H
    drho = -i*comm
    for L in L_ops:
        Lrho = L @ rho @ L.conj().T
        LL = L.conj().T @ L
        drho += Lrho - 0.5*(LL @ rho + rho @ LL)
    return drho

def rk4_step(rho, dt, H, L_ops):
    k1 = lindblad_rhs(rho, H, L_ops)
    k2 = lindblad_rhs(rho + 0.5*dt*k1, H, L_ops)
    k3 = lindblad_rhs(rho + 0.5*dt*k2, H, L_ops)
    k4 = lindblad_rhs(rho + dt*k3, H, L_ops)
    return rho + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

def projector(i, N):
    e = np.zeros((N,1)); e[i,0] = 1.0
    return e @ e.T

def dephasing_ops(gamma, N):
    return [np.sqrt(gamma) * projector(i, N) for i in range(N)]

def sink_op(rate, sink_idx, N):
    P = projector(sink_idx, N)
    return np.sqrt(rate) * P

def loss_ops(rate, N):
    return [np.sqrt(rate) * projector(i, N) for i in range(N)]