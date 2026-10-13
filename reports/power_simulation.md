# Power simulation (SYNTHETIC data, generated)

Question simulated: does the year-over-year change in ADR explain the change in visitors?

| Months of data | Detects true effect, naive SE | Detects true effect, HAC SE | Median 95% CI width | False positives when true effect is 0 (naive / HAC; should be 5%) |
|---|---|---|---|---|
| 20 (2025-01 to 2026-08 only) | 56% | 68% | 0.55 | 12% / 24% |
| 32 | 77% | 79% | 0.47 | 14% / 19% |
| 68 (2015-2019 and 2022-2026, COVID removed) | 96% | 95% | 0.36 | 16% / 14% |

Reading: with only the post-2025 months, a real effect is missed about a third to a half of the time, and a non-existent one is reported as significant two to five times more often than the nominal 5%, because neighbouring months move together. A longer series helps power but not the false-positive problem, and none of it identifies cause.
