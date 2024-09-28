# Gridwatch Dashboard

Built with Streamlit for the frontend, Plotly for the graphing visualization and SQLite as an in-memory database.
Has been tested on Gridwatch dataset from May 2011 to Sep 2024 on the https://www.gridwatch.templar.co.uk/ website.

Data dashboarding contains the below data details:
- Demand with a seven day moving average
- Average frequency and demand, peak and trough demand for daily, weekly and yearly summary
- Year on year averages 
- Energy source distribution over time

## How to Run

1. Install libraries and packages used with `pip install -r requirements.txt`.
2. Run Streamlit with `streamlit run main.py`.
3. Upload Gridwatch CSV file.

## Navigating the Repo

1. `database.py` contains functions related to: CSV processing, data cleanup, Sqlite database setup, Sql queries for charts.
2. `plot.py` contains functions related to: Chart plotting, anomalous detections.
3. `main.py` is the source file that calls `database` and `plot` helper functions for Streamlit dashboard.
