import os
import streamlit.components.v1 as components
import pandas as pd

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
    name: str,
    value: float,
    value_before: float,
    relative_change: bool = False,
    time_series: pd.Series = None,
    format: dict = None,
    background_color: str = "#ffffff",
    border: str = "1px solid #e5e7eb",
    shadow: bool = True,
    border_radius: str = "12px",
    line_color: str = None,
    decimals: int = None,
    height: str = None,
    show_average: bool = False,
    info_text: str = None,
    is_inverse: bool = False,
    chart_type: str = "line",
    key: str = None
):
    """
    Create a KPI card component with name, value, delta, and time series chart.

    Parameters
    ----------
    name : str
        The name/label of the KPI
    value : float
        The current value
    value_before : float
        The previous value for comparison
    relative_change : bool, default False
        If True, show percentage change. If False, show absolute difference.
    time_series : pd.Series, optional
        Time series data to display as a chart
    format : dict, optional
        Format configuration dict with keys:
        - type: 'number', 'percentage', 'currency', 'integer' (default: 'number')
        - decimals: number of decimal places (default: 1)
        - currency: currency symbol like '$', '€', '£' (default: '$')
        Example: {"type": "currency", "decimals": 2, "currency": "€"}
    background_color : str, default "#ffffff"
        Background color of the card
    border : str, optional, default "1px solid #e5e7eb"
        Border style (CSS border property). Set to None or "" for no border.
    shadow : bool, default True
        Whether to show shadow on the card
    border_radius : str, default "12px"
        Border radius (rounded corners)
    line_color : str, optional
        Color of the time series line. If None, uses green/red based on delta.
    decimals : int, optional
        DEPRECATED: Use format dict instead. Number of decimal places.
    height : str, optional
        Height of the card (CSS height property). If None, height is auto.
    show_average : bool, default False
        Show a dashed horizontal line representing the average value
    info_text : str, optional
        Info text to display on hover over info icon. Icon only shows if text provided.
    is_inverse : bool, default False
        If True, lower values are better (inverts green/red coloring)
    chart_type : str, default "line"
        Type of chart: 'line', 'bar', or 'area'
    key : str, optional
        Unique key for the component

    Returns
    -------
    None
    """
    # Handle format parameter
    if format is None:
        format = {"type": "number", "decimals": 1, "currency": "$"}
    else:
        # Ensure all required keys exist with defaults
        format = {
            "type": format.get("type", "number"),
            "decimals": format.get("decimals", 1),
            "currency": format.get("currency", "$")
        }

    # Backward compatibility: if decimals parameter is provided, override format decimals
    if decimals is not None:
        format["decimals"] = decimals

    # Calculate delta
    delta = value - value_before
    delta_percent = ((value - value_before) / value_before * 100) if value_before != 0 else 0

    # Prepare time series data
    time_series_data = None
    average_value = None
    if time_series is not None:
        time_series_data = [
            {"index": str(idx), "value": float(val)}
            for idx, val in time_series.items()
        ]
        # Calculate average if needed
        if show_average:
            average_value = float(time_series.mean())

    component_value = _component_func(
        name=name,
        value=float(value),
        valueBefore=float(value_before),
        delta=float(delta),
        deltaPercent=float(delta_percent),
        relativeChange=relative_change,
        timeSeriesData=time_series_data,
        format=format,
        backgroundColor=background_color,
        border=border,
        shadow=shadow,
        borderRadius=border_radius,
        lineColor=line_color,
        height=height,
        showAverage=show_average,
        averageValue=average_value,
        infoText=info_text,
        isInverse=is_inverse,
        chartType=chart_type,
        key=key,
        default=None
    )

    return component_value


__all__ = ["kpi_card"]
