"""Clean the raw booking file and build monthly KPIs.

Input : data/raw/hotel_bookings.csv
Output: data/processed/bookings_clean.csv.gz, data/processed/monthly_kpis.csv,
        reports/data_quality.md
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

raw = pd.read_csv(ROOT / "data/raw/hotel_bookings.csv")
d = raw.copy()
d["arrival_date"] = pd.to_datetime(dict(
    year=d.arrival_date_year,
    month=d.arrival_date_month.map({m: i for i, m in enumerate(MONTHS, 1)}),
    day=d.arrival_date_day_of_month))
d["nights"] = d.stays_in_weekend_nights + d.stays_in_week_nights
d["guests"] = d.adults + d.children.fillna(0) + d.babies
d["revenue"] = d.adr * d.nights
d["arrival_month"] = d.arrival_date.dt.to_period("M").astype(str)

checks = [
    ("Rows in raw file", len(d), "kept"),
    ("Missing `children`", int(d.children.isna().sum()), "filled with 0"),
    ("Missing `country`", int(d.country.isna().sum()), "set to 'Unknown'"),
    ("`agent` missing (no agent)", int(d.agent.isna().sum()), "kept; means booked without agent"),
    ("`company` missing", int(d.company.isna().sum()), "column not used"),
    ("Bookings with 0 guests", int((d.guests == 0).sum()), "dropped"),
    ("Negative ADR", int((d.adr < 0).sum()), "dropped"),
    ("ADR above 1,000 (entry error)", int((d.adr > 1000).sum()), "dropped"),
    ("Market segment 'Undefined'", int((d.market_segment == "Undefined").sum()), "dropped"),
    ("0-night stays (day use)", int((d.nights == 0).sum()), "kept, flagged"),
    ("Exact duplicate rows", int(raw.duplicated().sum()), "kept (no booking ID; duplicates can be real group bookings)"),
]
d["children"] = d.children.fillna(0)
d["country"] = d.country.fillna("Unknown")
d = d[(d.guests > 0) & (d.adr >= 0) & (d.adr <= 1000) & (d.market_segment != "Undefined")].copy()
d["day_use"] = d.nights == 0
checks.append(("Rows after cleaning", len(d), ""))

d.to_csv(ROOT / "data/processed/bookings_clean.csv.gz", index=False, compression="gzip")

stayed = d[d.is_canceled == 0]
m = d.groupby(["hotel", "arrival_month"]).agg(
    bookings=("is_canceled", "size"), cancel_rate=("is_canceled", "mean"))
m = m.join(stayed.groupby(["hotel", "arrival_month"]).agg(
    room_nights=("nights", "sum"), revenue=("revenue", "sum")))
m = m.join(d[d.is_canceled == 1].groupby(["hotel", "arrival_month"]).revenue.sum().rename("cancelled_revenue"))
m["adr_realized"] = m.revenue / m.room_nights
m = m.reset_index().round(4)
m.to_csv(ROOT / "data/processed/monthly_kpis.csv", index=False)

lines = ["# Data quality log", "",
         "Source file: `data/raw/hotel_bookings.csv` (119,390 bookings, 32 columns).", "",
         "| Check | Rows | Action |", "|---|---|---|"]
lines += [f"| {a} | {b:,} | {c} |" for a, b, c in checks]
lines += ["", "Leakage columns excluded from every model: `reservation_status`, "
          "`reservation_status_date` (they record the outcome), `assigned_room_type` (known only at arrival) and "
          "`booking_changes` (counted until check-in or cancellation, so unknown when the booking is made). "
          "Both are kept for descriptive use only.", ""]
(ROOT / "reports/data_quality.md").write_text("\n".join(lines))
print("\n".join(lines))
