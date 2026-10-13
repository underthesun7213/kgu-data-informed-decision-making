"""Phase 4 mock analysis: RQ1-RQ4 on the cleaned booking data.

Writes reports/phase4_results.md and figures/p4_*.png.
Train/test split is by time: arrivals 2015-07..2016-12 train, 2017-01..2017-08 test.
"""
from pathlib import Path
import numpy as np, pandas as pd, statsmodels.formula.api as smf
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, brier_score_loss
from style import plt, save, SERIES, TEXT_2

ROOT = Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "data/processed/bookings_clean.csv.gz", parse_dates=["arrival_date"])
d["month"] = d.arrival_date.dt.month
d["log_lead"] = np.log1p(d.lead_time)
d["prev_cancel"] = (d.previous_cancellations > 0).astype(int)
d["special_req"] = d.total_of_special_requests.clip(upper=3)
d["parking"] = (d.required_car_parking_spaces > 0).astype(int)
d["has_agent"] = d.agent.notna().astype(int)
d["season"] = d.month.map(lambda m: "peak" if m in (6, 7, 8) else ("low" if m in (11, 12, 1, 2) else "shoulder"))
train = d.arrival_date < "2017-01-01"; test = ~train
md = []
def table(df, fmt="{:,.3f}"):
    cols = list(df.columns)
    rows = ["| " + " | ".join([df.index.name or ""] + cols) + " |", "|" + "---|" * (len(cols) + 1)]
    def cell(c, v):
        if c in ("bookings", "targeted") or c.endswith("_eur"):
            return f"{v:,.0f}"
        return fmt.format(v) if isinstance(v, (int, float, np.floating, np.integer)) else str(v)
    for i, r in df.iterrows():
        rows.append("| " + " | ".join([str(i)] + [cell(c, v) for c, v in r.items()]) + " |")
    return "\n".join(rows)

# RQ1: drivers of cancellation (interpretable logit) and predictability (GBM)
f = ("is_canceled ~ C(hotel) + log_lead + C(market_segment, Treatment('Direct')) + C(deposit_type)"
     " + C(customer_type, Treatment('Transient')) + prev_cancel + is_repeated_guest + special_req"
     " + has_agent + C(season, Treatment('shoulder')) + nights + I(adr/10)")
logit = smf.logit(f, d[train]).fit(disp=0, maxiter=200)
ors = pd.DataFrame({"odds_ratio": np.exp(logit.params), "p_value": logit.pvalues}).drop("Intercept")
ors.index = [i.replace("C(market_segment, Treatment('Direct'))", "segment").replace("C(customer_type, Treatment('Transient'))", "customer")
             .replace("C(season, Treatment('shoulder'))", "season").replace("C(deposit_type)", "deposit").replace("C(hotel)", "hotel") for i in ors.index]
ors.index.name = "term"
p_logit = logit.predict(d[test])
auc_logit = roc_auc_score(d.is_canceled[test], p_logit)

feat = ["hotel", "lead_time", "month", "nights", "adults", "children", "babies", "meal", "market_segment",
        "distribution_channel", "is_repeated_guest", "previous_cancellations", "previous_bookings_not_canceled",
        "reserved_room_type", "deposit_type", "days_in_waiting_list", "customer_type", "adr",
        "required_car_parking_spaces", "total_of_special_requests", "has_agent"]
X = pd.get_dummies(d[feat], drop_first=True).astype(float)
gbm = HistGradientBoostingClassifier(random_state=0).fit(X[train], d.is_canceled[train])
p_gbm = gbm.predict_proba(X[test])[:, 1]
auc_gbm = roc_auc_score(d.is_canceled[test], p_gbm)
Xn = X.drop(columns=[c for c in X if c.startswith("deposit_type")])
gbm_nd = HistGradientBoostingClassifier(random_state=0).fit(Xn[train], d.is_canceled[train])
auc_nd = roc_auc_score(d.is_canceled[test], gbm_nd.predict_proba(Xn[test])[:, 1])
base = d.is_canceled[train].mean()
md += ["## RQ1. Which booking characteristics predict cancellation?", "",
       f"Train: {train.sum():,} bookings (2015-07 to 2016-12). Test: {test.sum():,} bookings (2017-01 to 2017-08).", "",
       "| Model | Test AUC | Brier score |", "|---|---|---|",
       f"| Baseline (train cancel rate {base:.3f} for everyone) | 0.500 | {brier_score_loss(d.is_canceled[test], np.full(test.sum(), base)):.3f} |",
       f"| Logistic regression (12 interpretable terms) | {auc_logit:.3f} | {brier_score_loss(d.is_canceled[test], p_logit):.3f} |",
       f"| Gradient boosting (all booking-time fields) | {auc_gbm:.3f} | {brier_score_loss(d.is_canceled[test], p_gbm):.3f} |",
       f"| Gradient boosting without `deposit_type` | {auc_nd:.3f} | |", "",
       "Odds ratios from the logistic regression (train period). Above 1 raises the odds of cancelling.", "",
       table(ors.sort_values("odds_ratio", ascending=False), "{:.3f}"), "",
       f"Parking requests are left out of the logit: none of the {int(d.parking.sum()):,} bookings that asked for parking "
       f"cancelled (rate {d[d.parking == 1].is_canceled.mean():.3f}), which makes the coefficient infinite.", ""]

# RQ2: where is revenue at risk concentrated?
t = d[test].copy(); t["p"] = p_gbm
nd = t[t.deposit_type == "No Deposit"].copy()
nd["risk_decile"] = pd.qcut(nd.p.rank(method="first"), 10, labels=range(1, 11))
dec = nd.groupby("risk_decile", observed=True).agg(bookings=("p", "size"), predicted=("p", "mean"), actual_cancel=("is_canceled", "mean"),
                                    cancelled_value_eur=("revenue", lambda s: s[nd.loc[s.index, "is_canceled"] == 1].sum()))
dec["share_of_cancelled_value"] = dec.cancelled_value_eur / dec.cancelled_value_eur.sum()
dec.index.name = "risk decile (10 = highest)"
segtab = d.groupby("market_segment").agg(bookings=("revenue", "size"), cancel_rate=("is_canceled", "mean"),
                                         cancelled_value_eur=("revenue", lambda s: s[d.loc[s.index, "is_canceled"] == 1].sum()))
segtab["share_of_cancelled_value"] = segtab.cancelled_value_eur / segtab.cancelled_value_eur.sum()
segtab = segtab.sort_values("cancelled_value_eur", ascending=False); segtab.index.name = "segment"
md += ["## RQ2. Where is booked revenue at risk concentrated?", "",
       "All periods, by market segment:", "", table(segtab, "{:,.3f}"), "",
       "Test period, `No Deposit` bookings only (the group a new policy could change), by predicted risk decile:", "",
       table(dec, "{:,.3f}"), "",
       f"Top two deciles hold {dec.share_of_cancelled_value.iloc[-2:].sum():.1%} of cancelled value among No Deposit bookings in the test period.", ""]

fig, ax = plt.subplots(figsize=(7, 3.8))
ax.bar(dec.index.astype(str), dec.actual_cancel * 100, color=SERIES[0], width=0.7, label="Actual")
ax.plot(dec.index.astype(str), dec.predicted * 100, color=SERIES[1], marker="o", label="Predicted")
ax.set_xlabel("Predicted risk decile (No Deposit bookings, 2017 test period)"); ax.set_ylabel("Cancellation rate (%)")
ax.set_title("Ranking holds on 2017 data; mid deciles are under-predicted"); ax.legend(loc="upper left")
save(fig, ROOT / "figures/p4_risk_deciles.png")

# RQ3: does price follow demand? monthly realized room-nights vs ADR
m = pd.read_csv(ROOT / "data/processed/monthly_kpis.csv")
m = m[(m.arrival_month > "2015-07") & (m.arrival_month < "2017-08")]  # drop partial first/last months
rq3 = []
for h in ["City Hotel", "Resort Hotel"]:
    mm = m[m.hotel == h]
    r = np.corrcoef(mm.room_nights, mm.adr_realized)[0, 1]
    el = smf.ols("np.log(adr_realized) ~ np.log(room_nights)", mm).fit()
    rq3.append((h, len(mm), r, el.params.iloc[1], el.rsquared, mm.cancel_rate.corr(mm.room_nights)))
md += ["## RQ3. Does pricing follow demand across the year?", "",
       "Monthly realized room-nights (stayed bookings) against realized ADR, 2015-08 to 2017-07.", "",
       "| Hotel | Months | Corr(room-nights, ADR) | Elasticity of ADR to room-nights | R² | Corr(room-nights, cancel rate) |", "|---|---|---|---|---|---|"]
md += [f"| {h} | {n} | {r:.2f} | {b:.2f} | {r2:.2f} | {c:.2f} |" for h, n, r, b, r2, c in rq3] + [""]
fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharey=False)
for ax, (i, h) in zip(axes, enumerate(["City Hotel", "Resort Hotel"])):
    mm = m[m.hotel == h]
    ax.scatter(mm.room_nights / 1000, mm.adr_realized, color=SERIES[i], s=36, edgecolor="white", linewidth=1.5)
    ax.set_title(h); ax.set_xlabel("Room-nights sold ('000)"); ax.set_ylabel("Realized ADR (EUR)")
fig.suptitle("Monthly demand vs price", fontweight="bold", y=1.03)
save(fig, ROOT / "figures/p4_demand_vs_adr.png")

# RQ4: policy simulation - targeted deposit/reconfirmation for top-k% risk No Deposit bookings
rows = []
months_in_test = 8
for k in (0.10, 0.20):
    thr = nd.p.quantile(1 - k); tgt = nd[nd.p >= thr]
    canc_val = tgt.loc[tgt.is_canceled == 1, "revenue"].sum(); stay_val = tgt.loc[tgt.is_canceled == 0, "revenue"].sum()
    for prevent in (0.10, 0.20, 0.30):
        for resale in (0.0, 0.5):
            for lost in (0.02, 0.05):
                gain = canc_val * prevent * (1 - resale)
                loss = stay_val * lost
                cost = len(tgt) * 1.0
                rows.append(dict(target=f"top {int(k*100)}%", targeted=len(tgt), prevent=prevent, resale=resale, lost_genuine=lost,
                                 gain=gain, loss=loss, cost=cost, net=gain - loss - cost))
sim = pd.DataFrame(rows)
sim["net_annualized"] = sim.net * 12 / months_in_test
show = sim[sim.lost_genuine == 0.02].pivot_table(index=["target", "prevent"], columns="resale", values="net_annualized")
show.columns = [f"net EUR/yr, resale {int(c*100)}%" for c in show.columns]; show.index = [f"{a}, prevents {int(b*100)}%" for a, b in show.index]
show.index.name = "policy"
worst = sim[sim.lost_genuine == 0.05].pivot_table(index=["target", "prevent"], columns="resale", values="net_annualized")
worst.columns = [f"net EUR/yr, resale {int(c*100)}%" for c in worst.columns]; worst.index = [f"{a}, prevents {int(b*100)}%" for a, b in worst.index]
worst.index.name = "policy"
md += ["## RQ4. What would a targeted deposit / reconfirmation policy be worth?", "",
       "Scenario simulation on 2017 test bookings (8 months, annualized x12/8). Assumptions, all adjustable in the script:",
       "- the policy applies to the highest-risk `No Deposit` bookings, scored by the RQ1 model;",
       "- it prevents 10-30% of cancellations among targeted bookings;",
       "- a cancelled room is resold 0% or 50% of the time (resold value is not a real loss);",
       "- 2% (or 5%) of targeted guests who would have stayed walk away because of the deposit;",
       "- handling cost EUR 1 per targeted booking.", "",
       "Net annual effect with 2% walk-away:", "", table(show, "{:,.0f}"), "",
       "Net annual effect with 5% walk-away:", "", table(worst, "{:,.0f}"), ""]
(ROOT / "reports/phase4_results.md").write_text("# Phase 4 results (generated)\n\n" + "\n".join(md))
print("\n".join(md))
