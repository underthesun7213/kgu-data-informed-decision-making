# Phase 3 (mock): Research Proposal

## 1. Issues and questions

Cancellations put 43% (City) and 33% (Resort) of booked value at risk, concentrated in group and travel-agent channels, and prices swing strongly by season. RQ1-RQ4 are listed in `phase2_research_questions.md`.

## 2. Variables and data sources

| RQ | Outcome | Key variables | Primary source | Alternative / check |
|---|---|---|---|---|
| RQ1 | `is_canceled` | lead time, market segment, deposit type, customer type, prior cancellations, repeat guest, special requests, parking, ADR, nights, season, hotel | booking file (PMS extract) | rerun without `deposit_type` (suspect field); compare with published cancellation studies on the same data |
| RQ2 | cancelled booked value | segment, predicted risk decile | booking file + RQ1 scores | segment-level shares as a model-free version |
| RQ3 | realized ADR | realized room-nights per month, cancellation rate | monthly KPI table built from the booking file | STR or national statistics (INE Portugal) for a market benchmark |
| RQ4 | net revenue effect | risk score, booked value, assumed prevention, resale and walk-away rates | RQ1/RQ2 outputs | sensitivity grid over every assumption |

## 3. Methods and tools

| RQ | Method | Why | Tool |
|---|---|---|---|
| RQ1 | Logistic regression (odds ratios) plus gradient boosting; out-of-time test (train 2015-07..2016-12, test 2017-01..08) | logit is explainable to managers; boosting shows how much accuracy the simple model leaves out; time split mimics real use | Python (statsmodels, scikit-learn) |
| RQ2 | Decile table and segment shares | simple, readable concentration measure | pandas |
| RQ3 | Monthly correlation and log-log regression | small sample (24 months per hotel), so a simple model | statsmodels |
| RQ4 | Scenario simulation with a sensitivity grid | the policy has never been tried, so its effect must be assumed and stress-tested | pandas |

Excel or Tableau could reproduce RQ2 and RQ3; RQ1 and RQ4 need Python.

## 4. Analytical process

1. `scripts/01_prepare.py`: build dates, nights and booked value; drop 184 invalid rows; write the clean file and monthly KPIs; log every check.
2. `scripts/02_phase1_evidence.py`: descriptive evidence and charts.
3. `scripts/03_phase4_analysis.py`: RQ1-RQ4, writing `phase4_results.md` and the Phase 4 charts.

## 5. Feasibility, challenges, adjustments

| Challenge | Effect | Adjustment |
|---|---|---|
| Leakage columns (`reservation_status`, `assigned_room_type`, `booking_changes`) | inflated accuracy | excluded from all models |
| Suspect `deposit_type` and prior-cancellation coding | odds ratios that reflect a data artifact | report results with and without them; keep the policy to `No Deposit` bookings |
| No room inventory | no occupancy or RevPAR | use booked and realized value and ADR |
| Unknown resale of cancelled rooms | overstated losses | treat resale as an assumption (0% and 50%) |
| Policy effect unobserved | ROI cannot be measured directly | scenario grid; recommend a pilot to measure it |
| Data from 2015-2017 | figures may differ today | present the method as reusable on current PMS data |

## 6. Expected outcomes

- RQ1: a ranked list of cancellation drivers and an accuracy figure that tells management whether scoring bookings is worth doing.
- RQ2: the share of at-risk value that a targeted policy could reach.
- RQ3: whether pricing already tracks demand.
- RQ4: an expected annual value range for a targeted policy, and the assumptions it depends on.
