"""bootstrap dependency injection autowiring."""
import logging
import os
from logging import Logger

from api.temperature.service import ITemperatureService
from kink import di
from pymongo import MongoClient
from pymongo.database import Database

DEFAULT_MONGO_URI = "mongodb://localhost:27017"
DEFAULT_MONGO_DB_NAME = "timeseries-visualization-test"
DEFAULT_MONGO_TEMP_COLLECTION_NAME = "temperature"


def bootstrap_di():
    di[Logger] = logging.getLogger("data-api")
    mongo_uri = os.getenv("MONGO_URI", DEFAULT_MONGO_URI)
    mongo_db_name = os.getenv("MONGO_DB_NAME", DEFAULT_MONGO_DB_NAME)
    temp_collection_name = os.getenv(
        "MONGO_COLLECTION_NAME", DEFAULT_MONGO_TEMP_COLLECTION_NAME)
    mongo_client = MongoClient(mongo_uri)
    di[Database] = mongo_client[mongo_db_name]
    di["temp_collection"] = di[Database][temp_collection_name]
