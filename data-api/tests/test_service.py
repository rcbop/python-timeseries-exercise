from unittest.mock import Mock

import pymongo
import pytest
from api.sensors.models import SensorData
from api.sensors.service import TemperatureService
from bson import ObjectId


def prepare_collection_mock(expected_resultset: list[dict]) -> Mock:
    temp_collection_mock = Mock()
    mock_cursor = Mock()
    mock_cursor_with_limit = Mock()
    mock_cursor.limit = Mock(return_value=mock_cursor_with_limit)
    mock_cursor_with_limit.sort = Mock(return_value=expected_resultset)
    temp_collection_mock.find = Mock(return_value=mock_cursor)
    return temp_collection_mock


def prepare_mongo_query_builder_mock(expected_query: dict) -> Mock:
    mongo_query_builder_mock = Mock()
    mongo_query_builder_mock.build_from_filters = Mock(
        return_value=expected_query)
    return mongo_query_builder_mock


@pytest.mark.parametrize("filters,limit,mongo_query,expected_result_set", [
    (
        None,
        100,
        {},
        [
            {
                "_id": ObjectId(),
                "value": 20.0,
                "timestamp": "2021-05-18T00:00:00.000Z",
                "metadata": {
                    "area": "kitchen",
                    "type": "TEMPERATURE",
                    "uuid": "1234"
                }
            }
        ]
    ),
    (
        {"limit": 1},
        1,
        {},
        [
            {
                "_id": ObjectId(),
                "value": 20.0,
                "timestamp": "2021-05-18T00:00:00.000Z",
                "metadata": {
                    "area": "kitchen",
                    "type": "TEMPERATURE",
                    "uuid": "1234"
                }
            }
        ]
    ),
    (
        {"limit": 2, "area": "kitchen"},
        2,
        {"metadata.area": "kitchen"},
        [
            {
                "_id": ObjectId(),
                "value": 20.0,
                "timestamp": "2021-05-18T00:00:00.000Z",
                "metadata": {
                    "area": "kitchen",
                    "type": "TEMPERATURE",
                    "uuid": "1234"
                }
            },
            {
                "_id": ObjectId(),
                "value": 21.0,
                "timestamp": "2021-05-18T00:00:00.000Z",
                "metadata": {
                    "area": "kitchen",
                    "type": "TEMPERATURE",
                    "uuid": "1234"
                }
            }
        ]
    )
])
def test_sensor_service_get_sensor_data(filters: dict,
                                        limit: int,
                                        mongo_query: dict,
                                        expected_result_set: list[dict]):
    """Test the get_temperatures method."""
    mocked_collection = prepare_collection_mock(expected_result_set)
    mocked_mongo_query_builder = prepare_mongo_query_builder_mock(mongo_query)
    temperature_service = TemperatureService(
        mocked_collection, mocked_mongo_query_builder)
    got_result_set = temperature_service.get_sensor_data(filters)
    mocked_collection.find.assert_called_once_with(mongo_query)
    mocked_collection.find.return_value.limit.assert_called_once_with(limit)
    mocked_collection.find.return_value.limit.return_value.sort.assert_called_once_with("timestamp",
                                                                                        pymongo.DESCENDING)
    assert got_result_set == [SensorData(**doc) for doc in expected_result_set]
