"""insert generator module."""
import json
import time
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from logging import Logger
from typing import Callable

from kink import inject
from paho.mqtt import client as mqtt
from paho.mqtt.client import Client
from sensor.generator import IRandomDataGenerator
from sensor.model import SensorConfig, SensorData

KEEP_ALIVE = 60


class SensorDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.name
        return json.JSONEncoder.default(self, obj)


class PayloadSerializer:
    @staticmethod
    def serialize(data: SensorData) -> str:
        return json.dumps(asdict(data), cls=SensorDataEncoder)


@inject
class SensorController:
    def __init__(self,
                 logger: Logger,
                 sensor_config: SensorConfig,
                 random_gen: IRandomDataGenerator,
                 mqtt_client: Client = Client()) -> None:
        self.__logger = logger
        self.__sensor_config = sensor_config
        self.__random_gen = random_gen
        self.__mqtt_client = mqtt_client

    def get_topic_name(self) -> str:
        return f"sensors/{self.__sensor_config.type.name}/{self.__sensor_config.area.name}"

    def __on_publish(self, client, userdata, mid):
        self.__logger.info("published message with id: %s", mid)

    def __on_connect(self, client, userdata, flags, rc):
        self.__logger.info("%s:%s:%s:%s", client, userdata, flags, rc)
        if rc != mqtt.MQTT_ERR_SUCCESS:
            self.__logger.error("failed to connect to mqtt broker")
            return
        self.__logger.info("connected to mqtt broker")

    def __on_disconnect(self, client, userdata, rc):
        if rc != mqtt.MQTT_ERR_SUCCESS:
            self.__logger.error("failed to disconnect from mqtt broker")
            return
        self.__logger.info("disconnected from mqtt broker")

    def __setup_mqtt_client(self):
        self.__logger.info("connecting to mqtt broker %s:%s",
                           self.__sensor_config.mqtt.host, self.__sensor_config.mqtt.port)
        self.__mqtt_client.connect(
            self.__sensor_config.mqtt.host,
            self.__sensor_config.mqtt.port, KEEP_ALIVE)

        self.__mqtt_client.on_connect = self.__on_connect
        self.__mqtt_client.on_disconnect = self.__on_disconnect
        self.__mqtt_client.on_publish = self.__on_publish

    def run(self, should_run: Callable[[], bool] = lambda: True):
        self.__setup_mqtt_client()
        self.__mqtt_client.loop_start()

        while should_run():
            self.__logger.info("starting to insert data points")
            sensor_data = self.__random_gen.generate_sensor_data()
            topic_name = self.get_topic_name()
            self.__logger.info(
                "[%s] sending data to mqtt broker on topic: %s", sensor_data.metadata.id,
                topic_name)
            self.__mqtt_client.publish(
                topic_name, PayloadSerializer.serialize(sensor_data))
            time.sleep(self.__sensor_config.read_interval_seconds)

        self.__mqtt_client.loop_stop()
        self.__mqtt_client.disconnect()
