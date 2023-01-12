from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import plotly.graph_objects as go
from dash import html
from dashboard.main import (DBConfig, calculate_percentage_distribution,
                            get_app_layout, get_collection,
                            get_latest_data_frame, get_line_fig,
                            get_page_layout, get_pie_fig, get_pie_graph, main)

mocked_result_set = [
    {
        "timestamp": "2023-01-11T17:23:13.957+0000",
        "metadata": {
            "type": "TEMPERATURE",
            "area": "BEDROOM",
            "uuid": "36bd2ee443004f1f"
        },
        "_id": "63bef081d183da4b381b1cff",
        "value": 19.901
    },
    {
        "timestamp": "2023-01-11T17:23:18.960+0000",
        "metadata": {
            "type": "HUMIDITY",
            "area": "KITCHEN",
            "uuid": "36bd2ee443004f1f"
        },
        "_id": "63bef086d183da4b381b1d13",
        "value": 40.138
    },
    {
        "timestamp": "2023-01-11T17:23:19.961+0000",
        "metadata": {
            "type": "TEMPERATURE",
            "area": "BEDROOM",
            "uuid": "36bd2ee443004f1f"
        },
        "_id": "63bef087d183da4b381b1d17",
        "value": 19.589
    }
]

expected_flattened_result_set = [
    {
        "timestamp": "2023-01-11T17:23:13.957+0000",
        "type": "TEMPERATURE",
        "area": "BEDROOM",
        "uuid": "36bd2ee443004f1f",
        "_id": "63bef081d183da4b381b1cff",
        "value": 19.901
    },
    {
        "timestamp": "2023-01-11T17:23:18.960+0000",
        "type": "HUMIDITY",
        "area": "KITCHEN",
        "uuid": "36bd2ee443004f1f",
        "_id": "63bef086d183da4b381b1d13",
        "value": 40.138
    },
    {
        "timestamp": "2023-01-11T17:23:19.961+0000",
        "type": "TEMPERATURE",
        "area": "BEDROOM",
        "uuid": "36bd2ee443004f1f",
        "_id": "63bef087d183da4b381b1d17",
        "value": 19.589
    }
]


def test_get_latest_data_frame():
    collection = Mock()
    with patch('dashboard.main.fetch_latest_data') as mocked_fetch_data:
        mocked_fetch_data.return_value = mocked_result_set
        df = get_latest_data_frame(collection)
        mocked_fetch_data.assert_called_once_with(collection)
        assert df.to_dict('records') == expected_flattened_result_set


def test_get_pie_graph():
    df = pd.DataFrame(expected_flattened_result_set)
    graph = get_pie_graph(df)
    assert isinstance(graph, go.Pie)
    assert graph.labels == ('BEDROOM', 'KITCHEN')


def test_get_line_fig():
    df = pd.DataFrame(expected_flattened_result_set)
    fig = get_line_fig(df)
    assert isinstance(fig, go.Figure)
    assert fig.data[0].mode == 'lines'
    assert all(elm in fig.data[0].y for elm in (19.901, 40.138, 19.589))
    assert all(elm in fig.data[0].x for elm in ('2023-01-11T17:23:13.957+0000',
                                                '2023-01-11T17:23:18.960+0000',
                                                '2023-01-11T17:23:19.961+0000'))


def test_get_collection():
    db_cfg = DBConfig(
        collection_name='sensor_data',
        db_name='test_db',
        mongo_uri='mongodb://localhost:27017'
    )
    with patch('dashboard.main.pymongo.MongoClient') as mocked_mongo_client:
        db = MagicMock()
        mocked_mongo_client.return_value = db
        get_collection(db_cfg)
        mocked_mongo_client.assert_called_once_with(
            'mongodb://localhost:27017')


def test_get_page_layout():
    layout = get_page_layout("test", "title", "content")
    assert isinstance(layout, html.Div)


def test_get_app_layout():
    layout = get_app_layout(MagicMock())
    assert isinstance(layout, html.Div)


def test_calculate_percentage_distribution():
    df = pd.DataFrame(expected_flattened_result_set)
    result = calculate_percentage_distribution(df)
    assert isinstance(result, tuple)
    assert result[0].to_dict() == {'BEDROOM': 2, 'KITCHEN': 1}
    assert result[1].to_dict() == {
        'BEDROOM': 66.66666666666666, 'KITCHEN': 33.33333333333333}


def test_get_pie_fig():
    df = pd.DataFrame(expected_flattened_result_set)
    fig = get_pie_fig(df)
    assert isinstance(fig, go.Figure)
    assert fig.data[0].type == 'pie'
