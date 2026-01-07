"""Модуль с обработчиком для парковки"""

from abc import ABC, abstractmethod

from models import Client
from parking import ParkingLot


class ParkingEventHandler(ABC):
    """Базовый класс для реализации логики обработчика событий парковки"""

    @abstractmethod
    def handle_arrival(self, client: Client, parking_lot: ParkingLot):
        """Обработка прибытия машины для парковки"""
        raise NotImplementedError

    @abstractmethod
    def handle_departure(self, client: Client, parking_lot: ParkingLot):
        """Обработка отбытия машины с парковки"""
        raise NotImplementedError
