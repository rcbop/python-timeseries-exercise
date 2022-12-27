"""Models for the API."""
import uuid
from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SensorMetadata(BaseModel):
    sensor_area: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "sensor_area": "kitchen"
            }
        }


class SensorData(BaseModel):
    id: PyObjectId = Field(default_factory=uuid.uuid4, alias="_id")
    temperature: float = Field(...)
    timestamp: datetime = Field(...)
    metadata: Optional[SensorMetadata] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "metadata": {
                    "sensor_area": "kitchen"
                },
                "temperature": 23.4,
                "timestamp": "2022-12-27T21:29:37.448000"
            }
        }
