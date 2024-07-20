import pytest

from slop_chewy.base.address import Column


columns = {
    "A": 0, "Z": 25, "AA": 26,  "AB": 26 + 1, "AZ": 26 + 25,  # passing
    "BA": (26 * 2) + 1, "ZZ": (26 * 25) + 25}  # failing


@pytest.mark.parametrize("name,value", columns.items(), ids=columns.keys())
def test_init(name: str, value: int):
    # NOTE: indirectly tests Column.value_of_name()
    column = Column(name)
    assert column.value == value


@pytest.mark.parametrize("name", columns.keys(), ids=columns.keys())
def test_str(name: str):
    # NOTE: indirectly tests Column.name_of_value()
    column = Column(name)
    assert str(column) == name
