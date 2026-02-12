"""
Streamlit KPI Card Component

A beautiful, interactive KPI card component for Streamlit with support for
time series visualization and delta indicators.
"""

import os
import warnings
from typing import Optional, Dict, Any, Union, Literal, List
from typing_extensions import TypedDict
import streamlit.components.v1 as components
import pandas as pd

__version__ = "0.2.0"


# =============================================================================
# Style TypedDicts
# =============================================================================

class CardStyleDict(TypedDict, total=False):
    """Card container styling options."""
    # Core styling
    padding: str                    # CSS padding (e.g., "8px 12px")
    borderRadius: str               # CSS border-radius (e.g., "8px")
    backgroundColor: str            # CSS color (e.g., "#fff")
    shadow: str                     # "none"|"subtle"|"sharp"|"glow"|"inset" or CSS
    border: str                     # "none"|"hairline"|"left-accent"|"top-accent"|"full" or CSS
    height: str                     # CSS height
    backgroundStyle: str            # "solid"|"gradient"|"glass"|"tinted"|"transparent"
    accentColor: str                # Accent color for borders/glow
    # Header & detail
    showHeader: bool                # Show name/info section
    showDetail: bool                # Show detail expand button
    detailHeight: int               # Height of detail section in pixels
    # Overlay (chart-focus layout)
    overlayPosition: str            # "auto"|"bottom-left"|"bottom-right"|"top-left"|"top-right"
    overlayOpacity: float           # Overlay transparency (0-1)


class ChartStyleDict(TypedDict, total=False):
    """Chart area styling and options."""
    # Core styling
    type: str                       # "line"|"gradient-area"|"dots"|"rounded-bar"|"sparkline-dot"
    lineColor: str                  # Line/bar color
    height: str                     # CSS height (e.g., "60px")
    maxHeight: str                  # Max height (e.g., "30px")
    margin: str                     # CSS margin
    fill: bool                      # Enable gradient fill
    fillOpacity: float              # Fill opacity (0-1)
    # Visibility
    show: bool                      # Show/hide chart
    showAverage: bool               # Show average line
    # Axes & grid
    axis: str                       # "none"|"x"|"y"|"both"
    gridX: Union[bool, List]        # Vertical grid lines
    gridY: Union[bool, List]        # Horizontal grid lines
    yStartAtZero: bool              # Y axis starts at 0
    xLabels: List                   # X-axis labels [(idx, "label"), ...]
    # Data features
    markers: List[int]              # Highlighted dots at indices
    focusLastN: int                 # Highlight last N bars
    referenceLine: Dict             # {value, label, color, style}


class TextStyleDict(TypedDict, total=False):
    """Typography styling options."""
    # Name/title styling
    nameSize: str                   # Name font size (e.g., "12px")
    nameColor: str                  # Name text color
    nameWeight: Union[str, int]     # Name font weight (e.g., 500, "bold")
    nameMarginBottom: str           # Margin below name (e.g., "8px")
    nameLetterSpacing: str          # Letter spacing (e.g., "0.05em")
    nameTransform: str              # Text transform: "uppercase"|"lowercase"|"capitalize"|"none"
    # Value styling
    valueSize: str                  # Value font size (e.g., "24px")
    valueColor: str                 # Value text color
    valueWeight: Union[str, int]    # Value font weight (e.g., 600, "bold")
    # Formatting
    millify: bool                   # Format large numbers as K, M, B
    millifyDecimals: int            # Decimals for millified values
    infoText: str                   # Hover info text


class DeltaStyleDict(TypedDict, total=False):
    """Delta indicator styling options."""
    format: str                     # "pill"|"text"|"badge"|"inline"|"icon"
    position: str                   # "below-value"|"right-of-value"|"below-name"
    stack: str                      # "horizontal"|"vertical"
    label: str                      # Delta label (e.g., "vs previous")
    positiveColor: str              # Color for positive deltas
    negativeColor: str              # Color for negative deltas
    # Size & spacing
    fontSize: str                   # Delta text font size (e.g., "12px")
    arrowSize: int                  # Arrow icon size in pixels (e.g., 12)
    padding: str                    # Padding for pill/badge (e.g., "4px 8px")
    borderRadius: str               # Border radius for pill/badge (e.g., "6px")
    labelSize: str                  # Label font size (e.g., "11px")
    gap: str                        # Gap between delta and label (e.g., "4px")

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "kpi_card",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("kpi_card", path=build_dir)


def kpi_card(
    # === Required ===
    name: str,
    value: float,
    value_before: float,
    # === Data ===
    time_series: Optional[pd.Series] = None,
    format: Optional[Union[str, Dict[str, Any]]] = None,
    relative_change: bool = False,
    is_inverse: bool = False,
    extra_deltas: Optional[List[Dict[str, Any]]] = None,
    # === Style Dicts ===
    card_style: Optional[CardStyleDict] = None,
    chart_style: Optional[ChartStyleDict] = None,
    text_style: Optional[TextStyleDict] = None,
    delta_style: Optional[DeltaStyleDict] = None,
    # === Layout ===
    layout: Literal["vertical", "horizontal", "value-focus", "chart-focus", "compact", "mini"] = "vertical",
    size: Literal["small", "medium", "large"] = "medium",
    theme: Literal["light", "dark", "auto"] = "auto",
    key: Optional[str] = None,
) -> None:
    """
    Create a KPI card component with name, value, delta, and time series chart.

    This component displays a key performance indicator with:
    - A prominent value display
    - Delta indicator (absolute or percentage change)
    - Optional time series chart
    - Customizable styling and formatting

    Parameters
    ----------
    name : str
        The name/label of the KPI.
    value : float
        The current value to display.
    value_before : float
        The previous value for comparison (to calculate delta).
    relative_change : bool, default False
        If True, show percentage change. If False, show absolute difference.
    time_series : pd.Series, optional
        Time series data to display as a chart.
    format : str or dict, optional
        Format type as string: 'number', 'percentage', 'currency', 'integer'
        Or dict with keys: type, decimals, currency

        If not specified, auto-detects: 'integer' for whole numbers, 'number' for decimals
        String formats default to 2 decimals, '€' for currency

        Examples:
            format="currency"  # Uses 2 decimals and €
            format={"type": "currency", "decimals": 0, "currency": "$"}
    background_color : str, optional
        Custom background color (CSS color). Overrides background_style if set.
    border : str, optional
        Custom border (CSS border property). Overrides border_style if set.
    border_radius : str, default "12px"
        Border radius for rounded corners (CSS border-radius).
    line_color : str, optional
        Color of the time series line. If None, uses green for positive/red for negative delta.
    height : str, optional
        Height of the card (CSS height property). If None, height is auto.
    show_average : bool, default False
        Show a dashed horizontal line representing the average value in the time series.
    info_text : str, optional
        Info text to display on hover over info icon. Icon only shows if text provided.
    is_inverse : bool, default False
        If True, lower values are better (inverts green/red coloring for delta).
    theme : str, default "auto"
        Color theme: 'light', 'dark', or 'auto' (follows system preference).
    shadow_style : str, default "subtle"
        Shadow style: 'none', 'subtle', 'sharp', 'glow', 'inset'.
    border_style : str, default "hairline"
        Border style preset: 'none', 'hairline', 'left-accent', 'top-accent', 'full'.
    accent_color : str, optional
        Custom accent color for borders and glow effects.
    background_style : str, default "solid"
        Background style: 'solid', 'gradient', 'glass', 'tinted', 'transparent'.
    delta_style : str, default "pill"
        Delta indicator style: 'pill', 'text', 'badge', 'inline', 'icon'.
    chart_style : str, default "line"
        Chart style: 'line', 'gradient-area', 'dots', 'rounded-bar', 'sparkline-dot'.
    layout : str, default "vertical"
        Layout variant: 'vertical', 'horizontal', 'value-focus', 'chart-focus', 'compact'.
    delta_label : str, default "vs previous"
        Custom label for the delta comparison (e.g., "vs last month", "vs target", "YoY").
    focus_last_n : int, optional
        For bar charts, highlight only the last N bars (others dimmed).
    show_chart : bool, default True
        Whether to show the sparkline/chart. Set to False for minimal cards.
    extra_deltas : list, optional
        Additional delta comparisons. Each dict has: value_before, label, is_inverse.
    delta_position : str, default "below-value"
        Delta position: 'below-value', 'right-of-value', 'below-name'.
    delta_stack : str, default "horizontal"
        Stack direction for multiple deltas: 'horizontal', 'vertical'.
    size : str, default "medium"
        Card size: 'small', 'medium', 'large'.
    millify : bool, default False
        Format large numbers as K, M, B (e.g., 1.2M instead of 1,200,000).
    key : str, optional
        Unique key for the component to enable multiple instances.

    Returns
    -------
    None
        This component does not return a value.

    Examples
    --------
    Basic usage with currency formatting:

    >>> import pandas as pd
    >>> from streamlit_kpi_card import kpi_card
    >>> time_series = pd.Series([100, 105, 103, 108, 110])
    >>> kpi_card(
    ...     name="Revenue",
    ...     value=14500.00,
    ...     value_before=12000.00,
    ...     relative_change=True,
    ...     time_series=time_series,
    ...     format="currency"
    ... )
    """
    # Handle format parameter
    if format is None:
        # Auto-detect format based on value type
        if isinstance(value, int) or (isinstance(value, float) and value == int(value)):
            format = {"type": "integer"}
        else:
            format = {"type": "number", "decimals": 2}
    elif isinstance(format, str):
        # Convert string format to dict
        format = {"type": format, "decimals": 2}
        if format["type"] == "currency":
            format["currency"] = "€"
    else:
        # Ensure all required keys exist with defaults
        format_type = format.get("type", "number")
        currency_val = format.get("currency", "€")
        format = {
            "type": format_type,
            "decimals": format.get("decimals", 2)
        }
        if format_type == "currency":
            format["currency"] = currency_val

    # Calculate primary delta
    delta = value - value_before
    delta_percent = ((value - value_before) / value_before * 100) if value_before != 0 else 0

    # Process extra deltas
    deltas_list = None
    if extra_deltas:
        deltas_list = []
        for d in extra_deltas:
            vb = d.get("value_before", d.get("valueBefore", 0))
            lbl = d.get("label", "")
            inv = d.get("is_inverse", d.get("isInverse", False))
            d_val = value - vb
            d_pct = ((value - vb) / vb * 100) if vb != 0 else 0
            deltas_list.append({
                "delta": float(d_val),
                "deltaPercent": float(d_pct),
                "label": lbl,
                "isInverse": inv,
            })

    # Prepare time series data
    time_series_data = None
    average_value = None
    if time_series is not None:
        time_series_data = [
            {"index": str(idx), "value": float(val)}
            for idx, val in time_series.items()
        ]
        # Calculate average if showAverage is in chart_style
        if chart_style and chart_style.get("showAverage"):
            average_value = float(time_series.mean())

    component_value = _component_func(
        # Core data
        name=name,
        value=float(value),
        valueBefore=float(value_before),
        delta=float(delta),
        deltaPercent=float(delta_percent),
        relativeChange=relative_change,
        isInverse=is_inverse,
        timeSeriesData=time_series_data,
        averageValue=average_value,
        format=format,
        extraDeltas=deltas_list,
        # Style dicts (frontend will extract all options from these)
        cardStyle=card_style,
        chartStyle=chart_style,
        textStyle=text_style,
        deltaStyle=delta_style,
        # Layout
        layout=layout,
        size=size,
        theme=theme,
        key=key,
        default=None
    )

    return component_value


def kpi_cards(
    cards: Union[List[Dict[str, Any]], List[List[Dict[str, Any]]]],
    columns: Optional[int] = None,
    # === Grid Layout ===
    gap: str = "12px",
    row_gap: Optional[str] = None,
    column_gap: Optional[str] = None,
    # === Global Style Dicts (apply to all cards) ===
    card_style: Optional[CardStyleDict] = None,
    chart_style: Optional[ChartStyleDict] = None,
    text_style: Optional[TextStyleDict] = None,
    delta_style: Optional[DeltaStyleDict] = None,
    # === Layout & Theme ===
    layout: Literal["vertical", "horizontal", "value-focus", "chart-focus", "compact", "mini"] = "vertical",
    size: Literal["small", "medium", "large"] = "medium",
    theme: Literal["light", "dark", "auto"] = "auto",
    # === Chart & Delta Type ===
    chart_type: Literal["line", "gradient-area", "dots", "rounded-bar", "sparkline-dot"] = "line",
    delta_format: Literal["pill", "text", "badge", "inline", "icon"] = "pill",
    # === Chart Options ===
    show_chart: bool = True,
    axis: Literal["none", "x", "y", "both"] = "none",
    grid_x: Union[bool, List] = False,
    grid_y: Union[bool, List] = False,
    y_start_at_zero: bool = False,
    x_labels: Optional[List] = None,
    reference_line: Optional[Dict[str, Any]] = None,
    markers: Optional[List[int]] = None,
    # === Formatting ===
    millify: bool = False,
    millify_decimals: int = 2,
    # === Detail & Overlay ===
    show_detail_button: bool = False,
    detail_height: int = 300,
    overlay_position: Literal["auto", "bottom-left", "bottom-right", "top-left", "top-right"] = "auto",
    overlay_opacity: Optional[float] = None,
    # === Mini Layout ===
    mini_columns: str = "auto",
    # === Selection ===
    selectable: bool = False,
    selected: Optional[str] = None,
    searchable: bool = False,
    key: Optional[str] = None,
) -> Optional[str]:
    """
    Render multiple KPI cards in a single iframe for better performance.

    Use this instead of multiple kpi_card() calls when displaying many cards
    together. All cards share one iframe, reducing load time significantly.

    Supports two layout modes:
    1. Flat list + columns: `kpi_cards([card1, card2, card3], columns=3)`
    2. Grid rows (nested lists): `kpi_cards([[card1, card2], [card3, card4, card5]])`

    Parameters
    ----------
    cards : list of dict OR list of list of dict
        Card configurations. Can be:
        - Flat list: cards distributed into `columns` columns
        - Nested list: each inner list becomes a row (columns param ignored)

        Each card dict can have:
        - name (required): Card title
        - value (required): Current value
        - value_before (required): Previous value for delta calculation
        - All other kpi_card() parameters are supported
        - Per-card values override the global defaults
    columns : int, optional
        Number of columns (only for flat list mode). Default 4.
        Ignored when using nested list (grid) mode.
    gap : str, default "12px"
        Gap between cards (CSS value). Used for both row and column gap if
        row_gap/column_gap are not specified.
    row_gap : str, optional
        Vertical gap between rows (CSS value). Overrides gap for vertical spacing.
    column_gap : str, optional
        Horizontal gap between columns (CSS value). Overrides gap for horizontal spacing.
    theme : str, default "auto"
        Global theme for all cards (can be overridden per-card)
    shadow_style : str, optional
        Global shadow style for all cards
    border_style : str, optional
        Global border style for all cards
    background_style : str, optional
        Global background style for all cards
    delta_style : str, default "pill"
        Global delta indicator style for all cards
    chart_style : str, optional
        Global chart style for all cards
    layout : str, default "vertical"
        Global layout for all cards
    delta_label : str, default "vs previous"
        Global delta label for all cards
    show_chart : bool, default True
        Global show_chart setting for all cards
    delta_position : str, default "below-value"
        Global delta position for all cards
    delta_stack : str, default "horizontal"
        Global delta stack direction for all cards
    key : str, optional
        Unique key for the component

    Example
    -------
    >>> # Flat list with columns
    >>> kpi_cards([
    ...     {"name": "Revenue", "value": 142500, "value_before": 128000},
    ...     {"name": "Users", "value": 12450, "value_before": 11200},
    ... ], columns=2, shadow_style="subtle")
    >>>
    >>> # Grid layout with rows (nested lists)
    >>> kpi_cards([
    ...     [{"name": "Revenue", "value": 100, "value_before": 90}],  # row 1: 1 card (full width)
    ...     [{"name": "Users", "value": 50, "value_before": 45}, {"name": "Orders", "value": 30, "value_before": 25}],  # row 2: 2 cards
    ...     [{"name": "A", "value": 1, "value_before": 1}, {"name": "B", "value": 2, "value_before": 2}, {"name": "C", "value": 3, "value_before": 3}],  # row 3: 3 cards
    ... ])
    """
    # Global defaults
    defaults = {
        # Style dicts
        "card_style": card_style,
        "chart_style": chart_style,
        "text_style": text_style,
        "delta_style": delta_style,
        # Layout & theme
        "layout": layout,
        "size": size,
        "theme": theme,
        # Chart & delta type
        "chart_type": chart_type,
        "delta_format": delta_format,
        # Chart options
        "show_chart": show_chart,
        "axis": axis,
        "grid_x": grid_x,
        "grid_y": grid_y,
        "y_start_at_zero": y_start_at_zero,
        "x_labels": x_labels,
        "reference_line": reference_line,
        "markers": markers,
        # Formatting
        "millify": millify,
        "millify_decimals": millify_decimals,
        # Detail & overlay
        "show_detail_button": show_detail_button,
        "detail_height": detail_height,
        "overlay_position": overlay_position,
        "overlay_opacity": overlay_opacity,
    }

    def merge_style_dicts(global_style, card_style):
        """Merge global style dict with per-card overrides."""
        if not global_style and not card_style:
            return None
        result = {}
        if global_style:
            result.update(global_style)
        if card_style:
            result.update(card_style)
        return result or None

    def process_card(card):
        """Process a single card dict into component format."""
        name = card.get("name", "")
        value = card.get("value", 0)
        value_before = card.get("value_before", 0)

        # Handle format
        fmt = card.get("format")
        if fmt is None:
            if isinstance(value, int) or (isinstance(value, float) and value == int(value)):
                fmt = {"type": "integer"}
            else:
                fmt = {"type": "number", "decimals": 2}
        elif isinstance(fmt, str):
            fmt = {"type": fmt, "decimals": 2}
            if fmt["type"] == "currency":
                fmt["currency"] = "€"
        else:
            format_type = fmt.get("type", "number")
            currency_val = fmt.get("currency", "€")
            fmt = {"type": format_type, "decimals": fmt.get("decimals", 2)}
            if format_type == "currency":
                fmt["currency"] = currency_val

        # Calculate delta
        delta = value - value_before
        delta_percent = ((value - value_before) / value_before * 100) if value_before != 0 else 0

        # Process time series
        time_series = card.get("time_series")
        time_series_data = None
        average_value = None
        if time_series is not None:
            time_series_data = [
                {"index": str(idx), "value": float(val)}
                for idx, val in time_series.items()
            ]
            # Calculate average for showAverage
            average_value = float(time_series.mean())

        # Process extra deltas
        extra_deltas = card.get("extra_deltas")
        deltas_list = None
        if extra_deltas:
            deltas_list = []
            for d in extra_deltas:
                vb = d.get("value_before", d.get("valueBefore", 0))
                d_val = value - vb
                d_pct = ((value - vb) / vb * 100) if vb != 0 else 0
                deltas_list.append({
                    "delta": float(d_val),
                    "deltaPercent": float(d_pct),
                    "label": d.get("label", ""),
                    "isInverse": d.get("is_inverse", d.get("isInverse", False)),
                })

        # Use per-card value if set, otherwise fall back to global default
        def get_val(key):
            card_val = card.get(key)
            if card_val is not None:
                return card_val
            return defaults.get(key)

        # Merge style dicts (global + per-card)
        merged_card_style = merge_style_dicts(defaults.get("card_style"), card.get("card_style"))
        merged_chart_style = merge_style_dicts(defaults.get("chart_style"), card.get("chart_style"))
        merged_text_style = merge_style_dicts(defaults.get("text_style"), card.get("text_style"))
        merged_delta_style = merge_style_dicts(defaults.get("delta_style"), card.get("delta_style"))

        # Merge top-level convenience params into style dicts
        if merged_chart_style is None:
            merged_chart_style = {}
        if "type" not in merged_chart_style:
            merged_chart_style["type"] = get_val("chart_type")
        if "show" not in merged_chart_style:
            merged_chart_style["show"] = get_val("show_chart")
        if "showAverage" not in merged_chart_style:
            merged_chart_style["showAverage"] = False
        if "axis" not in merged_chart_style:
            merged_chart_style["axis"] = get_val("axis")
        if "gridX" not in merged_chart_style:
            merged_chart_style["gridX"] = get_val("grid_x") or False
        if "gridY" not in merged_chart_style:
            merged_chart_style["gridY"] = get_val("grid_y") or False
        if "yStartAtZero" not in merged_chart_style:
            merged_chart_style["yStartAtZero"] = get_val("y_start_at_zero")
        if "xLabels" not in merged_chart_style:
            merged_chart_style["xLabels"] = get_val("x_labels")
        if "referenceLine" not in merged_chart_style:
            merged_chart_style["referenceLine"] = get_val("reference_line")
        if "markers" not in merged_chart_style:
            merged_chart_style["markers"] = card.get("markers") or get_val("markers")
        if "focusLastN" not in merged_chart_style:
            merged_chart_style["focusLastN"] = card.get("focus_last_n")

        if merged_delta_style is None:
            merged_delta_style = {}
        if "format" not in merged_delta_style:
            merged_delta_style["format"] = get_val("delta_format")

        if merged_card_style is None:
            merged_card_style = {}
        if "showHeader" not in merged_card_style:
            merged_card_style["showHeader"] = card.get("show_header", True)
        if "showDetail" not in merged_card_style:
            merged_card_style["showDetail"] = get_val("show_detail_button")
        if "detailHeight" not in merged_card_style:
            merged_card_style["detailHeight"] = get_val("detail_height")
        if "overlayPosition" not in merged_card_style:
            merged_card_style["overlayPosition"] = get_val("overlay_position")
        if "overlayOpacity" not in merged_card_style:
            merged_card_style["overlayOpacity"] = get_val("overlay_opacity")

        if merged_text_style is None:
            merged_text_style = {}
        if "millify" not in merged_text_style:
            merged_text_style["millify"] = get_val("millify")
        if "millifyDecimals" not in merged_text_style:
            merged_text_style["millifyDecimals"] = get_val("millify_decimals")
        if "infoText" not in merged_text_style and card.get("info_text"):
            merged_text_style["infoText"] = card.get("info_text")

        return {
            # Core data
            "name": name,
            "value": float(value),
            "valueBefore": float(value_before),
            "delta": float(delta),
            "deltaPercent": float(delta_percent),
            "relativeChange": card.get("relative_change", False),
            "isInverse": card.get("is_inverse", False),
            "timeSeriesData": time_series_data,
            "averageValue": average_value,
            "format": fmt,
            "extraDeltas": deltas_list,
            # Style dicts (all styling options are inside these)
            "cardStyle": merged_card_style,
            "chartStyle": merged_chart_style,
            "textStyle": merged_text_style,
            "deltaStyle": merged_delta_style,
            # Layout & theme
            "layout": get_val("layout"),
            "size": get_val("size"),
            "theme": get_val("theme"),
        }

    # Detect grid mode (nested lists) vs flat mode
    is_grid_mode = cards and isinstance(cards[0], list)

    if is_grid_mode:
        # Grid mode: list of rows, each row is a list of cards
        grid_rows = []
        for row in cards:
            grid_rows.append([process_card(card) for card in row])
        return _component_func(
            multiCardMode=True,
            gridMode=True,
            gridRows=grid_rows,
            gap=gap,
            rowGap=row_gap,
            columnGap=column_gap,
            miniColumns=mini_columns,
            selectable=selectable,
            selected=selected,
            searchable=searchable,
            key=key,
            default=None
        )
    else:
        # Flat mode: single list with columns
        processed_cards = [process_card(card) for card in cards]
        return _component_func(
            multiCardMode=True,
            gridMode=False,
            cards=processed_cards,
            columns=columns if columns is not None else 4,
            gap=gap,
            rowGap=row_gap,
            columnGap=column_gap,
            miniColumns=mini_columns,
            selectable=selectable,
            selected=selected,
            searchable=searchable,
            key=key,
            default=None
        )


__all__ = ["kpi_card", "kpi_cards", "__version__"]
