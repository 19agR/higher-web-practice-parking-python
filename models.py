from dataclasses import dataclass
from enum import StrEnum

@dataclass
class Client:
    plate: str
    car_type: str # regular, electric, premium
    is_parked: bool = False


@dataclass
class ParkingSpot:
    id: int
    spot_type: str
    client: Client | None = None


class EventType(StrEnum):
    ARRIVE = "arrive"
    LEAVE = "leave"
