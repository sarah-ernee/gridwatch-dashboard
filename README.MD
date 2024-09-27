# Gridwatch Dashboard

Data dashboarding contains the below data details:
- Demand with a seven day moving average
- Average frequency and demand, peak and trough demand for daily, weekly and yearly summary
- Year on year averages 
- Energy source distribution over time

Built with Streamlit for the frontend, Plotly for the graphing visualization and SQLite as an in-memory database.

## How to Run

1. Install libraries and packages used with `pip install -r requirements.txt`.
2. Run Streamlit with `streamlit run main.py`.
3. Upload Gridwatch CSV file or the sample file provided.
3. Given the size of CSV file processed, do refresh Streamlit or rerun step 2 if it lags.