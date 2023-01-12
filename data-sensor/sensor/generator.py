"""random data generator module."""
from datetime import datetime
from random import uniform
from typing import Protocol

from kink import inject
from sensor.model import RandomConfig, SensorData, SensorMetadata


class IRandomDataGenerator(Protocol):
    def generate_sensor_data(self) -> SensorData:
        ...


@inject(alias=IRandomDataGenerator)
class RandomDataGenerator:
    def __init__(self,
                 random_config: RandomConfig,
                 metadata: SensorMetadata) -> None:
        self.__config = random_config
        self.__sensor_metadata = metadata
        self.__buffer: list = [self.__generate_random_number()]

    def __generate_random_number(self) -> float:
        return uniform(self.__config.min_value, self.__config.max_value)

    def __generate_approximate_random_number(self) -> float:
        """ Generate a random number between min_value and max_value.
        The number will be close to the average of the last buffer numbers. """
        avg = sum(self.__buffer) / len(self.__buffer)
        new_value = uniform(max(avg - 1, self.__config.min_value),
                            min(avg + 1, self.__config.max_value))

        new_value = round(new_value, 3)
        self.__buffer.append(new_value)
        # slice the list to keep only the last buffer_size elements, sliding the window
        self.__buffer = self.__buffer[-self.__config.max_buffer_size:]
        return new_value

    def generate_sensor_data(self) -> SensorData:
        return SensorData(
            value=self.__generate_approximate_random_number(),
            timestamp=datetime.now(),
            metadata=self.__sensor_metadata
        )
