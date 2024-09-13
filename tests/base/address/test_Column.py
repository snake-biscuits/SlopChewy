import pytest

from slop_chewy.base.address import Column


columns = {
    "A": 0, "B": 1, "Z": 25,
    "AA": (26 * 1), "AB": (26 * 1) + 1, "AZ": (26 * 1) + 25,
    "BA": (26 * 2), "BB": (26 * 2) + 1, "ZZ": (26 * 26) + 25,
    "AAA": (26 ** 2) + (26 ** 1) + 0,
    "AAB": (26 ** 2) + (26 ** 1) + 1}


@pytest.mark.parametrize("name,value", columns.items(), ids=columns.keys())
def test_name_of_value(name: str, value: int):
    # NOTE: expected value on the left
    assert name == Column.name_of_value(value)


@pytest.mark.parametrize("name,value", columns.items(), ids=columns.keys())
def test_value_of_name(name: str, value: int):
    # NOTE: expected value on the left
    assert value == Column.value_of_name(name)


def test_compare():
    assert Column("A") < Column("B")
    assert Column("A") == Column("A")
    assert Column("B") > Column("A")
    assert Column("A") != Column("B")


def test_increment():
    cursor = Column("A")  # 0
    cursor += 1
    assert cursor == Column("B")  # 1
    cursor += 1
    assert cursor == Column("C")  # 2
    cursor += 2
    assert cursor == Column("E")  # 4
    cursor += 20
    assert cursor == Column("Y")  # 24


def test_decrement():
    cursor = Column("Z")  # 25
    cursor -= 1
    assert cursor == Column("Y")  # 24
    cursor -= 1
    assert cursor == Column("X")  # 23
    cursor -= 2
    assert cursor == Column("V")  # 21
    cursor -= 10
    assert cursor == Column("L")  # 11
