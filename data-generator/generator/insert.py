"""insert generator module."""
import time
from logging import Logger
from typing import Callable

from generator.db import TemperatureSensorDAO
from generator.random_sensor import RandomSensorDataGenerator
from kink import inject

@inject
class InsertGenerator:
    def __init__(self,
                 logger: Logger,
                 temperature_dao: TemperatureSensorDAO,
                 random_gen: RandomSensorDataGenerator,
                 insert_interval_seconds: int) -> None:
        self.__logger = logger
        self.__temperature_dao = temperature_dao
        self.__random_gen = random_gen
        self.__insert_interval_seconds = insert_interval_seconds

    def run(self, should_run: Callable[[], bool] = lambda: True):
        self.__logger.info("starting to insert data points")

        while should_run():
            data = self.__random_gen.generate_sensor_data()
            self.__temperature_dao.insert_data(data)
            time.sleep(self.__insert_interval_seconds)
