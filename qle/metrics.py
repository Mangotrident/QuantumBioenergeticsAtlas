import numpy as np

def ete_sink_integral(traj_sink_pop, dt):
    return float(np.trapz(traj_sink_pop, dx=dt))

def coherence_lifetime(traj_rho, i=0, j=1, threshold=1e-2):
    mags = [abs(r[i,j]) for r in traj_rho]
    if not mags:
        return 0.0
    init = mags[0] if mags[0] > 0 else max(mags)
    for t, m in enumerate(mags):
        if init > 0 and m <= threshold*init:
            return t
    return len(mags)