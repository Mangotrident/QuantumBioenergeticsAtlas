import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from qle.simulate import run_sim

def edge_sensitivity_map(epsilon, J, gamma=0.02, sigma=0.01,
                         k_sink=0.1, k_loss=0.01, source_idx=0, sink_idx=-1,
                         tmax=2000, dt=0.5, delta=0.05, out_png="coherence_map.png"):
    """
    Perturbs each edge weight ±delta and measures ΔETE relative to baseline.
    Produces a heatmap showing which edges most affect transport efficiency.
    """
    N = len(epsilon)
    base = run_sim(epsilon, J, gamma, sigma, k_sink, k_loss, source_idx, sink_idx, tmax, dt)
    base_ete = base["ETE"]
    sensitivity = np.zeros_like(J)

    for i in range(N):
        for j in range(i+1, N):
            if J[i,j] == 0: continue
            Jp, Jm = J.copy(), J.copy()
            Jp[i,j] = Jp[j,i] = J[i,j]*(1+delta)
            Jm[i,j] = Jm[j,i] = J[i,j]*(1-delta)
            ete_plus = run_sim(epsilon, Jp, gamma, sigma, k_sink, k_loss, source_idx, sink_idx, tmax, dt)["ETE"]
            ete_minus = run_sim(epsilon, Jm, gamma, sigma, k_sink, k_loss, source_idx, sink_idx, tmax, dt)["ETE"]
            sensitivity[i,j] = sensitivity[j,i] = 0.5*(abs(ete_plus-base_ete)+abs(ete_minus-base_ete))

    fig, ax = plt.subplots(figsize=(6,5))
    sns.heatmap(sensitivity, annot=True, fmt=".3f", cmap="mako", ax=ax)
    ax.set_title("Metabolic Coherence Map (Edge Sensitivity ΔETE)")
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()
    return sensitivity
