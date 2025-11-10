import pandas as pd
import numpy as np

def tpm_to_zscores(tpm_df):
    log = np.log1p(tpm_df)
    mu = log.mean(axis=1).values[:,None]
    sd = log.std(axis=1).values[:,None] + 1e-9
    z = (log - mu)/sd
    return z