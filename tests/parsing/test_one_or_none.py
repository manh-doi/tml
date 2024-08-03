import pytest

from tml.parsing.builder import terminate
from tml.testing.functions import build_test_case
from tml.common.tokens import INT, Token, IDENT
from tml.parsing.combinators import one_or_none, seq


def build_one_or_none():
    inputs = [
        # ("1", one_or_none(terminate(INT)), Token(INT, "1"), Token(INT, "1")),
        # ("a", one_or_none(terminate(INT)), None, Token(IDENT, "a")),
        # ("a 1", one_or_none(terminate(INT)), None, Token(IDENT, "a")),
        # ("a 1 b", seq(terminate(IDENT), one_or_none(terminate(IDENT))), [Token(IDENT, "a"), None], Token(INT, "1")),
        ("a 1 b", seq(one_or_none(terminate(INT)), one_or_none(terminate(INT))), [None, None],
         Token(IDENT, "a"))
    ]

    return [build_test_case(*t_input) for t_input in inputs]


one_or_none_func = pytest.fixture(scope="module", params=build_one_or_none())(lambda request: request.param)


def test_one_or_none(one_or_none_func):
    one_or_none_func()
