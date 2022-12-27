"""API routes."""

from api.temperature.filters import parse_query_string
from api.temperature.models import SensorData, TemperatureFilterParams
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
       service (ITemperatureService, optional): The temperature service to be injected by kink. Defaults to Depends(lambda: di[ITemperatureService]).

    Returns:
       list[SensorData]: The list of temperatures to be serialized and sent to the client.
    """
    params = TemperatureFilterParams()
    if request.url.query:
        parsed_filters = parse_query_string(request.url.query)
        gte = parsed_filters.get("timestamp", {}).get("gte", None)
        lte = parsed_filters.get("timestamp", {}).get("lte", None)
        limit = parsed_filters.get("limit", {}).get("eq", None)
        params = TemperatureFilterParams(
            min_time=gte, max_time=lte, limit=int(limit) if limit else 100)
    return service.get_temperatures(params)
