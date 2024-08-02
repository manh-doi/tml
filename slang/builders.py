from functools import reduce

from slang.nodes import IntNode, TermNode, SumNode
from tml.common.tokens import INT, FLOAT, DIV, MUL, MINUS, PLUS, EOF
from tml.parsing.builder import Builder, terminate
from tml.parsing.combinators import select, seq, repeat


class File(Builder):
    def init_builder(self):
        return seq(Statements, terminate(EOF))


class Statements(Builder):
    def init_builder(self):
        return repeat(Statement)


class Statement(Builder):
    def init_builder(self):
        return Expression


class Expression(Builder):
    def init_builder(self):
        return Sum


class Sum(Builder):
    def init_builder(self):
        return seq(Term, repeat(seq(select(terminate(PLUS), terminate(MINUS)), Term)))

    def make_node(self, res):
        left, tails = res
        return reduce(lambda r, x: SumNode(r, *x), tails, left)


class Term(Builder):
    def init_builder(self):
        return seq(Factor, repeat(seq(select(terminate(MUL), terminate(DIV)), Factor)))

    def make_node(self, res):
        left, tails = res
        return reduce(lambda r, x: TermNode(r, *x), tails, left)


class Factor(Builder):
    def init_builder(self):
        return Atom


class Atom(Builder):
    def init_builder(self):
        return select(Int, Float)


class Int(Builder):
    def init_builder(self):
        return terminate(INT)

    def make_node(self, res):
        return IntNode(res)


class Float(Builder):
    def init_builder(self):
        return terminate(FLOAT)

    def make_node(self, res):
        return IntNode(res)
