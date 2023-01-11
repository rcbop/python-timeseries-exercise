from dataclasses import asdict
from unittest.mock import MagicMock, Mock, patch

import pytest
from consumer.db import DBBootstrap, SensorDAO, SensorDataParser


@pytest.mark.unit
class TestDBModule:
    def test_sensor_data_parser(self):
        raw_data = {
            "value": 1.0,
            "timestamp": "2021-01-01T00:00:00",
            "metadata": {
                "area": "kitchen",
                "type": "temperature",
                "uuid": "1234"
            }
        }
        sensor_data = SensorDataParser.parse_raw_data(raw_data)
        assert sensor_data.value == 1.0
        assert sensor_data.timestamp.isoformat() == "2021-01-01T00:00:00"
        assert sensor_data.metadata.area == "kitchen"
        assert sensor_data.metadata.type == "temperature"
        assert sensor_data.metadata.uuid == "1234"

    def test_sensor_dao(self):
        raw_data = {
            "value": 1.0,
            "timestamp": "2021-01-01T00:00:00",
            "metadata": {
                "area": "kitchen",
                "type": "temperature",
                "uuid": "1234"
            }
        }
        logger = Mock()
        collection = Mock()
        sensor_dao = SensorDAO(logger, collection)
        sensor_dao.insert_data(raw_data)
        sensor_data = SensorDataParser.parse_raw_data(raw_data)
        logger.info.assert_called_once()
        collection.insert_one.assert_called_once_with(asdict(sensor_data))

    def test_db_bootstrap(self):
        db_config = Mock()
        mongo_client = MagicMock()
        mongo_client.__getattribute__ = MagicMock(return_value=MagicMock())
        logger = Mock()
        db_bootstrap = DBBootstrap(db_config, mongo_client, logger)
        db_bootstrap.init()
        mongo_client[db_config.db_name].create_collection.assert_called_once()
