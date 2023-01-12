from dataclasses import dataclass
from datetime import datetime


@dataclass
class DBConfig:
    db_uri: str
    db_name: str
    collection: str


@dataclass
class MQTTConfig:
    host: str
    port: int
    topic: str


@dataclass
class SensorMetadata:
    type: str
    area: str
    uuid: str


@dataclass
class SensorData:
    value: float
    timestamp: datetime
    metadata: SensorMetadata
