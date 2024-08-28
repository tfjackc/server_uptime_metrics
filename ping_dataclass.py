from dataclasses import dataclass
from datetime import datetime


@dataclass
class ServerStatus:
    name: str
    ipaddress: str
    byte_value: int
    time: str
    ttl: int
    timestamp: datetime
    status: str