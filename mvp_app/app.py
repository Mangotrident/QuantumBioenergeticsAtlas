import streamlit as st
import pandas as pd
import numpy as np
import json, yaml, os
import matplotlib.pyplot as plt
import seaborn as sns

from q_mnet.batch import load_graph, cohort_metrics
from q_mnet.mapping import map_expr_to_params
from qle.simulate import sweep_gamma

st.set_page_config(page_title="Quantum Bioenergetics Atlas", page_icon="🧬", layout="wide")
st.title("Quantum Bioenergetics Atlas — Heavy Backend MVP")

tab1, tab2, tab3, tab4 = st.tabs(["Upload", "Simulate", "Cohort Analysis", "About"])

with tab1:
    st.subheader("Upload Expression + Labels")
    demo = st.checkbox("Use demo dataset", True)
    if demo:
        expr = pd.read_csv("data/demo/tpm_matrix.csv", index_col=0)
        labels = pd.read_csv("data/demo/labels.csv")
        st.success("Loaded demo TPM and labels.")
    else:
        expr_file = st.file_uploader("TPM CSV (genes x samples)", type=["csv"])
        labels_file = st.file_uploader("Labels CSV (sample_id, phenotype)", type=["csv"])
        if expr_file: expr = pd.read_csv(expr_file, index_col=0)
        if labels_file: labels = pd.read_csv(labels_file)
    if 'expr' in locals():
        st.write("Expression shape:", expr.shape)
        st.dataframe(expr.head())

with tab2:
    st.subheader("Simulate a Single Sample (ETE vs γ)")
    graph_json = "data/refs/graph.json"
    mapping_yaml = "data/refs/mapping.yaml"
    nodes, edges = load_graph(graph_json)

    if 'expr' in locals():
        sid = st.selectbox("Pick sample id", list(expr.columns))
        if st.button("Run Simulation"):
            series = np.log1p(expr[sid])  # log1p before mapping
            epsilon, J, cfg = map_expr_to_params(series, mapping_yaml, len(nodes), edges)
            g0, g1, gs = cfg["gamma_sweep"]
            gammas = np.arange(g0, g1+1e-12, gs)
            res = sweep_gamma(epsilon, J, gammas, sigma=cfg["sigma"], k_sink=cfg["k_sink"], k_loss=cfg["k_loss"],
                              source_idx=cfg.get("source_idx",0), sink_idx=cfg.get("sink_idx",len(nodes)-1),
                              tmax=cfg.get("tmax",2000), dt=cfg.get("dt",0.5))
            etes = [r["ETE"] for r in res]
            fig = plt.figure()
            plt.plot(gammas, etes, marker="o")
            plt.xlabel("γ (dephasing)"); plt.ylabel("ETE")
            st.pyplot(fig)
            st.json({"ETE_peak": float(np.max(etes)), "gamma_star": float(gammas[int(np.argmax(etes))])})
    else:
        st.info("Load expression in the Upload tab.")

with tab3:
    st.subheader("Cohort Analysis (ΔETE, γ* shift)")
    if st.button("Run Cohort on Current Data"):
        if 'expr' in locals() and 'labels' in locals():
            os.makedirs("runs/streamlit_tmp", exist_ok=True)
            out_parquet = "runs/streamlit_tmp/cohort_metrics.parquet"
            expr.to_csv("runs/streamlit_tmp/_expr.csv")
            labels.to_csv("runs/streamlit_tmp/_labels.csv", index=False)
            cohort_metrics("runs/streamlit_tmp/_expr.csv", "runs/streamlit_tmp/_labels.csv",
                           "data/refs/graph.json", "data/refs/mapping.yaml", out_parquet)
            df = pd.read_parquet(out_parquet)
            st.success(f"Cohort metrics computed: {df.shape}")
            st.dataframe(df.head())

            st.markdown("**ETE_peak by phenotype**")
            fig2 = plt.figure()
            sns.boxplot(data=df, x="phenotype", y="ETE_peak")
            st.pyplot(fig2)

            from analysis.stats import compare_groups
            stats = compare_groups(out_parquet, metric="ETE_peak", group_col="phenotype", group_a="healthy", group_b="tumor")
            st.subheader("Stats")
            st.json(stats)
        else:
            st.error("Please load expression and labels in the Upload tab.")
with tab4:
    st.write("""
**About**

- **Mission:** Model coherence collapse in mitochondrial networks and convert patient omics into physics-level biomarkers (ETE, τc, QLS) for early disease prediction.
- **Engine:** Lindblad master equation with dephasing + sink/loss channels; ENAQT curves.
- **Mapping:** RNA-seq TPM → (ε, J, γ) via configurable YAML mapping.
- **Cohorts:** Run healthy vs disease comparisons to obtain ΔETE and γ* shifts.
- **Product:** Streamlit dashboard + CLI + Dockerized service, suitable for labs and startups.
""")