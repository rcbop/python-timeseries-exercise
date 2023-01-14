"""API routes."""

from logging import Logger

from api.filters import InvalidQueryError, QueryFilters
from api.sensors.models import SensorData
from api.sensors.service import ISensorService, NoResultsFound
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from kink import di

router = APIRouter()


@router.get("/",
            response_description="Get all sensor data in a given time range",
            response_model=list[SensorData])
async def list_sensor_data(request: Request,
                           service: ISensorService = Depends(lambda: di[ISensorService])):
    """Get all sensor data in a given time range or area.

    Args:
       request (Request): The request object.
       service (ITemperatureService, optional): The temperature service to be injected by kink.

    Returns:
       list[SensorData]: The list of temperatures to be serialized and sent to the client.
    """
    parsed_filters = {}
    if not request.url.query:
        return service.get_sensor_data(parsed_filters)

    query_filters = QueryFilters()
    try:
        parsed_filters = query_filters.parse_and_validate(
            request.url.query)
        return service.get_sensor_data(parsed_filters)
    except InvalidQueryError as err:
        di[Logger].error(err)
        return JSONResponse(content={"error": "Invalid query"}, status_code=400, headers={"Content-Type": "application/json"})
    except NoResultsFound as err:
        return JSONResponse(content={"error": "No results found"}, status_code=404, headers={"Content-Type": "application/json"})
