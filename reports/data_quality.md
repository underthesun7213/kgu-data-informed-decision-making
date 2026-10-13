# Data quality log

Source file: `data/raw/hotel_bookings.csv` (119,390 bookings, 32 columns).

| Check | Rows | Action |
|---|---|---|
| Rows in raw file | 119,390 | kept |
| Missing `children` | 4 | filled with 0 |
| Missing `country` | 488 | set to 'Unknown' |
| `agent` missing (no agent) | 16,340 | kept; means booked without agent |
| `company` missing | 112,593 | column not used |
| Bookings with 0 guests | 180 | dropped |
| Negative ADR | 1 | dropped |
| ADR above 1,000 (entry error) | 1 | dropped |
| Market segment 'Undefined' | 2 | dropped |
| 0-night stays (day use) | 715 | kept, flagged |
| Exact duplicate rows | 31,994 | kept (no booking ID; duplicates can be real group bookings) |
| Rows after cleaning | 119,206 |  |

Leakage columns excluded from every model: `reservation_status`, `reservation_status_date` (they record the outcome), `assigned_room_type` (known only at arrival) and `booking_changes` (counted until check-in or cancellation, so unknown when the booking is made). Both are kept for descriptive use only.
