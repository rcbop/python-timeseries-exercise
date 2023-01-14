from unittest.mock import Mock

import pymongo
import pytest
from api.sensors.models import SensorData
from api.sensors.service import NoResultsFound, SensorService
from bson import ObjectId


def prepare_collection_mock(expected_resultset: list[dict]) -> Mock:
    temp_collection_mock = Mock()
    mock_cursor = Mock()
    mock_cursor_with_limit = Mock()
    mock_cursor.limit = Mock(return_value=mock_cursor_with_limit)
    mock_cursor_with_limit_skip = Mock()
    mock_cursor_with_limit.sort = Mock(
        return_value=mock_cursor_with_limit_skip)
    temp_collection_mock.find = Mock(return_value=mock_cursor)
    mock_cursor_with_limit_skip.skip = Mock(return_value=expected_resultset)
    return temp_collection_mock


def prepare_mongo_query_builder_mock(expected_query: dict) -> Mock:
    mongo_query_builder_mock = Mock()
    mongo_query_builder_mock.build_from_filters = Mock(
        return_value=expected_query)
    return mongo_query_builder_mock


@pytest.mark.parametrize("filters,limit,offset,mongo_query,expected_result_set,exception", [
    (
        None,
        100,
        0,
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
        ],
        None
    ),
    (
        {"limit": 2, "metadata.area": "kitchen"},
        100,
        0,
        {"metadata.area": "kitchen"},
        [],
        NoResultsFound
    ),
    (
        {"limit": 1},
        1,
        0,
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
        ],
        None
    ),
    (
        {"limit": 2, "metadata.area": "kitchen"},
        2,
        0,
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
        ],
        None
    )
])
def test_sensor_service_get_sensor_data(filters: dict,
                                        limit: int,
                                        offset: int,
                                        mongo_query: dict,
                                        expected_result_set: list[dict],
                                        exception: Exception):
    """Test the get_temperatures method."""
    mocked_collection = prepare_collection_mock(expected_result_set)
    mocked_mongo_query_builder = prepare_mongo_query_builder_mock(mongo_query)
    temperature_service = SensorService(
        mocked_collection, mocked_mongo_query_builder)
    if exception:
        with pytest.raises(exception):
            temperature_service.get_sensor_data(filters)
        return

    got_result_set = temperature_service.get_sensor_data(filters)
    mocked_collection.find.assert_called_once_with(mongo_query)
    mocked_collection.find.return_value.limit.assert_called_once_with(limit)
    mocked_collection.find.return_value.limit.return_value.sort.assert_called_once_with("timestamp",
                                                                                        pymongo.DESCENDING)
    mocked_collection.find.return_value.limit.return_value.sort.return_value.skip.assert_called_once_with(
        offset)
    assert got_result_set == [SensorData(**doc) for doc in expected_result_set]
