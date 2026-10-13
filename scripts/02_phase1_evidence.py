"""Phase 1 evidence: descriptive statistics and charts for the candidate issues."""
from pathlib import Path
import json
import pandas as pd
from style import plt, save, SERIES, TEXT_2

ROOT = Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "data/processed/bookings_clean.csv.gz", parse_dates=["arrival_date"])
out = {}

# Issue 1: cancellations and revenue at risk
by_hotel = d.groupby("hotel").agg(bookings=("is_canceled", "size"), cancel_rate=("is_canceled", "mean"))
rev = d.groupby(["hotel", "is_canceled"]).revenue.sum().unstack()
by_hotel["cancelled_revenue_eur"] = rev[1]
by_hotel["cancelled_share_of_booked_revenue"] = rev[1] / (rev[0] + rev[1])
out["by_hotel"] = by_hotel.round(4).to_dict("index")

# Issue 2: channel / segment
seg = d.groupby(["hotel", "market_segment"]).agg(bookings=("is_canceled", "size"), cancel_rate=("is_canceled", "mean"))
seg["share"] = seg.bookings / seg.groupby(level=0).bookings.transform("sum")
out["segment"] = {f"{h}|{s}": v for (h, s), v in seg.round(4).to_dict("index").items()}

# Issue 3: lead time
bins = [-1, 7, 30, 90, 180, 365, 800]
labels = ["0-7", "8-30", "31-90", "91-180", "181-365", "366+"]
d["lead_bucket"] = pd.cut(d.lead_time, bins, labels=labels)
lead = d.groupby("lead_bucket", observed=True).agg(bookings=("is_canceled", "size"), cancel_rate=("is_canceled", "mean"))
out["lead_time"] = lead.round(4).to_dict("index")

# Issue 4: seasonality of ADR (stayed bookings, paid ADR)
st = d[(d.is_canceled == 0) & (d.adr > 0)].copy()
st["month"] = st.arrival_date.dt.month
season = st.groupby(["hotel", "month"]).adr.mean().unstack(0)
out["adr_by_month"] = season.round(2).to_dict()

# Issue 5: repeat guests and deposit anomaly
out["repeat_guest_share"] = round(d.is_repeated_guest.mean(), 4)
out["deposit"] = d.groupby("deposit_type").agg(bookings=("is_canceled", "size"), cancel_rate=("is_canceled", "mean")).round(4).to_dict("index")
(ROOT / "reports/phase1_metrics.json").write_text(json.dumps(out, indent=2, default=str))

# Charts
fig, ax = plt.subplots(figsize=(7.5, 4))
segs = ["Direct", "Corporate", "Online TA", "Offline TA/TO", "Groups"]
x = range(len(segs)); w = 0.38
for i, h in enumerate(["City Hotel", "Resort Hotel"]):
    vals = [seg.loc[(h, s), "cancel_rate"] * 100 for s in segs]
    bars = ax.bar([j + (i - 0.5) * w for j in x], vals, w - 0.03, color=SERIES[i], label=h)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.0f}%", ha="center", fontsize=8, color=TEXT_2)
ax.set_xticks(list(x), segs); ax.set_ylabel("Cancellation rate (%)")
ax.set_title("Cancellation rate by market segment"); ax.legend(loc="upper left")
save(fig, ROOT / "figures/p1_cancel_by_segment.png")

fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(labels, lead.cancel_rate * 100, marker="o", color=SERIES[0])
for i, v in enumerate(lead.cancel_rate * 100):
    ax.annotate(f"{v:.0f}%", (i, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8, color=TEXT_2)
ax.set_xlabel("Lead time (days between booking and arrival)"); ax.set_ylabel("Cancellation rate (%)")
ax.set_ylim(0, 80); ax.set_title("Longer lead times cancel more often (both hotels)")
save(fig, ROOT / "figures/p1_cancel_by_leadtime.png")

fig, ax = plt.subplots(figsize=(7.5, 3.8))
mn = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for i, h in enumerate(["City Hotel", "Resort Hotel"]):
    ax.plot(mn, season[h], marker="o", markersize=4, color=SERIES[i], label=h)
ax.set_ylabel("Average daily rate (EUR)"); ax.set_title("ADR by arrival month (stayed bookings)")
ax.legend(loc="upper left")
save(fig, ROOT / "figures/p1_adr_seasonality.png")

m = pd.read_csv(ROOT / "data/processed/monthly_kpis.csv")
m["date"] = pd.to_datetime(m.arrival_month)
fig, ax = plt.subplots(figsize=(8, 3.8))
for i, h in enumerate(["City Hotel", "Resort Hotel"]):
    mm = m[m.hotel == h]
    ax.plot(mm.date, mm.cancelled_revenue / 1000, color=SERIES[i], label=h)
ax.set_ylabel("Cancelled booking value (EUR '000)"); ax.set_title("Booked revenue lost to cancellations, by arrival month")
ax.legend(loc="upper left")
save(fig, ROOT / "figures/p1_cancelled_revenue_monthly.png")
print(json.dumps({k: out[k] for k in ["by_hotel", "lead_time", "repeat_guest_share", "deposit"]}, indent=1, default=str))
print(seg.round(3))
