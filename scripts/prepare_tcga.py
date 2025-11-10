import argparse, pandas as pd, numpy as np, os

def counts_to_tpm(counts_df, gene_lengths=None):
    # If gene_lengths provided: TPM = (counts/length) / sum(counts/length) * 1e6
    if gene_lengths is None:
        # fallback: normalize by library size only (approximate)
        rate = counts_df.div(counts_df.sum(axis=0), axis=1)
    else:
        rate = counts_df.div(gene_lengths, axis=0)
        rate = rate.div(rate.sum(axis=0), axis=1)
    return rate * 1e6

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="Input counts or TPM CSV (genes x samples)")
    ap.add_argument("--out", dest="out", required=True, help="Output TPM CSV")
    ap.add_argument("--pathway", required=True, help="Pathway genes list (one per line)")
    args = ap.parse_args()

    df = pd.read_csv(args.inp, index_col=0)
    genes = [g.strip() for g in open(args.pathway,"r").read().splitlines() if g.strip()]
    df = df[df.index.isin(genes)]

    # heuristic: if values are big integers -> counts; else already TPM
    if (df.values.max() > 1e4):
        print("Detected counts; converting to TPM (approx).")
        tpm = counts_to_tpm(df)
    else:
        print("Detected TPM; passing through.")
        tpm = df.copy()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    tpm.to_csv(args.out)
    print("Wrote", args.out)

if __name__ == "__main__":
    main()