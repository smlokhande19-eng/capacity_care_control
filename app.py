"""
System Capacity & Care Load Analytics for Unaccompanied Children - Streamlit Dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import config
from src.data_loader import load_data, validate_data, filter_date_range, aggregate_by_frequency
from src.metrics import (
    get_all_kpis,
    calculate_total_system_load,
    calculate_net_daily_intake,
    calculate_care_load_growth_rate,
    identify_stress_periods,
    get_period_summary,
    calculate_rolling_metrics
)
from src.visualizations import (
    create_system_load_chart,
    create_cbp_vs_hhs_comparison,
    create_net_intake_chart,
    create_flow_analysis_chart,
    create_volatility_chart,
    create_stress_period_chart
)
from src.utils import format_number

# Page configuration
st.set_page_config(**config.PAGE_CONFIG)

# Custom styling
st.markdown("""
<style>
    .dashboard-header {
        padding: 1rem 1rem 0.75rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #0d3a5a 0%, #1a6fb9 100%);
        color: white;
        margin-bottom: 1rem;
    }
    .dashboard-header h1, .dashboard-header p {
        color: white;
    }
    .kpi-card {
        border-radius: 24px;
        padding: 22px;
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 18px 45px rgba(15, 60, 95, 0.14);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        margin-bottom: 18px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 22px 55px rgba(15, 60, 95, 0.22);
    }
    .kpi-label {
        font-size: 0.9rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.85);
        margin-bottom: 0.55rem;
    }
    .kpi-value {
        font-size: 2.35rem;
        font-weight: 800;
        line-height: 1.05;
        color: #ffffff;
    }
    .kpi-description {
        margin-top: 0.85rem;
        color: rgba(255,255,255,0.75);
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .insight-block {
        padding: 18px;
        border-radius: 1rem;
        background: #0f324f;
        color: #f4f9ff;
        box-shadow: 0 18px 45px rgba(12, 40, 68, 0.18);
    }
    .insight-block h4 {
        color: #ffffff;
        margin-bottom: 0.75rem;
    }
    .insight-block ul {
        padding-left: 1rem;
        color: #d9e3f5;
    }
    .insight-block li {
        margin-bottom: 0.55rem;
    }
    .footer-note {
        color: #6c7b8d;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown(
    f"<div class='dashboard-header'><h1>{config.APP_ICON} {config.APP_TITLE}</h1>"
    f"<p><strong>Mission</strong>: Provide data-driven insights into system capacity, care load dynamics, and operational performance of the Unaccompanied Children (UAC) care pipeline.</p></div>",
    unsafe_allow_html=True
)

# Load data
@st.cache_data
def get_data():
    df = load_data()
    return df

df = get_data()
validation = validate_data(df)

# Sidebar controls
st.sidebar.header("📋 Controls & Settings")

# Date range selector
st.sidebar.subheader("Date Range Selector")
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        value=df['Date'].min().date(),
        min_value=df['Date'].min().date(),
        max_value=df['Date'].max().date()
    )
with col2:
    end_date = st.date_input(
        "End Date",
        value=df['Date'].max().date(),
        min_value=df['Date'].min().date(),
        max_value=df['Date'].max().date()
    )

# Ensure start_date <= end_date
if start_date > end_date:
    st.sidebar.error("Start date must be before end date!")
    start_date, end_date = end_date, start_date

# Convert to datetime
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Filter data
df_filtered = filter_date_range(df, start_datetime, end_datetime)

# Time granularity selector
st.sidebar.subheader("Time Granularity")
granularity = st.sidebar.selectbox(
    "Select aggregation level",
    ["Daily", "Weekly", "Monthly"],
    index=0
)

granularity_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}
df_display = aggregate_by_frequency(df_filtered, granularity_map[granularity]) if granularity != "Daily" else df_filtered

# Metric toggles
st.sidebar.subheader("Metric Toggles")
show_cbp_hhs = st.sidebar.checkbox("CBP vs HHS Comparison", value=True)
show_net_intake = st.sidebar.checkbox("Net Intake & Backlog", value=True)
show_flow = st.sidebar.checkbox("Flow Analysis", value=True)
show_volatility = st.sidebar.checkbox("Volatility Index", value=True)
show_stress = st.sidebar.checkbox("Stress Periods", value=True)

# Data quality indicator
with st.sidebar.expander("📊 Data Quality"):
    st.write(f"**Total Records**: {validation['total_records']}")
    st.write(f"**Date Range**: {validation['date_range']}")
    if validation['is_valid']:
        st.success("✅ Data integrity verified")
    else:
        for issue in validation['issues']:
            st.warning(issue)

# Main content - KPI Cards
st.header("📈 Key Performance Indicators (KPIs)")

kpis = get_all_kpis(df_filtered)

# Derived trend insights
total_load = calculate_total_system_load(df_filtered)
net_intake = calculate_net_daily_intake(df_filtered)
growth_rate = calculate_care_load_growth_rate(df_filtered)
peak_load = format_number(total_load.max()) if len(total_load) > 0 else "N/A"
peak_date = df_filtered.loc[total_load.idxmax(), 'Date'].date() if len(total_load) > 0 else "N/A"
stress_data = identify_stress_periods(df_filtered)
stress_days = int(stress_data['Is Stressed'].sum())
weekly_growth = format_number(growth_rate.iloc[-1], 2) if len(growth_rate) > 0 else "N/A"

kpi_cols = st.columns(5)

with kpi_cols[0]:
    st.markdown(
        f"<div class='kpi-card'><div class='kpi-label'>{config.KPI_DEFINITIONS['total_children_under_care']['name']}</div>"
        f"<div class='kpi-value'>{format_number(kpis['total_children_under_care'])}</div>"
        f"<div class='kpi-description'>{config.KPI_DEFINITIONS['total_children_under_care']['description']}</div></div>",
        unsafe_allow_html=True
    )

with kpi_cols[1]:
    st.markdown(
        f"<div class='kpi-card'><div class='kpi-label'>{config.KPI_DEFINITIONS['net_intake_pressure']['name']}</div>"
        f"<div class='kpi-value'>{format_number(kpis['net_intake_pressure'], 1)}</div>"
        f"<div class='kpi-description'>{config.KPI_DEFINITIONS['net_intake_pressure']['description']}</div></div>",
        unsafe_allow_html=True
    )

with kpi_cols[2]:
    st.markdown(
        f"<div class='kpi-card'><div class='kpi-label'>{config.KPI_DEFINITIONS['care_load_volatility_index']['name']}</div>"
        f"<div class='kpi-value'>{format_number(kpis['care_load_volatility_index'], 1)}</div>"
        f"<div class='kpi-description'>{config.KPI_DEFINITIONS['care_load_volatility_index']['description']}</div></div>",
        unsafe_allow_html=True
    )

with kpi_cols[3]:
    st.markdown(
        f"<div class='kpi-card'><div class='kpi-label'>{config.KPI_DEFINITIONS['backlog_accumulation_rate']['name']}</div>"
        f"<div class='kpi-value'>{format_number(kpis['backlog_accumulation_rate'], 2)}%</div>"
        f"<div class='kpi-description'>{config.KPI_DEFINITIONS['backlog_accumulation_rate']['description']}</div></div>",
        unsafe_allow_html=True
    )

with kpi_cols[4]:
    st.markdown(
        f"<div class='kpi-card'><div class='kpi-label'>{config.KPI_DEFINITIONS['discharge_offset_ratio']['name']}</div>"
        f"<div class='kpi-value'>{format_number(kpis['discharge_offset_ratio'], 1)}%</div>"
        f"<div class='kpi-description'>{config.KPI_DEFINITIONS['discharge_offset_ratio']['description']}</div></div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# Overview and chart layout
left_col, right_col = st.columns([3, 1])
with left_col:
    st.subheader("System Load Overview")
    fig_system_load = create_system_load_chart(df_filtered)
    st.plotly_chart(fig_system_load, width='stretch')

with right_col:
    st.markdown('<div class="insight-block"><h4>Quick Insights</h4><ul>'
                f'<li><strong>Peak load</strong> reached {peak_load} on {peak_date}.</li>'
                f'<li><strong>{stress_days}</strong> high-stress day(s) detected.</li>'
                f'<li><strong>Latest growth</strong>: {weekly_growth}% total load change.</li>'
                '<li>Toggle charts and aggregation in the sidebar.</li>'
                '</ul></div>', unsafe_allow_html=True)

# Detailed trend analysis
st.header("📊 Detailed Trend Analysis")

if show_cbp_hhs:
    st.subheader("CBP vs HHS Load Comparison")
    fig_cbp_hhs = create_cbp_vs_hhs_comparison(df_filtered)
    st.plotly_chart(fig_cbp_hhs, width='stretch')

if show_net_intake:
    st.subheader("Net Intake & Backlog Trends")
    fig_net_intake = create_net_intake_chart(df_filtered)
    st.plotly_chart(fig_net_intake, width='stretch')

if show_flow:
    st.subheader("Intake & Discharge Flow Analysis")
    fig_flow = create_flow_analysis_chart(df_filtered)
    st.plotly_chart(fig_flow, width='stretch')

if show_volatility:
    st.subheader("System Load & Volatility Index")
    fig_volatility = create_volatility_chart(df_filtered)
    st.plotly_chart(fig_volatility, width='stretch')

if show_stress:
    st.subheader("Stress Period Identification")
    fig_stress = create_stress_period_chart(df_filtered, stress_data)
    st.plotly_chart(fig_stress, width='stretch')
    if stress_days > 0:
        st.warning(f"⚠️ High Stress Alert: {stress_days} day(s) with severe system load detected")

# Period Summary Statistics
st.header("📑 Period Summary Statistics")

period_summary = get_period_summary(df_filtered, start_datetime, end_datetime)

if period_summary:
    summary_cols = st.columns(3)
    
    with summary_cols[0]:
        st.metric("Days in Period", period_summary.get('days', 0))
        st.metric("Total Apprehended", format_number(period_summary.get('total_apprehended', 0)))
        st.metric("Total Transferred", format_number(period_summary.get('total_transferred', 0)))
    
    with summary_cols[1]:
        st.metric("Avg CBP Custody", format_number(period_summary.get('avg_cbp_custody', 0), 0))
        st.metric("Avg HHS Care", format_number(period_summary.get('avg_hhs_care', 0), 0))
        st.metric("Net Intake", format_number(period_summary.get('net_intake', 0)))
    
    with summary_cols[2]:
        total_discharged = period_summary.get('total_discharged', 0)
        st.metric("Total Discharged", format_number(total_discharged))
        if period_summary.get('total_transferred', 0) > 0:
            offset_ratio = (total_discharged / period_summary['total_transferred']) * 100
            st.metric("Discharge Offset %", f"{offset_ratio:.1f}%")
        else:
            st.metric("Discharge Offset %", "N/A")

# Data Explorer
with st.expander("🔍 Data Explorer"):
    st.subheader("Raw Data View")
    
    st.dataframe(
        df_display,
        width=1200,
        height=400
    )
    
    # Download option
    csv = df_display.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"uac_analytics_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
**Disclaimer**: This dashboard provides analytical insights based on available data. 
All findings should be reviewed in context with operational constraints and policy guidelines.

**Data Source**: System Capacity & Care Load Analytics for Unaccompanied Children (2023-2025)
""")
