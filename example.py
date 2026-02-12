"""Example usage of streamlit-kpi-card."""
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_kpi_card import kpi_card, kpi_cards

st.set_page_config(page_title="KPI Card Examples", layout="wide")
st.title("Streamlit KPI Card")

# Sample data
np.random.seed(42)
ts_up = pd.Series(np.cumsum(np.random.randn(20)) + 100, index=[f"W{i}" for i in range(1, 21)])
ts_down = pd.Series(np.cumsum(np.random.randn(20) - 0.3) + 50, index=[f"W{i}" for i in range(1, 21)])
ts_short = pd.Series([10, 12, 11, 15, 14])

# --- Row 1: Basic Examples ---
st.subheader("Basic Examples")
cols = st.columns(4)
with cols[0]:
    kpi_card(name="Percentage", value=87.5, value_before=82.3, format="percentage", time_series=ts_up)
with cols[1]:
    kpi_card(name="Revenue", value=142500, value_before=128000, layout="horizontal", format="currency", time_series=ts_up)
with cols[2]:
    kpi_card(name="CPU Usage", value=67.3, value_before=72.1, layout="chart-focus",
             chart_style={"type": "line"}, format="percentage", time_series=ts_down, is_inverse=True)
with cols[3]:
    kpi_card(name="Bar Focus Last 5", value=150, value_before=130, format="integer", time_series=ts_up,
             chart_style={"type": "rounded-bar", "focusLastN": 5})

# --- Row 2: Compact & Spacious ---
st.subheader("Compact & Spacious")
cols = st.columns(4)
for i, (n, v, vb) in enumerate([("Rev", 14500, 13000), ("Users", 8200, 7800), ("Orders", 520, 490), ("ARPU", 42.5, 40.1)]):
    with cols[i]:
        kpi_card(name=n, value=v, value_before=vb, layout="compact", time_series=ts_short,
                 format="integer" if isinstance(v, int) else "number")

cols = st.columns(2)
with cols[0]:
    kpi_card(name="Spacious (24px)", value=100, value_before=90, format="integer", time_series=ts_short,
             card_style={"padding": "24px"})
with cols[1]:
    kpi_card(name="Stack: horizontal", value=1500, value_before=1200,
             delta_style={"stack": "horizontal"}, format="integer",
             extra_deltas=[{"value_before": 1000, "label": "vs target"}, {"value_before": 1100, "label": "vs budget"}])

# --- Row 3: Style Showcase ---
st.subheader("Style Showcase")
cols = st.columns(3)
with cols[0]:
    kpi_card(
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
    kpi_card(
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
with cols[2]:
    kpi_card(
        name="BOLD CAPS", value=789, value_before=654, format="integer", time_series=ts_short,
        card_style={"padding": "16px", "border": "top-accent", "accentColor": "#000", "shadow": "sharp"},
        text_style={"nameSize": "14px", "nameWeight": 900, "nameColor": "#000", "valueWeight": 400, "valueColor": "#525252"},
        delta_style={"format": "badge"},
    )

# --- Row 4: Dark Theme ---
st.subheader("Dark Theme")
cols = st.columns(3)
with cols[0]:
    kpi_card(
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
    )
with cols[1]:
    kpi_card(
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
with cols[2]:
    kpi_card(name="Stack: vertical", value=1500, value_before=1200,
             delta_style={"stack": "vertical"}, format="integer",
             extra_deltas=[{"value_before": 1000, "label": "vs target"}, {"value_before": 1100, "label": "vs budget"}])
