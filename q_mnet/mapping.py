import numpy as np
import yaml

def map_expr_to_params(expr_series, mapping_yaml, N_nodes, edge_list):
    cfg = yaml.safe_load(open(mapping_yaml, "r"))
    e0 = cfg.get("epsilon0", 0.0)
    alpha = cfg.get("alpha", 0.02)
    J0 = cfg.get("J0", 0.03)
    Jmax = cfg.get("Jmax", 0.05)

    # demo mapping: use average z-score; you can replace with node-specific mapping table
    zval = float(expr_series.mean())
    zvals = np.array([zval]*N_nodes)

    epsilon = e0 - alpha*zvals

    J = np.zeros((N_nodes, N_nodes))
    for (i,j) in edge_list:
        zij = max(0.0, zvals[i]) * max(0.0, zvals[j])
        J[i,j] = J[j,i] = min(Jmax, J0*np.sqrt(zij + 1e-12))
    return epsilon, J, cfg