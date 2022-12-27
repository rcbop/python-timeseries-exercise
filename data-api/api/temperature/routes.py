"""API routes."""

from api.filters import QueryFilters
from api.temperature.models import SensorData
from api.temperature.service import ITemperatureService
from fastapi import APIRouter, Depends, Request
from kink import di

router = APIRouter()


@router.get("/",
            response_description="Get all temperatures in a given time range",
            response_model=list[SensorData])
async def list_temperatures(request: Request,
                            service: ITemperatureService = Depends(lambda: di[ITemperatureService])):
    """Get all temperatures in a given time range or area.

    Args:
       request (Request): The request object.
       service (ITemperatureService, optional): The temperature service to be injected by kink.

    Returns:
       list[SensorData]: The list of temperatures to be serialized and sent to the client.
    """
    parsed_filters = {}
    if request.url.query:
        query_filters = QueryFilters(
            valid_fields=["timestamp", "metadata", "limit"])
        parsed_filters = query_filters.parse_and_validate(request.url.query)
    return service.get_temperatures(parsed_filters)
