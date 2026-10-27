# Project Report: Olympic Performance Analysis

## 1\. Introduction

Olympic competitions generate data that can be examined from several perspectives, including country performance, athlete participation, medal outcomes, host context, seasonal differences, and changes across editions. This project uses Tableau to turn the supplied Olympic-related datasets into interactive dashboards and a guided Story.

The aim is to make comparisons easier to explore and to communicate patterns in the supplied data through visual analysis.

## 2\. Objectives

* Build interactive Tableau dashboards to summarize and compare Olympic-related performance.
* Explore country rankings, medal counts, medal points, and efficiency indicators.
* Examine athlete profiles and participation-related attributes.
* Compare Summer and Winter editions and inspect changes across years.
* Explore regional and sport-level patterns.
* Present investment-related indicators as exploratory context rather than proof of causation.
* Communicate the analysis through a seven-point Tableau Story.

## 3\. Tools and Technologies

* Tableau Desktop / Tableau Public for data visualization, dashboard authoring, Story assembly, and publishing.
* CSV files as the supplied data inputs.
* Tableau packaged workbook (`.twbx`) for sharing the workbook and its packaged data extract.
* GitHub for versioning and documenting project assets.

## 4\. Dataset Description

The project includes four supplied CSV datasets:

1. **All-time country rankings:** country, region, rank, medal totals, medal points, Games entered, and average efficiency fields.
2. **Athletes:** athlete identifiers and profile attributes, sport/category, Games participation, medal indicators, and other supplied performance-related fields.
3. **Games summary:** host city/country, season, year, participating nations, athletes, and Games-level medal summaries.
4. **Medal results:** country-by-edition medal outcomes alongside contextual indicators such as host advantage, sports investment tier, GDP tier, and population.

The repository preserves the original column names so they remain compatible with the supplied workbook. Detailed schemas can be inspected directly in the CSV files.

## 5\. Methodology

The project uses Tableau to organize the supplied datasets into visual summaries and comparisons. The dashboard and Story structure is designed to move from a broad overview to more focused perspectives.

The seven Story points are:

1. **Overview** — introduces the overall Olympic landscape represented in the workbook.
2. **Top Nations** — focuses on country-level performance and rankings.
3. **Seasonal Split** — compares Summer and Winter perspectives.
4. **Trends** — examines performance across time.
5. **Regions** — explores regional efficiency and productivity indicators.
6. **Sports** — examines sport-level patterns and competitive strengths.
7. **Investment** — explores investment-related patterns and contextual indicators.

Specific conclusions should be taken from the final published views and their displayed metrics. The report intentionally avoids inventing numerical findings before the final dashboards and data definitions have been validated.

## 6\. Dashboard and Story Design

The project is organized into two standalone dashboards and one Tableau Story containing seven navigable points. The dashboards provide direct views for comparison, while the Story supplies a guided sequence through the main analytical themes.

The final submission should include screenshots of both dashboards and the complete Story. Add those images to the `screenshots/` directory and refer to them here once they are available.

## 7\. Key Observations

Complete this section after reviewing the final published workbook. Record two to four observations that can be directly supported by visible charts, labels, and metrics. For each observation, specify the measure and comparison involved, and avoid implying that an observed association proves a cause.

* Observation 1: *Add a verified finding from the published dashboard.*
* Observation 2: *Add a verified finding from the published dashboard.*
* Observation 3: *Optional: add another verified finding.*

## 8\. Limitations

The datasets were supplied for this project, but their provenance and construction have not been independently established in this report. The files contain years extending through 2026; therefore, the records should not automatically be treated as official historical Olympic data. Confirm the source, definitions, coverage, and accuracy before making authoritative claims.

Measures such as medal efficiency, medal points, investment tier, and host advantage should be interpreted according to the workbook's definitions. Associations between investment and medal outcomes do not, on their own, demonstrate causation. Comparisons across datasets should also account for differing levels of aggregation and any missing or inconsistent values.

## 9\. Conclusion

This project demonstrates the use of Tableau to structure Olympic-related data into dashboards and a navigable analytical Story. Its value lies in making the supplied data easier to explore, compare, and discuss. The final conclusions should be grounded in verified observations from the published workbook, with clear acknowledgement of data limitations.

## 10\. Project Links

* Tableau Public Dashboard 1: https://public.tableau.com/app/profile/mayank.tanwani/viz/Olympic\_Performance\_Analysis\_Dashboard01/01GlobalOlympicPerformance
* Tableau Public Dashboard 2: https://public.tableau.com/app/profile/mayank.tanwani/viz/Olympic\_Performance\_Analysis\_Dashboard02/02EfficiencyPerformance
* Tableau Public Story: https://public.tableau.com/app/profile/mayank.tanwani/viz/Olympic\_Performance\_Analysis\_Stories/TheOlympicStory
* Deployed Website: https://olympic-performance-analysis-1.onrender.com/

