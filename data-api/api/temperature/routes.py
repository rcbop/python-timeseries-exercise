"""API routes."""

from api.temperature.models import SensorData
from api.temperature.service import TemperatureService
from fastapi import APIRouter, Depends, Request
from kink import di

router = APIRouter()

@router.get("/",
            response_description="List all temperatures",
            response_model=list[SensorData])
async def list_temperatures(_: Request,
                            service: TemperatureService = Depends(lambda: di[TemperatureService])):
    return service.list_temperatures()
