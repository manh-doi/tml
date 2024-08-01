from functools import wraps, reduce

from tml.common.tokens import Token
from tml.parsing.parse_results import ParseSuccess, ParseFailure


def debug(func):
    @wraps(func)
    def wrap(self, parser, *args, **kwargs):
        res = func(self, parser, *args, **kwargs)
        print(
            f"{res}, func: {self.__class__.__name__}, idx: {parser.current_index}, tok: {parser.current_token}, toks: {parser.tokens}")
        return res

    return wrap


class Builder:

    def __init__(self):
        self.builder_class = self.init_builder()
        self.first = None

    def init_builder(self):
        pass

    def first_k(self):
        if self.first is None:
            first_s = self.builder_class().first_k()
            self.first = reduce(lambda r, x: x in r and r or r + [x], first_s, [])
        return self.first

    def follow_k(self):
        pass

    def in_first(self, token):
        self.first = self.first_k()
        return reduce(lambda r, x: r or x.__eq__(token), self.first, False)

    def is_llk(self):
        return self.builder_class().is_llk()

    def make_node(self, res):
        return res

    @debug
    def __call__(self, parser, *args, **kwargs):
        res = self.builder_class()(parser)
        if res.is_success():
            node = self.make_node(res.res)
            return res.__class__(node)
        return res


class Terminate(Builder):

    def __init__(self, t_type, value=None):
        super().__init__()
        self.t_type = t_type
        self.value = value

    @debug
    def __call__(self, parser, *args, **kwargs):
        if self.value is not None:
            if parser.current_token is not None and parser.current_token.t_type == self.t_type and parser.current_token.value == self.value:
                return ParseSuccess(parser.current_token)
            return ParseFailure(f"Syntax error: a {self.value} is expected")
        else:
            if parser.current_token is not None and parser.current_token.t_type == self.t_type:
                return ParseSuccess(parser.current_token)
            return ParseFailure(f"Syntax error: a {self.t_type} is expected")

    def first_k(self):
        return [Token(self.t_type, self.value)]

    def in_first(self, token):
        return self.value is None and token.t_type == self.t_type or (
                token.t_type == self.t_type and token.value == self.value)

    def is_llk(self):
        return True


def terminate(t_type, value=None):
    return lambda: Terminate(t_type, value)
