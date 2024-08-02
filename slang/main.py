from slang.builders import File
from tml.lexical.lexer import Lexer, DIGITS, build_number, ASCII_LETTERS_UNDERSCORE, build_ident, build_string
from tml.parsing.parser import Parser

if __name__ == '__main__':
    file_name = "slang/slang_files/first.sl"

    with open(file_name) as f:
        input_str = f.read()

    lexer = Lexer() \
        .m_plus(lambda x: x in DIGITS, build_number) \
        .m_plus(lambda x: x in ASCII_LETTERS_UNDERSCORE, build_ident) \
        .m_plus(lambda x: x == "\"", build_string)

    tokens, error = lexer.tokenize(input_str, file_name)

    if tokens:
        print(f"tokens: {tokens}")
        parser = Parser(tokens)
        parser.move_next()
        res = File()(parser)
        if res.is_success():
            print(f"nodes: {res.res}")
