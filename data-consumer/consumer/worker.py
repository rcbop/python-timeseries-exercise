import json
from logging import Logger

from consumer.db import SensorDAO
from consumer.model import MQTTConfig
from kink import inject
from paho.mqtt import client as mqtt

KEEP_ALIVE = 60


@inject
class Worker:
    def __init__(self, logger: Logger, mqtt_cfg: MQTTConfig, sensor_dao: SensorDAO):
        self.__logger = logger
        self.__mqtt_cfg = mqtt_cfg
        self.__sensor_dao = sensor_dao

    def run(self):
        client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.__logger.info("Connected with result code " + str(rc))
            else:
                self.__logger.info("Bad connection Returned code=", rc)

        def on_message(client, userdata, msg):
            self.__logger.info(
                f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            parsed_payload = json.loads(msg.payload.decode())
            self.__sensor_dao.insert_data(parsed_payload)

        self.__logger.info("connecting to mqtt broker")

        client.connect(self.__mqtt_cfg.host,
                       self.__mqtt_cfg.port, KEEP_ALIVE)
        self.__logger.info(
            "starting receiving messages from mqtt topic: %s", self.__mqtt_cfg.topic + "#")
        client.subscribe(f"#")
        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_forever()
