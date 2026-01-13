"""Основной файл с созданием списка клиентов и запуском работы парковки."""

import random
import time

from constants import CHANCE_ARRIVAL, CHANCE_DEPARTING, FREEZE_TIME
from handler.abc import ParkingEventHandler
from handler.impl import ParkingEventHandlerImpl
from models import CarType, Client, EventType
from parking import ParkingLot


class ParkingService:
    """Парковочный сервис."""

    def __init__(
        self,
        handler: ParkingEventHandler,
        clients: list[Client],
        parking_lot: ParkingLot,
    ) -> None:
        """Инициализация обработчиков и клиентов парковки."""
        self.handler = handler
        self.parking = parking_lot
        self.clients = clients

    def run(self) -> None:
        """
        Запуск основного цикла парковки.

        По ходу цикла проверяется, уедет ли машина с парковки или заедет с
        определенными в константах шансами.
        Обработка событий происходит в обработчике handler.

        Цикл повторяется каждые FREEZE_TIME секунд
        """
        print("🚗 Парковочный сервис запущен...")

        while self.clients:
            client = random.choice(self.clients)

            if client.is_parked:
                if random.random() >= CHANCE_DEPARTING:
                    continue
                event = EventType.LEAVE
            else:
                if random.random() >= CHANCE_ARRIVAL:
                    continue
                event = EventType.ARRIVE

            print(f"⚡ Событие: {event.upper()} — {client.plate}")

            if event == EventType.ARRIVE:
                self.handler.handle_arrival(client, self.parking)
            elif event == EventType.LEAVE:
                self.handler.handle_departure(client, self.parking)
                if not client.is_parked:
                    self.clients.remove(client)

            if not self.clients:
                print("✅ Все клиенты обработаны, парковка пуста. "
                      "Завершение работы.")
                break

            time.sleep(FREEZE_TIME)


if __name__ == "__main__":
    car_types = [CarType.REGULAR, CarType.ELECTRIC, CarType.PREMIUM]

    plates = [f"A{str(i).zfill(3)}AA" for i in range(1, 51)]

    clients = [Client(plate, random.choice(car_types)) for plate in plates]

    handler = ParkingEventHandlerImpl()
    parking_lot = ParkingLot(20, 2, 2)
    service = ParkingService(handler, clients, parking_lot)
    service.run()
