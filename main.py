import streamlit as st
import sqlite3
import pandas as pd
from helpers import *

# Caching functions so streamlit is not so laggy even with large CSV uploaded
@st.cache_data(hash_funcs={sqlite3.Connection: lambda _: None})
def get_cached_energy_mix(conn):
    return get_energy_mix(conn)

@st.cache_data(hash_funcs={sqlite3.Connection: lambda _: None})
def get_cached_daily_summary(conn):
    return get_daily_summary(conn)

@st.cache_data(hash_funcs={sqlite3.Connection: lambda _: None})
def get_cached_weekly_summary(conn):
    return get_weekly_summary(conn)

@st.cache_data(hash_funcs={sqlite3.Connection: lambda _: None})
def get_cached_yearly_summary(conn):
    return get_yearly_summary(conn)

# Initialize session state
if 'conn' not in st.session_state:
    st.session_state.conn = sqlite3.connect(':memory:', check_same_thread=False)
    setup_sql_db(st.session_state.conn)

if 'df' not in st.session_state:
    st.session_state.df = None

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

st.title("Gridwatch UK Power Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file and not st.session_state.data_loaded:
    st.session_state.df = load_and_clean_data(uploaded_file)
    write_to_sql(st.session_state.conn, st.session_state.df)
    st.session_state.data_loaded = True

# Display the data in streamlit once data is ready
if st.session_state.data_loaded:
    st.subheader("Demand with Moving Average")
    demand_with_moving_avg(st.session_state.df)

    st.subheader("Energy Mix Distribution")
    with st.spinner("Loading energy mix data..."):
        energy_mix = get_cached_energy_mix(st.session_state.conn)
        energy_mix_pie_chart(energy_mix)

    st.subheader("Daily Summary")
    with st.spinner("Loading daily summary data..."):
        daily_summary = get_cached_daily_summary(st.session_state.conn)
        daily_peaks_and_troughs(daily_summary)

    st.subheader("Weekly Summary")
    with st.spinner("Loading weekly summary data..."):
        weekly_summary = get_cached_weekly_summary(st.session_state.conn)
        st.write(weekly_summary)
        weekly_peaks_and_troughs(weekly_summary)

    st.subheader("Yearly Summary")
    with st.spinner("Loading yearly summary data..."):
        yearly_summary = get_cached_yearly_summary(st.session_state.conn)
        st.write(yearly_summary)
        yearly_peaks_and_troughs(yearly_summary)

    st.subheader("Year-on-Year Comparison")
    with st.spinner("Loading year-on-year data..."):
        yearly_summary = get_cached_yearly_summary(st.session_state.conn)
        year_on_year_comparison(yearly_summary)

else:
    st.info("Please upload a CSV file to begin.")

def close_db():
    if 'conn' in st.session_state and st.session_state.conn is not None:
        st.session_state.conn.close()