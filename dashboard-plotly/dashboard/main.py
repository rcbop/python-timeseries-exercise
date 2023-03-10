import os
from dataclasses import dataclass

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pymongo
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas.io.json import json_normalize
from pymongo.collection import Collection

INTERVAL_MILLISECONDS = 5000
DEFAULT_MONGO_URI = "mongodb://localhost:27017/"
DEFAULT_MONGO_DB_NAME = "timeseries-visualization-test"
DEFAULT_COLLECTION_NAME = "sensor_data"


@dataclass
class DBConfig:
    mongo_uri: str
    db_name: str
    collection_name: str


def fetch_latest_data(collection: Collection, limit: int = 100) -> list[dict]:
    """Fetches the last given X temperature data points from the collection."""
    data = collection.find().sort(
        [("timestamp", pymongo.DESCENDING)]).limit(limit)
    return list(data)


def calculate_percentage_distribution(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Calculates the percentage distribution of the sensor_area column."""
    sensor_area_counts = df["area"].value_counts()
    sensor_area_percentages = sensor_area_counts / sensor_area_counts.sum() * 100
    return sensor_area_counts, sensor_area_percentages


def get_latest_data_frame(collection: Collection) -> pd.DataFrame:
    """Updates the DataFrame with the latest temperature data points."""
    data = fetch_latest_data(collection)
    df = pd.DataFrame(data)
    df[['type', 'area', 'uuid']] = df['metadata'].apply(lambda x: pd.Series(x))
    df.drop(columns=["metadata"], inplace=True)
    return df


def get_line_fig(df: pd.DataFrame) -> go.Figure:
    """Creates a line plot of the sensor data timeseries."""
    return px.line(df,
                   x="timestamp",
                   y="value",
                   color="uuid",
                   hover_name="type",
                   title="Sensor Data Timeseries")


def get_pie_graph(df: pd.DataFrame) -> go.Pie:
    """Creates a pie chart of the sensor_area distribution."""
    sensor_area_counts, sensor_area_percentages = calculate_percentage_distribution(
        df)
    return go.Pie(values=sensor_area_counts,
                  labels=sensor_area_percentages.index.to_list(),
                  hoverinfo="label+percent",
                  hoverlabel={"bgcolor": "black", "bordercolor": "black", "font": {
                      "family": "Arial", "size": 16, "color": "white"}},
                  title="Sensor Area Distribution")


def get_pie_fig(df: pd.DataFrame) -> go.Figure:
    """Creates a pie chart figure of the sensor_area distribution."""
    pie_graph = get_pie_graph(df)
    return go.Figure(data=[pie_graph], layout={"title": {"text": "Sensor Area Distribution"}})


def get_collection(cfg: DBConfig) -> Collection:
    """Returns the MongoDB collection."""
    client = pymongo.MongoClient(cfg.mongo_uri)
    db = client[cfg.db_name]
    return db[cfg.collection_name]


def get_page_layout(page_id: str, page_title: str, page_content: dict) -> html.Div:
    """Returns the layout of a page."""
    return html.Div([
        html.H1(page_title),
        dcc.Graph(id=page_id, figure=page_content),
    ])


def get_app_layout(all_tabs: list[dcc.Tab]) -> html.Div:
    return html.Div([
        dcc.Interval(
            id="interval-component",
            interval=INTERVAL_MILLISECONDS,
            n_intervals=0
        ),
        dcc.Tabs(id="tabs", value="page_1", children=all_tabs),
    ])


def get_mongo_db_config() -> DBConfig:
    mongo_uri = os.getenv("MONGO_URI", DEFAULT_MONGO_URI)
    db_name = os.getenv("MONGO_DB_NAME", DEFAULT_MONGO_DB_NAME)
    collection_name = os.getenv(
        "MONGO_COLLECTION_NAME", DEFAULT_COLLECTION_NAME)
    return DBConfig(mongo_uri, db_name, collection_name)


def get_page_1_layout(df: pd.DataFrame) -> html.Div:
    """Returns the layout of page 1."""
    line_fig = get_line_fig(df)
    return get_page_layout("line-plot", "Sensor Data Over Time", line_fig)


def get_page_2_layout(df: pd.DataFrame) -> html.Div:
    """Returns the layout of page 2."""
    pie_fig = get_pie_fig(df)
    return get_page_layout("pie-chart", "Sensor Area Distribution", pie_fig)


def setup_dash_app(tabs: list[dcc.Tab], collection: Collection) -> Dash:
    app = Dash()

    app.layout = get_app_layout(all_tabs=tabs)

    # Callback function to update the plot data
    @app.callback(
        Output("line-plot", "figure"),
        [Input("interval-component", "n_intervals")]
    )
    def update_plot(n_intervals):
        df = get_latest_data_frame(collection)
        return get_line_fig(df)

    # Callback function to update the pie chart data
    @app.callback(
        Output("pie-chart", "figure"),
        [Input("interval-component", "n_intervals")]
    )
    def update_pie_chart(n_intervals):
        df = get_latest_data_frame(collection)
        return get_pie_fig(df)
    return app


def main():
    collection = get_collection(get_mongo_db_config())

    df = get_latest_data_frame(collection)
    page_1_layout = get_page_1_layout(df)
    page_2_layout = get_page_2_layout(df)

    app = setup_dash_app(tabs=[
        dcc.Tab(label="Page 1", value="page_1", children=page_1_layout),
        dcc.Tab(label="Page 2", value="page_2", children=page_2_layout),
    ], collection=collection)

    app.run(host="0.0.0.0", port=8050, debug=True)


if __name__ == "__main__":
    main()
