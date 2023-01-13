"""bootstrap dependency injection autowiring."""
import logging
import os
from dataclasses import dataclass
from logging import Logger

from api.constants import (DEFAULT_MONGO_DB_NAME,
                           DEFAULT_MONGO_TS_COLLECTION_NAME, DEFAULT_MONGO_URI)
from kink import di
from pymongo import MongoClient
from pymongo.database import Database


@dataclass
class EnvConfig:
    mongo_uri: str
    mongo_db_name: str
    mongo_collection_name: str


def get_env_config() -> EnvConfig:
    mongo_uri = os.getenv("MONGO_URI", DEFAULT_MONGO_URI)
    mongo_db_name = os.getenv("MONGO_DB_NAME", DEFAULT_MONGO_DB_NAME)
    mongo_collection_name = os.getenv(
        "MONGO_COLLECTION_NAME", DEFAULT_MONGO_TS_COLLECTION_NAME)
    return EnvConfig(mongo_uri, mongo_db_name, mongo_collection_name)


def bootstrap_di():
    di[Logger] = logging.getLogger("data-api")
    config = get_env_config()
    mongo_client = MongoClient(config.mongo_uri)
    di[Database] = mongo_client[config.mongo_db_name]
    di["sensors_collection"] = di[Database][config.mongo_collection_name]
