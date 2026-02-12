"""Tests for kpi_card() — format handling, delta calculation, time series, extra deltas, param passthrough."""
import pandas as pd
import pytest
from streamlit_kpi_card import kpi_card


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _call_kwargs(mock):
    """Return the kwargs dict that _component_func was last called with."""
    return mock.call_args[1]


# ===========================================================================
# 1. Format handling (10 tests)
# ===========================================================================
class TestFormatHandling:
    def test_none_integer_auto(self, mock_component_func):
        """None format + int value -> auto-detect integer."""
        kpi_card(name="X", value=100, value_before=90)
        assert _call_kwargs(mock_component_func)["format"] == {"type": "integer"}

    def test_none_float_whole_auto(self, mock_component_func):
        """None format + float that equals int -> integer."""
        kpi_card(name="X", value=100.0, value_before=90)
        assert _call_kwargs(mock_component_func)["format"] == {"type": "integer"}

    def test_none_float_decimal_auto(self, mock_component_func):
        """None format + float with decimals -> number with 2 decimals."""
        kpi_card(name="X", value=3.14, value_before=2.0)
        assert _call_kwargs(mock_component_func)["format"] == {"type": "number", "decimals": 2}

    def test_string_number(self, mock_component_func):
        """String 'number' -> dict with 2 decimals."""
        kpi_card(name="X", value=10, value_before=5, format="number")
        assert _call_kwargs(mock_component_func)["format"] == {"type": "number", "decimals": 2}

    def test_string_percentage(self, mock_component_func):
        kpi_card(name="X", value=10, value_before=5, format="percentage")
        assert _call_kwargs(mock_component_func)["format"] == {"type": "percentage", "decimals": 2}

    def test_string_currency_defaults_euro(self, mock_component_func):
        """String 'currency' defaults to euro."""
        kpi_card(name="X", value=10, value_before=5, format="currency")
        fmt = _call_kwargs(mock_component_func)["format"]
        assert fmt == {"type": "currency", "decimals": 2, "currency": "\u20ac"}

    def test_string_integer(self, mock_component_func):
        kpi_card(name="X", value=10, value_before=5, format="integer")
        assert _call_kwargs(mock_component_func)["format"] == {"type": "integer", "decimals": 2}

    def test_dict_passthrough(self, mock_component_func):
        """Dict format gets normalized with defaults."""
        kpi_card(name="X", value=10, value_before=5, format={"type": "number"})
        assert _call_kwargs(mock_component_func)["format"] == {"type": "number", "decimals": 2}

    def test_dict_currency_default_euro(self, mock_component_func):
        """Dict currency without currency key defaults to euro."""
        kpi_card(name="X", value=10, value_before=5, format={"type": "currency", "decimals": 0})
        fmt = _call_kwargs(mock_component_func)["format"]
        assert fmt["currency"] == "\u20ac"
        assert fmt["decimals"] == 0

    def test_dict_currency_custom(self, mock_component_func):
        """Dict currency with explicit currency keeps it."""
        kpi_card(name="X", value=10, value_before=5, format={"type": "currency", "decimals": 1, "currency": "$"})
        fmt = _call_kwargs(mock_component_func)["format"]
        assert fmt["currency"] == "$"
        assert fmt["decimals"] == 1


# ===========================================================================
# 2. Delta calculation (4 tests)
# ===========================================================================
class TestDeltaCalculation:
    def test_positive_delta(self, mock_component_func):
        kpi_card(name="X", value=110, value_before=100)
        kw = _call_kwargs(mock_component_func)
        assert kw["delta"] == 10.0
        assert kw["deltaPercent"] == pytest.approx(10.0)

    def test_negative_delta(self, mock_component_func):
        kpi_card(name="X", value=90, value_before=100)
        kw = _call_kwargs(mock_component_func)
        assert kw["delta"] == -10.0
        assert kw["deltaPercent"] == pytest.approx(-10.0)

    def test_zero_delta(self, mock_component_func):
        kpi_card(name="X", value=100, value_before=100)
        kw = _call_kwargs(mock_component_func)
        assert kw["delta"] == 0.0
        assert kw["deltaPercent"] == 0.0

    def test_division_by_zero(self, mock_component_func):
        """value_before=0 should not raise; deltaPercent=0."""
        kpi_card(name="X", value=50, value_before=0)
        kw = _call_kwargs(mock_component_func)
        assert kw["delta"] == 50.0
        assert kw["deltaPercent"] == 0


# ===========================================================================
# 3. Time series processing (3 tests)
# ===========================================================================
class TestTimeSeries:
    def test_none_time_series(self, mock_component_func):
        kpi_card(name="X", value=10, value_before=5)
        kw = _call_kwargs(mock_component_func)
        assert kw["timeSeriesData"] is None
        assert kw["averageValue"] is None

    def test_basic_series(self, mock_component_func):
        ts = pd.Series([1, 2, 3], index=["a", "b", "c"])
        kpi_card(name="X", value=3, value_before=1, time_series=ts)
        kw = _call_kwargs(mock_component_func)
        assert len(kw["timeSeriesData"]) == 3
        assert kw["timeSeriesData"][0] == {"index": "a", "value": 1.0}
        assert kw["timeSeriesData"][2] == {"index": "c", "value": 3.0}

    def test_average_calculation(self, mock_component_func):
        ts = pd.Series([10, 20, 30])
        kpi_card(name="X", value=30, value_before=10, time_series=ts, chart_style={"showAverage": True})
        kw = _call_kwargs(mock_component_func)
        assert kw["averageValue"] == pytest.approx(20.0)


# ===========================================================================
# 4. Extra deltas (3 tests)
# ===========================================================================
class TestExtraDeltas:
    def test_none_extra_deltas(self, mock_component_func):
        kpi_card(name="X", value=10, value_before=5)
        assert _call_kwargs(mock_component_func)["extraDeltas"] is None

    def test_basic_extra_delta(self, mock_component_func):
        kpi_card(
            name="X",
            value=100,
            value_before=90,
            extra_deltas=[{"value_before": 80, "label": "vs target", "is_inverse": False}],
        )
        deltas = _call_kwargs(mock_component_func)["extraDeltas"]
        assert len(deltas) == 1
        assert deltas[0]["delta"] == 20.0
        assert deltas[0]["deltaPercent"] == pytest.approx(25.0)
        assert deltas[0]["label"] == "vs target"
        assert deltas[0]["isInverse"] is False

    def test_extra_delta_division_by_zero(self, mock_component_func):
        kpi_card(
            name="X",
            value=100,
            value_before=90,
            extra_deltas=[{"value_before": 0, "label": "zero"}],
        )
        deltas = _call_kwargs(mock_component_func)["extraDeltas"]
        assert deltas[0]["deltaPercent"] == 0


# ===========================================================================
# 5. Style dict passthrough (2 tests)
# ===========================================================================
class TestParamPassthrough:
    def test_style_dicts_passed(self, mock_component_func):
        """Style dicts should be passed to the component."""
        kpi_card(
            name="X",
            value=10,
            value_before=5,
            card_style={"shadow": "glow", "border": "left-accent", "backgroundStyle": "glass"},
            delta_style={"format": "badge", "position": "right-of-value", "stack": "vertical"},
            chart_style={"type": "dots"},
        )
        kw = _call_kwargs(mock_component_func)
        assert kw["cardStyle"]["shadow"] == "glow"
        assert kw["cardStyle"]["border"] == "left-accent"
        assert kw["cardStyle"]["backgroundStyle"] == "glass"
        assert kw["deltaStyle"]["format"] == "badge"
        assert kw["deltaStyle"]["position"] == "right-of-value"
        assert kw["deltaStyle"]["stack"] == "vertical"
        assert kw["chartStyle"]["type"] == "dots"

    def test_size_and_text_style_passthrough(self, mock_component_func):
        """Size param and text_style should be passed correctly."""
        kpi_card(
            name="X",
            value=10,
            value_before=5,
            size="large",
            text_style={"millify": True, "millifyDecimals": 1},
            chart_style={"fill": True, "maxHeight": "40px"},
        )
        kw = _call_kwargs(mock_component_func)
        assert kw["size"] == "large"
        assert kw["textStyle"]["millify"] is True
        assert kw["textStyle"]["millifyDecimals"] == 1
        assert kw["chartStyle"]["fill"] is True
        assert kw["chartStyle"]["maxHeight"] == "40px"
