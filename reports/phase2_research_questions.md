# Phase 2 (mock): Research Questions

## Selected issues

1. Cancellations put 43% (City) and 33% (Resort) of booked value at risk.
2. Group and travel-agent channels cancel two to four times more often than direct bookings.
3. Seasonal pricing swings of up to 3.7x at the resort.

## Research questions

| # | Question | Type | How it is measured | Linked issue |
|---|---|---|---|---|
| RQ1 | Which booking characteristics, known at the time of booking, predict cancellation, and how accurately? | Quantitative | odds ratios from logistic regression; out-of-time AUC on 2017 bookings | 1, 2 |
| RQ2 | Where is the booked revenue at risk concentrated (segment, predicted-risk group)? | Quantitative | share of cancelled value by segment and by risk decile | 1, 2 |
| RQ3 | Does the hotels' pricing follow demand across months? | Quantitative | monthly correlation and elasticity between room-nights sold and realized ADR | 3 |
| RQ4 | What would a targeted deposit or reconfirmation policy for high-risk bookings be worth, net of side effects? | Quantitative (scenario) | simulated annual net revenue under stated assumptions | 1 |

## Justifications

- **RQ1.** A policy can only act on information available when the booking is made. Restricting the model to booking-time fields, and testing it on a later period, checks whether the pattern would hold in practice instead of only describing the past.
- **RQ2.** Management attention and policy cost should go where the money is. If a small share of bookings holds most of the cancelled value, a targeted policy is cheaper than a blanket one.
- **RQ3.** If ADR rises with demand, the hotels already price dynamically and the seasonality issue is about demand, not pricing. If ADR stays flat while demand swings, there is unused pricing power.
- **RQ4.** A recommendation needs an expected return. Because the data cannot show what guests would do under a new policy, the question is framed as a scenario with explicit, adjustable assumptions.

## Link to business goals

RQ1 and RQ2 find the risky bookings, RQ4 prices the response, and RQ3 checks whether revenue can also be raised on the stays that do happen. Together they answer: how can the group protect and grow room revenue with the data it already collects?

## Conceptual map

```
Booking attributes ──RQ1──> Cancellation risk ──RQ2──> Revenue at risk ──RQ4──> Policy ROI
Monthly demand ─────RQ3──> Pricing response ────────────────────────────────────> Pricing advice
```
