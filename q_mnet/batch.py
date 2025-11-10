import json, yaml, os
import pandas as pd
import numpy as np
from tqdm import tqdm
from q_mnet.preprocess import tpm_to_zscores
from q_mnet.mapping import map_expr_to_params
from qle.simulate import sweep_gamma

def load_graph(graph_json):
    g = json.load(open(graph_json,"r"))
    nodes = [n["id"] for n in g["nodes"]]
    idx = {n:i for i,n in enumerate(nodes)}
    edges = [(idx[u], idx[v]) for (u,v) in g["edges"]]
    return nodes, edges

def cohort_metrics(expr_csv, labels_csv, graph_json, mapping_yaml, out_parquet):
    expr = pd.read_csv(expr_csv, index_col=0)
    labels = pd.read_csv(labels_csv)
    nodes, edges = load_graph(graph_json)
    z = tpm_to_zscores(expr)

    cfg = yaml.safe_load(open(mapping_yaml,"r"))
    g0, g1, gs = cfg["gamma_sweep"]
    gammas = np.arange(g0, g1+1e-12, gs)

    rows = []
    for sid, series in tqdm(z.items(), desc="Samples"):
        epsilon, J, _ = map_expr_to_params(series, mapping_yaml, len(nodes), edges)
        res = sweep_gamma(epsilon, J, gammas, sigma=cfg["sigma"], k_sink=cfg["k_sink"], k_loss=cfg["k_loss"],
                          source_idx=cfg.get("source_idx",0), sink_idx=cfg.get("sink_idx",len(nodes)-1),
                          tmax=cfg.get("tmax",2000), dt=cfg.get("dt",0.5))
        etes = [r["ETE"] for r in res]
        gstar = float(gammas[int(np.argmax(etes))])
        ete_peak = float(np.max(etes))
        tau_c = float(np.mean([r["tau_c"] for r in res]))
        qls = float(np.mean([r["QLS"] for r in res]))
        ph = labels.loc[labels["sample_id"]==sid, "phenotype"]
        phenotype = ph.values[0] if len(ph)>0 else "NA"
        rows.append({"sample_id":sid,"phenotype":phenotype,"ETE_peak":ete_peak,"gamma_star":gstar,"tau_c":tau_c,"QLS":qls})
    pd.DataFrame(rows).to_parquet(out_parquet, index=False)