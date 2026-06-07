"""
Configuration constants for UAC Analytics Dashboard
"""

# Application Settings
APP_TITLE = "System Capacity & Care Load Analytics for Unaccompanied Children"
APP_ICON = "📊"
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# KPI Names and Descriptions
KPI_DEFINITIONS = {
    "total_children_under_care": {
        "name": "Total Children Under Care",
        "description": "System-wide responsibility (CBP Custody + HHS Care)"
    },
    "net_intake_pressure": {
        "name": "Net Intake Pressure",
        "description": "Inflow vs outflow imbalance (Transfers - Discharges)"
    },
    "care_load_volatility_index": {
        "name": "Care Load Volatility Index",
        "description": "Stability of system (7-day rolling std dev)"
    },
    "backlog_accumulation_rate": {
        "name": "Backlog Accumulation Rate",
        "description": "Sustained care pressure (% increase over 7 days)"
    },
    "discharge_offset_ratio": {
        "name": "Discharge Offset Ratio",
        "description": "Ability to relieve load (Discharges / Transfers)"
    }
}

# Data Columns
DATA_COLUMNS = {
    "date": "Date",
    "apprehended": "Children Apprehended",
    "cbp_custody": "Children in CBP Custody",
    "transferred": "Children Transferred from CBP",
    "hhs_care": "Children in HHS Care",
    "discharged": "Children Discharged"
}

# Analysis Parameters
ROLLING_WINDOW_7DAY = 7
ROLLING_WINDOW_14DAY = 14
VOLATILITY_WINDOW = 7

# Date Format
DATE_FORMAT = "%Y-%m-%d"

# Color Palette
COLORS = {
    "cbp": "#1f77b4",      # Blue
    "hhs": "#ff7f0e",      # Orange
    "total": "#2ca02c",    # Green
    "net_intake": "#d62728", # Red
    "discharge": "#9467bd"  # Purple
}

# Data Generation Parameters (for sample data)
SAMPLE_DATA_START_DATE = "2023-01-01"
SAMPLE_DATA_END_DATE = "2025-12-31"
SAMPLE_DATA_AVG_APPREHENDED = 450
SAMPLE_DATA_AVG_TRANSFERRED = 380
SAMPLE_DATA_AVG_DISCHARGED = 350
