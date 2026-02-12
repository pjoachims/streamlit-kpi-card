"""Tests for kpi_cards() — global defaults, overrides, flat vs grid, delta/time series per card."""
import pandas as pd
import pytest
from streamlit_kpi_card import kpi_cards


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _call_kwargs(mock):
    return mock.call_args[1]


# ===========================================================================
# 1. Global defaults + per-card overrides (3 tests)
# ===========================================================================
class TestGlobalDefaults:
    def test_global_style_applied(self, mock_component_func):
        """Global card_style should appear on each processed card."""
        kpi_cards(
            cards=[
                {"name": "A", "value": 100, "value_before": 90},
                {"name": "B", "value": 200, "value_before": 180},
            ],
            card_style={"shadow": "glow"},
        )
        kw = _call_kwargs(mock_component_func)
        for card in kw["cards"]:
            assert card["cardStyle"]["shadow"] == "glow"

    def test_per_card_override(self, mock_component_func):
        """Per-card style should override the global default."""
        kpi_cards(
            cards=[
                {"name": "A", "value": 100, "value_before": 90, "card_style": {"shadow": "sharp"}},
                {"name": "B", "value": 200, "value_before": 180},
            ],
            card_style={"shadow": "glow"},
        )
        kw = _call_kwargs(mock_component_func)
        assert kw["cards"][0]["cardStyle"]["shadow"] == "sharp"
        assert kw["cards"][1]["cardStyle"]["shadow"] == "glow"

    def test_global_size_and_millify(self, mock_component_func):
        kpi_cards(
            cards=[{"name": "A", "value": 1000000, "value_before": 900000}],
            size="large",
            millify=True,
            millify_decimals=1,
        )
        kw = _call_kwargs(mock_component_func)
        assert kw["cards"][0]["size"] == "large"
        assert kw["cards"][0]["textStyle"]["millify"] is True
        assert kw["cards"][0]["textStyle"]["millifyDecimals"] == 1


# ===========================================================================
# 2. Flat mode vs grid mode (3 tests)
# ===========================================================================
class TestLayoutModes:
    def test_flat_mode(self, mock_component_func):
        kpi_cards(
            cards=[
                {"name": "A", "value": 10, "value_before": 8},
                {"name": "B", "value": 20, "value_before": 18},
            ],
            columns=2,
        )
        kw = _call_kwargs(mock_component_func)
        assert kw["multiCardMode"] is True
        assert kw["gridMode"] is False
        assert kw["columns"] == 2
        assert len(kw["cards"]) == 2

    def test_flat_mode_default_columns(self, mock_component_func):
        """columns=None defaults to 4."""
        kpi_cards(cards=[{"name": "A", "value": 10, "value_before": 8}])
        kw = _call_kwargs(mock_component_func)
        assert kw["columns"] == 4

    def test_grid_mode(self, mock_component_func):
        kpi_cards(
            cards=[
                [{"name": "A", "value": 10, "value_before": 8}],
                [{"name": "B", "value": 20, "value_before": 18}, {"name": "C", "value": 30, "value_before": 25}],
            ],
        )
        kw = _call_kwargs(mock_component_func)
        assert kw["multiCardMode"] is True
        assert kw["gridMode"] is True
        assert len(kw["gridRows"]) == 2
        assert len(kw["gridRows"][0]) == 1
        assert len(kw["gridRows"][1]) == 2


# ===========================================================================
# 3. Delta / time series per card (3 tests)
# ===========================================================================
class TestCardProcessing:
    def test_delta_calculated_per_card(self, mock_component_func):
        kpi_cards(
            cards=[
                {"name": "A", "value": 110, "value_before": 100},
                {"name": "B", "value": 80, "value_before": 100},
            ],
        )
        kw = _call_kwargs(mock_component_func)
        assert kw["cards"][0]["delta"] == pytest.approx(10.0)
        assert kw["cards"][1]["delta"] == pytest.approx(-20.0)

    def test_time_series_per_card(self, mock_component_func):
        ts = pd.Series([1, 2, 3], index=["x", "y", "z"])
        kpi_cards(
            cards=[
                {"name": "A", "value": 3, "value_before": 1, "time_series": ts},
                {"name": "B", "value": 5, "value_before": 4},
            ],
        )
        kw = _call_kwargs(mock_component_func)
        assert kw["cards"][0]["timeSeriesData"] is not None
        assert len(kw["cards"][0]["timeSeriesData"]) == 3
        assert kw["cards"][1]["timeSeriesData"] is None

    def test_format_auto_detect_per_card(self, mock_component_func):
        kpi_cards(
            cards=[
                {"name": "Int", "value": 100, "value_before": 90},
                {"name": "Float", "value": 3.14, "value_before": 2.0},
            ],
        )
        kw = _call_kwargs(mock_component_func)
        assert kw["cards"][0]["format"]["type"] == "integer"
        assert kw["cards"][1]["format"]["type"] == "number"

    def test_extra_deltas_per_card(self, mock_component_func):
        kpi_cards(
            cards=[
                {
                    "name": "A",
                    "value": 100,
                    "value_before": 90,
                    "extra_deltas": [{"value_before": 80, "label": "vs target"}],
                },
            ],
        )
        kw = _call_kwargs(mock_component_func)
        deltas = kw["cards"][0]["extraDeltas"]
        assert len(deltas) == 1
        assert deltas[0]["delta"] == 20.0
