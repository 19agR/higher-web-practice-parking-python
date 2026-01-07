
from models import Client
from parking import ParkingLot
from handler.abc import ParkingEventHandler


class ParkingEventHandlerImpl(ParkingEventHandler):

    def handle_arrival(self, client: Client, parking_lot: ParkingLot):
        """Обработка прибытия машины для парковки"""
        # TODO: реализовать метод
        return None

    def handle_departure(self, client: Client, parking_lot: ParkingLot):
        """Обработка отбытия машины с парковки"""
        # TODO: реализовать метод
        return None
