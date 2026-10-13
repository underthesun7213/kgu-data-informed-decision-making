# UCI Las Vegas Strip results (generated)

Rows: 504; hotels: 21; reviews per hotel: 24-24; mean score 4.12.

## Score by traveler type

| Traveler type | Reviews | Mean score |
|---|---|---|
| Business | 74 | 3.88 |
| Solo | 24 | 3.92 |
| Families | 110 | 4.02 |
| Couples | 214 | 4.23 |
| Friends | 82 | 4.26 |

Lowest-rated hotels: Circus Circus Hotel & Casino Las Vegas (3.21), Monte Carlo Resort&Casino (3.29), Excalibur Hotel & Casino (3.71).
Highest-rated: Marriott's Grand Chateau (4.54), The Venetian Las Vegas Hotel (4.58), Wynn Las Vegas (4.62).

## Regression of score (OLS)

n = 503, R² = 0.155 (adjusted 0.118). Hotel identity alone gives R² = 0.134.

| Term | Coef. | p (naive SE) | p (SE clustered by hotel, 21 clusters) |
|---|---|---|---|
| stars | 0.286 | 0.000 | 0.000 |
| Pool | 1.063 | 0.001 | 0.000 |
| Gym | 0.966 | 0.004 | 0.000 |
| Spa | -0.511 | 0.024 | 0.000 |
| Free_internet | 0.745 | 0.000 | 0.000 |
| C(Traveler_type)[T.Couples] | 0.373 | 0.005 | 0.001 |
| C(Traveler_type)[T.Friends] | 0.448 | 0.004 | 0.000 |

Hotel amenities do not vary within a hotel, so their effects are really estimated from 21 hotels, not 503 reviews. Clustered standard errors with 21 clusters and this many regressors are themselves unreliable, so two cleaner checks follow.

### Check 1: hotel-level model (n = 21)

R² = 0.80, adjusted 0.71, F-test p = 0.000. Hotels without a pool: Circus Circus Hotel & Casino Las Vegas; without a gym: The Cromwell; without free internet: Monte Carlo Resort&Casino. Each amenity 'effect' is therefore the gap between one hotel and the rest, and cannot be separated from everything else about that hotel.

| Term | Coef. | p |
|---|---|---|
| stars | 0.273 | 0.004 |
| pool | 0.870 | 0.014 |
| gym | 0.598 | 0.060 |
| spa | -0.279 | 0.139 |
| wifi | 0.796 | 0.003 |
| np.log(rooms) | -0.064 | 0.532 |

### Check 2: traveler type within the same hotel (hotel fixed effects)

| Traveler type vs Business | Coef. | p |
|---|---|---|
| Couples | 0.415 | 0.000 |
| Families | 0.202 | 0.131 |
| Friends | 0.496 | 0.000 |
| Solo | 0.238 | 0.286 |

## Predicting a 4-5 score (5-fold cross-validation)

Share of 4-5 scores (accuracy of always guessing 'high'): 0.776. Logistic regression accuracy 0.770, AUC 0.658.
