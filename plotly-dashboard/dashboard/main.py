import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pymongo
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


def main():
    # Connect to the MongoDB database
    DEFAULT_MONGO_URI = "mongodb://localhost:27017/"
    DEFAULT_MONGO_DB_NAME = "timeseries-visualization-test"
    DEFAULT_COLLECTION_NAME = "temperature"

    mongo_uri = os.getenv("MONGO_URI", DEFAULT_MONGO_URI)
    db_name = os.getenv("MONGO_DB_NAME", DEFAULT_MONGO_DB_NAME)
    collection_name = os.getenv("MONGO_COLLECTION_NAME", DEFAULT_COLLECTION_NAME)

    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Query the last 100 temperature data points from the collection
    temperature_data = list(collection.find().sort([("timestamp", pymongo.DESCENDING)]).limit(100))

    # Create a DataFrame from the temperature data
    df = pd.DataFrame(temperature_data)

    # Create a linear plot of the temperature timeseries
    line_fig = px.line(df, x="timestamp", y="temperature", title="Temperature Timeseries")

    # Calculate the percentage distribution of the sensor_area
    df["sensor_area"] = df["metadata"].apply(lambda x: x["sensor_area"])
    sensor_area_counts = df["sensor_area"].value_counts()
    sensor_area_percentages = sensor_area_counts / sensor_area_counts.sum() * 100

    # Create a pie chart of the sensor_area distribution
    pie_graph = go.Pie(values=sensor_area_counts,
                labels=sensor_area_percentages.index.to_list(),
                text=sensor_area_percentages.round(1).astype(str) + "%",
                title="Sensor Area Distribution")

    pie_fig = {
        "data": [pie_graph],
        "layout": {
            "title": {
                "text": "Sensor Area Distribution"
            }
        }
    }

    page_1_layout = html.Div([
        html.H1("Page 1"),
        dcc.Graph(figure=line_fig),
    ])

    page_2_layout = html.Div([
        html.H1("Page 2"),
        dcc.Graph(figure=pie_fig),
    ])

    tabs = dcc.Tabs(id="tabs", value="page_1", children=[
        dcc.Tab(label="Page 1", value="page_1", children=page_1_layout),
        dcc.Tab(label="Page 2", value="page_2", children=page_2_layout),
    ])

    app = Dash()

    app.layout = html.Div([
        tabs
    ])

    app.run(host="0.0.0.0", port=8050, debug=True)

if __name__ == "__main__":
    main()
