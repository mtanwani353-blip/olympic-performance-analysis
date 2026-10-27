# Global Olympic Performance Analysis (1992–2026)

Tableau dashboards analysing medal achievements, athlete participation, regional efficiency, sport-category performance and the relationship between sports investment and medal outcomes across Summer and Winter Games.

## Contents
- `workbook/Olympic_Performance_Analysis_FINAL.twbx` – packaged Tableau workbook (open in Tableau Desktop or Tableau Public)
- `data/` – cleaned CSVs: `country_rankings`, `athletes`, `games_summary`, `medal_results`
- `scripts/build_workbook.py` – script that generated the workbook from the CSVs

## Dashboards
1. **Olympic Performance Dashboard** – avg medals per athlete by sport category, top 20 countries, trend of total medals awarded
2. **Regional Efficiency Dashboard** – sports investment vs medal performance (bubble), avg medal efficiency by region, host-nation medal totals, regional medal distribution

## Data notes
- Column names were cleaned (e.g. `Country (Medal Results.Csv)` → `Country`).
- `Investment Score` was added to `medal_results` (Low = 1, Medium = 2, High = 3).

## Deployed Website link
https://olympic-performance-analysis-1.onrender.com/
