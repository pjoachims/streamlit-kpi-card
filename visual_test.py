"""Visual test page — renders KPI cards in every combination for screenshot inspection."""
import streamlit as st
import pandas as pd
import numpy as np
import textwrap
from streamlit_kpi_card import kpi_card, kpi_cards

st.set_page_config(page_title="KPI Card Visual Test", layout="wide")

def format_value(v, ts_names):
    """Format a value for code display."""
    if isinstance(v, str):
        return f'"{v}"'
    elif isinstance(v, bool):
        return str(v)
    elif isinstance(v, dict):
        items = ", ".join(f'"{k}": {format_value(val, ts_names)}' for k, val in v.items())
        return "{" + items + "}"
    elif isinstance(v, list):
        items = ", ".join(format_value(item, ts_names) for item in v)
        return "[" + items + "]"
    elif isinstance(v, pd.Series):
        # Check if it's one of our named time series
        for name, series in ts_names.items():
            if v is series:
                return name
        return "time_series_data"
    elif v is None:
        return "None"
    else:
        return str(v)

def card_with_code(ts_names, **kwargs):
    """Render a kpi_card and show its code in an expander."""
    # Render the card
    result = kpi_card(**kwargs)

    # Build code string
    args = []
    for k, v in kwargs.items():
        formatted = format_value(v, ts_names)
        args.append(f"{k}={formatted}")

    code = f"kpi_card(\n    " + ",\n    ".join(args) + "\n)"

    with st.expander("Show code", expanded=False):
        st.code(code, language="python")

    return result

def cards_with_code(ts_names, cards_data, **kwargs):
    """Render kpi_cards and show its code in an expander."""
    # Render the cards
    result = kpi_cards(cards_data, **kwargs)

    def format_card(card):
        if isinstance(card, list):
            # Nested list (grid mode row)
            items = ",\n            ".join(format_card(c) for c in card)
            return f"[\n            {items}\n        ]"
        else:
            # Single card dict
            card_items = ", ".join(f'"{k}": {format_value(v, ts_names)}' for k, v in card.items())
            return f"{{{card_items}}}"

    # Build cards_data string
    cards_str = "[\n        " + ",\n        ".join(format_card(card) for card in cards_data) + "\n    ]"

    # Build kwargs string
    kwargs_str = ",\n    ".join(f"{k}={format_value(v, ts_names)}" for k, v in kwargs.items())

    code = f"kpi_cards(\n    {cards_str},\n    {kwargs_str}\n)"

    with st.expander("Show code", expanded=False):
        st.code(code, language="python")

    return result
st.markdown("""<style>
    .block-container { padding-top: 1rem; max-width: 100%; }
    h2 { margin-top: 1.5rem !important; margin-bottom: 0.5rem !important; border-bottom: 2px solid #e5e5e5; padding-bottom: 0.3rem; }
    h3 { margin-top: 1rem !important; margin-bottom: 0.3rem !important; }
    /* Force full-height layout so Chrome "Capture full size screenshot" works */
    section.main { overflow: visible !important; height: auto !important; }
    .main .block-container { overflow: visible !important; height: auto !important; max-height: none !important; }
    [data-testid="stAppViewContainer"] { overflow: visible !important; height: auto !important; }
    [data-testid="stVerticalBlock"] { overflow: visible !important; }
</style>""", unsafe_allow_html=True)

# -- Sample data --
np.random.seed(42)
ts_up = pd.Series(np.cumsum(np.random.randn(20)) + 100, index=[f"W{i}" for i in range(1, 21)])
ts_down = pd.Series(np.cumsum(np.random.randn(20) - 0.3) + 50, index=[f"W{i}" for i in range(1, 21)])
ts_flat = pd.Series(np.random.randn(20) * 2 + 100, index=[f"W{i}" for i in range(1, 21)])
ts_short = pd.Series([10, 12, 11, 15, 14])

# Mapping for code display
TS = {"ts_up": ts_up, "ts_down": ts_down, "ts_flat": ts_flat, "ts_short": ts_short}

# ============================================================
st.header("1. Format Types")
# ============================================================
cols = st.columns(5)
with cols[0]:
    card_with_code(TS, name="Auto Integer", value=42000, value_before=38000, time_series=ts_up)
with cols[1]:
    card_with_code(TS, name="Auto Decimal", value=3.14, value_before=2.71, time_series=ts_up)
with cols[2]:
    card_with_code(TS, name="Percentage", value=87.5, value_before=82.3, format="percentage", time_series=ts_up)
with cols[3]:
    card_with_code(TS, name="Currency EUR", value=14500, value_before=12000, format="currency", time_series=ts_up)
with cols[4]:
    card_with_code(TS, name="Currency USD", value=9800, value_before=10200, format={"type": "currency", "currency": "$", "decimals": 0}, time_series=ts_down)

# ============================================================
st.header("2. Delta Styles")
# ============================================================
cols = st.columns(5)
delta_formats = ["pill", "text", "badge", "inline", "icon"]
for i, ds in enumerate(delta_formats):
    with cols[i]:
        card_with_code(TS, name=f"Delta: {ds}", value=1250, value_before=1100,
                 delta_style={"format": ds}, time_series=ts_up, format="integer")

# ============================================================
st.header("3. Chart Styles")
# ============================================================
cols = st.columns(6)
chart_types = ["line", "gradient-area", "dots", "bar", "rounded-bar", "sparkline-dot"]
for i, ct in enumerate(chart_types):
    with cols[i]:
        card_with_code(TS, name=ct, value=150, value_before=130,
                 chart_style={"type": ct}, time_series=ts_up, format="integer")

# ============================================================
st.header("4. Layouts")
# ============================================================

st.subheader("4a. Vertical (default)")
cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Revenue", value=142500, value_before=128000, layout="vertical", format="currency", time_series=ts_up)
with cols[1]:
    card_with_code(TS, name="Users", value=12450, value_before=11200, layout="vertical", format="integer", time_series=ts_up, relative_change=True)
with cols[2]:
    card_with_code(TS, name="Churn", value=4.2, value_before=5.1, layout="vertical", format="percentage", time_series=ts_down, is_inverse=True)

st.subheader("4b. Horizontal")
cols = st.columns(2)
with cols[0]:
    card_with_code(TS, name="Revenue", value=142500, value_before=128000, layout="horizontal", format="currency", time_series=ts_up)
with cols[1]:
    card_with_code(TS, name="Orders", value=3420, value_before=3100, layout="horizontal", format="integer", time_series=ts_up)

st.subheader("4c. Value Focus")
cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="ARR", value=2400000, value_before=1900000, layout="value-focus", format="currency", time_series=ts_up,
             text_style={"millify": True})
with cols[1]:
    card_with_code(TS, name="NPS", value=72, value_before=68, layout="value-focus", format="integer", time_series=ts_up)
with cols[2]:
    card_with_code(TS, name="CSAT", value=94.5, value_before=91.2, layout="value-focus", format="percentage", time_series=ts_up)

st.subheader("4d. Chart Focus")
cols = st.columns(2)
with cols[0]:
    card_with_code(TS, name="Stock Price", value=182.50, value_before=175.30, layout="chart-focus",
             chart_style={"type": "gradient-area"},
             format={"type": "currency", "currency": "$", "decimals": 2}, time_series=ts_up)
with cols[1]:
    card_with_code(TS, name="CPU Usage", value=67.3, value_before=72.1, layout="chart-focus",
             chart_style={"type": "line"},
             format="percentage", time_series=ts_down, is_inverse=True)

st.subheader("4d-ii. Chart Focus with Axes & Reference Lines")
budget_cf = (ts_up.values * 0.97 + np.random.randn(len(ts_up)) * 0.5).tolist()
cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Both Axes + Grid", value=142500, value_before=128000, layout="chart-focus",
             chart_style={"type": "gradient-area", "axis": "both", "gridX": True, "gridY": True},
             card_style={"overlayPosition": "top-left", "overlayOpacity": 0.7, "height": "250px"},
             format="currency", time_series=ts_up)
with cols[1]:
    card_with_code(TS, name="X Axis Only", value=67.3, value_before=72.1, layout="chart-focus",
             chart_style={"type": "gradient-area", "axis": "x"},
             card_style={"overlayPosition": "top-left", "overlayOpacity": 0.7, "height": "250px"},
             format="percentage", time_series=ts_down, is_inverse=True)
with cols[2]:
    card_with_code(TS, name="Y Labels Only", value=12450, value_before=11200, layout="chart-focus",
             chart_style={"type": "gradient-area", "axis": "y"},
             card_style={"overlayPosition": "top-left", "overlayOpacity": 0.7, "height": "250px"},
             format="integer", time_series=ts_up)

cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Grid Only", value=3420, value_before=3100, layout="chart-focus",
             chart_style={"type": "line", "gridX": True, "gridY": True},
             card_style={"overlayPosition": "top-right", "overlayOpacity": 0.7, "height": "250px"},
             format="integer", time_series=ts_flat)
with cols[1]:
    card_with_code(TS, name="Flat Ref Line", value=67.3, value_before=72.1, layout="chart-focus",
             chart_style={"type": "gradient-area", "referenceLine": {"value": 45, "label": "Target", "color": "#f59e0b"}},
             card_style={"overlayPosition": "top-left", "overlayOpacity": 0.7, "height": "250px"},
             format="percentage", time_series=ts_down, is_inverse=True)
with cols[2]:
    card_with_code(TS, name="Flex Ref Line", value=150, value_before=130, layout="chart-focus",
             chart_style={"type": "gradient-area", "referenceLine": {"values": budget_cf, "label": "Budget", "color": "#8b5cf6"}},
             card_style={"overlayPosition": "top-left", "overlayOpacity": 0.7, "height": "250px"},
             format="integer", time_series=ts_up)

st.subheader("4e. Compact")
cols = st.columns(4)
for i, (n, v, vb) in enumerate([("Rev", 14500, 13000), ("Users", 8200, 7800), ("Orders", 520, 490), ("ARPU", 42.5, 40.1)]):
    with cols[i]:
        card_with_code(TS, name=n, value=v, value_before=vb, layout="compact", time_series=ts_short,
                 format="integer" if isinstance(v, int) else "number")

st.subheader("4f. Mini")
cards_with_code(TS, [
    {"name": "Revenue", "value": 142500, "value_before": 128000, "format": "currency", "time_series": ts_up},
    {"name": "Users", "value": 12450, "value_before": 11200, "format": "integer", "time_series": ts_up},
    {"name": "Orders", "value": 3420, "value_before": 3100, "format": "integer", "time_series": ts_flat},
    {"name": "Churn Rate", "value": 4.2, "value_before": 5.1, "format": "percentage", "is_inverse": True, "time_series": ts_down},
    {"name": "ARPU", "value": 42.50, "value_before": 40.10, "format": {"type": "currency", "decimals": 2}, "time_series": ts_up},
], columns=1, layout="mini")

# ============================================================
st.header("5. Shadow Styles")
# ============================================================
cols = st.columns(5)
for i, ss in enumerate(["none", "subtle", "sharp", "glow", "inset"]):
    with cols[i]:
        card_with_code(TS, name=f"Shadow: {ss}", value=100, value_before=90,
                 card_style={"shadow": ss},
                 format="integer", time_series=ts_short)

# ============================================================
st.header("6. Border Styles")
# ============================================================
cols = st.columns(5)
for i, bs in enumerate(["none", "hairline", "left-accent", "top-accent", "full"]):
    with cols[i]:
        card_with_code(TS, name=f"Border: {bs}", value=100, value_before=90,
                 card_style={"border": bs},
                 format="integer", time_series=ts_short)

# ============================================================
st.header("7. Background Styles")
# ============================================================
cols = st.columns(5)
for i, bg in enumerate(["solid", "gradient", "glass", "tinted", "transparent"]):
    with cols[i]:
        card_with_code(TS, name=f"BG: {bg}", value=100, value_before=90,
                 card_style={"backgroundStyle": bg},
                 format="integer", time_series=ts_short)

# ============================================================
st.header("8. Sizes")
# ============================================================
cols = st.columns(3)
for i, sz in enumerate(["small", "medium", "large"]):
    with cols[i]:
        card_with_code(TS, name=f"Size: {sz}", value=14500, value_before=12000, size=sz, format="currency", time_series=ts_up)

# ============================================================
st.header("9. Millify + Axes + Features")
# ============================================================
cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Millify On", value=2345678, value_before=1987654,
             text_style={"millify": True, "millifyDecimals": 1},
             format="integer", time_series=ts_up * 100)
with cols[1]:
    card_with_code(TS, name="With Axes", value=150, value_before=130,
             chart_style={"axis": "both", "gridX": True, "gridY": True},
             format="integer", time_series=ts_up)
with cols[2]:
    card_with_code(TS, name="Y Labels", value=150, value_before=130,
             chart_style={"axis": "y", "xLabels": [[0, "W1"], [10, "W11"], [19, "W20"]]},
             format="integer", time_series=ts_up)

# ============================================================
st.header("10. Delta Positions + Stacking")
# ============================================================
cols = st.columns(2)
positions = ["below-value", "right-of-value"]
for i, dp in enumerate(positions):
    with cols[i]:
        card_with_code(TS,
            name=f"Pos: {dp}", value=1500, value_before=1200,
            delta_style={"position": dp}, format="integer", time_series=ts_short,
            extra_deltas=[{"value_before": 1000, "label": "vs target"}],
        )

cols = st.columns(2)
with cols[0]:
    card_with_code(TS, name="Stack: horizontal", value=1500, value_before=1200,
             delta_style={"stack": "horizontal"}, format="integer",
             extra_deltas=[{"value_before": 1000, "label": "vs target"}, {"value_before": 1100, "label": "vs budget"}])
with cols[1]:
    card_with_code(TS, name="Stack: vertical", value=1500, value_before=1200,
             delta_style={"stack": "vertical"}, format="integer",
             extra_deltas=[{"value_before": 1000, "label": "vs target"}, {"value_before": 1100, "label": "vs budget"}])

# ============================================================
st.header("11. Accent Colors + Inverse")
# ============================================================
cols = st.columns(4)
with cols[0]:
    card_with_code(TS, name="Accent Blue", value=100, value_before=90,
             card_style={"accentColor": "#3b82f6", "border": "left-accent", "shadow": "glow"},
             format="integer", time_series=ts_short)
with cols[1]:
    card_with_code(TS, name="Accent Purple", value=100, value_before=90,
             card_style={"accentColor": "#8b5cf6", "border": "top-accent", "shadow": "glow"},
             format="integer", time_series=ts_short)
with cols[2]:
    card_with_code(TS, name="Inverse (lower=good)", value=4.2, value_before=5.1, is_inverse=True, format="percentage", time_series=ts_down)
with cols[3]:
    card_with_code(TS, name="Inverse (higher=bad)", value=5.1, value_before=4.2, is_inverse=True, format="percentage", time_series=ts_up)

# ============================================================
st.header("12. kpi_cards() Grid Mode")
# ============================================================
cards_with_code(TS, [
    [{"name": "Revenue", "value": 142500, "value_before": 128000, "format": "currency", "time_series": ts_up}],
    [
        {"name": "Users", "value": 12450, "value_before": 11200, "format": "integer", "time_series": ts_up},
        {"name": "Orders", "value": 3420, "value_before": 3100, "format": "integer", "time_series": ts_flat},
    ],
    [
        {"name": "ARPU", "value": 42.5, "value_before": 40.1, "time_series": ts_short},
        {"name": "Churn", "value": 4.2, "value_before": 5.1, "format": "percentage", "is_inverse": True, "time_series": ts_down},
        {"name": "NPS", "value": 72, "value_before": 68, "format": "integer", "time_series": ts_up},
    ],
], card_style={"shadow": "subtle"}, chart_style={"type": "gradient-area"})

# ============================================================
st.header("13. kpi_cards() Flat with Overrides")
# ============================================================
cards_with_code(TS, [
    {"name": "Default Style", "value": 100, "value_before": 90, "format": "integer", "time_series": ts_short},
    {"name": "Custom Border", "value": 200, "value_before": 180, "format": "integer", "time_series": ts_short,
     "card_style": {"border": "left-accent", "accentColor": "#f59e0b"}},
    {"name": "Custom Chart", "value": 300, "value_before": 250, "format": "integer", "time_series": ts_short,
     "chart_style": {"type": "sparkline-dot"}},
    {"name": "No Chart", "value": 400, "value_before": 350, "format": "integer",
     "chart_style": {"show": False}},
], columns=4, card_style={"shadow": "subtle"})

# ============================================================
st.header("14. Reference Line + Average + Bar Focus")
# ============================================================
cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="With Average", value=150, value_before=130,
             chart_style={"type": "line", "showAverage": True},
             format="integer", time_series=ts_up)
with cols[1]:
    card_with_code(TS, name="Reference Line", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "referenceLine": {"value": 140, "label": "Target", "color": "#f59e0b"}})
with cols[2]:
    card_with_code(TS, name="Bar Focus Last 5", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "rounded-bar", "focusLastN": 5})

# ============================================================
st.header("15. Edge Cases")
# ============================================================
cols = st.columns(4)
with cols[0]:
    card_with_code(TS, name="Zero Before", value=50, value_before=0, format="integer")
with cols[1]:
    card_with_code(TS, name="Same Value", value=100, value_before=100, format="integer", time_series=ts_flat)
with cols[2]:
    card_with_code(TS, name="Big Drop", value=10, value_before=1000, format="integer", time_series=ts_down, relative_change=True)
with cols[3]:
    card_with_code(TS, name="No Chart", value=42, value_before=38, format="integer", chart_style={"show": False})

# ============================================================
st.header("16. Chart Fill (edge-to-edge)")
# ============================================================
cols = st.columns(2)
with cols[0]:
    card_with_code(TS, name="Normal Chart", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area"})
with cols[1]:
    card_with_code(TS, name="Chart Fill", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "fill": True})

# ============================================================
st.header("17. Row Expand in Grid (detail synced per row)")
# ============================================================
cards_with_code(TS, [
    [
        {"name": "Suspicious", "value": 17.5, "value_before": 17.6, "format": "percentage", "time_series": ts_up,
         "chart_style": {"type": "gradient-area", "showAverage": True}, "is_inverse": True},
        {"name": "No WHS", "value": 43.6, "value_before": 37.2, "format": "percentage", "time_series": ts_down,
         "chart_style": {"type": "gradient-area", "showAverage": True}, "is_inverse": True},
    ],
    [
        {"name": "Revenue", "value": 142500, "value_before": 128000, "format": "currency", "time_series": ts_up,
         "chart_style": {"type": "line"}},
        {"name": "Orders", "value": 3420, "value_before": 3100, "format": "integer", "time_series": ts_flat,
         "chart_style": {"type": "rounded-bar"}},
        {"name": "ARPU", "value": 42.5, "value_before": 40.1, "time_series": ts_short,
         "chart_style": {"type": "sparkline-dot"}},
    ],
], show_detail_button=True, card_style={"shadow": "subtle"})

# ============================================================
st.header("18. Chart Focus Overlay Positions + Opacity")
# ============================================================
cols = st.columns(4)
with cols[0]:
    card_with_code(TS, name="Bottom Left", value=182.50, value_before=175.30, layout="chart-focus",
             chart_style={"type": "gradient-area"},
             card_style={"overlayPosition": "bottom-left"},
             format={"type": "currency", "currency": "$", "decimals": 2}, time_series=ts_up)
with cols[1]:
    card_with_code(TS, name="Top Left", value=67.3, value_before=72.1, layout="chart-focus",
             chart_style={"type": "gradient-area"},
             card_style={"overlayPosition": "top-left"},
             format="percentage", time_series=ts_down, is_inverse=True)
with cols[2]:
    card_with_code(TS, name="Top Right", value=12450, value_before=11200, layout="chart-focus",
             chart_style={"type": "line"},
             card_style={"overlayPosition": "top-right"},
             format="integer", time_series=ts_up)
with cols[3]:
    card_with_code(TS, name="Bottom Right", value=94.5, value_before=91.2, layout="chart-focus",
             chart_style={"type": "gradient-area"},
             card_style={"overlayPosition": "bottom-right", "overlayOpacity": 0.5},
             format="percentage", time_series=ts_up)

# ============================================================
st.header("19. Flexible Reference Line (array)")
# ============================================================
budget = (ts_up.values * 0.95 + np.random.randn(len(ts_up)) * 0.5).tolist()
cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Actuals vs Budget", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "line", "referenceLine": {"values": budget, "label": "Budget", "color": "#f59e0b"}})
with cols[1]:
    card_with_code(TS, name="Area + Ref Line", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "referenceLine": {"values": budget, "label": "Target", "color": "#8b5cf6", "style": "solid"}})
with cols[2]:
    card_with_code(TS, name="Bars + Ref Line", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "rounded-bar", "referenceLine": {"values": budget, "label": "Plan", "color": "#ef4444"}})

# ============================================================
st.header("20. Grid X / Grid Y")
# ============================================================
cols = st.columns(4)
with cols[0]:
    card_with_code(TS, name="grid_y=True", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "gridY": True}, card_style={"height": "180px"})
with cols[1]:
    card_with_code(TS, name="grid_x=True", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "gridX": True}, card_style={"height": "180px"})
with cols[2]:
    card_with_code(TS, name="Both Auto", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "gridX": True, "gridY": True, "axis": "both"}, card_style={"height": "180px"})
with cols[3]:
    card_with_code(TS, name="Explicit Positions", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "gridY": [105, 110, 115], "gridX": [0, 5, 10, 15, 19]}, card_style={"height": "180px"})

# ============================================================
st.header("21. Axis X HTML Labels")
# ============================================================
cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="axis=x (auto labels)", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "axis": "x"})
with cols[1]:
    card_with_code(TS, name="axis=x + grid_y", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "line", "axis": "x", "gridY": True})
with cols[2]:
    card_with_code(TS, name="axis=x chart-focus", value=182.50, value_before=175.30, layout="chart-focus",
             chart_style={"type": "gradient-area", "axis": "x"},
             card_style={"overlayPosition": "top-left", "overlayOpacity": 0.7, "height": "250px"},
             format={"type": "currency", "currency": "$", "decimals": 2}, time_series=ts_up)

# ============================================================
st.header("22. Weekday Comparison (grid_x + markers + x_labels)")
# ============================================================
weekday_idx = list(range(0, 20, 7))
wk_labels = [[i, f"W{i+1}"] for i in weekday_idx]
budget_wk = (ts_up.values * 0.97 + np.random.randn(len(ts_up)) * 0.5).tolist()

cols = st.columns(2)
with cols[0]:
    card_with_code(TS, name="Weekday vlines + markers", value=150, value_before=130, format="integer",
             time_series=ts_up,
             chart_style={"type": "gradient-area", "axis": "y", "gridX": weekday_idx, "markers": weekday_idx,
                          "xLabels": wk_labels, "referenceLine": {"values": budget_wk, "label": "prev", "color": "#9ca3af"}},
             card_style={"height": "200px"})
with cols[1]:
    card_with_code(TS, name="Chart-focus weekday", value=150, value_before=130, format="integer",
             time_series=ts_up, layout="chart-focus",
             chart_style={"type": "gradient-area", "axis": "y", "gridX": weekday_idx, "markers": weekday_idx,
                          "xLabels": wk_labels, "referenceLine": {"values": budget_wk, "label": "prev", "color": "#9ca3af"}},
             card_style={"overlayPosition": "top-left", "overlayOpacity": 0.7, "height": "250px"})

# ============================================================
st.header("23. PADDING Examples")
# ============================================================
st.markdown("Different padding values using `card_style={'padding': '...'}`")

cols = st.columns(4)
with cols[0]:
    card_with_code(TS, name="Tight (4px)", value=100, value_before=90, format="integer", time_series=ts_short,
             card_style={"padding": "4px"})
with cols[1]:
    card_with_code(TS, name="Default (16px)", value=100, value_before=90, format="integer", time_series=ts_short,
             card_style={"padding": "16px"})
with cols[2]:
    card_with_code(TS, name="Spacious (24px)", value=100, value_before=90, format="integer", time_series=ts_short,
             card_style={"padding": "24px"})
with cols[3]:
    card_with_code(TS, name="Asymmetric", value=100, value_before=90, format="integer", time_series=ts_short,
             card_style={"padding": "8px 24px"})

cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Pad: 4px 16px 4px 16px", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area"},
             card_style={"padding": "4px 16px 4px 16px", "border": "left-accent", "accentColor": "#3b82f6"})
with cols[1]:
    card_with_code(TS, name="Pad: 32px", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area"},
             card_style={"padding": "32px", "border": "hairline"})
with cols[2]:
    card_with_code(TS, name="Pad: 12px 8px", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "line"},
             card_style={"padding": "12px 8px", "shadow": "subtle"})

# ============================================================
st.header("24. HEIGHT Examples")
# ============================================================
st.markdown("Fixed heights using `card_style={'height': '...'}`")

cols = st.columns(4)
with cols[0]:
    card_with_code(TS, name="Height: 100px", value=100, value_before=90, format="integer", time_series=ts_short,
             card_style={"height": "100px"})
with cols[1]:
    card_with_code(TS, name="Height: 150px", value=100, value_before=90, format="integer", time_series=ts_short,
             card_style={"height": "150px"})
with cols[2]:
    card_with_code(TS, name="Height: 200px", value=100, value_before=90, format="integer", time_series=ts_short,
             card_style={"height": "200px"}, chart_style={"type": "gradient-area"})
with cols[3]:
    card_with_code(TS, name="Height: 250px", value=100, value_before=90, format="integer", time_series=ts_short,
             card_style={"height": "250px"}, chart_style={"type": "gradient-area"})

cols = st.columns(2)
with cols[0]:
    card_with_code(TS, name="Tall Chart Focus (300px)", value=182.50, value_before=175.30, layout="chart-focus",
             chart_style={"type": "gradient-area", "axis": "both", "gridX": True, "gridY": True},
             card_style={"height": "300px", "overlayPosition": "top-left"},
             format={"type": "currency", "currency": "$", "decimals": 2}, time_series=ts_up)
with cols[1]:
    card_with_code(TS, name="Short Chart Focus (120px)", value=67.3, value_before=72.1, layout="chart-focus",
             chart_style={"type": "line"},
             card_style={"height": "120px", "overlayPosition": "bottom-left"},
             format="percentage", time_series=ts_down)

# ============================================================
st.header("25. BORDER RADIUS Examples")
# ============================================================
cols = st.columns(5)
for i, br in enumerate(["0px", "4px", "12px", "24px", "50px"]):
    with cols[i]:
        card_with_code(TS, name=f"Radius: {br}", value=100, value_before=90, format="integer", time_series=ts_short,
                 card_style={"borderRadius": br, "border": "hairline"})

# ============================================================
st.header("26. TEXT STYLING")
# ============================================================
st.markdown("Custom text sizes, colors, weights, and spacing using `text_style`")

cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Small Text", value=14500, value_before=12000, format="currency", time_series=ts_up,
             text_style={"nameSize": "9px", "valueSize": "20px"})
with cols[1]:
    card_with_code(TS, name="Large Text", value=14500, value_before=12000, format="currency", time_series=ts_up,
             text_style={"nameSize": "14px", "valueSize": "40px"})
with cols[2]:
    card_with_code(TS, name="Custom Colors", value=14500, value_before=12000, format="currency", time_series=ts_up,
             text_style={"nameColor": "#8b5cf6", "valueColor": "#3b82f6"})

cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Bold Name", value=14500, value_before=12000, format="currency", time_series=ts_up,
             text_style={"nameWeight": 700, "valueWeight": 400})
with cols[1]:
    card_with_code(TS, name="lowercase title", value=14500, value_before=12000, format="currency", time_series=ts_up,
             text_style={"nameTransform": "none", "nameLetterSpacing": "0"})
with cols[2]:
    card_with_code(TS, name="Tight Name", value=14500, value_before=12000, format="currency", time_series=ts_up,
             text_style={"nameMarginBottom": "2px"})

# ============================================================
st.header("27. CHART STYLING")
# ============================================================
st.markdown("Chart height, margins, colors using `chart_style`")

cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Custom Line Color", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "line", "lineColor": "#8b5cf6"})
with cols[1]:
    card_with_code(TS, name="Chart Height 100px", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "height": "100px"})
with cols[2]:
    card_with_code(TS, name="Y Start at Zero", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "gradient-area", "yStartAtZero": True})

# ============================================================
st.header("28. DELTA STYLING")
# ============================================================
st.markdown("Custom delta colors, sizes, padding, and labels using `delta_style`")

cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Custom Label", value=1500, value_before=1200, format="integer", time_series=ts_short,
             delta_style={"label": "vs last month"})
with cols[1]:
    card_with_code(TS, name="Custom + Colors", value=1500, value_before=1200, format="integer", time_series=ts_short,
             delta_style={"label": "MoM", "positiveColor": "#06b6d4", "negativeColor": "#f97316"})
with cols[2]:
    card_with_code(TS, name="Badge + Label", value=1500, value_before=1200, format="integer", time_series=ts_short,
             delta_style={"format": "badge", "label": "vs target"})

cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="Large Delta", value=1500, value_before=1200, format="integer", time_series=ts_short,
             delta_style={"fontSize": "16px", "arrowSize": 16, "labelSize": "14px"})
with cols[1]:
    card_with_code(TS, name="Small Delta", value=1500, value_before=1200, format="integer", time_series=ts_short,
             delta_style={"fontSize": "10px", "arrowSize": 10, "labelSize": "9px"})
with cols[2]:
    card_with_code(TS, name="Custom Pill", value=1500, value_before=1200, format="integer", time_series=ts_short,
             delta_style={"padding": "6px 12px", "borderRadius": "16px", "gap": "8px"})

# ============================================================
st.header("29. INFO TEXT (Hover)")
# ============================================================
cols = st.columns(3)
with cols[0]:
    card_with_code(TS, name="With Info", value=14500, value_before=12000, format="currency", time_series=ts_up,
             text_style={"infoText": "Revenue includes all product lines excluding returns."})
with cols[1]:
    card_with_code(TS, name="Long Info", value=12450, value_before=11200, format="integer", time_series=ts_up,
             text_style={"infoText": "Monthly active users calculated as unique visitors with at least one session in the past 30 days."})
with cols[2]:
    card_with_code(TS, name="Short Info", value=87.5, value_before=82.3, format="percentage", time_series=ts_up,
             text_style={"infoText": "NPS score"})

# ============================================================
st.header("30. COMBINED STYLE SHOWCASE")
# ============================================================
st.markdown("Combining multiple style options for maximum customization")

cols = st.columns(2)
with cols[0]:
    card_with_code(TS,
        name="Executive Dashboard Card", value=2456789, value_before=1987654, format="currency", time_series=ts_up,
        card_style={
            "padding": "20px",
            "height": "220px",
            "borderRadius": "16px",
            "border": "left-accent",
            "accentColor": "#3b82f6",
            "shadow": "subtle",
            "backgroundStyle": "gradient",
        },
        chart_style={
            "type": "gradient-area",
            "axis": "y",
            "gridY": True,
            "showAverage": True,
        },
        text_style={
            "millify": True,
            "millifyDecimals": 2,
            "infoText": "Total revenue across all regions including recurring and one-time sales.",
        },
        delta_style={
            "format": "pill",
            "label": "vs last quarter",
        },
    )
with cols[1]:
    card_with_code(TS,
        name="Compact Metric", value=94.7, value_before=91.2, format="percentage", time_series=ts_up,
        card_style={
            "padding": "12px",
            "height": "220px",
            "borderRadius": "8px",
            "border": "hairline",
            "shadow": "none",
            "backgroundStyle": "tinted",
        },
        chart_style={
            "type": "sparkline-dot",
            "lineColor": "#10b981",
        },
        delta_style={
            "format": "text",
            "label": "improvement",
        },
    )

cols = st.columns(3)
with cols[0]:
    card_with_code(TS,
        name="Glass Card", value=3420, value_before=3100, format="integer", time_series=ts_up,
        card_style={
            "padding": "16px 20px",
            "borderRadius": "12px",
            "border": "none",
            "shadow": "glow",
            "accentColor": "#8b5cf6",
            "backgroundStyle": "glass",
        },
        chart_style={"type": "line", "lineColor": "#8b5cf6"},
        delta_style={"format": "badge"},
    )
with cols[1]:
    card_with_code(TS,
        name="Inset Shadow", value=67.3, value_before=72.1, format="percentage", time_series=ts_down, is_inverse=True,
        card_style={
            "padding": "16px",
            "borderRadius": "8px",
            "border": "hairline",
            "shadow": "inset",
            "backgroundStyle": "solid",
        },
        chart_style={"type": "dots"},
        delta_style={"format": "icon"},
    )
with cols[2]:
    card_with_code(TS,
        name="Sharp Modern", value=520, value_before=490, format="integer", time_series=ts_short,
        card_style={
            "padding": "20px",
            "borderRadius": "0px",
            "border": "top-accent",
            "accentColor": "#f59e0b",
            "shadow": "sharp",
            "backgroundStyle": "solid",
        },
        chart_style={"type": "rounded-bar", "focusLastN": 3},
        delta_style={"format": "inline"},
    )

# Row 3: More creative combinations
st.subheader("Dark Theme Showcase")
cols = st.columns(3)
with cols[0]:
    card_with_code(TS,
        name="Neon Glow", value=1847, value_before=1520, format="integer", time_series=ts_up,
        card_style={
            "padding": "18px",
            "borderRadius": "12px",
            "border": "full",
            "accentColor": "#06b6d4",
            "shadow": "glow",
            "backgroundStyle": "solid",
        },
        chart_style={"type": "gradient-area", "lineColor": "#06b6d4"},
        text_style={"nameColor": "#06b6d4", "nameWeight": 600},
        delta_style={"format": "badge", "label": ""},
        theme="dark",
    )
with cols[1]:
    card_with_code(TS,
        name="Minimalist Dark", value=89.2, value_before=85.0, format="percentage", time_series=ts_up,
        card_style={
            "padding": "24px",
            "borderRadius": "4px",
            "border": "none",
            "shadow": "none",
            "backgroundStyle": "solid",
        },
        chart_style={"type": "line", "lineColor": "#a3a3a3"},
        text_style={"valueSize": "42px", "valueWeight": 300, "nameTransform": "none", "nameLetterSpacing": "0"},
        delta_style={"format": "text", "label": ""},
        theme="dark",
    )
with cols[2]:
    card_with_code(TS,
        name="Accent Strip", value=42500, value_before=38000, format="currency", time_series=ts_up,
        card_style={
            "padding": "16px 20px",
            "borderRadius": "8px",
            "border": "left-accent",
            "accentColor": "#f43f5e",
            "shadow": "subtle",
            "backgroundStyle": "gradient",
        },
        chart_style={"type": "sparkline-dot", "lineColor": "#f43f5e"},
        text_style={"millify": True},
        delta_style={"format": "pill", "label": "MoM"},
        theme="dark",
    )

# Row 4: Typography focused
st.subheader("Typography Variations")
cols = st.columns(4)
with cols[0]:
    card_with_code(TS,
        name="Large Title", value=156, value_before=142, format="integer", time_series=ts_short,
        card_style={"padding": "16px", "border": "hairline", "shadow": "subtle"},
        text_style={"nameSize": "16px", "nameWeight": 700, "nameTransform": "capitalize", "nameLetterSpacing": "0", "valueSize": "28px"},
        delta_style={"format": "text", "fontSize": "14px", "label": ""},
    )
with cols[1]:
    card_with_code(TS,
        name="tiny label", value=2.4, value_before=2.1, format={"type": "number", "decimals": 1}, time_series=ts_short,
        card_style={"padding": "16px", "border": "hairline", "shadow": "subtle"},
        text_style={"nameSize": "9px", "nameTransform": "lowercase", "valueSize": "36px", "valueWeight": 800},
        delta_style={"format": "pill", "fontSize": "10px", "arrowSize": 8, "label": ""},
    )
with cols[2]:
    card_with_code(TS,
        name="BOLD CAPS", value=789, value_before=654, format="integer", time_series=ts_short,
        card_style={"padding": "16px", "border": "top-accent", "accentColor": "#000", "shadow": "sharp"},
        text_style={"nameSize": "14px", "nameWeight": 900, "nameColor": "#000", "valueWeight": 400, "valueColor": "#525252"},
        delta_style={"format": "badge"},
    )
with cols[3]:
    card_with_code(TS,
        name="Elegant Serif", value=12750, value_before=11200, format="currency", time_series=ts_short,
        card_style={"padding": "20px", "borderRadius": "0", "border": "hairline", "shadow": "none"},
        text_style={"nameTransform": "none", "nameLetterSpacing": "0.1em", "nameWeight": 400, "millify": True},
        delta_style={"format": "text", "label": "growth"},
    )

# Row 5: Chart-focus variations
st.subheader("Chart-Focus Combinations")
cols = st.columns(2)
with cols[0]:
    card_with_code(TS,
        name="Sales Trend", value=847200, value_before=792000, format="currency", time_series=ts_up,
        layout="chart-focus",
        card_style={
            "height": "200px",
            "borderRadius": "16px",
            "border": "none",
            "shadow": "subtle",
            "backgroundStyle": "glass",
            "overlayPosition": "top-left",
            "overlayOpacity": 0.9,
        },
        chart_style={"type": "gradient-area", "axis": "both", "lineColor": "#10b981"},
        text_style={"millify": True},
        delta_style={"label": "vs target"},
    )
with cols[1]:
    card_with_code(TS,
        name="Performance Score", value=94.7, value_before=91.2, format="percentage", time_series=ts_up,
        layout="chart-focus",
        card_style={
            "height": "200px",
            "borderRadius": "0",
            "border": "left-accent",
            "accentColor": "#6366f1",
            "shadow": "sharp",
            "overlayPosition": "bottom-right",
        },
        chart_style={"type": "line", "axis": "x", "lineColor": "#6366f1", "gridX": [5, 10, 15]},
        delta_style={"label": "improvement"},
    )

# Row 6: Delta styling showcase
st.subheader("Delta Style Combinations")
cols = st.columns(4)
with cols[0]:
    card_with_code(TS,
        name="Large Pill", value=1250, value_before=1100, format="integer", time_series=ts_short,
        card_style={"padding": "16px", "border": "hairline"},
        delta_style={"format": "pill", "fontSize": "14px", "arrowSize": 14, "padding": "6px 14px", "borderRadius": "20px", "label": ""},
    )
with cols[1]:
    card_with_code(TS,
        name="Compact Badge", value=78, value_before=72, format="integer", time_series=ts_short,
        card_style={"padding": "16px", "border": "hairline"},
        delta_style={"format": "badge", "fontSize": "10px", "arrowSize": 8, "padding": "2px 6px", "label": ""},
    )
with cols[2]:
    card_with_code(TS,
        name="Wide Gap", value=340, value_before=310, format="integer", time_series=ts_short,
        card_style={"padding": "16px", "border": "hairline"},
        delta_style={"format": "pill", "gap": "12px", "labelSize": "12px", "label": "since Monday"},
    )
with cols[3]:
    card_with_code(TS,
        name="Stacked", value=520, value_before=480, format="integer", time_series=ts_short,
        card_style={"padding": "16px", "border": "hairline"},
        delta_style={"format": "icon", "fontSize": "16px", "arrowSize": 20},
        extra_deltas=[{"delta": 15, "deltaPercent": 3.2, "label": "WoW"}],
    )

# Row 7: Horizontal layout combinations
st.subheader("Horizontal Variations")
cols = st.columns(2)
with cols[0]:
    card_with_code(TS,
        name="Revenue Stream", value=156000, value_before=142000, format="currency", time_series=ts_up,
        layout="horizontal",
        card_style={
            "padding": "20px 24px",
            "borderRadius": "12px",
            "border": "none",
            "shadow": "subtle",
            "backgroundStyle": "gradient",
        },
        chart_style={"type": "gradient-area", "lineColor": "#22c55e"},
        text_style={"millify": True, "valueSize": "28px"},
        delta_style={"format": "pill", "label": "quarterly"},
    )
with cols[1]:
    card_with_code(TS,
        name="Error Rate", value=0.12, value_before=0.18, format="percentage", time_series=ts_down, is_inverse=True,
        layout="horizontal",
        card_style={
            "padding": "20px 24px",
            "borderRadius": "4px",
            "border": "left-accent",
            "accentColor": "#22c55e",
            "shadow": "none",
        },
        chart_style={"type": "line", "lineColor": "#22c55e"},
        text_style={"valueSize": "28px"},
        delta_style={"format": "text", "label": "reduced"},
    )

