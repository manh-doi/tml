import pytest

from tml.common.tokens import INT, Token, FLOAT
from tml.parsing.builder import terminate
from tml.parsing.combinators import select
from tml.testing.functions import build_test_case


def build_select():
    inputs = [
        ("1.0", select(terminate(FLOAT)), Token(FLOAT, "1.0"), Token(FLOAT, "1.0")),
        ("1", select(terminate(INT)), Token(INT, "1"), Token(INT, "1")),
        ("1.0", select(terminate(FLOAT)), Token(FLOAT, "1.0"), Token(FLOAT, "1.0"))
    ]
    return [build_test_case(*t_input) for t_input in inputs]


select_func = pytest.fixture(scope="module", params=build_select())(lambda request: request.param)


def test_select(select_func):
    select_func()
