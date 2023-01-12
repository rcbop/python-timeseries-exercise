import logging
from unittest.mock import patch

import pytest
from consumer.bootstrap import get_db_config, get_logger, get_mqtt_config


@pytest.mark.unit
class TestBoostrap:

    def test_get_db_config(self):
        with patch("consumer.bootstrap.os") as os_mock:
            os_mock.getenv.side_effect = lambda key, default: {
                "MONGO_URI": "mongodb://localhost:27017/",
                "MONGO_DB_NAME": "timeseries-visualization-test",
                "MONGO_COLLECTION_NAME": "sensor_data"
            }.get(key, default)
            db_config = get_db_config()
            assert db_config.db_uri == "mongodb://localhost:27017/"
            assert db_config.db_name == "timeseries-visualization-test"
            assert db_config.collection == "sensor_data"

    def test_get_logger(self):
        with patch("consumer.bootstrap.logging") as logging_mock:
            with patch("consumer.bootstrap.os") as os_mock:
                logging_mock.getLevelNamesMapping.return_value = logging.getLevelNamesMapping()
                logging_mock.getLogger.return_value = logging.getLogger(
                    "data-consumer")
                os_mock.getenv.return_value = "DEBUG"
                logger = get_logger()
                logging_mock.basicConfig.assert_called_once_with(
                    level=logging_mock.INFO)
                assert logger.level == logging.DEBUG

    def test_get_logger_with_error(self):
        with patch("consumer.bootstrap.logging") as logging_mock:
            with patch("consumer.bootstrap.os") as os_mock:
                logging_mock.getLevelNamesMapping.return_value = logging.getLevelNamesMapping()
                logging_mock.getLogger.return_value = logging.getLogger(
                    "data-consumer")
                os_mock.getenv.return_value = "XXXX"
                pytest.raises(ValueError, get_logger)

    def test_get_mqtt_config(self):
        with patch("consumer.bootstrap.os") as os_mock:
            os_mock.getenv.side_effect = lambda key, default: {
                "MQTT_HOST": "localhost",
                "MQTT_PORT": 1883,
                "MQTT_TOPIC_PREFIX": "sensors/"
            }.get(key, default)
            mqtt_config = get_mqtt_config()
            assert mqtt_config.host == "localhost"
            assert mqtt_config.port == 1883
            assert mqtt_config.topic == "sensors/"
