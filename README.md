# Streamlit KPI Card

A beautiful, interactive KPI card component for Streamlit with support for time series visualization and delta indicators.

## Features

- **Clean Design**: Modern card layout with shadows and borders
- **Large Value Display**: Prominent display of the main KPI value
- **Delta Indicators**: Show absolute or relative changes with color coding (green for positive, red for negative)
- **Time Series Chart**: Interactive mini chart with hover tooltips using Recharts
- **Flexible Formatting**: Support for numbers, percentages, currency, integers, and decimals
- **Responsive**: Adapts to different screen sizes

## Installation

### Development Setup

1. **Install Python dependencies**:
```bash
pip install -e .
```

2. **Install frontend dependencies**:
```bash
cd streamlit_kpi_card/frontend
npm install
```

3. **Build the frontend**:
```bash
npm run build
```

### For Development with Hot Reload

1. In `streamlit_kpi_card/__init__.py`, set `_RELEASE = False`

2. Start the frontend development server:
```bash
cd streamlit_kpi_card/frontend
npm start
```

3. Run your Streamlit app:
```bash
streamlit run example.py
```

## Usage

```python
import streamlit as st
import pandas as pd
from streamlit_kpi_card import kpi_card

# Create sample time series data
time_series = pd.Series([100, 105, 103, 108, 110, 115, 120])

# Display KPI card with percentage change
kpi_card(
    name='Revenue',
    value=14500.00,
    value_before=12000.00,
    relative_change=True,  # Show percentage change
    time_series=time_series,
    format={"type": "currency", "decimals": 2, "currency": "$"}
)
```

## Parameters

### Required Parameters

- **name** (str): The label/name of the KPI
- **value** (float): The current value
- **value_before** (float): The previous value for comparison

### Optional Parameters

- **relative_change** (bool): If True, show percentage change; if False, show absolute difference. Default: False
- **time_series** (pd.Series): Time series data to display as a chart
- **format** (dict): Format configuration with keys:
  - `type`: Format type - 'number', 'percentage', 'currency', 'integer' (default: 'number')
  - `decimals`: Number of decimal places (default: 1)
  - `currency`: Currency symbol like '$', '€', '£' (default: '$')
- **background_color** (str): Background color of the card. Default: "#ffffff"
- **border** (str): Border style (CSS border property). Default: "1px solid #e5e7eb"
- **shadow** (bool): Whether to show shadow on the card. Default: True
- **border_radius** (str): Border radius for rounded corners. Default: "12px"
- **line_color** (str): Color of the time series line. If None, uses green/red based on delta
- **height** (str): Height of the card (CSS height property)
- **show_average** (bool): Show a dashed horizontal line representing the average value. Default: False
- **info_text** (str): Info text to display on hover over info icon
- **is_inverse** (bool): If True, lower values are better (inverts green/red coloring). Default: False
- **chart_type** (str): Type of chart: 'line', 'bar', or 'area'. Default: 'line'
- **key** (str): Unique key for the component

## Format Configuration

The `format` parameter accepts a dictionary with the following options:

- **'number'**: Standard number formatting with thousand separators (e.g., 1,234.56)
- **'percentage'**: Displays value with % symbol (e.g., 14.5%)
- **'currency'**: Displays value with currency symbol and specified decimal places (e.g., $1,234.56)
- **'integer'**: Rounds to whole number (e.g., 1,234)

**Example:**
```python
format={"type": "currency", "decimals": 2, "currency": "€"}
```

## Examples

See `example.py` for comprehensive examples including:
- Revenue metrics with currency formatting
- Conversion rates with percentage formatting
- User counts with integer formatting
- Different delta display modes (absolute vs relative)
- Positive and negative changes

Run the example:
```bash
streamlit run example.py
```

## Project Structure

```
streamlit-kpi-card/
├── streamlit_kpi_card/
│   ├── __init__.py              # Python component wrapper
│   └── frontend/
│       ├── package.json          # React dependencies
│       ├── tsconfig.json         # TypeScript config
│       ├── public/
│       │   └── index.html
│       └── src/
│           ├── index.tsx         # Streamlit integration
│           └── KpiCard.tsx       # Main React component
├── setup.py                      # Package setup
├── MANIFEST.in                   # Package manifest
├── example.py                    # Demo application
└── README.md
```

## Technologies Used

- **Python**: Streamlit component framework
- **React**: UI component library
- **TypeScript**: Type-safe JavaScript
- **Recharts**: Charting library for time series visualization
- **streamlit-component-lib**: Streamlit's component library

## License

MIT
