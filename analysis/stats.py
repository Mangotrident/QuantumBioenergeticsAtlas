import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu

def compare_groups(parquet_path, metric="ETE_peak", group_col="phenotype",
                   group_a="healthy", group_b="tumor"):
    df = pd.read_parquet(parquet_path)
    A = df[df[group_col]==group_a][metric].values
    B = df[df[group_col]==group_b][metric].values
    u, p = mannwhitneyu(A, B, alternative="two-sided")
    d = (A.mean()-B.mean())/np.sqrt(0.5*(A.var()+B.var()) + 1e-9)
    return {"u": float(u), "p": float(p), "cohens_d": float(d),
            "mean_A": float(A.mean()), "mean_B": float(B.mean()),
            "n_A": int(len(A)), "n_B": int(len(B))}