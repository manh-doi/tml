import pytest

from tml.common.tokens import INT
from tml.lexical.lexer import Lexer, DIGITS, build_number
from tml.parsing import parser
from tml.parsing.builder import terminate
from tml.parsing.combinators import seq


@pytest.fixture(scope="module", params=[
    "1 1 1.0"
])
def input_str(request):
    return request.param


def test_parsing_error(input_str):
    lexer = Lexer().m_plus(lambda x: x in DIGITS, build_number)
    tokens, error = lexer.tokenize(input_str, "<stdin>")
    assert tokens is not None
    res = parser.parse(tokens, seq(terminate(INT), terminate(INT), terminate(INT)))
    assert not res.is_success()
    assert res.errors

    for error in res.errors:
        print(error)
