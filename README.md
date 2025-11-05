# Streamlit KPI Card

KPI card component for Streamlit with time series charts and delta indicators.

![Example KPI Cards](example.png)

## Usage

```python
import streamlit as st
import pandas as pd
from streamlit_kpi_card import kpi_card

# Create sample time series data
time_series = pd.Series([100, 105, 103, 108, 110, 115, 120])

# Simple usage with string format (defaults to € with 2 decimals)
kpi_card(
    name='Revenue',
    value=14500.00,
    value_before=12000.00,
    relative_change=True,
    time_series=time_series,
    format="currency"
)

# Advanced usage with dict format for custom currency
kpi_card(
    name='Revenue (USD)',
    value=14500.00,
    value_before=12000.00,
    format={"type": "currency", "decimals": 2, "currency": "$"}
)
```

## Parameters

**Required:**
- `name` - KPI label
- `value` - Current value
- `value_before` - Previous value for delta calculation

**Optional:**
- `relative_change` - Show percentage vs absolute change (default: False)
- `time_series` - pd.Series for chart display
- `format` - String ('number', 'percentage', 'currency', 'integer') or dict with `type`, `decimals`, `currency`. Currency defaults to € with 2 decimals
- `chart_type` - 'line', 'bar', or 'area' (default: 'line')
- `line_color` - Chart line color
- `show_average` - Show average line on chart
- `info_text` - Hover text for info icon
- `is_inverse` - Invert colors for "lower is better" metrics
- `background_color`, `border`, `shadow`, `border_radius`, `height` - Styling options

## License

MIT
