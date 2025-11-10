REAL DATA DOWNLOAD NOTES

- TCGA via GDC Portal: create a manifest for RNA-seq (HTSeq counts or FPKM/TPM), then download using the GDC data portal or client.
- AMP-AD via Synapse (ROSMAP/Mayo): request access; download harmonized RNA-seq tables.
- Place expression matrix at: data/tcga_brca/tpm_matrix.csv (genes x samples)
- Prepare labels at: data/tcga_brca/labels.csv with columns: sample_id, phenotype
- Then run: python cli.py cohort --graph data/refs/graph.json --expr data/tcga_brca/tpm_matrix.csv --labels data/tcga_brca/labels.csv --mapping data/refs/mapping.yaml --out runs/tcga_brca/