"""RQ2/RQ4 partial analysis from the curated published figures.

1. How much of the 2024->2025 visitor drop came from international (incl. Canadian) visitors?
2. A one-month comparison of gaming-win change by area (August 2026).
Writes reports/decomposition.md.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "data/curated/lv_indicators_secondary.csv")
v = lambda ind, geo, per: d[(d.indicator == ind) & (d.geography == geo) & (d.period == per)].iloc[0]

tot24, tot25 = v("visitor_volume", "Las Vegas", "2024").value, v("visitor_volume", "Las Vegas", "2025").value
can24, can25 = v("canadian_visitors", "Las Vegas", "2024").value, v("canadian_visitors", "Las Vegas", "2025").value
int25 = v("international_visitors", "Las Vegas", "2025")
int24 = int25.value / (1 + int25.yoy_change / 100)          # implied 2024 level from the reported % change
drop_tot, drop_can, drop_int = tot24 - tot25, can24 - can25, int24 - int25.value
dom24, dom25 = tot24 - int24, tot25 - int25.value

lines = ["# Decomposition of the 2025 visitor decline (generated)", "",
         "| Group | 2024 | 2025 | Change | Share of total decline |", "|---|---|---|---|---|",
         f"| All visitors | {tot24:,.0f} | {tot25:,.0f} | {-drop_tot:,.0f} | 100% |",
         f"| International (implied 2024 from -4.8%) | {int24:,.0f} | {int25.value:,.0f} | {-drop_int:,.0f} | {drop_int / drop_tot:.1%} |",
         f"| of which Canadian | {can24:,.0f} | {can25:,.0f} | {-drop_can:,.0f} | {drop_can / drop_tot:.1%} |",
         f"| Domestic (residual) | {dom24:,.0f} | {dom25:,.0f} | {-(dom24 - dom25):,.0f} | {(dom24 - dom25) / drop_tot:.1%} |", "",
         f"International visitors other than Canadians changed by {-(drop_int - drop_can):+,.0f}, i.e. they did not fall.",
         "Assumption: LVCVA's international count includes Canada (consistent with the numbers: the Canadian drop is larger than the international drop).", ""]

areas = ["Nevada statewide", "Clark County", "Strip", "North Las Vegas", "Downtown"]
g = {a: v("gaming_win", a, "2026-08").yoy_change for a in areas}
lines += ["## Gaming win, August 2026 vs August 2025", "", "| Area | Change | Gap vs statewide (points) |", "|---|---|---|"]
lines += [f"| {a} | {g[a]:+.2f}% | {g[a] - g['Nevada statewide']:+.2f} |" for a in areas]
lines += ["", "One month only: a difference, not yet a difference-in-differences. The planned RQ2 test needs the same comparison for every month 2015-2026."]
(ROOT / "reports/decomposition.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
