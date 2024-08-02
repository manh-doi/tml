from tml.lexical.lexer import Lexer, DIGITS, build_number, ASCII_LETTERS_UNDERSCORE, build_ident, build_string


def lex(input_str):
    lexer = Lexer() \
        .m_plus(lambda x: x in DIGITS, build_number) \
        .m_plus(lambda x: x in ASCII_LETTERS_UNDERSCORE, build_ident) \
        .m_plus(lambda x: x == "\"", build_string)

    tokens, error = lexer.tokenize(input_str, "<stdin>")
    if tokens:
        return tokens
    raise error
