# Streamlit KPI Card

KPI card component for Streamlit with time series charts and delta indicators.

![Example KPI Cards](https://raw.githubusercontent.com/pjoachims/streamlit-kpi-card/main/example.png)

## Usage

```python
import streamlit as st
import pandas as pd
from streamlit_kpi_card import kpi_card

# Create sample time series data
time_series = pd.Series([100, 105, 103, 108, 110, 115, 120])

# Minimal usage - format auto-detected from value type
kpi_card(
    name='Active Users',
    value=1250,
    value_before=1100
)

# With currency formatting
kpi_card(
    name='Revenue',
    value=14500.00,
    value_before=12000.00,
    time_series=time_series,
    format="currency"
)

# Custom styling
kpi_card(
    name='Conversion',
    value=3.24,
    value_before=2.87,
    format="percentage",
    shadow_style="glow",
    border_style="left-accent",
    chart_style="gradient-area"
)
```

## Parameters

**Required:**
- `name` - KPI label
- `value` - Current value
- `value_before` - Previous value for delta calculation

**Formatting:**
- `format` - String ('number', 'percentage', 'currency', 'integer') or dict with type/decimals/currency
- `relative_change` - Show percentage vs absolute change (default: False)
- `millify` - Format large numbers as K, M, B (default: False)

**Style Presets:**
- `shadow_style` - 'none', 'subtle', 'sharp', 'glow', 'inset' (default: 'subtle')
- `border_style` - 'none', 'hairline', 'left-accent', 'top-accent', 'full' (default: 'hairline')
- `background_style` - 'solid', 'gradient', 'glass', 'tinted', 'transparent' (default: 'solid')
- `delta_style` - 'pill', 'text', 'badge', 'inline', 'icon' (default: 'pill')
- `chart_style` - 'line', 'gradient-area', 'dots', 'rounded-bar', 'sparkline-dot' (default: 'line')
- `layout` - 'vertical', 'horizontal', 'value-focus', 'chart-focus', 'compact' (default: 'vertical')
- `size` - 'small', 'medium', 'large' (default: 'medium')

**Custom Styling (overrides presets):**
- `background_color` - Custom CSS color (e.g., '#e0f2fe', 'rgba(59, 130, 246, 0.3)')
- `border` - Custom CSS border (e.g., '2px dashed red')
- `accent_color` - Custom accent color for borders and glow
- `line_color` - Chart line color

**Chart Options:**
- `time_series` - pd.Series for chart display
- `show_chart` - Show/hide chart (default: True)
- `show_average` - Show average line on chart (default: False)
- `focus_last_n` - Highlight last N bars in bar charts

**Delta Options:**
- `delta_label` - Label for delta (default: 'vs previous')
- `delta_position` - 'below-value', 'right-of-value', 'below-name'
- `extra_deltas` - List of additional comparisons
- `is_inverse` - Invert colors for "lower is better" metrics

**Other:**
- `info_text` - Hover text for info icon
- `theme` - 'light', 'dark', 'auto' (default: 'auto')
- `height`, `border_radius` - CSS values

## License

MIT
