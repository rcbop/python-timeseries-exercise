"""bootstrap dependency injection autowiring."""
import logging
import os
from logging import Logger
from dataclasses import dataclass
from kink import di
from pymongo import MongoClient
from pymongo.database import Database

DEFAULT_MONGO_URI = "mongodb://localhost:27017"
DEFAULT_MONGO_DB_NAME = "timeseries-visualization-test"
DEFAULT_MONGO_TEMP_COLLECTION_NAME = "temperature"


@dataclass
class EnvConfig:
    mongo_uri: str
    mongo_db_name: str
    mongo_collection_name: str


def get_env_config() -> EnvConfig:
    mongo_uri = os.getenv("MONGO_URI", DEFAULT_MONGO_URI)
    mongo_db_name = os.getenv("MONGO_DB_NAME", DEFAULT_MONGO_DB_NAME)
    mongo_collection_name = os.getenv(
        "MONGO_COLLECTION_NAME", DEFAULT_MONGO_TEMP_COLLECTION_NAME)
    return EnvConfig(mongo_uri, mongo_db_name, mongo_collection_name)


def bootstrap_di():
    di[Logger] = logging.getLogger("data-api")
    config = get_env_config()
    mongo_client = MongoClient(config.mongo_uri)
    di[Database] = mongo_client[config.mongo_db_name]
    di["temp_collection"] = di[Database][config.mongo_collection_name]
