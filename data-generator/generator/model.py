"""generator models module."""
from dataclasses import dataclass
from enum import Enum, auto

class SensorArea(Enum):
    LIVING_ROOM = auto()
    KITCHEN = auto()
    BEDROOM = auto()
    BATHROOM = auto()

@dataclass
class SensorData:
    sensor_area: SensorArea
    temperature: float

