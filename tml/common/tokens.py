NEWLINE = "NL"
INT = "INT"
FLOAT = "FLOAT"
STRING = "STRING"

LPAREN = "LPAREN"
RPAREN = "RPAREN"
LBRACE = "LBRACE"
RBRACE = "RBRACE"
LSQBRACE = "LSQBRACE"
RSQBRACE = "RSQBRACE"

PLUS = "PLUS"
MINUS = "MINUS"
DIV = "DIV"
MUL = "MUL"

IDENT = "IDENT"
KW = "KW"

EQ = "EQ"

COMMA = "COMMA"
COLON = "COLON"
DOUBLE_QUOTE = "DOUBLE_QUOTE"

EOF = "EOF"


class Token:
    def __init__(self, t_type, value=None, position=None):
        self.t_type = t_type
        self.value = value
        self.position = position

    def __repr__(self):
        if self.value is not None:
            return f"[TOK {self.t_type}:{self.value}]"
        return f"[{self.t_type}]"

    def __eq__(self, other):
        if isinstance(other, Token):
            if self.value is not None:
                return other.t_type == self.t_type and other.value == self.value
            return other.t_type == self.t_type
        return False
