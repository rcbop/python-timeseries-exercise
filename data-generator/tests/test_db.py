from unittest.mock import ANY, MagicMock, Mock

import pytest
from generator.db import (DBConfig, TemperatureSensorDAO,
                          TimeseriesDBBootstrap)
from generator.model import SensorArea, SensorData

@pytest.mark.unit
class TestDBModule:
    @pytest.fixture
    def fix_db_config(self) -> DBConfig:
        return DBConfig(
            db_uri="test-host",
            db_name="test-db",
            collection_name="test-timeseries"
        )

    def test_init(self, fix_db_config: DBConfig):
        client_mock = MagicMock()
        db_mock = MagicMock()
        db_mock.list_collection_names = Mock(return_value=[])
        db_mock.create_collection = Mock()
        collection_mock = MagicMock()
        db_mock.__getitem__ = Mock(return_value=collection_mock)
        client_mock.__getitem__ = Mock(return_value=db_mock)
        initializer = TimeseriesDBBootstrap(
            db_config=fix_db_config,
            mongo_client=client_mock,
            logger=MagicMock())
        initializer.init()

        db_mock.list_collection_names.assert_called_once()
        db_mock.create_collection.assert_called_once_with(fix_db_config.collection_name, timeseries={
            "timeField": "timestamp"
        })

    @pytest.mark.parametrize("temperature,area", [
        (1.0, SensorArea.KITCHEN),
        (13.0, SensorArea.BEDROOM),
        (25.2, SensorArea.LIVING_ROOM)
    ])
    def test_temperature_sensor(self, temperature: float, area: SensorArea):
        collection_mock = Mock()
        collection_mock.insert_one = Mock()
        sensor_dao = TemperatureSensorDAO(MagicMock(), collection_mock)
        sensor_dao.insert_data(SensorData(area, temperature))
        collection_mock.insert_one.assert_called_once_with({
            "metadata": {
                "sensor_area": area.name,
            },
            "temperature": temperature,
            "timestamp": ANY
        })
