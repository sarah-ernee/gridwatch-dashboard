import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objs as go

import pandas as pd

# should read from sql too
def demand_with_moving_avg(df):
    df['demand_7day_ma'] = df['demand'].rolling(window=7).mean()
    fig = px.line(df, x='timestamp', y=['demand', 'demand_7day_ma'], 
                  labels={'value': 'Power Demand (MW)', 'timestamp': 'Date'}, 
                  title='Power Demand with 7-day Moving Average')
    
    # for i in range(len(df) - 2):
    #     if df['demand'][i] < df['demand'][i + 1] > df['demand'][i + 2]:  
    #         fig.add_annotation(x=df['timestamp'][i + 1], y=df['demand'][i + 1],
    #                            text="Peak Demand",
    #                            showarrow=True,
    #                            arrowhead=2,
    #                            ax=0,
    #                            ay=-40)
    st.plotly_chart(fig)


def frequency_over_time(frequency_data):

    fig = px.line(frequency_data, x='timestamp', y='frequency', 
                  labels={'frequency': 'Frequency (Hz)', 'timestamp': 'Date'}, 
                  )
    
    st.plotly_chart(fig)


def energy_mix_pie_chart(energy_mix):
    labels = energy_mix.columns
    values = energy_mix.iloc[0].values  
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)]) 
    
    st.plotly_chart(fig)


def daily_peaks_and_troughs(daily_summary):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=daily_summary['date'], y=daily_summary['peak_demand'], 
                             mode='lines', name='Peak Demand'))
    fig.add_trace(go.Scatter(x=daily_summary['date'], y=daily_summary['trough_demand'], 
                             mode='lines', name='Trough Demand'))
    fig.update_layout(title='Daily Peak and Trough Power Demand',
                      xaxis_title='Date', yaxis_title='Power Demand (MW)')
    
    # for i in range(len(daily_summary) - 1):
    #     if daily_summary['peak_demand'][i] < daily_summary['peak_demand'][i + 1] > daily_summary['peak_demand'][i + 2]:
    #         fig.add_annotation(x=daily_summary['date'][i + 1], y=daily_summary['peak_demand'][i + 1],
    #                            text="Peak Day",
    #                            showarrow=True,
    #                            arrowhead=2,
    #                            ax=0,
    #                            ay=-40)

    fig.update_layout(xaxis_title='Date', yaxis_title='Power Demand (MW)')
    st.plotly_chart(fig)


def weekly_peaks_and_troughs(weekly_summary):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=weekly_summary['week'], y=weekly_summary['peak_demand'], 
                             mode='lines', name='Peak Demand'))
    fig.add_trace(go.Scatter(x=weekly_summary['week'], y=weekly_summary['trough_demand'], 
                             mode='lines', name='Trough Demand'))
    fig.update_layout(title='Weekly Peak and Trough Power Demand',
                      xaxis_title='Week', yaxis_title='Power Demand (MW)')
    
    st.plotly_chart(fig)


def yearly_peaks_and_troughs(yearly_summary):
    fig = go.Figure()

    fig.add_trace(go.Bar(x=yearly_summary['year'], y=yearly_summary['peak_demand'], 
                         name='Peak Demand'))
    fig.add_trace(go.Bar(x=yearly_summary['year'], y=yearly_summary['trough_demand'], 
                         name='Trough Demand'))
    fig.update_layout(title='Yearly Peak and Trough Power Demand',
                      xaxis_title='Year', yaxis_title='Power Demand (MW)')
    
    st.plotly_chart(fig)


def year_on_year_comparison(yearly_summary):

    fig = go.Figure()

    fig.add_trace(go.Bar(x=yearly_summary['year'], y=yearly_summary['avg_demand'], name='Average Demand'))
    fig.add_trace(go.Scatter(x=yearly_summary['year'], y=yearly_summary['peak_demand'], mode='lines+markers', name='Peak Demand'))
    fig.add_trace(go.Scatter(x=yearly_summary['year'], y=yearly_summary['trough_demand'], mode='lines+markers', name='Trough Demand'))
    fig.update_layout(title='Yearly Power Demand Comparison',
                      xaxis_title='Year', yaxis_title='Power Demand (MW)')
    
    st.plotly_chart(fig)
