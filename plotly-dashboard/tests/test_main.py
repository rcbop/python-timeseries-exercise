from unittest.mock import Mock, patch

import pandas as pd
from dash import html
from dashboard.main import (calculate_percentage_distribution,
                            get_latest_data_frame, get_line_fig,
                            get_page_layout, get_pie_fig)

df = pd.DataFrame({"metadata": [
    {"area": "A"}, {"area": "B"}, {"area": "A"},
    {"area": "C"}, {"area": "A"}, {"area": "B"},
    {"area": "A"}
]})


def test_calculate_percentage_distribution():
    sensor_area_counts, sensor_area_percentages = calculate_percentage_distribution(
        df)
    assert sensor_area_counts.to_list() == [4, 2, 1]
    assert sensor_area_percentages.to_list(
    ) == [57.14285714285714, 28.57142857142857, 14.285714285714285]


@patch("dashboard.main.fetch_latest_data")
def test_get_latest_data_frame(mock_fetch_latest_data):
    mock_fetch_latest_data.return_value = [{"timestamp": 1, "value": 2}]
    df = get_latest_data_frame(Mock())
    assert df.to_dict() == {"timestamp": {0: 1}, "value": {0: 2}}


def test_get_pie_fig():
    fig = get_pie_fig(df)
    for i, v in enumerate(fig["data"][0]["values"]):
        assert v == [4, 2, 1][i]
    for i, v in enumerate(fig["data"][0]["labels"]):
        assert v == ["A", "B", "C"][i]


def test_get_line_fig():
    df = pd.DataFrame({"timestamp": [1, 2, 3], "value": [4, 5, 6]})
    fig = get_line_fig(df)
    for i, v in enumerate(fig["data"][0]["x"]):
        assert v == [1, 2, 3][i]
    for i, v in enumerate(fig["data"][0]["y"]):
        assert v == [4, 5, 6][i]


def test_get_page_layout():
    fig_mock = Mock()
    layout = get_page_layout("id", "Dashboard", fig_mock)
    assert isinstance(layout, html.Div)
