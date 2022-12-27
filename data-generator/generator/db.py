"""database access module."""
from dataclasses import dataclass
from datetime import datetime
from logging import Logger

from generator.model import SensorData
from kink import inject
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult


@dataclass
class DBConfig:
    db_uri: str
    db_name: str
    collection_name: str


@inject
class TimeseriesDBBootstrap:
    def __init__(self,
                 db_config: DBConfig,
                 mongo_client: MongoClient,
                 logger: Logger):
        self.__db_config = db_config
        self.__mongo_client = mongo_client
        self.__logger = logger

    def init(self) -> Database:
        database = self.__mongo_client[self.__db_config.db_name]
        self.__init_collection_if_not_exists(database)
        return database

    def __init_collection_if_not_exists(self, database: Database) -> None:
        collection_name = self.__db_config.collection_name
        if collection_name not in database.list_collection_names():
            self.__logger.info(
                "creating timeseries collection: %s", collection_name)
            database.create_collection(collection_name, timeseries={
                                       "timeField": "timestamp"})


@inject
class TemperatureSensorDAO:
    def __init__(self, logger: Logger, collection: Collection) -> None:
        self.__logger = logger
        self.__collection = collection

    def insert_data(self, sensor_data: SensorData):
        insert_result: InsertOneResult = self.__collection.insert_one({
            "metadata": {
                "sensor_area": sensor_data.sensor_area.name,
            },
            "temperature": sensor_data.temperature,
            "timestamp": datetime.utcnow()
        })
        self.__logger.info("inserted data: %s", insert_result.inserted_id)
