"""Service layer for the API."""
from logging import Logger
from typing import Protocol

import pymongo
from api.query import MongoQueryFilter
from api.sensors.models import SensorData
from kink import inject
from pymongo.collection import Collection


class NoResultsFound(Exception):
    """Exception raised when no results are found for a given query."""


class ISensorService(Protocol):
    def get_sensor_data(self, filters: dict = None, limit: int = 100, offset: int = 0) -> list[SensorData]:
        ...


@inject(alias=ISensorService)
class SensorService:
    def __init__(self, sensors_collection: Collection, logger: Logger, mongo_query_filter: MongoQueryFilter = MongoQueryFilter()):
        self.__sensors_collection = sensors_collection
        self.__mongo_query_filter = mongo_query_filter
        self.__logger = logger

    def _run_query(self, mongo_query: dict, limit: int, offset: int) -> list[SensorData]:
        self.__logger.info("Service Running query: %s", mongo_query)
        cursor = self.__sensors_collection.find(mongo_query).limit(
            limit).sort("timestamp", pymongo.DESCENDING).skip(offset)
        return [SensorData(**doc) for doc in cursor]

    def get_sensor_data(self, filters: dict = None, limit: int = 100, offset: int = 0) -> list[SensorData]:
        """Queries the database for sensor data in a given time range or area.

        Args:
            filters (dict): The filters to be applied to the query.

        Returns:
            list[SensorData]: The list of sensor data to be serialized and sent to the client.
        """
        mongo_query_filters = {}
        if not filters:
            return self._run_query(mongo_query_filters, limit, offset)

        if "limit" in filters:
            limit = int(filters["limit"])
            del filters["limit"]
        if "offset" in filters:
            offset = int(filters["offset"])
            del filters["offset"]

        mongo_query_filters = self.__mongo_query_filter.build_from_filters(
            filters)
        results = self._run_query(mongo_query_filters, limit, offset)
        if len(results) == 0:
            raise NoResultsFound("No results found for the given query")
        return results
