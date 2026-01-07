"""Модуль с моделями Клиента, Парковки и Enums для событий, и типов машин."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Optional


# Хотел создать отдельный файл enums.py для них, но тесты не дали :с
class EventType(StrEnum):
    """Типы событий парковки: прибытие или отбытие."""

    ARRIVE = "arrive"
    LEAVE = "leave"


class CarType(StrEnum):
    """Типы автомобилей."""

    REGULAR = "regular"
    ELECTRIC = "electric"
    PREMIUM = "premium"


class SpotType(StrEnum):
    """Типы парковочных мест."""

    REGULAR = "regular"
    PREMIUM = "premium"
    ELECTRIC = "electric"


@dataclass
class Client:
    """Класс, описывающий клиента с автомобилем на парковке."""

    plate: str
    car_type: CarType
    # По сути в моей реализации уже не нужен is_parked, но тесты требуют
    is_parked: bool = False
    parking_spot: Optional["ParkingSpot"] = None

    def park(self, spot: "ParkingSpot") -> None:
        """Припарковать клиента на указанное место."""
        self.parking_spot = spot
        self.is_parked = True
        spot.client = self

    def leave(self) -> None:
        """Снять клиента с парковки, освободив место."""
        if self.parking_spot:
            self.parking_spot.client = None
            self.parking_spot = None
            self.is_parked = False


@dataclass
class ParkingSpot:
    """Класс, описывающий парковочное место."""

    id: int
    spot_type: SpotType
    client: Optional[Client] = None

    def is_free(self) -> bool:
        """Проверяет, свободно ли место."""
        return self.client is None

    def park(self, client: Client) -> None:
        """Поставить клиента на место (двусторонняя связь)."""
        self.client = client
        client.parking_spot = self

    def leave(self) -> None:
        """Освободить место, снимая клиента."""
        if self.client:
            self.client.parking_spot = None
            self.client = None
