# Phase 3 (mock): Research Proposal

## 1. Variables and data sources

| RQ | Outcome | Key variables | Primary source | Alternative |
|---|---|---|---|---|
| RQ1 shortfall vs forecast | monthly visitors, occupancy, ADR, RevPAR | month, year, calendar dummies (holiday shifts, convention rotation), COVID break | LVCVA Summary of Monthly Tourism Indicators 2015-2025 (one PDF per year) + 2026 Executive Summaries | LVCVA historical annual series 1970-2025 |
| RQ2 Downtown vs others | occupancy by area; gaming win by area | area, month, post-2025 indicator | LVCVA Strip/Downtown tables; NGCB monthly revenue reports by area | UNLV Center for Gaming Research 10-year monthly comparisons |
| RQ3 guest ratings | review score; review text themes | traveler type, hotel class, amenities, price mentions | UCI Las Vegas Strip (2015, 504 reviews) | Inside Airbnb Clark County reviews (2026); manual sample of recent hotel reviews |
| RQ4 origin and access | visitor change by origin; airport passengers | Canadian, international and domestic visitors; air passengers | LVCVA year-end figures; Harry Reid airport reports | Statistics Canada 24-10-0053-01; NTTO I-94 |

## 2. Methods and tools

| RQ | Method | Why |
|---|---|---|
| RQ1 | seasonal forecast (e.g., SARIMA or ETS) fitted on pre-2025 months, compared with actuals | separates trend from seasonality and calendar timing |
| RQ2 | difference-in-differences, area x month panel | other areas act as a comparison group |
| RQ3 | regression with hotel fixed effects; keyword or topic counts in review text | within-hotel comparisons avoid confusing hotels with amenities |
| RQ4 | arithmetic decomposition; correlation with airport traffic | simple, transparent sizing of external causes |

Tools: Python (pandas, statsmodels), Excel for transcribing PDF tables, Tableau or matplotlib for charts.

## 3. Feasibility and challenges

| Challenge | Effect | Adjustment |
|---|---|---|
| All official data is PDF | 11 annual PDFs + monthly NGCB reports must be transcribed | split transcription across four members; double-enter 10% of cells to check errors |
| Aggregates only (one row per month) | small samples, autocorrelation (see `power_simulation.md`) | use comparison areas (RQ2) and forecast gaps (RQ1) rather than regressions of one series on another |
| COVID 2020-2021 | structural break | exclude or model separately |
| No recent review text in UCI | qualitative evidence is dated | Inside Airbnb reviews or a manual recent sample |
| Single destination, many simultaneous shocks | causes cannot be separated | report associations and sizes, not causal effects |

## 4. Expected outcomes

RQ1: size of the "unexplained" shortfall; RQ2: whether Downtown underperforms beyond the city-wide decline; RQ3: which guest groups rate lowest; RQ4: how much of the decline is domestic.
