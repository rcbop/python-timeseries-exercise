import os
import asyncio
from dataclasses import dataclass
from datetime import datetime

import pymongo
from nicegui import ui
from pymongo.collection import Collection

DEFAULT_MONGO_URI = "mongodb://localhost:27017/"
DEFAULT_MONGO_DB_NAME = "timeseries-visualization-test"
DEFAULT_COLLECTION_NAME = "sensor_data"

@dataclass
class DBConfig:
    mongo_uri: str
    db_name: str
    collection_name: str

def get_collection(cfg: DBConfig) -> Collection:
    """Returns the MongoDB collection."""
    client = pymongo.MongoClient(cfg.mongo_uri)
    db = client[cfg.db_name]
    return db[cfg.collection_name]

def main():
    db_cfg = DBConfig(
        mongo_uri=os.getenv("MONGO_URI", DEFAULT_MONGO_URI),
        db_name=os.getenv("MONGO_DB_NAME", DEFAULT_MONGO_DB_NAME),
        collection_name=os.getenv("MONGO_COLLECTION_NAME", DEFAULT_COLLECTION_NAME)
    )
    collection = get_collection(db_cfg)
    def get_series() -> list[dict]:
        data = list(collection.find().sort([("timestamp", pymongo.DESCENDING)]).limit(50))
        # this returns a list of dicts, each dict has a timestamp and a value

        series = {}
        for item in data:
            if item['metadata']['uuid'] not in series:
                series[item['metadata']['uuid']] = []
            series[item['metadata']['uuid']].append(item)
        allSeries = []
        for sensor_uuid, items in series.items():
            data = []
            for item in items:
                data.append([datetime.timestamp(item['timestamp']), item['value']])
            allSeries.append({'name': sensor_uuid, 'data': data})
        return allSeries

    chart = ui.chart({
        'title': 'Temperature over time',
        'chart': {'type': 'line'},
        'xAxis': {'type': 'datetime', 'title': {'text': 'Time'}},
        'yAxis': {'type': 'linear', 'title': {'text': 'Temperature'}},
        'series': get_series(),
    }).classes('w-full h-full')

    async def update():
        ui.notify('Updating...')
        await asyncio.sleep(1)
        chart.options['series'] = get_series()
        chart.update()
        ui.notify('Updated!')

    ui.button('Update', on_click=update)

    ui.run(port=8060)


if __name__ in {"__main__", "__mp_main__"}:
    main()
