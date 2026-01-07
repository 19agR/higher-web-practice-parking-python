"""Модуль с реализацией обработчика для парковки."""

from handler.abc import ParkingEventHandler
from models import Client
from parking import ParkingLot


class ParkingEventHandlerImpl(ParkingEventHandler):
    """Обработчик прибытия и отбытия машин на парковку."""

    def handle_arrival(self, client: Client, parking_lot: ParkingLot):
        """Обработка прибытия машины для парковки."""
        parking_lot.park_client(client)
        return None

    def handle_departure(self, client: Client, parking_lot: ParkingLot):
        """Обработка отбытия машины с парковки."""
        parking_lot.remove_client(client)
        return None
