import pytest

from tml.testing.functions import build_test_case
from tml.common.tokens import INT, Token, IDENT, COMMA, EOF
from demo_lang.parsing.builder import terminate
from tml.parsing.combinators import repeat, seq, one_or_none


def build_seq():
    inputs = [
        ("1", seq(repeat(terminate(IDENT)), terminate(INT)), [[], Token(INT, "1")], Token(INT, "1")),
        ("1 2", repeat(seq(terminate(INT), repeat(seq(terminate(COMMA), terminate(INT))))),
         [[Token(INT, "1"), []], [Token(INT, "2"), []]], Token(EOF)),
        ("1 2", seq(seq(terminate(INT), repeat(seq(terminate(COMMA), terminate(INT)))), terminate(INT)),
         [[Token(INT, "1"), []], Token(INT, "2")], Token(INT, "2")),
        ("1 a", seq(terminate(INT), repeat(seq(terminate(COMMA), terminate(INT))), terminate(IDENT, "a")),
         [Token(INT, "1"), [], Token(IDENT, "a")],
         Token(IDENT, "a")),
        ("1 a", seq(seq(terminate(INT), repeat(seq(terminate(COMMA), terminate(INT)))), terminate(IDENT)),
         [[Token(INT, "1"), []], Token(IDENT, "a")],
         Token(IDENT, "a")),
        ("1 2 3 a", seq(terminate(INT), terminate(INT), terminate(INT)),
         [Token(INT, "1"), Token(INT, "2"), Token(INT, "3")], Token(INT, "3")),
        ("a b c", seq(terminate(IDENT), terminate(IDENT), terminate(IDENT)),
         [Token(IDENT, "a"), Token(IDENT, "b"), Token(IDENT, "c")],
         Token(IDENT, "c")),
        ("a,1", seq(terminate(IDENT), terminate(COMMA), terminate(INT)),
         [Token(IDENT, "a"), Token(COMMA), Token(INT, "1")], Token(INT, "1")),
        ("1, 2, 3", seq(terminate(INT), repeat(seq(terminate(COMMA), terminate(INT)))),
         [Token(INT, "1"), [[Token(COMMA), Token(INT, "2")], [Token(COMMA), Token(INT, "3")]]], Token(INT, "3")),
        ("1 a", seq(terminate(INT), one_or_none(terminate(IDENT))), [Token(INT, "1"), Token(IDENT, "a")],
         Token(IDENT, "a")),
        ("1", seq(terminate(INT), one_or_none(terminate(IDENT))), [Token(INT, "1"), None], Token(EOF))
    ]

    return [build_test_case(*t_input) for t_input in inputs]


seq_func = pytest.fixture(scope="module", params=build_seq())(lambda request: request.param)


def test_seq(seq_func):
    seq_func()
