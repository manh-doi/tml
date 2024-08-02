from tml.testing.utils import lex
from tml.parsing.parser import Parser


def build_test_case(input_str, builder_class, expectation, end_token):
    def wrap():
        tokens = lex(input_str)
        parser = Parser(tokens)
        parser.move_next()

        res = builder_class()(parser)
        print(res)
        assert res.is_success()
        assert res.res == expectation
        assert parser.current_token == end_token

    wrap.__name__ = input_str

    return wrap
