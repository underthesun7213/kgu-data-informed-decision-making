"""Phase 4 (mock) RQ on guest ratings, using the only row-level Las Vegas data
available here: UCI Las Vegas Strip (504 TripAdvisor reviews, 21 hotels, 2015 stays).
Writes reports/uci_results.md.
"""
from pathlib import Path
import warnings
import numpy as np, pandas as pd, statsmodels.formula.api as smf
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "data/raw/uci_las_vegas_strip/LasVegasTripAdvisorReviews-Dataset.csv", sep=";")
d.columns = [c.replace(".", "").replace(" ", "_") for c in d.columns]
d["stars"] = d.Hotel_stars.str.replace(",", ".").astype(float)
d.loc[d.Member_years < 0, "Member_years"] = np.nan          # one entry error (-1806)
for c in ["Pool", "Gym", "Tennis_court", "Spa", "Casino", "Free_internet"]:
    d[c] = (d[c] == "YES").astype(int)
md = ["# UCI Las Vegas Strip results (generated)", "",
      f"Rows: {len(d)}; hotels: {d.Hotel_name.nunique()}; reviews per hotel: {d.groupby('Hotel_name').size().min()}-{d.groupby('Hotel_name').size().max()}; mean score {d.Score.mean():.2f}.", ""]

# Descriptive: score by traveler type and by hotel
tt = d.groupby("Traveler_type").Score.agg(["size", "mean"]).sort_values("mean")
md += ["## Score by traveler type", "", "| Traveler type | Reviews | Mean score |", "|---|---|---|"]
md += [f"| {i} | {int(r['size'])} | {r['mean']:.2f} |" for i, r in tt.iterrows()] + [""]
ht = d.groupby("Hotel_name").Score.mean().sort_values()
md += [f"Lowest-rated hotels: {', '.join(f'{h} ({v:.2f})' for h, v in ht.head(3).items())}.",
       f"Highest-rated: {', '.join(f'{h} ({v:.2f})' for h, v in ht.tail(3).items())}.", ""]

# OLS with review-level and hotel-level variables, naive vs cluster-robust SEs
f = ("Score ~ stars + np.log(Nr_rooms) + C(Traveler_type) + C(Period_of_stay) + Pool + Gym + Spa + Casino"
     " + Free_internet + C(User_continent) + Member_years + np.log1p(Nr_reviews)")
dd = d.dropna()
naive = smf.ols(f, dd).fit()
groups = pd.factorize(dd.Hotel_name)[0]
clus = smf.ols(f, dd).fit(cov_type="cluster", cov_kwds={"groups": groups})
terms = ["stars", "Pool", "Gym", "Spa", "Free_internet", "C(Traveler_type)[T.Couples]", "C(Traveler_type)[T.Friends]"]
md += ["## Regression of score (OLS)", "",
       f"n = {int(naive.nobs)}, R² = {naive.rsquared:.3f} (adjusted {naive.rsquared_adj:.3f}). "
       f"Hotel identity alone gives R² = {smf.ols('Score ~ C(Hotel_name)', d).fit().rsquared:.3f}.", "",
       "| Term | Coef. | p (naive SE) | p (SE clustered by hotel, 21 clusters) |", "|---|---|---|---|"]
md += [f"| {t} | {naive.params[t]:.3f} | {naive.pvalues[t]:.3f} | {clus.pvalues[t]:.3f} |" for t in terms] + [""]
md += ["Hotel amenities do not vary within a hotel, so their effects are really estimated from 21 hotels, "
       "not 503 reviews. Clustered standard errors with 21 clusters and this many regressors are themselves unreliable, "
       "so two cleaner checks follow.", ""]

# Check 1: hotel-level regression (the honest sample size for amenity effects)
h = d.groupby("Hotel_name").agg(score=("Score", "mean"), stars=("stars", "first"), pool=("Pool", "first"),
                                gym=("Gym", "first"), spa=("Spa", "first"), wifi=("Free_internet", "first"),
                                rooms=("Nr_rooms", "first"))
hl = smf.ols("score ~ stars + pool + gym + spa + wifi + np.log(rooms)", h).fit()
md += ["### Check 1: hotel-level model (n = 21)", "",
       f"R² = {hl.rsquared:.2f}, adjusted {hl.rsquared_adj:.2f}, F-test p = {hl.f_pvalue:.3f}. "
       f"Hotels without a pool: {', '.join(h.index[h.pool == 0])}; without a gym: {', '.join(h.index[h.gym == 0])}; "
       f"without free internet: {', '.join(h.index[h.wifi == 0])}. Each amenity 'effect' is therefore the gap between "
       "one hotel and the rest, and cannot be separated from everything else about that hotel.", "",
       "| Term | Coef. | p |", "|---|---|---|"]
md += [f"| {t} | {hl.params[t]:.3f} | {hl.pvalues[t]:.3f} |" for t in hl.params.index if t != "Intercept"] + [""]

# Check 2: traveler-type gap within hotels (hotel fixed effects)
fe = smf.ols("Score ~ C(Hotel_name) + C(Traveler_type, Treatment('Business'))", d).fit(
    cov_type="cluster", cov_kwds={"groups": pd.factorize(d.Hotel_name)[0]})
md += ["### Check 2: traveler type within the same hotel (hotel fixed effects)", "",
       "| Traveler type vs Business | Coef. | p |", "|---|---|---|"]
md += [f"| {t.split('T.')[-1].rstrip(']')} | {fe.params[t]:.3f} | {fe.pvalues[t]:.3f} |" for t in fe.params.index if "Traveler_type" in t] + [""]

# Classification: can we predict a 4-5 score?
X = pd.get_dummies(d[["stars", "Nr_rooms", "Traveler_type", "Period_of_stay", "Pool", "Gym", "Spa", "Casino",
                      "Free_internet", "User_continent", "Nr_reviews", "Helpful_votes"]], drop_first=True).astype(float)
y = (d.Score >= 4).astype(int)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
auc = cross_val_score(clf, X, y, cv=cv, scoring="roc_auc").mean()
acc = cross_val_score(clf, X, y, cv=cv).mean()
md += ["## Predicting a 4-5 score (5-fold cross-validation)", "",
       f"Share of 4-5 scores (accuracy of always guessing 'high'): {y.mean():.3f}. Logistic regression accuracy {acc:.3f}, AUC {auc:.3f}.", ""]
(ROOT / "reports/uci_results.md").write_text("\n".join(md))
print("\n".join(md))
