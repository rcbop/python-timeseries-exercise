"""bootstrap dependency injection autowiring."""
import logging
import os
from logging import Logger

from generator.db import DBConfig, TemperatureSensorDAO, TimeseriesDBBootstrap
from generator.model import SensorArea
from generator.random_sensor import RandomSensorDataGenerator
from kink import di
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

DEFAULT_MONGO_URI = "mongodb://localhost:27017/"
DEFAULT_DB_NAME = "timeseries-visualization-test"
DEFAULT_COLLECTION_NAME = "temperature"


def bootstrap_db_config() -> DBConfig:
    mongo_uri = os.getenv("MONGO_URI", DEFAULT_MONGO_URI)
    db_name = os.getenv("MONGO_DB_NAME", DEFAULT_DB_NAME)
    collection_name = os.getenv("MONGO_COLLECTION_NAME", DEFAULT_COLLECTION_NAME)
    return DBConfig(
        db_uri=mongo_uri,
        db_name=db_name,
        collection_name=collection_name
    )


def bootstrap_di() -> None:
    db_config = bootstrap_db_config()
    di[DBConfig] = db_config
    logger = logging.getLogger("random-data-generator")
    di[Logger] = logger
    di["insert_interval_seconds"] = int(os.getenv("INSERT_INTERVAL", "2"))
    logger.info("connecting to database")
    di[MongoClient] = MongoClient(host=db_config.db_uri)
    db_init = TimeseriesDBBootstrap()

    database: Database = db_init.init()
    # temp collection
    di[Collection] = database[db_config.collection_name]

    di[TemperatureSensorDAO] = TemperatureSensorDAO()
    di[RandomSensorDataGenerator] = RandomSensorDataGenerator(sensors=[
        SensorArea.LIVING_ROOM,
        SensorArea.KITCHEN,
        SensorArea.BEDROOM,
        SensorArea.BATHROOM
    ])
