import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def boxplot_metric(parquet_path, metric="ETE_peak", group_col="phenotype", out_png="boxplot.png"):
    df = pd.read_parquet(parquet_path)
    plt.figure(figsize=(6,4))
    sns.boxplot(x=group_col, y=metric, data=df)
    plt.title(f"{metric} by {group_col}")
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()