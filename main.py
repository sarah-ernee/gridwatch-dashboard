import streamlit as st
import sqlite3
import pandas as pd
from helpers import * 

st.title("Gridwatch UK Power Dashboard")
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = load_and_clean_data(uploaded_file)
    conn = sqlite3.connect(':memory:')
    setup_sql_db(conn)
    write_to_sql(conn, df)

    st.subheader("Demand with Moving Average")
    demand_with_moving_avg(df)

    st.subheader("Frequency Over Time")
    frequency_data = get_frequency(conn)
    frequency_over_time(frequency_data) 

    st.subheader("Energy Mix Distribution")
    energy_mix = get_energy_mix(conn)
    energy_mix_pie_chart(energy_mix)

    st.subheader("Daily Summary")
    daily_summary = get_daily_summary(conn)
    daily_peaks_and_troughs(daily_summary)

    st.subheader("Weekly Summary")
    weekly_summary = get_weekly_summary(conn)
    st.write(weekly_summary)  

    st.subheader("Yearly Summary")
    yearly_summary = get_yearly_summary(conn)
    st.write(yearly_summary)

    st.subheader("Year-on-Year")
    year_on_year_comparison(yearly_summary)
    
    conn.close()
