"""
compute_metrics.py
------------------
Computes the derived quantities used in the manuscript

    "Scalability and Performance Paradoxes in Agile Cloud Environments:
     A Comparative Analytical Evaluation of Hyperscale Platforms"

from the PUBLISHED benchmark values in data/published_benchmarks.json.

This is a literature-SYNTHESIS study. The inputs are transcribed from cited
public sources (see data/sources.json). This module does NOT provision cloud
resources or measure anything live; it aggregates published figures and
*derives* Elasticity Velocity (Ev) and the Scalability Efficiency Index (SEI),
reproducing Table 3 and Table 5 of the manuscript.

Definitions (manuscript Section IV):
    Eq. (1)  Ev_p   = dC / dt_p           (instances provisioned per second)
    Eq. (3)  SEI_p  = (Ev_norm_p * rho_p) / C_norm_p
             where  Ev_norm_p = Ev_p / max_q Ev_q
                    rho_p     = 1 - f_p          (burst-provisioning success rate)
                    C_norm_p  = kappa_p / min_q kappa_q
             SEI*_p = SEI_p / max_q SEI_q        (optional 0..1 form)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "published_benchmarks.json")


def load_inputs(path=DATA):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def compute_elasticity_velocity(provisioning):
    """Ev = delta_capacity / time_to_ready  (Eq. 1). Computed, not hardcoded."""
    dC = provisioning["_delta_capacity_instances"]
    rows = []
    for p in provisioning["platforms"]:
        ev = dC / p["time_to_ready_s"]
        rows.append({
            "platform": p["platform"],
            "architecture": p["architecture"],
            "time_to_ready_s": p["time_to_ready_s"],
            "ev_instances_per_s": round(ev, 2),
            "burst_failure_rate_pct": p["burst_failure_rate_pct"],
        })
    return rows


def compute_sei(ev_rows, cost_efficiency):
    """SEI per Eq. (3). Pulls Ev from ev_rows, cost index from cost_efficiency."""
    kappa = {c["platform"]: c["kappa_relative"] for c in cost_efficiency["platforms"]}
    ev = {r["platform"]: r["ev_instances_per_s"] for r in ev_rows}
    fail = {r["platform"]: r["burst_failure_rate_pct"] / 100.0 for r in ev_rows}

    ev_max = max(ev.values())
    kappa_min = min(kappa.values())

    rows = []
    for platform in ev:
        ev_norm = ev[platform] / ev_max
        rho = 1.0 - fail[platform]
        c_norm = kappa[platform] / kappa_min
        sei = (ev_norm * rho) / c_norm
        rows.append({
            "platform": platform,
            "ev_norm": round(ev_norm, 3),
            "rho": round(rho, 3),
            "c_norm": round(c_norm, 2),
            "sei": round(sei, 3),
        })
    sei_max = max(r["sei"] for r in rows)
    for r in rows:
        r["sei_star"] = round(r["sei"] / sei_max, 2)
    return rows


def minmax_normalise(values):
    """Min-max normalisation to [0,1] (manuscript Section 4.1)."""
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]


def main():
    data = load_inputs()
    ev_rows = compute_elasticity_velocity(data["provisioning"])
    sei_rows = compute_sei(ev_rows, data["cost_efficiency"])

    print("== Elasticity Velocity (Table 3, computed from published time-to-ready) ==")
    for r in ev_rows:
        print(f"  {r['platform']:<22} Ev = {r['ev_instances_per_s']:.2f} inst/s"
              f"  (100 / {r['time_to_ready_s']} s)")

    print("\n== Scalability Efficiency Index (Table 5, Eq. 3) ==")
    for r in sei_rows:
        print(f"  {r['platform']:<22} Ev~={r['ev_norm']:.3f}  rho={r['rho']:.3f}"
              f"  C~={r['c_norm']:.2f}  SEI={r['sei']:.3f}  SEI*={r['sei_star']:.2f}")

    os.makedirs(os.path.join(HERE, "..", "outputs"), exist_ok=True)
    out = os.path.join(HERE, "..", "outputs", "computed_metrics.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"elasticity_velocity": ev_rows, "sei": sei_rows}, fh, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
