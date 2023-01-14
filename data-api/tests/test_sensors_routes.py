import logging
from logging import Logger
from unittest.mock import Mock

import pytest
from api.sensors.models import SensorData, SensorMetadata
from api.sensors.service import ISensorService
from bson import ObjectId
from fastapi import FastAPI
from fastapi.testclient import TestClient
from kink import di

sensor_data_list: list[SensorData] = [
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-28T21:29:37.448000",
        value=12.0,
        metadata=SensorMetadata(
            area="kitchen",
            type="TEMPERATURE",
            uuid="12345")),
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-28T20:35:41.410000",
        value=18.0,
        metadata=SensorMetadata(
            area="bedroom",
            type="HUMIDITY",
            uuid="65432")),
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-22T23:50:01.420000",
        value=18.0,
        metadata=SensorMetadata(
            area="bedroom",
            type="TEMPERATURE",
            uuid="12345")),
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-21T20:30:41.410000",
        value=22.0,
        metadata=SensorMetadata(
            area="bedroom",
            type="TEMPERATURE",
            uuid="12345")),
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-20T09:30:41.410000",
        value=22.0,
        metadata=SensorMetadata(
            area="bedroom",
            type="TEMPERATURE",
            uuid="12345")),
]


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the API."""
    from api.sensors.routes import router
    app = FastAPI()
    app.include_router(router)
    di[Logger] = logging.getLogger("test")
    return TestClient(app)


def test_get_sensor_data(client: TestClient):
    """Test the get_sensor_data route."""
    temperature_service = Mock()
    temperature_service.get_sensor_data = Mock(return_value=sensor_data_list)
    di[ISensorService] = temperature_service

    response = client.get("/")
    assert response.status_code == 200
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "application/json"
    got_response = response.json()
    assert len(got_response) == len(sensor_data_list)
    for i in range(len(sensor_data_list)):
        assert got_response[i]["_id"] == str(sensor_data_list[i].id)
        assert got_response[i]["timestamp"] == sensor_data_list[i].timestamp.isoformat(
        )
        assert got_response[i]["value"] == sensor_data_list[i].value
        assert got_response[i]["metadata"] == sensor_data_list[i].metadata
    temperature_service.get_sensor_data.assert_called()


def test_get_sensor_data_with_limit_invalid_operator(client: TestClient):
    """Test the get_sensor_data route with a limit."""
    temperature_service = Mock()
    temperature_service.get_sensor_data = Mock(
        return_value=[sensor_data_list[0]])
    di[ISensorService] = temperature_service

    response = client.get("/?limit[eq]=1")
    assert response.status_code == 400
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "application/json"


def test_get_sensor_data_timestamp_between_period(client: TestClient):
    """Test the get_sensor_data route with a time period."""
    temperature_service = Mock()
    expected_slice = sensor_data_list[2:4]
    temperature_service.get_sensor_data = Mock(return_value=expected_slice)
    di[ISensorService] = temperature_service
    response = client.get(
        "/?timestamp[gt]=2022-12-21T00:00:00.000000&timestamp[lt]=2022-12-23T00:00:00.000000")
    assert response.status_code == 200
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "application/json"
    got_response = response.json()
    assert len(got_response) == len(expected_slice)
    for i in range(len(expected_slice)):
        assert got_response[i]["_id"] == str(expected_slice[i].id)
        assert got_response[i]["timestamp"] == expected_slice[i].timestamp.isoformat(
        )
        assert got_response[i]["value"] == expected_slice[i].value
        assert got_response[i]["metadata"] == expected_slice[i].metadata
    temperature_service.get_sensor_data.assert_called()
