import os
import sys
import importlib
import time
from pathlib import Path
import pytest
from multiprocessing import Process


IMPORT_MODULES = ("parking", "models", "main", "handler.abc", "handler.impl")
IMPORT_TIMEOUT_SECONDS = 1.0

TIMEOUT_ASSERT_MSG = (
    "Убедитесь, что исполняемый код оформлен под `if __name__ == '__main__':`.\n"
    "Убедитесь, что в коде нет бесконечных циклов, которые стартуют при импорте.\n"
    "Убедитесь, что при импорте не запрашивается ввод через `input()."
)


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))


def _import_main():
    import main


@pytest.fixture(scope="session")
def main_import_test():
    proc = Process(target=_import_main)
    proc.start()
    pid = proc.pid
    proc.join(timeout=1)
    if proc.is_alive():
        os.kill(pid, 9)
        raise AssertionError(TIMEOUT_ASSERT_MSG)


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda *_, **__: None)


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    import builtins
    def _no_input(*args, **kwargs):
        raise AssertionError("Сервис не должен запрашивать консольный ввод (input).")
    monkeypatch.setattr(builtins, "input", _no_input)


def _make_parking(total_spots=7, electric_spots=2, premium_spots=3):
    try:
        parking = importlib.import_module("parking")
    except Exception as error:
        raise AssertionError(
            "Убедитесь, что ваш проект содержит модуль `parking`. \n"
            "Не удалось импортировать модуль `parking`. \n"
            f"Ошибка: {type(error).__name__}: {error}"
        )
    try:
        ParkingLot = getattr(parking, "ParkingLot")
    except Exception as error:
        raise AssertionError(
            "Убедитесь, что в модуле `parking` определен класс `ParkingLot`. \n"
            "Не удалось импортировать класс `ParkingLot` из модуля `parking`. \n"
            f"Ошибка: {type(error).__name__}: {error}"
        )
    try:
        return ParkingLot(total_spots, electric_spots, premium_spots)
    except Exception as error:
        raise AssertionError(
            "При создании объекта `ParkingLot(total_spots, electric_spots, premium_spots)`.\n"
            f"Ошибка: {type(error).__name__}: {error}"
        )


def _make_client(car_type="regular", plate="A111AA", parked=False):
    try:
        models = importlib.import_module("models")
    except Exception as error:
        raise AssertionError(
            "Убедитесь, что ваш проект содержит модуль `models`. \n"
            "Не удалось импортировать модуль `models`. \n"
            f"Ошибка: {type(error).__name__}: {error}"
        )
    try:
        Client = getattr(models, "Client")
    except Exception as error:
        raise AssertionError(
            "Убедитесь, что в модуле `models` определен класс `Client`. \n"
            "Не удалось импортировать класс `Client` из модуля `models`. \n"
            f"Ошибка: {type(error).__name__}: {error}"
        )
    try:
        return Client(plate=plate, car_type=car_type, is_parked=parked)
    except Exception as error:
        raise AssertionError(
            "При создании объекта `Client(plate, car_type, is_parked)`.\n"
            f"Ошибка: {type(error).__name__}: {error}"
        )