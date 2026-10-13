# kgu-data-informed-decision-making: Portugal hotels (mock run)

Branch `sim/portugal-hotels`. A full mock run of project Phases 1-4 on the
**Hotel Booking Demand** dataset (two Portuguese hotels, 119,390 bookings, 2015-2017).

The course rubric grades how a team gets **from data to conclusions**, not whether the
data or conclusions are new. Every report here is therefore written as a visible chain:
data used -> metric -> result -> claim -> limit.

## Layout

```
data/
  raw/hotel_bookings.csv          original file (unchanged)
  processed/                      cleaned bookings + monthly KPIs
  README.md                       source, license, data dictionary, known quirks
scripts/
  01_prepare.py                   cleaning + monthly KPIs + data quality log
  02_phase1_evidence.py           Phase 1 metrics and charts
  03_phase4_analysis.py           RQ1-RQ4 analysis and charts
reports/
  data_quality.md
  phase1_issues.md
  phase2_research_questions.md
  phase3_proposal.md
  phase4_final_report.md          (+ phase4_results.md, generated tables)
figures/                          charts used in the reports
```

## Reproduce

```bash
pip install -r requirements.txt
python scripts/01_prepare.py
python scripts/02_phase1_evidence.py
python scripts/03_phase4_analysis.py
```

## How strong is the data-to-conclusion chain?

| Phase | Rubric focus | Chain in this run | Weak link |
|---|---|---|---|
| 1 | evidence for issues (5/10) | every issue is backed by a computed rate or EUR amount from 119k records | cancelled value is an upper bound (resale unknown) |
| 2 | specific, measurable questions (5/10) | each RQ names its metric and test | RQ3 rests on 24 monthly points per hotel |
| 3 | variables, sources, alternatives (10/30) | leakage and suspect fields handled before modelling | no external benchmark data downloaded |
| 4 | analysis (30) and recommendations (30) | out-of-time test (AUC 0.84) supports "risk scoring works"; scenario grid gives a value range for the policy | policy effect is assumed, so the recommendation is a pilot, not a rollout |

Main risk for grading: the 99% cancellation rate of `Non Refund` bookings looks like a
coding artifact. The reports flag it and show results without it; teams using this data
should do the same.
