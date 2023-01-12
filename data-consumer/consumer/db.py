"""database access module."""
from dataclasses import asdict
from datetime import datetime
from logging import Logger

from consumer.model import DBConfig, SensorData, SensorMetadata
from kink import inject
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult


@inject
class DBBootstrap:
    def __init__(self,
                 db_config: DBConfig,
                 mongo_client: MongoClient,
                 logger: Logger):
        self.__db_config = db_config
        self.__mongo_client = mongo_client
        self.__logger = logger

    def init(self) -> Database:
        database = self.__mongo_client[self.__db_config.db_name]
        self.__init_collections(database)
        return database

    def __init_collections(self, database: Database) -> None:
        if self.__db_config.collection not in database.list_collection_names():
            self.__logger.info(
                "creating timeseries collection: %s", self.__db_config.collection)
            database.create_collection(self.__db_config.collection, timeseries={
                "timeField": "timestamp"})


class SensorDataParser:
    @staticmethod
    def parse_raw_data(raw_data) -> SensorData:
        return SensorData(
            value=raw_data["value"],
            timestamp=datetime.fromisoformat(raw_data["timestamp"]),
            metadata=SensorMetadata(
                area=raw_data["metadata"]["area"],
                type=raw_data["metadata"]["type"],
                uuid=raw_data["metadata"]["uuid"]))


@inject
class SensorDAO:
    def __init__(self, logger: Logger, collection: Collection) -> None:
        self.__logger = logger
        self.__collection = collection

    def insert_data(self, raw_sensor_data: dict):
        sensor_data = SensorDataParser.parse_raw_data(raw_sensor_data)
        insert_result: InsertOneResult = self.__collection.insert_one(
            asdict(sensor_data))
        self.__logger.info(
            "inserted data [ id: %s ]", insert_result.inserted_id)
