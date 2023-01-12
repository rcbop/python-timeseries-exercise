import pytest
from sensor.generator import RandomDataGenerator
from sensor.model import RandomConfig, SensorArea, SensorMetadata, SensorType


@pytest.mark.unit
class TestRandomDataGenerator:
    @pytest.fixture
    def random_config(self):
        return RandomConfig(min_value=0, max_value=100)

    @pytest.fixture
    def sensor_metadata(self):
        return SensorMetadata(type=SensorType.TEMPERATURE, area=SensorArea.BATHROOM)

    def test_random_data_generator(self, random_config: RandomConfig, sensor_metadata: SensorMetadata):
        data_generator = RandomDataGenerator(random_config, sensor_metadata)
        previous_value = None
        for _ in range(100):
            sensor_data = data_generator.generate_sensor_data()
            assert sensor_data.value >= random_config.min_value
            assert sensor_data.value <= random_config.max_value
            assert sensor_data.metadata == sensor_metadata
            assert sensor_data.timestamp is not None
            if previous_value is not None:
                assert pytest.approx(previous_value, 1) == sensor_data.value
            previous_value = sensor_data.value
