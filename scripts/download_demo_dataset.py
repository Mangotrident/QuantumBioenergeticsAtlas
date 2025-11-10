import os, pandas as pd, requests, io

URL = "https://raw.githubusercontent.com/plotly/datasets/master/iris.csv"

def download_demo(out_dir="data/public_demo"):
    """
    Example downloader. Replace URL with any open-access RNA-seq TPM CSV in future.
    """
    os.makedirs(out_dir, exist_ok=True)
    print(f"Downloading small demo dataset from {URL} ...")
    r = requests.get(URL)
    if r.status_code != 200:
        raise RuntimeError("Download failed:", r.status_code)
    df = pd.read_csv(io.StringIO(r.text))
    df.to_csv(os.path.join(out_dir, "demo_dataset.csv"), index=False)
    print("Saved ->", os.path.join(out_dir, "demo_dataset.csv"))

if __name__ == "__main__":
    download_demo()
