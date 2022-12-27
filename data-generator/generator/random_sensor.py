"""random data generator module."""
from random import randint, uniform

from generator.model import SensorArea, SensorData


class RandomSensorDataGenerator:
    def __init__(self,
                 sensors: list[SensorArea],
                 min_temp: float = 0.0,
                 max_temp: float = 40.0) -> None:
        self.__sensors = sensors
        self.__min_temp = min_temp
        self.__max_temp = max_temp

    def __get_random_sensor_area(self) -> SensorArea:
        return self.__sensors[randint(0, len(self.__sensors) - 1)]

    def generate_sensor_data(self) -> SensorData:
        return SensorData(
            sensor_area=self.__get_random_sensor_area(),
            temperature=uniform(self.__min_temp, self.__max_temp)
        )
