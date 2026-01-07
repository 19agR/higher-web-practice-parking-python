import inspect
import importlib
from dataclasses import is_dataclass, fields

import pytest
pytestmark = pytest.mark.usefixtures("main_import_test")


def test_parkinglot_structure():
    try:
        parking = importlib.import_module("parking")
    except Exception as error:
        raise AssertionError(
            "Убедитесь, что ваш проект содержит модуль `parking`.\n"
            "Не удалось импортировать модуль `parking`.\n"
            f"Ошибка: {type(error).__name__}: {error}"
        )
    ParkingLot = getattr(parking, "ParkingLot", None)
    assert ParkingLot is not None, (
        "Убедитесь, что в модуле `parking` объявлен класс `ParkingLot`."
    )
    required_methods = ("park_client", "remove_client", "has_cars")
    for name in required_methods:
        assert hasattr(ParkingLot, name) and callable(getattr(ParkingLot, name)), (
            f"Убедитесь, что в классе `ParkingLot` определён метод `{name}`."
        )


def test_handler_abc_structure():
    try:
        abc_mod = importlib.import_module("handler.abc")
    except Exception as error:
        raise AssertionError(
            "Убедитесь, что ваш проект содержит модуль `handler.abc`.\n"
            "Не удалось импортировать модуль `handler.abc`.\n"
            f"Ошибка: {type(error).__name__}: {error}"
        )
    Handler = getattr(abc_mod, "ParkingEventHandler", None)
    assert Handler is not None, (
        "Убедитесь, что в модуле `handler/abc.py` определён класс `ParkingEventHandler`."
    )
    for name in ("handle_arrival", "handle_departure"):
        assert hasattr(Handler, name) and callable(getattr(Handler, name)), (
            f"Убедитесь, что в классе `ParkingEventHandler` определён метод `{name}`."
        )
        func = getattr(Handler, name)
        sig = inspect.signature(func)

        params = [p for p in sig.parameters.values() if p.name != "self"]
        assert len(params) == 2, (
            f"Убедитесь, что метод `{name}` класса `ParkingEventHandler` принимает два аргумента помимо `self`: "
            "`client`, `parking_lot`."
        )


def test_handler_impl_structure():
    try:
        impl_mod = importlib.import_module("handler.impl")
    except Exception as error:
        raise AssertionError(
            "Убедитесь, что ваш проект содержит модуль `handler.impl`.\n"
            "Не удалось импортировать модуль `handler.impl`.\n"
            f"Ошибка: {type(error).__name__}: {error}"
        )
    Handler = getattr(impl_mod, "ParkingEventHandlerImpl", None)
    assert Handler is not None, (
        "Убедитесь, что в модуле `handler/impl.py` определён класс `ParkingEventHandlerImpl`."
    )
    for name in ("handle_arrival", "handle_departure"):
        assert hasattr(Handler, name) and callable(getattr(Handler, name)), (
            f"Убедитесь, что в классе `ParkingEventHandlerImpl` определён метод `{name}`."
        )
        func = getattr(Handler, name)
        sig = inspect.signature(func)

        params = [p for p in sig.parameters.values() if p.name != "self"]
        assert len(params) == 2, (
            f"Убедитесь, что метод `{name}` класса `ParkingEventHandlerImpl` принимает два аргумента помимо `self`: "
            "`client`, `parking_lot`."
        )


def test_main_structure():
    try:
        main = importlib.import_module("main")
    except Exception as error:
        raise AssertionError(
            "Убедитесь, что ваш проект содержит модуль `main`.\n"
            "Не удалось импортировать модуль `main`.\n"
            f"Ошибка: {type(error).__name__}: {error}"
        )
    assert hasattr(main, "ParkingService"), (
        "Убедитесь, что в модуле `main.py` определён класс `ParkingService`."
    )


def test_models_structure():
    try:
        models = importlib.import_module("models")
    except Exception as error:
        raise AssertionError(
            "Убедитесь, что ваш проект содержит модуль `models`.\n"
            "Не удалось импортировать модуль `models`.\n"
            f"Ошибка: {type(error).__name__}: {error}"
        )

    Client = getattr(models, "Client", None)
    assert Client is not None, (
        "Убедитесь, что в модуле `models` определён класс `Client`."
    )
    assert is_dataclass(Client), (
        "Убедитесь, что класс `Client` являеется dataclass, (используйте декоратор `@dataclass`)."
    )
    client_field = {f.name for f in fields(Client)}
    check_field_client = {"plate", "car_type", "is_parked"}
    for name in check_field_client:
        assert name in client_field, (
            f"Убедитесь, что в клсаа `Client` определенно поле `{name}`."
        )

    ParkingSpot = getattr(models, "ParkingSpot", None)
    assert ParkingSpot is not None, (
        "Убедитесь, что в модуле `models` определён класс `ParkingSpot`."
    )
    assert is_dataclass(ParkingSpot), (
        "Убедитесь, что, класс `ParkingSpot` являеется dataclass, (используйте декоратор `@dataclass`)."
    )
    parkin_field = {f.name for f in fields(ParkingSpot)}
    check_field_parkin = {"spot_type", "client"}
    for name in check_field_parkin:
        assert name in parkin_field, (
            f"Убедитесь, что в классе `ParkingSpot` определенно поле `{name}`."
        )

    EventType = getattr(models, "EventType", None)
    assert EventType is not None, (
        "Убедитесь, что в модуле `models` определён  класс `EventType`."
    )
