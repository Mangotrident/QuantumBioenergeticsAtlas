import argparse, os, json, yaml, numpy as np, pandas as pd
from q_mnet.batch import cohort_metrics, load_graph
from q_mnet.mapping import map_expr_to_params
from qle.simulate import sweep_gamma

def simulate_one(graph, expr_csv, mapping_yaml, outdir):
    os.makedirs(outdir, exist_ok=True)
    s = pd.read_csv(expr_csv, index_col=0).iloc[:,0]  # single-sample series
    nodes, edges = load_graph(graph)
    epsilon, J, cfg = map_expr_to_params(s, mapping_yaml, len(nodes), edges)
    g0, g1, gs = cfg["gamma_sweep"]
    gammas = np.arange(g0, g1+1e-12, gs)
    res = sweep_gamma(epsilon, J, gammas, sigma=cfg["sigma"], k_sink=cfg["k_sink"], k_loss=cfg["k_loss"],
                      source_idx=cfg.get("source_idx",0), sink_idx=cfg.get("sink_idx",len(nodes)-1),
                      tmax=cfg.get("tmax",2000), dt=cfg.get("dt",0.5))
    out = [dict(ETE=r["ETE"], tau_c=r["tau_c"], QLS=r["QLS"], gamma=r["gamma"]) for r in res]
    with open(os.path.join(outdir, "metrics.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote", os.path.join(outdir, "metrics.json"))

def cohort(graph, expr_csv, labels_csv, mapping_yaml, outdir):
    os.makedirs(outdir, exist_ok=True)
    out_parquet = os.path.join(outdir, "cohort_metrics.parquet")
    cohort_metrics(expr_csv, labels_csv, graph, mapping_yaml, out_parquet)
    print("Wrote", out_parquet)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")

    s1 = sub.add_parser("simulate")
    s1.add_argument("--graph", required=True)
    s1.add_argument("--expr", required=True)
    s1.add_argument("--mapping", required=True)
    s1.add_argument("--out", required=True)

    s2 = sub.add_parser("cohort")
    s2.add_argument("--graph", required=True)
    s2.add_argument("--expr", required=True)
    s2.add_argument("--labels", required=True)
    s2.add_argument("--mapping", required=True)
    s2.add_argument("--out", required=True)

    args = ap.parse_args()
    if args.cmd == "simulate":
        simulate_one(args.graph, args.expr, args.mapping, args.out)
    elif args.cmd == "cohort":
        cohort(args.graph, args.expr, args.labels, args.mapping, args.out)
    else:
        ap.print_help()