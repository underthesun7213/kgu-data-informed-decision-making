# Phase 4 (mock): Final Report

This mock run uses only the data that could be obtained in this environment: 58 published figures and 504 UCI reviews. Sections marked **not executed** need the monthly tables listed in `data/source_manifest.csv`.

## Executive summary

The 2025 decline in Las Vegas visitation was mainly a domestic problem: international visitors explain about 8% of the 3.1M-visitor drop and domestic visitors about 92%. Downtown is underperforming the rest of the market on both hotel occupancy and gaming win. The LVCVA should therefore focus recovery spending on domestic drive-in and value-seeking segments and treat Downtown as a separate priority. These conclusions rest on published aggregates; the monthly analysis that would test them more rigorously has not been run yet.

## 1. Methodology actually used

| Step | Data | Script |
|---|---|---|
| Curated published figures with source and verification level | 58 indicators | (typed; `data/curated/`) |
| Decomposition of the 2025 decline by origin | LVCVA year-end figures | `04_decomposition.py` |
| One-month comparison of gaming win by area | NGCB August 2026 | `04_decomposition.py` |
| Guest-rating analysis | UCI 504 reviews | `02_uci_reviews_analysis.py` |
| Reliability check of monthly-aggregate regressions | synthetic data | `03_power_simulation.py` |

## 2. Findings

### RQ4 (executed): the 2025 decline was about 92% domestic

| Group | 2024 | 2025 | Change | Share of decline |
|---|---|---|---|---|
| All visitors | 41.68M | 38.55M | -3.13M | 100% |
| International (incl. Canada) | 4.96M | 4.73M | -0.24M | 7.6% |
| Canadian | 1.45M | 1.20M | -0.25M | 8.1% |
| Domestic (residual) | 36.71M | 33.82M | -2.89M | 92.4% |

**From data to claim:** the Canadian drop (-17.4%) dominated headlines, but in absolute numbers it is a small part of the total. Non-Canadian international visitors were flat. The claim depends on LVCVA counting Canada inside "international", which the numbers support.

### RQ2 (partially executed): Downtown underperforms

Downtown occupancy was 22-24 points below the Strip in July and August 2026, and Downtown gaming win fell 2.96% in August 2026 while the state rose 3.1% (a 6.1-point gap).
**From data to claim:** two independent measures agree, which makes the gap credible. It is one or two months, so it is a difference, not yet a difference-in-differences; the monthly panel is needed to show that the gap widened after 2025.

### RQ3 (executed on 2015 data): who rates lower, and what cannot be concluded

- Within the same hotel, business travelers score about 0.4-0.5 points lower than couples and friends (hotel fixed effects, p < 0.001).
- A naive regression suggests a pool adds 1.06 points and free internet 0.75. But only one hotel lacks each amenity (Circus Circus has no pool, The Cromwell no gym, Monte Carlo no free internet), so each "effect" is just one hotel's gap from the rest.
- Predicting a 4-5 score is no better than always guessing "high" (accuracy 0.770 vs 0.776).

**From data to claim:** the traveler-type gap is a within-hotel comparison and holds; the amenity effects are not identifiable and should not drive recommendations. The data is from 2015, so it describes rating patterns, not the 2025 decline.

### RQ1 (not executed): shortfall versus forecast

Needs monthly LVCVA data 2015-2026. `power_simulation.md` shows why a simple regression on 20 post-2025 months would be unreliable (a real effect missed 32-44% of the time; false positives 12-24% instead of 5%), which is why the plan uses a forecast-gap design instead.

## 3. Recommendations (conditional)

| # | Action | Evidence | Confidence |
|---|---|---|---|
| 1 | Shift recovery marketing toward domestic markets, especially drive-in visitors from California and the Southwest | 92% of the decline was domestic | medium: based on year-end aggregates |
| 2 | Treat Downtown as a separate program (events, value packages, transport links to the Strip) | occupancy and gaming gaps | medium: two indicators, short period |
| 3 | Address business-traveler satisfaction (workspace, fees, check-in speed) | within-hotel score gap | low: 2015 data, needs recent reviews |
| 4 | Do not invest in Canada-specific campaigns ahead of evidence; Canadian travel to the US is already recovering | StatCan +8.8% in August 2026 | medium |

ROI cannot be estimated from these data: there are no costs, budgets or campaign response rates. A full Phase 4 would need at least the monthly panel and an assumption set similar to the Portugal branch's policy simulation.

## 4. Reflection

- **Where the chain holds:** origin decomposition (simple arithmetic on official totals) and the Downtown gap (two measures agree).
- **Where it breaks:** no monthly series, no costs, dated review data, many simultaneous shocks. The analysis can size problems but cannot attribute causes or compute returns.
- **Lesson:** on aggregate public data, design the analysis around comparisons (areas, forecasts, origins) rather than regressions, and state the confidence of each recommendation.
