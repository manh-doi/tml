import pytest

from tml.common.position import Position
from tml.errors.error import error_detail


@pytest.fixture(scope="module")
def file_name():
    return "tests/files/error.txt"


@pytest.fixture(scope="module")
def start_position(file_name):
    position = Position(file_name)
    position.line = 2
    position.col = 28
    return position


@pytest.fixture(scope="module")
def end_position(file_name):
    position = Position(file_name)
    position.line = 3
    position.col = 32
    return position


def test_error_detail(file_name, start_position, end_position):
    res = error_detail(file_name, start_position, end_position)
    print(f"\n{res}")
