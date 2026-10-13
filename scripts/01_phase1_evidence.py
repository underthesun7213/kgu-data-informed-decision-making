"""Phase 1 evidence charts from the curated secondary indicators."""
from pathlib import Path
import pandas as pd
from style import plt, save, SERIES, TEXT_2

ROOT = Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "data/curated/lv_indicators_secondary.csv")
q = lambda ind, geo, per: d[(d.indicator == ind) & (d.geography == geo) & (d.period == per)].iloc[0]

# 1. Visitors 2024 vs 2025, total and Canadian
fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.6))
for ax, (ind, geo, title, scale, unit) in zip(axes, [
        ("visitor_volume", "Las Vegas", "All visitors", 1e6, "M"),
        ("canadian_visitors", "Las Vegas", "Canadian visitors", 1e6, "M")]):
    vals = [q(ind, geo, "2024").value / scale, q(ind, geo, "2025").value / scale]
    bars = ax.bar(["2024", "2025"], vals, color=[SERIES[0], SERIES[1]], width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.01, f"{v:.2f}{unit}", ha="center", fontsize=9, color=TEXT_2)
    ax.set_title(f"{title} ({q(ind, geo, '2025').yoy_change:+.1f}%)"); ax.set_ylim(0, max(vals) * 1.15)
fig.suptitle("Las Vegas visitation, 2024 vs 2025 (LVCVA, via secondary sources)", fontweight="bold", y=1.04)
save(fig, ROOT / "figures/p1_visitors_2024_2025.png")

# 2. Strip vs Downtown occupancy, July and August 2026
fig, ax = plt.subplots(figsize=(6.5, 3.6))
months = ["2026-07", "2026-08"]; w = 0.36
for i, geo in enumerate(["Strip", "Downtown"]):
    vals = [q("hotel_occupancy", geo, m).value for m in months]
    bars = ax.bar([j + (i - 0.5) * w for j in range(2)], vals, w - 0.03, color=SERIES[i], label=geo)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center", fontsize=9, color=TEXT_2)
ax.set_xticks([0, 1], ["July 2026", "August 2026"]); ax.set_ylim(0, 95); ax.set_ylabel("Hotel occupancy (%)")
ax.set_title("Downtown occupancy trails the Strip by 22-24 points"); ax.legend(loc="upper right")
save(fig, ROOT / "figures/p1_strip_vs_downtown_occupancy.png")

# 3. Gaming win YoY by area, August 2026
areas = ["Nevada statewide", "Clark County", "Strip", "North Las Vegas", "Downtown"]
yoy = [q("gaming_win", a, "2026-08").yoy_change for a in areas]
fig, ax = plt.subplots(figsize=(6.5, 3.4))
ax.barh(areas[::-1], yoy[::-1], color=[SERIES[1] if v < 0 else SERIES[0] for v in yoy[::-1]], height=0.55)
for y, v in enumerate(yoy[::-1]):
    ax.text(v + (0.1 if v >= 0 else -0.1), y, f"{v:+.2f}%", va="center", ha="left" if v >= 0 else "right", fontsize=9, color=TEXT_2)
ax.axvline(0, color=TEXT_2, linewidth=1); ax.set_xlim(-4.5, 4.5); ax.set_xlabel("Gaming win, change vs August 2025 (%)")
ax.set_title("August 2026 gaming win: Downtown falls while the state grows")
save(fig, ROOT / "figures/p1_gaming_win_yoy_aug2026.png")

# 4. Leisure & hospitality employment (context)
e = d[d.indicator == "employment_leisure_hospitality"].sort_values("period")
fig, ax = plt.subplots(figsize=(6.5, 3.4))
ax.plot(e.period, e.value, marker="o", color=SERIES[0])
ax.set_ylabel("Jobs ('000)"); ax.set_title("Las Vegas MSA leisure & hospitality employment (annual)")
save(fig, ROOT / "figures/p1_employment.png")
print("charts written")
