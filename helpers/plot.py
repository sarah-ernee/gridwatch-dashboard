import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objs as go

import pandas as pd

def demand_with_moving_avg(df):
    df['demand_7day_ma'] = df['demand'].rolling(window=2100).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['demand'], mode='lines', name='Power Demand (MW)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['demand_7day_ma'], mode='lines', name='7-Day Moving Average', line=dict(color='orange')))
    
    anomalous_points = df[df['demand'] > 200000]

    fig.add_trace(go.Scatter(
        x=anomalous_points['timestamp'], 
        y=anomalous_points['demand'], 
        mode='markers', 
        name='High Demand Anomalies',
        marker=dict(color='red', size=8, symbol='x', opacity=0.8)
    ))

    fig.update_layout(
        title='Power Demand with 7-Day Moving Average',
        xaxis_title='Date',
        yaxis_title='Power Demand (MW)',
        legend_title='Legend',
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
    
    highest_peak = daily_summary['peak_demand'].max()
    peak_date = daily_summary.loc[daily_summary['peak_demand'] == highest_peak, 'date'].iloc[0]
    fig.add_trace(go.Scatter(
        x=[peak_date], 
        y=[highest_peak], 
        mode='markers+text', 
        marker=dict(color='red', size=10, symbol='x'),
        text=['Highest Peak'],
        textposition="top center",
        name='Highest Peak'
    ))

    lowest_trough = daily_summary['trough_demand'].min()
    trough_date = daily_summary.loc[daily_summary['trough_demand'] == lowest_trough, 'date'].iloc[0]
    fig.add_trace(go.Scatter(
        x=[trough_date], 
        y=[lowest_trough], 
        mode='markers+text', 
        marker=dict(color='green', size=10, symbol='circle'),
        text=['Lowest Trough'],
        textposition="bottom center",
        name='Lowest Trough'
    ))

    fig.update_layout(
        xaxis_title='Date', 
        yaxis_title='Power Demand (MW)')
    st.plotly_chart(fig)


def weekly_peaks_and_troughs(weekly_summary):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=weekly_summary['week'], y=weekly_summary['peak_demand'], 
                             mode='lines', name='Peak Demand'))
    fig.add_trace(go.Scatter(x=weekly_summary['week'], y=weekly_summary['trough_demand'], 
                             mode='lines', name='Trough Demand'))
    
    highest_peak = weekly_summary['peak_demand'].max()
    peak_week = weekly_summary.loc[weekly_summary['peak_demand'] == highest_peak, 'week'].iloc[0]
    fig.add_trace(go.Scatter(
        x=[peak_week], 
        y=[highest_peak], 
        mode='markers+text', 
        marker=dict(color='red', size=10, symbol='x'),
        text=['Highest Peak'],
        textposition="top center",
        name='Highest Peak'
    ))

    lowest_trough = weekly_summary['trough_demand'].min()
    trough_week = weekly_summary.loc[weekly_summary['trough_demand'] == lowest_trough, 'week'].iloc[0]
    fig.add_trace(go.Scatter(
        x=[trough_week], 
        y=[lowest_trough], 
        mode='markers+text', 
        marker=dict(color='green', size=10, symbol='circle'),
        text=['Lowest Trough'],
        textposition="bottom center",
        name='Lowest Trough'
    ))

    fig.update_layout(
        title='Weekly Peak and Trough Power Demand',
        xaxis_title='Week', 
        yaxis_title='Power Demand (MW)')
    
    st.plotly_chart(fig)


def yearly_peaks_and_troughs(yearly_summary):
    fig = go.Figure()

    # Change from Bar to Scatter for peaks and troughs
    fig.add_trace(go.Scatter(x=yearly_summary['year'], y=yearly_summary['peak_demand'], 
                             mode='lines', name='Peak Demand'))
    fig.add_trace(go.Scatter(x=yearly_summary['year'], y=yearly_summary['trough_demand'], 
                             mode='lines', name='Trough Demand'))
    
    highest_peak = yearly_summary['peak_demand'].max()
    peak_year = yearly_summary.loc[yearly_summary['peak_demand'] == highest_peak, 'year'].iloc[0]
    fig.add_trace(go.Scatter(
        x=[peak_year], 
        y=[highest_peak], 
        mode='markers+text', 
        marker=dict(color='red', size=10, symbol='x'),
        text=['Highest Peak'],
        textposition="top center",
        name='Highest Peak'
    ))

    lowest_trough = yearly_summary['trough_demand'].min()
    trough_year = yearly_summary.loc[yearly_summary['trough_demand'] == lowest_trough, 'year'].iloc[0]
    fig.add_trace(go.Scatter(
        x=[trough_year], 
        y=[lowest_trough], 
        mode='markers+text', 
        marker=dict(color='green', size=10, symbol='circle'),
        text=['Lowest Trough'],
        textposition="bottom center",
        name='Lowest Trough'
    ))

    fig.update_layout(
        title='Yearly Peak and Trough Power Demand',
        xaxis_title='Year', 
        yaxis_title='Power Demand (MW)')
    
    st.plotly_chart(fig)


def year_on_year_comparison(yearly_summary):

    fig = go.Figure()

    fig.add_trace(go.Bar(x=yearly_summary['year'], y=yearly_summary['avg_demand'], name='Average Demand'))
    fig.add_trace(go.Scatter(x=yearly_summary['year'], y=yearly_summary['peak_demand'], mode='lines+markers', name='Peak Demand'))
    fig.add_trace(go.Scatter(x=yearly_summary['year'], y=yearly_summary['trough_demand'], mode='lines+markers', name='Trough Demand'))
    fig.update_layout(
        title='Yearly Power Demand Comparison',
        xaxis_title='Year', 
        yaxis_title='Power Demand (MW)', 
        xaxis=dict(
            tickmode='array', 
            tickvals=yearly_summary['year']
        ))
    
    st.plotly_chart(fig)
