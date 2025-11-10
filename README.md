# Quantum Bioenergetics Atlas (Heavy Backend)

This repository contains an **end-to-end stack**:

- **Phase 1 — Physics Engine (QLE):** Lindblad solver for energy transport (ETE), coherence lifetime (τc), composite QLS.
- **Phase 2 — Data Mapping (Q-MNet):** RNA-seq TPM → (ε, J, γ) parameters.
- **Phase 3 — Cohort Analysis:** Healthy vs disease ΔETE, γ* shift, Resilience Index; Mann–Whitney, Cohen's d; figures.
- **Phase 4 — Visualization API / Dashboard:** Streamlit app with upload, plots, and a "Metabolic Coherence Map" heatmap.
- **Phase 5 — Packaging & IP:** CLI, Dockerfile, docs, USPTO-ready draft.

## Quickstart (local)

```bash
conda env create -f environment.yml
conda activate qba

# Sanity tests
python -m qle.tests.test_engine

# Demo (toy) cohort
python cli.py cohort --graph data/refs/graph.json --expr data/demo/tpm_matrix.csv   --labels data/demo/labels.csv --mapping data/refs/mapping.yaml --out runs/demo_cohort/

# Launch dashboard
streamlit run mvp_app/app.py
```

## Real Data Workflow (TCGA / AMP-AD)

1. **Download** RNA-seq tables (counts or TPM) using the official portals:
   - TCGA via GDC Portal (generate manifest; download)  
   - AMP-AD via Synapse portal (ROSMAP or Mayo; request access)

2. **Prepare** with the provided scripts:
```bash
# Convert counts → TPM, filter ETC genes, align with labels
python scripts/prepare_tcga.py --in counts_or_tpm.csv --out data/tcga_brca/tpm_matrix.csv   --pathway data/refs/pathway_genes.txt

# Prepare labels: CSV with columns: sample_id, phenotype
# Place at: data/tcga_brca/labels.csv
```

3. **Run cohort:**
```bash
python cli.py cohort --graph data/refs/graph.json   --expr data/tcga_brca/tpm_matrix.csv   --labels data/tcga_brca/labels.csv   --mapping data/refs/mapping.yaml   --out runs/tcga_brca/
```

> We cannot include large public datasets directly in this repo, but the pipelines fully support REAL data.