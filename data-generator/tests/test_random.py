"""test random module."""
import pytest
from generator.random_sensor import RandomSensorDataGenerator
from generator.model import SensorArea,SensorData

@pytest.mark.unit
class TestRandomModule:
    available_sensors: list[SensorArea] = [
        SensorArea.BEDROOM,
        SensorArea.KITCHEN
    ]

    @pytest.fixture
    def fix_random_generator(self) -> RandomSensorDataGenerator:
        return RandomSensorDataGenerator(sensors=self.available_sensors)

    def test_generate_sensor_data(self, fix_random_generator: RandomSensorDataGenerator):
        sensor_data = fix_random_generator.generate_sensor_data()
        assert isinstance(sensor_data, SensorData)
        assert sensor_data.sensor_area in self.available_sensors
        assert isinstance(sensor_data.temperature, float)

    def test_generate_sensor_data_between_min_max(self):
        data = RandomSensorDataGenerator([SensorArea.KITCHEN], min_temp=8, max_temp=9).generate_sensor_data()
        assert data.sensor_area == SensorArea.KITCHEN
        assert data.temperature >= 8
        assert data.temperature <= 9
