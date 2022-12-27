"""Service layer for the API."""
from pymongo.collection import Collection
from api.temperature.models import SensorData, TemperatureFilterParams
from kink import inject
from typing import Protocol

class ITemperatureService(Protocol):
    def get_temperatures(self, params: TemperatureFilterParams) -> list[SensorData]:
        ...

@inject(alias=ITemperatureService)
class TemperatureService:
    def __init__(self, temp_collection: Collection):
        self.__temp_collection = temp_collection

    def get_temperatures(self, params: TemperatureFilterParams) -> list[SensorData]:
        """Queries the database for temperatures in a given time range or area.

        Args:
            params (TemperatureFilterParams): temperature filter parameters

        Returns:
            list[SensorData]: The list of temperatures to be serialized and sent to the client.
        """
        query_filter = {}
        if params.min_time:
            query_filter["timestamp"] = {"$gte": params.min_time}
        if params.max_time:
            query_filter.setdefault("timestamp", {})["$lte"] = params.max_time
        if params.sensor_area:
            query_filter.setdefault("metadata", {})["sensor_area"] = params.sensor_area

        cursor = self.__temp_collection.find(query_filter).limit(params.limit)
        return [SensorData(**doc) for doc in cursor]
