from functools import reduce

from tml.parsing.parse_results import ParseResult, ParseFailure, ParseNotMatch, ParseSuccess


class Combinator:
    first = None

    def __call__(self, parser, *args, **kwargs) -> ParseResult:
        pass

    def first_k(self):
        return []

    def in_first(self, token):
        if self.first is None:
            self.first = self.first_k()

        return token in self.first


class Seq(Combinator):
    def __init__(self):
        self.builder_classes = []
        self.current_builder = None
        self.final_state = None

    def is_llk(self):
        res = reduce(lambda r, x: r and x().is_llk(), self.builder_classes, True)
        return res

    def first_k(self):
        res = []
        for builder_class in self.builder_classes:
            fk = builder_class().first_k()
            res = res + fk
            if None not in fk:
                break
        return res

    def m_plus(self, builder_class):
        self.builder_classes.append(builder_class)
        return self

    def __call__(self, parser, *args, **kwargs) -> ParseResult:
        result = []
        latest_builder = self.builder_classes[-1:][0]
        for builder_class in self.builder_classes:
            self.current_builder = builder_class()
            res = self.current_builder(parser)
            if isinstance(res, ParseSuccess):
                result.append(res.res)
                if builder_class != latest_builder:
                    parser.move_next()
                self.final_state = ParseSuccess(result)
            elif isinstance(res, ParseNotMatch):
                result.append(res.res)
                self.final_state = ParseNotMatch(result)
            else:
                return ParseFailure("Syntax error")
        return self.final_state


class Select(Combinator):
    def __init__(self):
        self.builder_classes = []
        self.res = None
        self.current_builder = None
        self.index = -1

    def is_llk(self):
        first_s = reduce(lambda r, x: r + x, map(lambda x: x().first_k(), self.builder_classes), [])
        reduced_first_s = reduce(lambda r, x: x in r and r or r + [x], first_s, [])
        res = len(first_s) == len(reduced_first_s)
        return res

    def first_k(self):
        return reduce(lambda r, x: r + x().first_k(), self.builder_classes, [])

    def m_plus(self, builder_class):
        self.builder_classes.append(builder_class)
        return self

    def __call__(self, parser, *args, **kwargs) -> ParseResult:
        for builder in self.builder_classes:
            self.current_builder = builder()
            if parser.current_token is not None and self.current_builder.in_first(parser.current_token):
                # org_index, org_token = parser.current_index, parser.current_token
                self.res = self.current_builder(parser)
                if self.res.is_success():
                    return self.res
                # parser.current_index, parser.current_token = org_index, org_token
        self.res = ParseFailure("Syntax error")
        return self.res


class Repeat(Combinator):
    def __init__(self, builder_class):
        self.builder_class = builder_class
        self.result = []

    def __call__(self, parser, *args, **kwargs) -> ParseResult:
        org_index, org_token = parser.current_index, parser.current_token
        builder = self.builder_class()
        res = builder(parser)
        if res.is_success():
            final_class = res.__class__
            while res.is_success():
                final_class = res.__class__
                org_index, org_token = parser.current_index, parser.current_token
                self.result.append(res.res)
                if res.is_matched():
                    parser.move_next()
                res = builder(parser)
            parser.current_index, parser.current_token = org_index, org_token
            return final_class(self.result)
        return ParseNotMatch(self.result)

    def first_k(self):
        return [None] + self.builder_class().first_k()

    def is_llk(self):
        return self.builder_class().is_llk()


class OneOrNone(Combinator):
    def __init__(self, builder_class):
        self.builder_class = builder_class
        self.result = None

    def __call__(self, parser, *args, **kwargs) -> ParseResult:
        builder = self.builder_class()
        res = builder(parser)
        if res.is_success():
            self.result = res.res
            return ParseSuccess(self.result)
        return ParseNotMatch(self.result)

    def first_k(self):
        return [None] + self.builder_class().first_k()

    def is_llk(self):
        return self.builder_class().is_llk()


def repeat(builder_class):
    def wrap():
        return Repeat(builder_class)

    return wrap


def one_or_none(builder_class):
    def wrap():
        return OneOrNone(builder_class)

    return wrap


def select(*builder_classes):
    def wrap():
        return reduce(lambda r, x: r.m_plus(x), builder_classes, Select())

    return wrap


def seq(*builder_classes):
    def wrap():
        return reduce(lambda r, x: r.m_plus(x), builder_classes, Seq())

    return wrap
