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
    area: str = Field(...)
    type: str = Field(...)
    uuid: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "metadata": {
                    "type": "TEMPERATURE",
                    "area": "KITCHEN",
                    "uuid": "f0e060f737504d2d"
                }
            }
        }


class SensorData(BaseModel):
    id: PyObjectId = Field(default_factory=uuid.uuid4, alias="_id")
    value: float = Field(...)
    timestamp: datetime = Field(...)
    metadata: Optional[SensorMetadata] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "value": 5.474,
                "timestamp": "2023-01-10T22:43:29.398881",
                "metadata": {
                    "type": "TEMPERATURE",
                    "area": "KITCHEN",
                    "uuid": "f0e060f737504d2d"
                }
            }
        }
