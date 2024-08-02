import pytest

from tml.parsing.builder import terminate
from tml.testing.functions import build_test_case
from tml.common.tokens import INT, Token, IDENT
from tml.parsing.combinators import repeat, seq, select


def build_repeat():
    inputs = [
        ("1 2 3", repeat(terminate(INT)), [Token(INT, "1"), Token(INT, "2"), Token(INT, "3")], Token(INT, "3")),
        ("a b c", repeat(terminate(IDENT)), [Token(IDENT, "a"), Token(IDENT, "b"), Token(IDENT, "c")],
         Token(IDENT, "c")),
        ("a 1 c 2", repeat(select(terminate(IDENT), terminate(INT))),
         [Token(IDENT, "a"), Token(INT, "1"), Token(IDENT, "c"), Token(INT, "2")], Token(INT, "2")),
        ("a b c", repeat(terminate(INT)), [], Token(IDENT, "a")),
        ("a 1 c 2 3", repeat(seq(terminate(IDENT), terminate(INT))),
         [[Token(IDENT, "a"), Token(INT, "1")], [Token(IDENT, "c"), Token(INT, "2")]], Token(INT, "2")),
    ]

    return [build_test_case(*t_input) for t_input in inputs]


repeat_func = pytest.fixture(scope="module", params=build_repeat())(lambda request: request.param)


def test_repeat(repeat_func):
    repeat_func()
