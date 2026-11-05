# UIUC Meter Observer

Personal parking ticket records and an offline, interactive enforcement dashboard.

## View the dashboard

Download or clone this repository, then open `outputs/parking_enforcement/parking_dashboard.html` in a browser. No server or internet connection is required. GitHub's file viewer shows the HTML source; download the file to use the dashboard.

The dashboard supports street, date, Monday–Sunday calendar week, weekday, workday, observation type, and time filters. Hourly bars can be filled by street, weekday, observation type, meter payment status, person/source, or parking purpose. Hover over a weekday bar, or focus it with the keyboard, to preview that day's hourly counts. Filtered records can be downloaded as CSV.

## Files

| File | Purpose |
| --- | --- |
| `outputs/parking_enforcement/parking_enforcement_unified.csv` | Current dataset, with 13 columns |
| `outputs/parking_enforcement/parking_enforcement_unified.xlsx` | Formatted Excel dataset |
| `outputs/parking_enforcement/parking_dashboard.html` | Self-contained interactive dashboard with embedded data |
| `outputs/parking_enforcement/dashboard_template.html` | Dashboard HTML, CSS, and JavaScript source |
| `outputs/parking_enforcement/build_dashboard.py` | Embeds the CSV into the dashboard template |
| `build_parking.mjs` | Original records, normalization, deduplication, and CSV/Excel export |

## Data as of November 5, 2026

44 rows: 36 historical tickets with unique IDs, 2 additional reported tickets concerning other drivers, 4 officer sightings, and 2 no-ticket observations. The latest sighting is November 5, 2026 at 10:25 AM on Mathews Avenue.

- October 22, 2026 ticket `26PE101880` appears once. Its recent observation was merged with its historical ticket record.
- January 16, 2026 tickets `26PE400158` and `26PE400159` have the same timestamp and location but different IDs. Both remain separate tickets; whether they represent one parking incident is unconfirmed.
- The two additional reported tickets have no IDs. Their overlap with historical records cannot be conclusively checked.
- The October 15 afternoon date is uncertain: the user said October 15 and Friday, but October 15, 2026 was Thursday. The reported date and conflict are retained.
- Unconfirmed meter-payment statuses remain unconfirmed. Officer sightings are not counted as tickets.
- Workdays means Monday–Friday, without holiday adjustments. Times reflect the reported local times; no timezone conversion is applied.

These selected records describe observed frequency. They cannot estimate the probability of a ticket for an unpaid parking session: a representative denominator of comparable unpaid sessions, durations, and outcomes is missing.

## Rebuild the dashboard

Requires Python 3, using only its standard library:

```sh
python3 outputs/parking_enforcement/build_dashboard.py
```

To update the dashboard, edit the CSV while preserving the column names and date/time formats (`YYYY-MM-DD`, `HH:MM`), then run that command. It does not update the Excel workbook.

## Rebuild the dataset and Excel workbook

`build_parking.mjs` requires Node.js and the `@oai/artifact-tool` package supplied by the Codex spreadsheet runtime. It is not a standalone Python-only build. In an environment where that package is available:

```sh
node build_parking.mjs
python3 outputs/parking_enforcement/build_dashboard.py
```

The dataset builder regenerates CSV and Excel from records embedded in the script, overwriting those outputs. If adding records there, update its row-count validation and worksheet ranges as well. Preserve CSV-only edits before running it.

Source: user-supplied records and observations in the “Clarify Tick Or Ticket” conversation and subsequent updates. Records have not been independently verified.
