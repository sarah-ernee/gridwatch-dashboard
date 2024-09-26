import streamlit as st
import pandas as pd


# Utility functions
# @st.cache_data
# def load_and_clean_data(file):
#     df = pd.read_csv(file)

#     # remove trailing spaces and whitespace
#     df.columns = df.columns.str.strip()
#     df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

#     df.dropna(subset=['timestamp'], inplace=True)

#     # remove na values
#     df.fillna(0, inplace=True)

#     # remove duplicate timestamp rows
#     df.drop_duplicates(subset='timestamp', inplace=True)

#     return df

@st.cache_data
def load_and_clean_data(file):
    chunks = []

    for chunk in pd.read_csv(file, chunksize=10000):
        chunk.columns = chunk.columns.str.strip()
        
        chunk['timestamp'] = pd.to_datetime(chunk['timestamp'], errors='coerce')
        chunk.dropna(subset=['timestamp'], inplace=True)
        chunk.fillna(0, inplace=True)

        chunks.append(chunk)

    df = pd.concat(chunks, ignore_index=True)
    df.drop_duplicates(subset='timestamp', inplace=True)
    return df

def setup_sql_db(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS power_data (
                        timestamp DATETIME PRIMARY KEY,
                        demand FLOAT,
                        frequency FLOAT,
                        coal FLOAT DEFAULT 0,
                        nuclear FLOAT DEFAULT 0,
                        ccgt FLOAT DEFAULT 0,
                        wind FLOAT DEFAULT 0,
                        pumped FLOAT DEFAULT 0,
                        hydro FLOAT DEFAULT 0,
                        biomass FLOAT DEFAULT 0,
                        oil FLOAT DEFAULT 0,
                        solar FLOAT DEFAULT 0,
                        ocgt FLOAT DEFAULT 0,
                        year INT,
                        week INT
                     )''')

    # Indexing to speed up sql queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_year ON power_data(year)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_week ON power_data(week)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON power_data(timestamp)')
    conn.commit()

def get_yearly_summary(conn):
    query = """
    SELECT 
        CAST(year AS INTEGER) as year, 
        AVG(demand) as avg_demand,
        AVG(frequency) as avg_frequency,
        MAX(demand) as peak_demand,
        MIN(demand) as trough_demand
    FROM power_data 
    GROUP BY year
    """
    return pd.read_sql_query(query, conn)

def get_weekly_summary(conn):
    query = """
    SELECT 
        week, 
        AVG(demand) as avg_demand,
        AVG(frequency) as avg_frequency,
        MAX(demand) as peak_demand,
        MIN(demand) as trough_demand
    FROM power_data 
    GROUP BY week
    """
    return pd.read_sql_query(query, conn)

def get_daily_summary(conn):
    query = """
    SELECT 
        DATE(timestamp) as date, 
        AVG(demand) as avg_demand,
        AVG(frequency) as avg_frequency,
        MAX(demand) as peak_demand,
        MIN(demand) as trough_demand
    FROM power_data 
    GROUP BY DATE(timestamp)
    """
    return pd.read_sql_query(query, conn)

def get_energy_mix(conn):
    query = """
    SELECT 
        SUM(coal) as coal,
        SUM(nuclear) as nuclear,
        SUM(ccgt) as ccgt,
        SUM(wind) as wind,
        SUM(pumped) as pumped,
        SUM(hydro) as hydro,
        SUM(biomass) as biomass,
        SUM(oil) as oil,
        SUM(solar) as solar,
        SUM(ocgt) as ocgt
    FROM power_data
    """
    return pd.read_sql_query(query, conn)

def get_frequency(conn):
    query = """
    SELECT timestamp, frequency
    FROM power_data
    """
    return pd.read_sql_query(query, conn)

def write_to_sql(conn, df):
    energy_sources = ['coal', 'nuclear', 'ccgt', 'wind', 'pumped', 'hydro', 'biomass', 'oil', 'solar', 'ocgt']

    for col in energy_sources:
        if col not in df.columns:
            df[col] = 0

    df['year'] = df['timestamp'].dt.year
    df['week'] = df['timestamp'].dt.isocalendar().week
    df[['timestamp', 'demand', 'frequency'] + energy_sources + ['year', 'week']].to_sql('power_data', conn, if_exists='replace', index=False)
