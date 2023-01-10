import logging
import os
from logging import Logger

from consumer.db import DBBootstrap, SensorDAO
from consumer.model import DBConfig, MQTTConfig
from kink import di
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

DEFAULT_MONGO_URI = "mongodb://localhost:27017/"
DEFAULT_DB_NAME = "timeseries-visualization-test"
DEFAULT_COLLECTION_NAME = "sensor_data"

DEFAULT_MQTT_HOST = "localhost"
DEFAULT_MQTT_PORT = 1883
DEFAULT_MQTT_TOPIC_PREFIX = "sensors/"


def get_logger() -> Logger:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("data-consumer")
    all_levels = logging.getLevelNamesMapping()
    log_level = os.getenv("LOG_LEVEL", "INFO")
    if log_level not in all_levels:
        raise ValueError(f"invalid log level: {log_level}")
    logger.setLevel(all_levels[log_level])
    return logger


def get_db_config() -> DBConfig:
    mongo_uri = os.getenv("MONGO_URI", DEFAULT_MONGO_URI)
    db_name = os.getenv("MONGO_DB_NAME", DEFAULT_DB_NAME)
    collection = os.getenv(
        "MONGO_COLLECTION_NAME", DEFAULT_COLLECTION_NAME)
    return DBConfig(
        db_uri=mongo_uri,
        db_name=db_name,
        collection=collection
    )


def get_mqtt_config() -> MQTTConfig:
    mqtt_host = os.getenv("MQTT_HOST", DEFAULT_MQTT_HOST)
    mqtt_port = int(os.getenv("MQTT_PORT", DEFAULT_MQTT_PORT))
    mqtt_topic_prefix = os.getenv(
        "MQTT_TOPIC_PREFIX", DEFAULT_MQTT_TOPIC_PREFIX)
    return MQTTConfig(
        host=mqtt_host,
        port=mqtt_port,
        topic=mqtt_topic_prefix
    )


def bootstrap_di():
    di[Logger] = get_logger()
    db_config = get_db_config()
    di[DBConfig] = db_config
    di[MQTTConfig] = get_mqtt_config()
    di[MongoClient] = MongoClient(host=db_config.db_uri)
    db_init = DBBootstrap()
    database: Database = db_init.init()
    di[Collection] = database[db_config.collection]
    di[SensorDAO] = SensorDAO()
