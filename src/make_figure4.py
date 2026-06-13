"""
make_figure4.py
---------------
Regenerates manuscript Figure 4 (data-centre energy efficiency / PUE) from the
2024 provider sustainability disclosures synthesised in
data/published_benchmarks.json. Produces a labelled chart with axis titles,
units, numeric scale, per-bar data labels, and a source note.
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "published_benchmarks.json")
OUT = os.path.join(HERE, "..", "outputs")


def main():
    with open(DATA, "r", encoding="utf-8") as fh:
        pue = json.load(fh)["pue"]["platforms"]
    names = [p["platform"] for p in pue]
    fleet = [p["global_fleet_pue_2024"] for p in pue]
    best = [p["best_site_pue"] for p in pue]

    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    x = range(len(names))
    w = 0.38
    b1 = ax.bar([i - w / 2 for i in x], fleet, w, label="Global fleet PUE (2024)",
                color="#7C83FF", edgecolor="#3B3F8F")
    b2 = ax.bar([i + w / 2 for i in x], best, w, label="Best-performing site PUE",
                color="#B9C0FF", edgecolor="#3B3F8F")
    ax.set_ylim(1.00, 1.20)
    ax.set_ylabel("Power Usage Effectiveness (PUE)\n(ratio; 1.00 = ideal, lower is better)")
    ax.set_xlabel("Cloud Provider")
    ax.set_title("Figure 4. Data-Centre Energy Efficiency by Provider (2024)",
                 fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(names)
    ax.yaxis.grid(True, linestyle="--", alpha=0.45)
    ax.set_axisbelow(True)
    for bars in (b1, b2):
        for r in bars:
            ax.annotate(f"{r.get_height():.2f}",
                        (r.get_x() + r.get_width() / 2, r.get_height()),
                        textcoords="offset points", xytext=(0, 3),
                        ha="center", fontsize=9)
    ax.legend(loc="upper left", framealpha=0.9)
    fig.text(0.01, -0.02,
             "Source: provider sustainability disclosures, 2024 (global fleet and best-site PUE).",
             fontsize=7.5, style="italic", color="#444")
    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "figure4_pue.png")
    fig.savefig(path, dpi=170, bbox_inches="tight")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
