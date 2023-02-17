import os
from dataclasses import dataclass

import pandas as pd
import pymongo
import streamlit as st
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

def get_collection(cfg: DBConfig) -> Collection:
    """Returns the MongoDB collection."""
    client = pymongo.MongoClient(cfg.mongo_uri)
    db = client[cfg.db_name]
    return db[cfg.collection_name]

st.text('Loading data...')

db_cfg = DBConfig(
    mongo_uri=os.getenv("MONGO_URI", DEFAULT_MONGO_URI),
    db_name=os.getenv("MONGO_DB_NAME", DEFAULT_MONGO_DB_NAME),
    collection_name=os.getenv("MONGO_COLLECTION_NAME", DEFAULT_COLLECTION_NAME)
)
collection = get_collection(db_cfg)
cursor = collection.find().sort(
        [("timestamp", pymongo.DESCENDING)]).limit(100)
data = list(cursor)

st.text('Done loading data!')

st.title('Temperature Data')

df = pd.DataFrame(data)
df[['type', 'area', 'uuid']] = df['metadata'].apply(lambda x: pd.Series(x))
df.drop(columns=["metadata"], inplace=True)

print(df.head())

gk = df.groupby("uuid")
for uuid, group in gk:
    print(uuid)
    print(group.head())
    st.subheader(f"Sensor {uuid}")
    st.line_chart(group, x="timestamp", y="value")
