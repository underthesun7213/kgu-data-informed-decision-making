# Data

## Source

| Item | Value |
|---|---|
| Dataset | Hotel Booking Demand |
| Authors | Nuno Antonio, Ana de Almeida, Luis Nunes |
| Paper | "Hotel booking demand datasets", *Data in Brief* 22 (2019) 41-49, doi:10.1016/j.dib.2018.11.126 |
| License | CC BY 4.0 (open-access article and data) |
| Hotels | H1: resort hotel in the Algarve; H2: city hotel in Lisbon (both in Portugal, names withheld) |
| Period | Arrivals from 1 July 2015 to 31 August 2017 |
| Kaggle copy | kaggle.com/datasets/jessemostipak/hotel-booking-demand |
| File used here | `raw/hotel_bookings.csv`, the merged H1+H2 file published by TidyTuesday (2020-02-11): raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv |
| SHA-256 | `7c2ae42a7353905ea136e5c2287f17c92c5435826598bfbb8491c6f0c7b1fc06` |

## Files

| Path | Grain | Rows x columns | Produced by |
|---|---|---|---|
| `raw/hotel_bookings.csv` | one booking | 119,390 x 32 | download (unchanged) |
| `processed/bookings_clean.csv.gz` | one booking | 119,206 x 38 | `scripts/01_prepare.py` |
| `processed/monthly_kpis.csv` | hotel x arrival month | 52 x 8 | `scripts/01_prepare.py` |

Cleaning steps and counts are in `../reports/data_quality.md`.

## Data dictionary (raw columns)

| Column | Type | Meaning |
|---|---|---|
| hotel | category | `City Hotel` (Lisbon) or `Resort Hotel` (Algarve) |
| is_canceled | 0/1 | 1 if the booking was cancelled (target variable) |
| lead_time | int | days between booking date and arrival date |
| arrival_date_year / _month / _week_number / _day_of_month | int / text | arrival date parts |
| stays_in_weekend_nights / stays_in_week_nights | int | nights booked on weekend (Sat-Sun) and weekdays |
| adults, children, babies | int | party size |
| meal | category | BB, HB, FB, SC/Undefined (no meal) |
| country | ISO-3 | guest country of origin |
| market_segment | category | Direct, Corporate, Online TA, Offline TA/TO, Groups, Aviation, Complementary |
| distribution_channel | category | Direct, Corporate, TA/TO, GDS |
| is_repeated_guest | 0/1 | guest has stayed before |
| previous_cancellations / previous_bookings_not_canceled | int | guest history at booking time |
| reserved_room_type / assigned_room_type | code | room type booked / given at arrival (assigned is known only at arrival) |
| booking_changes | int | changes made until check-in or cancellation |
| deposit_type | category | No Deposit, Non Refund, Refundable |
| agent, company | ID | travel agent / company that made the booking (missing = none) |
| days_in_waiting_list | int | days before the booking was confirmed |
| customer_type | category | Transient, Contract, Group, Transient-Party |
| adr | EUR | average daily rate (room revenue / nights) |
| required_car_parking_spaces | int | parking spaces requested |
| total_of_special_requests | int | number of special requests |
| reservation_status / reservation_status_date | category / date | Check-Out, Canceled, No-Show and the date of the last status (outcome; never used as a predictor) |

## Derived columns (processed file)

| Column | Definition |
|---|---|
| arrival_date | date built from the three arrival parts |
| nights | weekend + week nights |
| guests | adults + children + babies |
| revenue | adr x nights (booked room revenue; realized only when `is_canceled` = 0) |
| arrival_month | YYYY-MM |
| day_use | nights = 0 |

## Known quirks

- **Non Refund deposits cancel 99.4% of the time** (14,586 bookings). 97% are Portuguese guests and 63% are Groups, which points to tour-operator block bookings released later rather than real non-refundable guests. Treat `deposit_type` as suspect.
- **Prior cancellations**: 6,479 bookings with a prior cancellation cancel 91.7% of the time; most of them are the same Non Refund blocks.
- **No room inventory**, so occupancy and RevPAR cannot be computed. ADR and booked or realized revenue are used instead.
- **Duplicates**: 31,994 rows are exact duplicates. There is no booking ID, so they are kept (group bookings produce identical rows).
