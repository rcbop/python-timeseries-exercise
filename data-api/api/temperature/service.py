"""Service layer for the API."""
from pymongo.collection import Collection
from api.temperature.models import SensorData
from kink import inject

@inject
class TemperatureService:
    def __init__(self, temp_collection: Collection):
        self.__temp_collection = temp_collection

    def list_temperatures(self, limit: int = 50) -> list[SensorData]:
        cursor = self.__temp_collection.find().limit(limit)
        return [SensorData(**doc) for doc in cursor]
