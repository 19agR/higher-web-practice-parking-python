
from models import Client, ParkingSpot


class ParkingLot:
    """Хранит информацию о местах и клиентах"""

    def __init__(self, total_spots: int, electric_spots: int, premium_spots: int):
        self.spots: list[ParkingSpot] = []
        self._init_spots(total_spots, electric_spots, premium_spots)

    def _init_spots(self, total, electric, premium):
        for i in range(1, total + 1):
            if i <= electric:
                spot_type = "electric"
            elif i <= electric + premium:
                spot_type = "premium"
            else:
                spot_type = "regular"

            self.spots.append(ParkingSpot(i, spot_type, None))

    def park_client(self, client: Client) -> None:
        """Паркуем клиента на подходящее место"""
        # TODO: реализовать метод
        raise NotImplementedError

    def remove_client(self, client: Client) -> None:
        """Освобождает место клиента"""
        # TODO: реализовать метод
        raise NotImplementedError

    def has_cars(self) -> bool:
        """Проверяет, есть ли машины на парковке"""
        # TODO: реализовать метод
        raise NotImplementedError

    def show_status(self):
        total = len(self.spots)
        occupied = sum(1 for s in self.spots if s.client)
        print(f"\n📊 Парковка: {occupied}/{total} занято")
        for s in self.spots:
            if s.client:
                print(f" - Место {s.id:2}: {s.spot_type:<8} — {s.client.plate} ({s.client.car_type})")
            else:
                print(f" - Место {s.id:2}: {s.spot_type:<8} — свободно")
        print()
