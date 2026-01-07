"""Модуль реализующий логику работы парковки."""

from models import CarType, Client, ParkingSpot, SpotType


class ParkingLot:
    """Хранит информацию о местах и клиентах."""

    def __init__(
        self,
        total_spots: int,
        electric_spots: int,
        premium_spots: int,
    ):
        """Создание парковочных мест и определение правил парковки."""
        self.spots: list[ParkingSpot] = []
        self._init_spots(total_spots, electric_spots, premium_spots)

        # правила, куда может встать каждый тип машин
        self.ALLOWED_SPOTS_BY_CAR_TYPE = {
            CarType.REGULAR: {SpotType.REGULAR},
            CarType.PREMIUM: {SpotType.PREMIUM, SpotType.REGULAR},
            CarType.ELECTRIC: {SpotType.ELECTRIC},
        }

    def _init_spots(self, total, electric, premium):
        """Создание парковочных мест согласно количеству каждого типа."""
        types = (
            [SpotType.ELECTRIC] * electric +
            [SpotType.PREMIUM] * premium +
            [SpotType.REGULAR] * (total - electric - premium)
        )

        self.spots = [ParkingSpot(i, t) for i, t in enumerate(types, start=1)]

    def _find_free_spot(self, client: Client) -> ParkingSpot | None:
        """Поиск первого подходящего места для парковки."""
        allowed_spots = self.ALLOWED_SPOTS_BY_CAR_TYPE[client.car_type]

        for spot in self.spots:
            if spot.is_free() and spot.spot_type in allowed_spots:
                return spot

        return None

    def park_client(self, client: Client) -> bool:
        """Паркуем клиента на подходящее место."""
        spot = self._find_free_spot(client)

        if not spot:
            print(f"❌ Нет места для {client.plate}")
            return False

        client.park(spot)
        print(f"✅ {client.plate} припарковался на месте {spot.id}")
        return True

    def remove_client(self, client: Client) -> bool:
        """Освобождает место клиента."""
        if client.parking_spot is None:
            print(f"❌ Клиент {client.plate} не припаркован")
            return False

        client.leave()
        print(f"✅ {client.plate} уехал с места")
        return True

    def has_cars(self) -> bool:
        """Проверяет, есть ли машины на парковке."""
        return any(not spot.is_free() for spot in self.spots)

    def show_status(self):
        """Отображение свободных/занятых мест по всей парковке."""
        total = len(self.spots)
        occupied = sum(1 for s in self.spots if s.client)
        print(f"\n📊 Парковка: {occupied}/{total} занято")
        for s in self.spots:
            if s.client:
                print(f" - Место {s.id:2}: {s.spot_type:<8} — {s.client.plate}"
                      f" ({s.client.car_type})")
            else:
                print(f" - Место {s.id:2}: {s.spot_type:<8} — свободно")
        print()
