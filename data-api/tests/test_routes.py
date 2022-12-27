from unittest.mock import Mock

import pytest
from api.temperature.models import SensorData
from api.temperature.service import TemperatureService
from bson import ObjectId
from fastapi import FastAPI
from fastapi.testclient import TestClient
from kink import di


@pytest.fixture
def sensor_data_list() -> list[SensorData]:
    """Create a list of SensorData objects."""
    return [
        SensorData(
            id=ObjectId(),
            timestamp="2022-12-28T21:29:37.448000",
            temperature=12.0,
            metadata={
                "sensor_area": "kitchen",
            }),
        SensorData(
            id=ObjectId(),
            timestamp="2022-12-28T20:35:41.410000",
            temperature=18.0,
            metadata={
                "sensor_area": "bedroom",
            }),
    ]


@pytest.fixture
def client(sensor_data_list: list[SensorData]) -> TestClient:
    """Create a test client for the API."""
    from api.temperature.routes import router
    app = FastAPI()
    app.include_router(router)
    temperature_service = Mock()
    temperature_service.list_temperatures.return_value = sensor_data_list
    di[TemperatureService] = temperature_service
    return TestClient(app)


def test_list_temperatures(client: TestClient, sensor_data_list: list[SensorData]):
    """Test the list_temperatures route."""
    response = client.get("/")
    assert response.status_code == 200
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "application/json"
    got_response = response.json()
    assert len(got_response) == 2
    for i in range(2):
        assert got_response[i]["_id"] == str(sensor_data_list[i].id)
        assert got_response[i]["timestamp"] == sensor_data_list[i].timestamp.isoformat(
        )
        assert got_response[i]["temperature"] == sensor_data_list[i].temperature
        assert got_response[i]["metadata"] == sensor_data_list[i].metadata
