"""bootstrap dependency injection autowiring."""
import logging
import os
from logging import Logger

import paho.mqtt.client as mqtt
from kink import di
from sensor.controller import SensorController
from sensor.generator import RandomDataGenerator
from sensor.model import (MQTTConfig, RandomConfig, SensorArea, SensorConfig,
                          SensorMetadata, SensorType)


def get_logger() -> Logger:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("sensor")
    all_levels = logging.getLevelNamesMapping()
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    if log_level not in all_levels.keys():
        raise ValueError(f"invalid log level: {log_level}")
    logger.setLevel(all_levels[log_level])
    return logger


def get_random_config() -> RandomConfig:
    return RandomConfig(
        min_value=float(os.getenv("MIN_VALUE", "-1")),
        max_value=float(os.getenv("MAX_VALUE", "100")),
        max_buffer_size=int(os.getenv("MAX_BUFFER_SIZE", "5"))
    )


def get_sensor_metadata(area_enum: SensorArea, type_enum: SensorType) -> SensorMetadata:
    return SensorMetadata(
        area=area_enum,
        type=type_enum,
    )


def get_sensor_config() -> SensorConfig:
    area = os.getenv("SENSOR_AREA", "LIVING_ROOM")
    sensor_type = os.getenv("SENSOR_TYPE", "TEMPERATURE")
    area_enum = SensorArea.__members__.get(
        area.upper(), SensorArea.LIVING_ROOM)
    type_enum = SensorType.__members__.get(
        sensor_type.upper(), SensorType.TEMPERATURE)
    read_interval_seconds = int(os.getenv("READ_INTERVAL_SECONDS", "1"))
    return SensorConfig(
        area=area_enum,
        type=type_enum,
        read_interval_seconds=read_interval_seconds,
        mqtt=MQTTConfig(
            os.getenv("MQTT_HOST", "localhost"),
            int(os.getenv("MQTT_PORT", "1883")),
        )
    )


def bootstrap_di() -> None:
    di[mqtt.Client] = mqtt.Client()
    di[Logger] = get_logger()
    di[RandomConfig] = get_random_config()
    di[SensorConfig] = get_sensor_config()
    di[SensorMetadata] = get_sensor_metadata(
        di[SensorConfig].area, di[SensorConfig].type)
    di[RandomDataGenerator] = RandomDataGenerator()
    di[SensorController] = SensorController(
        di[Logger],
        di[SensorConfig],
        di[RandomDataGenerator],
    )
