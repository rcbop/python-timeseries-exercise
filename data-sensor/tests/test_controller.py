from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
from sensor.controller import PayloadSerializer, SensorController
from sensor.model import (MQTTConfig, SensorArea, SensorConfig, SensorData,
                          SensorMetadata, SensorType)


@pytest.mark.unit
class TestSensorController:
    @pytest.fixture
    def mqtt_config(self) -> MQTTConfig:
        return MQTTConfig(host="localhost", port=1883)

    @pytest.fixture
    def sensor_config(self, mqtt_config: MQTTConfig) -> SensorConfig:
        return SensorConfig(
            area=SensorArea.BATHROOM,
            type=SensorType.TEMPERATURE,
            mqtt=mqtt_config,
            read_interval_seconds=1
        )

    @pytest.fixture
    def fix_mqtt_client(self) -> MagicMock:
        mqtt_controller_mock = MagicMock()
        mqtt_controller_mock.connect = Mock()
        mqtt_controller_mock.disconnect = Mock()
        mqtt_controller_mock.publish = Mock()
        mqtt_controller_mock.loop_start = Mock()
        return mqtt_controller_mock

    @pytest.fixture
    def fix_sensor_data(self) -> SensorData:
        return SensorData(
            metadata=SensorMetadata(
                area=SensorArea.BATHROOM,
                type=SensorType.TEMPERATURE),
            value=1.0,
            timestamp=datetime.utcnow()
        )

    @pytest.fixture
    def fix_random_gen(self, fix_sensor_data: SensorData) -> Mock:
        random_gen = Mock()
        random_gen.generate_sensor_data = Mock(return_value=fix_sensor_data)
        return random_gen

    @pytest.fixture
    def fix_sensor_controller(self, sensor_config: SensorConfig, fix_random_gen: Mock, fix_mqtt_client: MagicMock) -> SensorController:
        return SensorController(
            logger=MagicMock(),
            sensor_config=sensor_config,
            random_gen=fix_random_gen,
            mqtt_client=fix_mqtt_client
        )

    def test_get_topic_name(self,
                            fix_sensor_controller: SensorController):
        topic_name = fix_sensor_controller.get_topic_name()
        assert topic_name == "sensors/TEMPERATURE/BATHROOM"

    @patch("sensor.controller.time.sleep")
    def test_run(self, sleep_mock: Mock, fix_sensor_data: SensorData, fix_mqtt_client: MagicMock, fix_sensor_controller: SensorController, fix_random_gen: Mock):
        should_run = Mock(side_effect=[True, False])
        topic_name = fix_sensor_controller.get_topic_name()
        fix_sensor_controller.run(should_run)
        fix_random_gen.generate_sensor_data.assert_called_once()
        fix_mqtt_client.connect.assert_called_once()
        serialized_data = PayloadSerializer.serialize(fix_sensor_data)
        fix_mqtt_client.publish.assert_called_once_with(
            topic_name, serialized_data)
        fix_mqtt_client.disconnect.assert_called_once()
        sleep_mock.assert_called_once_with(1)
