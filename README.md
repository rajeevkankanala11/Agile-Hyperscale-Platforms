# Agile Cloud Scalability & Performance — Synthesis Artifact

Reproducibility artifact for the manuscript:

> **Scalability and Performance Paradoxes in Agile Cloud Environments: A Comparative Analytical Evaluation of Hyperscale Platforms**

## What this repository is

This is an **analytical literature-synthesis** study. The performance figures
compared across AWS, Microsoft Azure, and Google Cloud Platform are **transcribed
from published, citable sources** (industry benchmark reports, peer-reviewed
papers, and provider disclosures). The code here **aggregates and normalises those
published values and *computes* the paper's derived metrics** — Elasticity Velocity
(`Ev`) and the Scalability Efficiency Index (`SEI`) — and regenerates the
manuscript's tables and Figure 4.

**This repository does not provision cloud infrastructure and does not perform any
live measurement.** Every input value is sourced; see `data/sources.json`. This is
stated so reviewers and readers can see exactly what was done and reproduce it
deterministically.

## Repository structure

```
.
├── README.md
├── requirements.txt              # matplotlib only — no cloud SDKs
├── run.sh                        # reproduce everything
├── data/
│   ├── published_benchmarks.json # the synthesised published input values
│   └── sources.json              # citation for every input group
├── src/
│   ├── compute_metrics.py        # computes Ev (Eq. 1) and SEI (Eq. 3)
│   ├── make_tables.py            # regenerates Tables 1, 2, 3, 5 (Markdown + CSV)
│   └── make_figure4.py           # regenerates Figure 4 (labelled PUE chart)
└── outputs/                      # generated tables, CSVs, and figure
```

## How to reproduce

```bash
pip install -r requirements.txt
./run.sh
```

This writes `outputs/tables.md`, the per-table CSVs, `outputs/computed_metrics.json`,
and `outputs/figure4_pue.png`.

## Metric definitions (manuscript Section IV)

- **Elasticity Velocity** — Eq. (1): `Ev_p = ΔC / Δt_p`, with `ΔC = 100` instances
  and `Δt_p` the published time-to-ready (seconds). Units: instances/second.
  Computed in `compute_metrics.py`, not hardcoded — it reproduces Table 3 exactly
  (GCP 100/25 = 4.00; AWS 100/95 = 1.05; Azure 100/110 = 0.91).
- **Scalability Efficiency Index** — Eq. (3):
  `SEI_p = (Ẽv_p · ρ_p) / Ĉ_p`, where `Ẽv_p` is min–max-normalised `Ev`,
  `ρ_p = 1 − f_p` is the burst-provisioning success rate, and `Ĉ_p` is the
  normalised cost-efficiency index (cheapest provider = 1.0). `SEI*` is the
  optional 0–1 rescaling.

## Data provenance and the cost-efficiency index

All inputs are cited in `data/sources.json`. The cost-efficiency index
(`cost_efficiency.kappa_relative`) is **not** a raw list price — SEI is a
price-*performance* measure, so `kappa` is a normalised *effective* cost per unit
of sustained, workload-relevant compute (cheapest provider = 1.00). It is derived
transparently in `data/published_benchmarks.json` under
`cost_efficiency_derivation` from three sourced components:

1. published US-East x86 monthly list price per vCPU,
2. a billing-model efficiency multiplier (Cloud Run scale-to-zero / per-request
   vs. Fargate continuously-provisioned billing) appropriate to bursty Agile
   workloads, and
3. an ARM price-performance multiplier (e.g. Graviton4 ≈ 42% better
   price-performance than comparable x86).

The derivation, multipliers, and source references are all recorded in the data
file so the index can be inspected and challenged component-by-component. Notably,
once ARM price-performance is counted, **AWS is the most cost-efficient platform**
(`kappa` = 1.00); GCP nonetheless leads on overall SEI because its elasticity and
reliability advantages dominate the cost gap — consistent with the manuscript's
finding that GCP leads on deployment velocity while AWS leads on cost-performance.

## Note on tooling

Generative AI tools were used to assist in preparing the analysis and
figure-generation scripts in this repository. All input data, computations, and
conclusions were reviewed and verified by the author, who takes full responsibility
for the content. See the corresponding "Use of AI-assisted tools" statement in the
manuscript.

## License

Released under the MIT License (see `LICENSE`).
