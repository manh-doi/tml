from functools import reduce

import pytest

from tml.common.tokens import INT, Token, FLOAT
from tml.parsing.builder import terminate
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
def cases(request):
    return request.param


def test_first_k(cases):
    builder, first = cases
    builder_first_k = builder.first_k()
    assert reduce(lambda r, x: r and (x in builder_first_k), first, True)
