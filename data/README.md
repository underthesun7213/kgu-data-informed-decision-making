# Data

Network access from the environment that built this branch was blocked for every
publisher (LVCVA, NGCB, Statistics Canada, NTTO, FRED/BLS, Inside Airbnb, UCI), so the
branch holds three kinds of data:

| Folder / file | What it is | Grain | Status |
|---|---|---|---|
| `raw/uci_las_vegas_strip/LasVegasTripAdvisorReviews-Dataset.csv` | UCI "Las Vegas Strip" dataset, 504 TripAdvisor reviews of 21 hotels (2015 stays), CC BY 4.0, Moro, Rita & Coelho (2017) | one review | downloaded from a GitHub mirror (QiuRunwen/CategoryEncoderComparison); SHA-256 `c9711cc3...ba3ac85` |
| `curated/lv_indicators_secondary.csv` | 58 published figures (visitors, occupancy, ADR, RevPAR, gaming win, airport, Canada, US arrivals, employment, one poll), each with publisher, URL and verification level | one indicator x geography x period | typed in from news and search snippets that quote the official releases; **check against the PDFs before final use** |
| `source_manifest.csv` | every original source with URL, format, grain and target path | one source | run `scripts/00_fetch_sources.py` on an unrestricted network to fill `raw/` |

## UCI columns (verified from the file)

Semicolon-separated; `Hotel stars` uses a decimal comma ("3,5"). 504 rows x 20 columns, no missing values.

| Column | Type | Values |
|---|---|---|
| User country / User continent | category | 48 countries; North America 295, Europe 118, Oceania 41, Asia 36, Africa 7, South America 7 |
| Nr. reviews, Nr. hotel reviews, Helpful votes | int | reviewer activity |
| Score | int 1-5 | target; mean 4.12 |
| Period of stay | category | Dec-Feb, Mar-May, Jun-Aug, Sep-Nov |
| Traveler type | category | Couples 214, Families 110, Friends 82, Business 74, Solo 24 |
| Pool, Gym, Tennis court, Spa, Casino, Free internet | YES/NO | hotel amenities (constant within a hotel) |
| Hotel name, Hotel stars, Nr. rooms | hotel attributes | 21 hotels, 24 reviews each |
| Member years | int | one invalid value (-1806), set to missing |
| Review month, Review weekday | category | 42 reviews per month |

## Curated indicators: column meaning

`indicator, geography, period, value, unit, yoy_change, yoy_unit, original_publisher, source_url, verification, notes`.
`verification` says how the number was checked (for example "secondary (single source)").
