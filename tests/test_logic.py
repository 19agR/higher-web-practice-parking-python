from conftest import _make_parking, _make_client

# import pytest
# pytestmark = pytest.mark.usefixtures("main_import_test")


def _is_on_spot(client, lot, spot_type):
    return any(s.client is client and s.spot_type == spot_type for s in lot.spots)


def _not_on_spot(client, lot, spot_type):
    return all(not (s.client is client and s.spot_type == spot_type) for s in lot.spots)


def test_regular_car():
    lot = _make_parking(total_spots=4, electric_spots=1, premium_spots=1)
    regular_1 = _make_client("regular")
    assert lot.park_client(regular_1) is True, (
        "Убедитесь, что попытка парковки обычного автомобиля успешна "
        "при наличии обычного свободного места."
    )
    assert regular_1.is_parked is True, (
        "Убедитесь, что при успешной парковке обычного автомобиля "
        "значение `is_parked` становится True."
    )
    assert _is_on_spot(regular_1, lot, "regular"), (
        "Убедитесь, что обычный автомобиль размещается на обычном парковочном месте."
    )
    assert _not_on_spot(regular_1, lot, "electric"), (
        "Убедитесь, что обычный автомобиль размещается только на обычном парковочном месте."
    )
    assert _not_on_spot(regular_1, lot, "premium"), (
        "Убедитесь, что обычный автомобиль размещается только на обычном парковочном месте."
    )

    regular_2 = _make_client("regular")
    assert lot.park_client(regular_2) is True, (
            "Убедитесь, что попытка парковки обычного автомобиля успешна "
            "при наличии обычного свободного места."
    )

    regular_3 = _make_client("regular")
    assert lot.park_client(regular_3) is False, (
        "Убедитесь, что при отсутствии обычных свободных мест, "
        "попытка парковки обычного автомобиля не осуществляется."
    )
    assert regular_3.is_parked is False, (
        "Убедитесь, что при неуспешной попытке парковки обычного автомобиля "
        "значение `is_parked` у клиента остаётся False."
    )


def test_electric_car():
    lot = _make_parking(total_spots=3, electric_spots=1, premium_spots=1)
    electric_1 = _make_client("electric")
    assert lot.park_client(electric_1) is True, (
        "Убедитесь, что электромобиль может припарковаться, "
        "если есть свободное место для электроавтомобилей."
    )
    assert electric_1.is_parked is True, (
        "Убедитесь, что при успешной парковке электромобиль, "
        "значение `is_parked` становится True."
    )
    assert _is_on_spot(electric_1, lot, "electric"), (
        "Убедитесь, что электромобиль может припарковаться только на месте для электроавтомобилей."
    )

    electric_2 = _make_client("electric")
    assert lot.park_client(electric_2) is False, (
        "Убедитесь, что при отсутствии свободных мест для электроавтомобилей, "
        "парковка электромобиля не осуществляется."
    )
    assert electric_2.is_parked is False, (
        "Убедитесь, что при неуспешной попытке парковки электромобиля, "
        "значение `is_parked` у электромобиля остаётся False."
    )


def test_premium_car():
    lot = _make_parking(total_spots=5, electric_spots=1, premium_spots=2)
    premium_1 = _make_client("premium")
    assert lot.park_client(premium_1) is True, (
        "Убедитесь, что премиум автомобиль может припарковаться, "
        "при наличии свободного премиум места."
    )
    assert _is_on_spot(premium_1, lot, "premium"), (
        "Убедитесь, что премиум автомобиль паркуется на премиум место, "
        "если такое место свободно."
    )
    assert _not_on_spot(premium_1, lot, "electric"), (
        "Убедитесь, что премиум автомобиль не паркуется для электроавтомобилей."
    )

    premium_2 = _make_client("premium")
    assert lot.park_client(premium_2) is True, (
        "Убедитесь, что при наличии свободного премиум места "
        "попытка парковки премиум автомобиль возвращает True."
    )
    assert _is_on_spot(premium_2, lot, "premium"), (
        "Убедитесь, что премиум автомобиль занимает премиум место, когда оно доступно."
    )

    premium_3 = _make_client("premium")
    assert lot.park_client(premium_3) is True, (
        "Убедитесь, что при отсутствии свободных премиум мест, "
        "премиум автомобиль может занять обычное место."
    )
    assert _is_on_spot(premium_3, lot, "regular"), (
        "Убедитесь, что премиум автомобиль размещается на обычном месте, "
        "если премиум места недоступны."
    )
    assert _not_on_spot(premium_3, lot, "electric"), (
        "Убедитесь, что премиум автомобиль никогда не размещается на месте для электроавтомобилей."
    )


def test_premium_if_only_electric():
    lot = _make_parking(total_spots=2, electric_spots=2, premium_spots=0)
    premium = _make_client("premium")
    assert lot.park_client(premium) is False, (
        "Убедитесь, что если свободны только места типа `electric`, "
        "автомобиль типа `premium` не может быть припаркован (возвращается False)."
    )
    assert premium.is_parked is False, (
        "Убедитесь, что при неуспешной попытке парковки значение `is_parked` остаётся False."
    )


def test_remove_client():
    lot = _make_parking(total_spots=3, electric_spots=0, premium_spots=0)
    client = _make_client("regular")
    assert lot.park_client(client) is True, (
        "Убедитесь, что автомобиль типа `regular` может занять место типа `regular`."
    )
    assert lot.has_cars() is True, (
        "Убедитесь, что при наличии хотя бы одного припаркованного автомобиля, "
        "метод `has_cars()` возвращает True."
    )
    assert lot.remove_client(client) is True, (
        "Убедитесь, что освобождение занятого места возвращает True."
    )
    assert lot.has_cars() is False, (
        "Убедитесь, что при отсутствии припаркованных автомобилей, "
        "метод `has_cars()` возвращает False."
    )
    assert all(s.client is not client for s in lot.spots), (
        "Убедитесь, что после освобождения места, "
        "клиент больше не занимает ни одного парковочного места."
    )

    new_client = _make_client("regular")
    assert lot.park_client(new_client) is True, (
        "Убедитесь, что после освобождения место можно использовать повторно."
    )
    assert any(s.client is new_client for s in lot.spots), (
        "Убедитесь, что новый клиент занимает подходящее свободное место."
    )


def test_remove_client_not_present_returns_false():
    lot = _make_parking(total_spots=2, electric_spots=0, premium_spots=0)
    ghost = _make_client("regular")
    assert lot.remove_client(ghost) is False, (
        "Убедитесь, что при попытке освободить место для клиента, "
        "которого нет на парковке, возвращается False."
    )