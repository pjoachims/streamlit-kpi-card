import streamlit as st
import pandas as pd
import numpy as np
from streamlit_kpi_card import kpi_card

st.set_page_config(page_title="KPI Card Examples", layout="wide")

st.title("🎯 KPI Card Component Examples")

# Generate sample time series data
dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
revenue_series = pd.Series(np.random.randn(30).cumsum() * 100 + 100, index=dates)
conversion_series = pd.Series(np.random.randn(30).cumsum() + 15, index=dates)
users_series = pd.Series(np.random.randn(30).cumsum() + 1000, index=dates)

# Create columns for layout
col1, col2, col3, col4, col5 = st.columns([4, 4, 4, 2, 15])


with col1:
    kpi_card(
        name="Positive change -> green change/line",
        value=6000,
        value_before=5000,
        relative_change=False,
        time_series=revenue_series,
        border=True,
        shadow=False,
        background_color="#f8f8f8",
        format="integer",
        info_text="Total revenue for the current month compared to the previous month.",
    )
    kpi_card(
        name="Negative change -> red change/line. Relative change (click on it ;)",
        value=5000,
        value_before=6000,
        relative_change=True,
        time_series=-1*revenue_series,
        border=True,
        shadow=False,
        background_color="#f8f8f8",
        format="integer",
        info_text="Total revenue for the current month compared to the previous month.",
    )

with col2:
    kpi_card(
        name="bar chart and some colors",
        value=1000,
        value_before=900,
        relative_change=False,
        time_series=revenue_series,
        border=True,
        shadow=False,
        background_color="#dbe8ff",
        format="integer",
        info_text="Total revenue for the current month compared to the previous month.",
        chart_type='bar',
        line_color="#0022FF",
    )
    kpi_card(
        name="Show average line, show as currency",
        value=1000,
        value_before=900,
        relative_change=False,
        time_series=revenue_series,
        border=True,
        shadow=False,
        background_color="#f8f8f8",
        format={"type": "currency", "decimals": 0, "currency": "€"},
        info_text="Total revenue for the current month compared to the previous month.",
        chart_type='bar',
        show_average=True,
    )
with col3:
    kpi_card(
        name="show as area, values as percentage",
        value=6000,
        value_before=5000,
        relative_change=False,
        time_series=revenue_series,
        border=True,
        shadow=False,
        background_color="#f8f8f8",
        format="integer",
        info_text="Total revenue for the current month compared to the previous month.",
        chart_type='area',
    )
    kpi_card(
        name="just value and delta",
        value=6000,
        value_before=5000,
        relative_change=False,
        border=True,
        shadow=False,
        background_color="#f8f8f8",
        format="integer",
        info_text="Total revenue for the current month compared to the previous month.",
    )
with col4:
    kpi_card(
        name="Smoll",
        value=6000,
        value_before=5000,
        relative_change=False,
        border=True,
        shadow=False,
        background_color="#f8f8f8",
        format="integer",
        info_text="Total revenue for the current month compared to the previous month.",
    )


st.markdown("""
---

## Usage Example

```python
from streamlit_kpi_card import kpi_card
import pandas as pd

# Create a time series
time_series = pd.Series([10, 12, 11, 15, 14, 16, 18])

# Display KPI card with percentage formatting
kpi_card(
    name='Conversion Rate',
    value=14.5,
    value_before=12.0,
    relative_change=True,
    time_series=time_series,
    format="percentage"
)

# Display KPI card with currency formatting (string, defaults to € with 2 decimals)
kpi_card(
    name='Revenue (EUR)',
    value=14500.00,
    value_before=12000.00,
    format="currency"
)

# Display KPI card with custom currency (dict)
kpi_card(
    name='Revenue (USD)',
    value=14500.00,
    value_before=12000.00,
    format={"type": "currency", "decimals": 2, "currency": "$"}
)
```
""")
