from functools import reduce

import pytest

from demo_lang.parsing.builder import terminate
from tml.common.tokens import INT, Token, FLOAT
from tml.parsing.combinators import Seq, Repeat, Select, OneOrNone


@pytest.fixture(scope="module", params=[
    (Repeat(terminate(INT)), [Token(INT), None]),
    (Seq().m_plus(terminate(INT)), [Token(INT)]),
    (Seq().m_plus(terminate(INT)).m_plus(terminate(FLOAT)), [Token(INT)]),
    (Select().m_plus(terminate(INT)).m_plus(terminate(FLOAT)), [Token(INT)]),
    (OneOrNone(terminate(INT)), [Token(INT), None]),
    (OneOrNone(lambda: Select().m_plus(terminate(INT)).m_plus(terminate(FLOAT))),
     [Token(INT), None, Token(FLOAT)]),

])
def test_cases(request):
    return request.param


def test_first_k(test_cases):
    builder, first = test_cases
    builder_first_k = builder.first_k()
    assert reduce(lambda r, x: r and (x in builder_first_k), first, True)
