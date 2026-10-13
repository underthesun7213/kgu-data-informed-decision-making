# kgu-data-informed-decision-making: Las Vegas (mock run)

Branch `sim/las-vegas`. A mock run of project Phases 1-4 on the Las Vegas visitation decline.

The course grades how a team gets **from data to conclusions**. Each report therefore shows the
chain data -> metric -> result -> claim -> limit, and marks what could not be executed.

## Layout

```
data/
  raw/uci_las_vegas_strip/        504 TripAdvisor reviews (row-level)
  curated/lv_indicators_secondary.csv   58 published figures with sources
  source_manifest.csv             all original sources (PDF/CSV/Excel) and target paths
  README.md
scripts/
  00_fetch_sources.py             downloads the manifest on an unrestricted network
  01_phase1_evidence.py           Phase 1 charts
  02_uci_reviews_analysis.py      guest-rating analysis (RQ3)
  03_power_simulation.py          SYNTHETIC check of monthly-aggregate regressions
  04_decomposition.py             origin decomposition and area comparison (RQ2, RQ4)
reports/                          phase1-4 reports + generated result tables
figures/
```

## Reproduce

```bash
pip install -r requirements.txt
python scripts/00_fetch_sources.py      # optional; needs access to the publishers
python scripts/01_phase1_evidence.py
python scripts/02_uci_reviews_analysis.py
python scripts/03_power_simulation.py
python scripts/04_decomposition.py
```

## Strength of the data-to-conclusion chain

| Phase | Chain in this run | Weak link |
|---|---|---|
| 1 | every issue cites a published figure with source | figures are secondary copies; some Downtown numbers rest on one article |
| 2 | each RQ names a comparison design | depends on data not yet transcribed |
| 3 | sources, alternatives and the PDF transcription plan are explicit | heavy manual work |
| 4 | origin decomposition (92% domestic) and the Downtown gap hold; UCI analysis shows which claims are not identifiable | no monthly series, no costs: no ROI, causes not separable |

Compared with the Portugal branch (`sim/portugal-hotels`), this topic is stronger in Phase 1
and weaker in Phase 4 analysis and recommendations.
