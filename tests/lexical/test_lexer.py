import pytest

from tml.lexical.lexer import Lexer, DIGITS, build_number, ASCII_LETTERS_UNDERSCORE, build_ident, build_string


@pytest.fixture(scope="module", params=[
    "a",
    "10",
    "a 10 []"
])
def input_str(request):
    return request.param


def test_lexer(input_str):
    lexer = Lexer() \
        .m_plus(lambda x: x in DIGITS, build_number) \
        .m_plus(lambda x: x in ASCII_LETTERS_UNDERSCORE, build_ident) \
        .m_plus(lambda x: x == "\"", build_string)
    tokens, error = lexer.tokenize(input_str, "<stdin>")
    assert tokens
    print(tokens)


@pytest.fixture(scope="module", params=[
    "1.0.0"
])
def input_str_error(request):
    return request.param


def test_lexer_error(input_str_error):
    lexer = Lexer() \
        .m_plus(lambda x: x in DIGITS, build_number)
    tokens, error = lexer.tokenize(input_str_error, "<stdin>")
    assert error
    assert tokens is None
    print(error)
