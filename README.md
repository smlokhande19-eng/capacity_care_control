# System Capacity & Care Load Analytics for Unaccompanied Children

A comprehensive Streamlit dashboard for analyzing system capacity, care load dynamics, and operational performance of the Unaccompanied Children (UAC) care pipeline.

## 🎯 Project Overview

This project provides data-driven insights into:
- **Total System Load**: CBP custody + HHS care populations
- **Flow Dynamics**: Daily intake, transfers, and discharge patterns
- **Capacity Stress**: Identification of high-load periods and strain windows
- **Operational Metrics**: KPIs for decision-making and policy evaluation

## 📊 Key Features

### Dashboard Components
- **KPI Summary Cards**: Real-time metrics on system status
- **System Load Overview**: Stacked area chart of CBP vs HHS care
- **CBP vs HHS Comparison**: Side-by-side load analysis
- **Net Intake & Backlog Trends**: Transfers vs discharges analysis
- **Flow Analysis**: Daily and cumulative intake/discharge patterns
- **Volatility Index**: System stability assessment
- **Stress Period Detection**: Identification of high-load periods

### User Controls
- Date range selector with flexible filtering
- Time granularity options (daily, weekly, monthly)
- Metric toggles for customized dashboard views
- Data explorer with CSV export capability

## 📈 Key Performance Indicators (KPIs)

| KPI | Description |
|-----|-------------|
| **Total Children Under Care** | System-wide responsibility (CBP + HHS) |
| **Net Intake Pressure** | Inflow vs outflow imbalance (7-day avg) |
| **Care Load Volatility Index** | System stability measure (7-day std dev) |
| **Backlog Accumulation Rate** | Sustained care pressure (% change) |
| **Discharge Offset Ratio** | Ability to relieve load (%) |

## 🚀 Quick Start

### Installation

1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 🎨 Visual Dashboard

The app now includes a polished analytics layout with:
- responsive Plotly charts using Streamlit's `width='stretch'`
- a split overview section with system insights and trend summaries
- enhanced KPI cards and attention-grabbing stress alerts
- a clean data explorer for raw export and review

## 📁 Project Structure

```
capacity_care_load/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration & constants
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── src/
│   ├── __init__.py                # Package initialization
│   ├── data_loader.py             # Data loading & validation
│   ├── metrics.py                 # KPI calculations
│   ├── visualizations.py          # Chart & plot functions
│   └── utils.py                   # Utility functions
│
├── data/
│   └── sample_data.csv            # Sample dataset (2023-2025)
│
└── .github/
    └── copilot-instructions.md    # Project documentation
```

## 📊 Dataset Description

The sample dataset includes daily records from 2023-2025 with the following columns:

| Column | Description |
|--------|-------------|
| **Date** | Reporting date |
| **Children Apprehended** | Daily intake into CBP custody |
| **Children in CBP Custody** | Active CBP care load |
| **Children Transferred from CBP** | Flow into HHS system |
| **Children in HHS Care** | Active HHS care load |
| **Children Discharged** | Successful sponsor placements |

### Data Quality
- Complete daily records from 01-01-2023 to 12-31-2025
- Realistic trends with seasonal patterns
- Validated logical constraints (transfers ≤ CBP, discharges ≤ HHS)
- No missing or duplicate dates

## 📈 Metric Calculations

### Total System Load
```
Total = CBP Custody + HHS Care
```

### Net Daily Intake
```
Net Intake = Transfers - Discharges
```

### Care Load Growth Rate
```
Growth Rate (%) = (Current Total - Previous Total) / Previous Total × 100
```

### Backlog Indicator
```
Backlog = Rolling Sum of Net Intake (7-day window)
```

### Care Load Volatility
```
Volatility = Standard Deviation of Total Load (7-day window)
```

### Discharge Offset Ratio
```
Offset Ratio (%) = Discharges / Transfers × 100
```

## 🔍 Usage Examples

### Analyzing Capacity Stress
1. Use the date range selector to focus on specific periods
2. Check the "Stress Period Identification" chart for high-load windows
3. Review the Care Load Volatility Index for stability assessment

### Comparing Intake vs Discharge
1. Toggle the "Flow Analysis" metric
2. Observe cumulative flow patterns
3. Use weekly/monthly granularity for trend analysis

### Tracking System Performance
1. Monitor KPI cards for real-time metrics
2. Adjust date range to track period-specific changes
3. Export data for further analysis using the CSV download

## 🛠️ Technical Stack

- **Framework**: Streamlit 1.40.0
- **Data**: Pandas 2.2.0, NumPy 1.26.4
- **Visualization**: Plotly 5.18.0
- **Python**: 3.9+

## 📚 Data Analysis Features

### Validation & Integrity
- Automatic data quality checks
- Constraint validation (transfers ≤ CBP, discharges ≤ HHS)
- Anomaly flagging and reporting

### Trend Analysis
- Daily, weekly, and monthly aggregation
- Rolling averages (7-day, 14-day)
- Growth rate calculations
- Seasonal pattern identification

### Stress Identification
- Percentile-based thresholds
- Sustained high-load period detection
- Stress level classification (Normal/Moderate/High)

## 📋 Project Completion Checklist

- [x] Project structure created
- [x] All core modules implemented
- [x] Sample data generator included
- [x] Requirements specified
- [x] Dashboard fully functional
- [x] Data validation implemented
- [x] KPI calculations complete
- [x] Interactive visualizations working
- [x] Documentation complete

## 🤝 Contributing

To extend this project:

1. Add new metrics in `src/metrics.py`
2. Create visualizations in `src/visualizations.py`
3. Update KPI definitions in `config.py`
4. Add features to the dashboard in `app.py`

## 📝 Notes

- The sample dataset is procedurally generated with realistic patterns
- All calculations use best-practice statistical methods
- The dashboard is optimized for desktop viewing
- Data is cached for performance optimization

## 🔗 References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [U.S. Department of Health and Human Services](https://www.hhs.gov/)
- [Data Analysis Best Practices](https://pandas.pydata.org/docs/)

## 📧 Support

For questions or issues with this project, refer to the code comments and docstrings for detailed explanations of each module and function.

---

**Project Status**: ✅ Complete and Fully Functional

**Last Updated**: June 2026

**Python Version**: 3.9+
