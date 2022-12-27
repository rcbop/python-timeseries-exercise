"""test insert module."""
from unittest.mock import MagicMock, Mock, patch

import pytest
from generator.insert import InsertGenerator
from generator.model import SensorData, SensorArea


@pytest.mark.unit
class TestInsertGeneratorModule:
    class RandomGenMock(Mock):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def generate_sensor_data(self) -> SensorData:
            return SensorData(sensor_area=SensorArea.KITCHEN, temperature=17.8)

    @pytest.fixture
    def fix_random_gen(self) -> Mock:
        return self.RandomGenMock()

    @patch("generator.insert.time.sleep")
    def test_insert_generator_module(self,
                                     sleep_mock: Mock,
                                     fix_random_gen: RandomGenMock):
        fix_temp_dao = Mock()
        fix_temp_dao.insert_data = Mock()
        insert_generator = InsertGenerator(
            MagicMock(), fix_temp_dao, fix_random_gen, 1)
        should_mock = Mock(side_effect=[True, False])

        insert_generator.run(should_run=should_mock)

        generated_value = fix_random_gen.generate_sensor_data()

        fix_temp_dao.insert_data.assert_called_once_with(generated_value)
        sleep_mock.assert_called_once_with(1)
