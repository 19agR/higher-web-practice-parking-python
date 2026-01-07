"""Основной файл с созданием списка клиентов и запуском работы парковки."""

import random
import time

from constants import FREEZE_TIME
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
    ):
        """Инициализация обработчиков и клиентов парковки."""
        self.handler = handler
        self.parking = parking_lot
        self.clients = clients

    def run(self):
        """Запуск основного цикла парковки."""
        print("🚗 Парковочный сервис запущен...")

        while self.clients:
            client = random.choice(self.clients)

            if client.is_parked:
                # 70% шанс, что уедет
                if random.random() < 0.7:
                    event = EventType.LEAVE
                else:
                    continue  # остался стоять
            else:
                # 50% шанс, что заедет
                if random.random() < 0.5:
                    event = EventType.ARRIVE
                else:
                    continue  # остался снаружи

            print(f"⚡ Событие: {event.upper()} — {client.plate}")

            if event == EventType.ARRIVE:
                self.handler.handle_arrival(client, self.parking)
            elif event == EventType.LEAVE:
                self.handler.handle_departure(client, self.parking)
                # удаляем клиента, если он уехал окончательно
                if not client.is_parked:
                    self.clients.remove(client)

            # Проверяем, не опустела ли парковка
            if not self.clients:
                print("✅ Все клиенты обработаны, парковка пуста. "
                      "Завершение работы.")
                break

            # parking_lot.show_status()
            time.sleep(FREEZE_TIME)


if __name__ == "__main__":
    car_types = [CarType.REGULAR, CarType.ELECTRIC, CarType.PREMIUM]

    plates = [f"A{str(i).zfill(3)}AA" for i in range(1, 51)]

    clients = [Client(plate, random.choice(car_types)) for plate in plates]

    handler = ParkingEventHandlerImpl()
    parking_lot = ParkingLot(20, 2, 2)
    service = ParkingService(handler, clients, parking_lot)
    service.run()
