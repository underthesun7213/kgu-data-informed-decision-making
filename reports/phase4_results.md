# Phase 4 results (generated)

## RQ1. Which booking characteristics predict cancellation?

Train: 78,587 bookings (2015-07 to 2016-12). Test: 40,619 bookings (2017-01 to 2017-08).

| Model | Test AUC | Brier score |
|---|---|---|
| Baseline (train cancel rate 0.362 for everyone) | 0.500 | 0.238 |
| Logistic regression (12 interpretable terms) | 0.812 | 0.163 |
| Gradient boosting (all booking-time fields) | 0.842 | 0.157 |
| Gradient boosting without `deposit_type` | 0.827 | |

Odds ratios from the logistic regression (train period). Above 1 raises the odds of cancelling.

| term | odds_ratio | p_value |
|---|---|---|
| deposit[T.Non Refund] | 177.450 | 0.000 |
| prev_cancel | 91.958 | 0.000 |
| segment[T.Online TA] | 2.978 | 0.000 |
| segment[T.Aviation] | 2.000 | 0.002 |
| segment[T.Complementary] | 1.573 | 0.004 |
| log_lead | 1.428 | 0.000 |
| season[T.low] | 1.260 | 0.000 |
| segment[T.Groups] | 1.134 | 0.022 |
| I(adr / 10) | 1.038 | 0.000 |
| nights | 1.027 | 0.000 |
| has_agent | 1.025 | 0.581 |
| season[T.peak] | 1.007 | 0.783 |
| hotel[T.Resort Hotel] | 0.803 | 0.000 |
| segment[T.Offline TA/TO] | 0.723 | 0.000 |
| customer[T.Transient-Party] | 0.709 | 0.000 |
| segment[T.Corporate] | 0.696 | 0.000 |
| customer[T.Group] | 0.531 | 0.001 |
| customer[T.Contract] | 0.499 | 0.000 |
| special_req | 0.422 | 0.000 |
| deposit[T.Refundable] | 0.298 | 0.000 |
| is_repeated_guest | 0.139 | 0.000 |

Parking requests are left out of the logit: none of the 7,409 bookings that asked for parking cancelled (rate 0.000), which makes the coefficient infinite.

## RQ2. Where is booked revenue at risk concentrated?

All periods, by market segment:

| segment | bookings | cancel_rate | cancelled_value_eur | share_of_cancelled_value |
|---|---|---|---|---|
| Online TA | 56,408 | 0.368 | 10,227,646 | 0.612 |
| Groups | 19,790 | 0.611 | 2,800,544 | 0.167 |
| Offline TA/TO | 24,181 | 0.343 | 2,486,958 | 0.149 |
| Direct | 12,582 | 0.154 | 993,410 | 0.059 |
| Corporate | 5,282 | 0.188 | 196,383 | 0.012 |
| Aviation | 235 | 0.221 | 16,578 | 0.001 |
| Complementary | 728 | 0.122 | 270 | 0.000 |

Test period, `No Deposit` bookings only (the group a new policy could change), by predicted risk decile:

| risk decile (10 = highest) | bookings | predicted | actual_cancel | cancelled_value_eur | share_of_cancelled_value |
|---|---|---|---|---|---|
| 1 | 3,647 | 0.010 | 0.007 | 3,485 | 0.001 |
| 2 | 3,647 | 0.069 | 0.070 | 61,766 | 0.010 |
| 3 | 3,646 | 0.110 | 0.135 | 178,291 | 0.030 |
| 4 | 3,647 | 0.146 | 0.199 | 251,422 | 0.042 |
| 5 | 3,646 | 0.190 | 0.273 | 414,369 | 0.069 |
| 6 | 3,647 | 0.238 | 0.327 | 507,770 | 0.084 |
| 7 | 3,646 | 0.296 | 0.403 | 787,193 | 0.130 |
| 8 | 3,647 | 0.398 | 0.459 | 1,096,130 | 0.182 |
| 9 | 3,646 | 0.645 | 0.595 | 1,018,274 | 0.169 |
| 10 | 3,647 | 0.784 | 0.709 | 1,719,274 | 0.285 |

Top two deciles hold 45.3% of cancelled value among No Deposit bookings in the test period.

## RQ3. Does pricing follow demand across the year?

Monthly realized room-nights (stayed bookings) against realized ADR, 2015-08 to 2017-07.

| Hotel | Months | Corr(room-nights, ADR) | Elasticity of ADR to room-nights | R² | Corr(room-nights, cancel rate) |
|---|---|---|---|---|---|
| City Hotel | 24 | 0.85 | 0.47 | 0.73 | 0.29 |
| Resort Hotel | 24 | 0.65 | 0.97 | 0.46 | 0.80 |

## RQ4. What would a targeted deposit / reconfirmation policy be worth?

Scenario simulation on 2017 test bookings (8 months, annualized x12/8). Assumptions, all adjustable in the script:
- the policy applies to the highest-risk `No Deposit` bookings, scored by the RQ1 model;
- it prevents 10-30% of cancellations among targeted bookings;
- a cancelled room is resold 0% or 50% of the time (resold value is not a real loss);
- 2% (or 5%) of targeted guests who would have stayed walk away because of the deposit;
- handling cost EUR 1 per targeted booking.

Net annual effect with 2% walk-away:

| policy | net EUR/yr, resale 0% | net EUR/yr, resale 50% |
|---|---|---|
| top 10%, prevents 10% | 234,985 | 106,040 |
| top 10%, prevents 20% | 492,876 | 234,985 |
| top 10%, prevents 30% | 750,767 | 363,931 |
| top 20%, prevents 10% | 364,645 | 159,008 |
| top 20%, prevents 20% | 775,918 | 364,645 |
| top 20%, prevents 30% | 1,187,190 | 570,281 |

Net annual effect with 5% walk-away:

| policy | net EUR/yr, resale 0% | net EUR/yr, resale 50% |
|---|---|---|
| top 10%, prevents 10% | 208,832 | 79,886 |
| top 10%, prevents 20% | 466,723 | 208,832 |
| top 10%, prevents 30% | 724,614 | 337,778 |
| top 20%, prevents 10% | 311,132 | 105,496 |
| top 20%, prevents 20% | 722,405 | 311,132 |
| top 20%, prevents 30% | 1,133,678 | 516,769 |
