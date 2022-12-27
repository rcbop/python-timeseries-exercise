from unittest.mock import Mock

import pytest
from api.temperature.models import (SensorData, SensorMetadata,
                                    TemperatureFilterParams)
from api.temperature.service import ITemperatureService
from bson import ObjectId
from fastapi import FastAPI
from fastapi.testclient import TestClient
from kink import di

sensor_data_list: list[SensorData] = [
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-28T21:29:37.448000",
        temperature=12.0,
        metadata=SensorMetadata(sensor_area="kitchen")),
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-28T20:35:41.410000",
        temperature=18.0,
        metadata=SensorMetadata(sensor_area="bedroom")),
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-22T23:50:01.420000",
        temperature=18.0,
        metadata=SensorMetadata(sensor_area="bedroom")),
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-21T20:30:41.410000",
        temperature=22.0,
        metadata=SensorMetadata(sensor_area="bedroom")),
    SensorData(
        id=ObjectId(),
        timestamp="2022-12-20T09:30:41.410000",
        temperature=22.0,
        metadata=SensorMetadata(sensor_area="bedroom")),
]


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the API."""
    from api.temperature.routes import router
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_get_temperatures(client: TestClient):
    """Test the get_temperatures route."""
    temperature_service = Mock()
    temperature_service.get_temperatures = Mock(return_value=sensor_data_list)
    di[ITemperatureService] = temperature_service

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
        assert got_response[i]["temperature"] == sensor_data_list[i].temperature
        assert got_response[i]["metadata"] == sensor_data_list[i].metadata


def test_get_temperatures_with_limit(client: TestClient):
    """Test the get_temperatures route with a limit."""
    temperature_service = Mock()
    temperature_service.get_temperatures = Mock(
        return_value=[sensor_data_list[0]])
    di[ITemperatureService] = temperature_service

    response = client.get("/?limit[eq]=1")
    assert response.status_code == 200
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "application/json"
    got_response = response.json()
    assert len(got_response) == 1
    assert got_response[0]["_id"] == str(sensor_data_list[0].id)
    assert got_response[0]["timestamp"] == sensor_data_list[0].timestamp.isoformat(
    )
    assert got_response[0]["temperature"] == sensor_data_list[0].temperature
    assert got_response[0]["metadata"] == sensor_data_list[0].metadata
    temperature_service.get_temperatures.assert_called_once_with(TemperatureFilterParams(
        min_time=None, max_time=None, sensor_area=None, limit=1))

def test_get_temperatures_timestamp_between_period(client: TestClient):
    """Test the get_temperatures route with a time period."""
    temperature_service = Mock()
    expected_slice = sensor_data_list[2:4]
    temperature_service.get_temperatures = Mock(return_value=expected_slice)
    di[ITemperatureService] = temperature_service
    response = client.get("/?min_time[gt]=2022-12-21T00:00:00.000000&max_time[lt]=2022-12-23T00:00:00.000000")
    assert response.status_code == 200
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "application/json"
    got_response = response.json()
    assert len(got_response) == len(expected_slice)
    for i in range(len(expected_slice)):
        assert got_response[i]["_id"] == str(expected_slice[i].id)
        assert got_response[i]["timestamp"] == expected_slice[i].timestamp.isoformat()
        assert got_response[i]["temperature"] == expected_slice[i].temperature
        assert got_response[i]["metadata"] == expected_slice[i].metadata
