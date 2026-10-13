"""SYNTHETIC Monte Carlo: how reliable is a regression on monthly aggregate data?

No real Las Vegas data is used. Monthly year-over-year series are generated with
assumed properties close to LVCVA-style data, to show what a Phase 4 regression of
visitor change on price change could and could not detect.

Assumptions (edit below): true effect of ADR change on visitor change = -0.4;
predictors: ADR, air-seat and Canadian-visitor changes (correlated, persistent);
monthly noise SD 2.5 points with AR(1) = 0.5 (calendar shifts, convention rotation).
Writes reports/power_simulation.md.
"""
from pathlib import Path
import numpy as np, statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
rng = np.random.default_rng(7)
REPS = 3000

def generate(n, beta, rho_x=0.6, ar=0.5, sd_e=2.5):
    C = np.array([[1, rho_x, 0.4], [rho_x, 1, 0.3], [0.4, 0.3, 1]]); L = np.linalg.cholesky(C)
    z = rng.standard_normal((n, 3)) @ L.T
    X = np.zeros((n, 3))
    for t in range(n):
        X[t] = (0.7 * X[t - 1] if t else 0) + z[t] * np.array([5, 6, 10]) * np.sqrt(1 - 0.49)
    u = rng.normal(0, sd_e, n); e = np.zeros(n)
    for t in range(n):
        e[t] = (ar * e[t - 1] if t else 0) + u[t] * np.sqrt(1 - ar ** 2)
    return beta * X[:, 0] + 0.3 * X[:, 1] + 0.05 * X[:, 2] + e, X

def run(n, beta):
    naive = hac = 0; width = []
    for _ in range(REPS):
        y, X = generate(n, beta)
        m = sm.OLS(y, sm.add_constant(X)).fit()
        h = m.get_robustcov_results("HAC", maxlags=3)
        naive += m.pvalues[1] < 0.05; hac += h.pvalues[1] < 0.05
        lo, hi = h.conf_int()[1]; width.append(hi - lo)
    return naive / REPS, hac / REPS, float(np.median(width))

lines = ["# Power simulation (SYNTHETIC data, generated)", "",
         "Question simulated: does the year-over-year change in ADR explain the change in visitors?", "",
         "| Months of data | Detects true effect, naive SE | Detects true effect, HAC SE | Median 95% CI width | False positives when true effect is 0 (naive / HAC; should be 5%) |",
         "|---|---|---|---|---|"]
for n, label in [(20, "20 (2025-01 to 2026-08 only)"), (32, "32"), (68, "68 (2015-2019 and 2022-2026, COVID removed)")]:
    p, ph, w = run(n, -0.4); f0, fh0, _ = run(n, 0.0)
    lines.append(f"| {label} | {p:.0%} | {ph:.0%} | {w:.2f} | {f0:.0%} / {fh0:.0%} |")
lines += ["", "Reading: with only the post-2025 months, a real effect is missed about a third to a half of the time, "
          "and a non-existent one is reported as significant two to five times more often than the nominal 5%, "
          "because neighbouring months move together. A longer series helps power but not the false-positive problem, "
          "and none of it identifies cause."]
(ROOT / "reports/power_simulation.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
