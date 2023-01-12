"""generator models module."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from uuid import uuid4


class SensorArea(Enum):
    LIVING_ROOM = auto()
    KITCHEN = auto()
    BEDROOM = auto()
    BATHROOM = auto()


class SensorType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()


@dataclass
class RandomConfig:
    min_value: float = 0.0
    max_value: float = 40.0
    # the smaller the buffer, the more random the numbers will be
    max_buffer_size: int = 5


@dataclass
class MQTTConfig:
    host: str
    port: int


@dataclass
class SensorConfig:
    type: SensorType
    area: SensorArea
    mqtt: MQTTConfig
    read_interval_seconds: int


@dataclass
class SensorMetadata:
    type: SensorType
    area: SensorArea
    uuid: str = uuid4().hex[:16]

    @property
    def id(self) -> str:
        return f"{self.type.name}-{self.area.name}-{self.uuid}"


@dataclass
class SensorData:
    value: float
    timestamp: datetime
    metadata: SensorMetadata
