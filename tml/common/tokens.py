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
NOTEQ = "NOTEQ"
GT = "GT"
GTEQ = "GTEQ"
EQEQ = "EQEQ"
DER = "DER"

DOT = "DOT"
COMMA = "COMMA"
COLON = "COLON"
DOUBLE_QUOTE = "DOUBLE_QUOTE"

EOF = "EOF"

GREATER = "GREATER"
LESSEQ = "LESSEQ"
LESS = "LESS"
BACKSLASH = "BACKSLASH"


class Token:
    def __init__(self, t_type, value=None, start_position=None, end_position=None):
        self.t_type = t_type
        self.value = value
        self.start_position = start_position
        self.end_position = end_position

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
