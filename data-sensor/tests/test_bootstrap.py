from unittest.mock import patch

import pytest
from sensor.bootstrap import (get_logger, get_random_config, get_sensor_config,
                              get_sensor_metadata)
from sensor.model import SensorArea, SensorType


@pytest.mark.unit
class TestBootstrap:
    def test_get_logger(self):
        logger = get_logger()
        assert logger is not None
        assert logger.name == "sensor"

    def test_get_logger_invalid_level(self):
        with patch("sensor.bootstrap.os.environ.get", return_value="XXX"):
            with pytest.raises(ValueError):
                get_logger()

    def test_random_config_default(self):
        config = get_random_config()
        assert config.min_value == -1
        assert config.max_value == 100
        assert config.max_buffer_size == 5

    def test_random_config_change_buffer(self):
        with patch("sensor.bootstrap.os.environ.get", side_effect=["2", "20", "10"]):
            config = get_random_config()
            assert config.min_value == 2
            assert config.max_value == 20
            assert config.max_buffer_size == 10

    def test_random_config_error(self):
        with patch("sensor.bootstrap.os.environ.get", return_value="XXX"):
            with pytest.raises(ValueError):
                get_random_config()

    def test_get_sensor_metadata(self):
        metadata = get_sensor_metadata(
            SensorArea.LIVING_ROOM, SensorType.TEMPERATURE)
        assert metadata.area.name == "LIVING_ROOM"
        assert metadata.type.name == "TEMPERATURE"

    def test_get_sensor_config_default(self):
        config = get_sensor_config()
        assert config.area.name == "LIVING_ROOM"
        assert config.type.name == "TEMPERATURE"
        assert config.read_interval_seconds == 1
        assert config.mqtt.host == "localhost"
        assert config.mqtt.port == 1883

    def test_get_sensor_config_change_port(self):
        with patch("sensor.bootstrap.os.environ.get", side_effect=["KITCHEN", "HUMIDITY", "2", "localhost", "1234"]):
            config = get_sensor_config()
            assert config.area.name == "KITCHEN"
            assert config.type.name == "HUMIDITY"
            assert config.read_interval_seconds == 2
            assert config.mqtt.host == "localhost"
            assert config.mqtt.port == 1234

    def test_get_sensor_config_error(self):
        with patch("sensor.bootstrap.os.environ.get", side_effect=["<<INVALID>>", "TEMPERATURA", "12xinvalid"]):
            with pytest.raises(ValueError):
                get_sensor_config()
