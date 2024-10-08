from builders import File
from tml.lexical.lexer import Lexer, DIGITS, build_number, ASCII_LETTERS_UNDERSCORE, build_ident, build_string
from tml.parsing.parser import parse

if __name__ == '__main__':
    file_name = "slang_files/first.sl"

    with open(file_name) as f:
        input_str = f.read()

    lexer = Lexer() \
        .m_plus(lambda x: x in DIGITS, build_number) \
        .m_plus(lambda x: x in ASCII_LETTERS_UNDERSCORE, build_ident) \
        .m_plus(lambda x: x == "\"", build_string)

    tokens, error = lexer.tokenize(input_str, file_name)

    if not error:
        print(f"tokens: {tokens}")
        res = parse(tokens, File)
        if res.is_success():
            print(f"nodes: {res.res}")
        else:
            print(res.errors[0])

    else:
        print(error)
