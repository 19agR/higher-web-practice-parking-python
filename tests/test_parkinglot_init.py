import pytest
from conftest import _make_parking


# pytestmark = pytest.mark.usefixtures("main_import_test")


@pytest.mark.parametrize("total, electric, premium", [(7, 2, 3), (6, 1, 2),(5, 0, 2),(4, 0, 0)])
def test_init_spots_distribution(total, electric, premium):

    lot = _make_parking(total_spots=total, electric_spots=electric, premium_spots=premium)
    assert len(lot.spots) == total, "Должно создаваться указанное число мест."

    types = [s.spot_type for s in lot.spots]
    elec = types[:electric] == ["electric"] * electric
    prem = types[electric:electric+premium] == ["premium"] * premium
    reg = types[electric+premium:] == ["regular"] * (total - electric - premium)
    assert elec and prem and reg, (
        "Убедитесь, что ваш сервис делит парковочные места на разные категории: \n"
        "обычное, премиум и для электроавтомобилей"
    )
