from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture(autouse=True)
def mock_component_func():
    """Mock _component_func so tests never need a running Streamlit server."""
    fake = MagicMock(return_value=None)
    with patch("streamlit_kpi_card._component_func", fake):
        yield fake
