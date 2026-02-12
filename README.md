# Streamlit KPI Card

KPI card component for Streamlit with time series charts and delta indicators.

![Example KPI Cards](https://raw.githubusercontent.com/pjoachims/streamlit-kpi-card/main/example.png)

## Installation

```bash
pip install streamlit-kpi-card
```

## Quick Start

```python
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_kpi_card import kpi_card

# Sample time series
ts = pd.Series(np.cumsum(np.random.randn(20)) + 100)

# Basic usage - format auto-detected
kpi_card(name="Revenue", value=142500, value_before=128000, format="currency", time_series=ts)

# Different chart styles
kpi_card(name="Conversion", value=87.5, value_before=82.3, format="percentage",
         time_series=ts, chart_style={"type": "gradient-area"})

# Horizontal layout
kpi_card(name="Orders", value=1842, value_before=1650, format="integer",
         time_series=ts, layout="horizontal")

# Custom styling
kpi_card(
    name="Glass Card", value=3420, value_before=3100, format="integer", time_series=ts,
    card_style={"borderRadius": "12px", "shadow": "glow", "backgroundStyle": "glass"},
    chart_style={"type": "line", "lineColor": "#8b5cf6"},
    delta_style={"format": "badge"},
)
```

## Parameters

**Required:**
- `name` - KPI label
- `value` - Current value
- `value_before` - Previous value for delta calculation

**Formatting:**
- `format` - `"integer"`, `"number"`, `"percentage"`, `"currency"` or dict `{"type": "currency", "decimals": 2, "currency": "$"}`

**Style Dicts:**
- `card_style` - Card appearance: `shadow`, `border`, `borderRadius`, `padding`, `backgroundStyle`, `accentColor`, `height`
- `chart_style` - Chart options: `type` (line, gradient-area, dots, bar, rounded-bar, sparkline-dot), `lineColor`, `axis`, `gridX`, `gridY`, `referenceLine`, `focusLastN`
- `delta_style` - Delta display: `format` (pill, text, badge, inline, icon), `position`, `stack`, `label`
- `text_style` - Typography: `nameSize`, `valueSize`, `nameWeight`, `valueWeight`, `millify`

**Layout:**
- `layout` - `"vertical"`, `"horizontal"`, `"chart-focus"`, `"compact"`, `"mini"`
- `theme` - `"light"`, `"dark"`, `"auto"`

**Delta Options:**
- `is_inverse` - Invert colors for "lower is better" metrics
- `relative_change` - Show percentage change instead of absolute
- `extra_deltas` - Additional comparisons: `[{"value_before": 1000, "label": "vs target"}]`

**Chart Options:**
- `time_series` - pandas Series for chart display
- `axis` - `"x"`, `"y"`, `"both"` for axis labels

## Multi-Card Grid

```python
from streamlit_kpi_card import kpi_cards

kpi_cards([
    {"name": "Revenue", "value": 142500, "value_before": 128000, "format": "currency", "time_series": ts},
    {"name": "Users", "value": 12450, "value_before": 11200, "format": "integer", "time_series": ts},
    {"name": "Orders", "value": 1842, "value_before": 1650, "format": "integer", "time_series": ts},
], columns=3, chart_style={"type": "gradient-area"})
```

## License

MIT
