import string

from tml.common.position import Position
from tml.common.tokens import LBRACE, RBRACE, LSQBRACE, RSQBRACE, LPAREN, RPAREN, PLUS, MINUS, MUL, DIV, Token, EOF, \
    INT, FLOAT, KW, IDENT, EQ, STRING, COLON, COMMA
from tml.exceptions.lexical_errors import InvalidCharacterError

SIMPLE_CASES = {
    "{": LBRACE,
    "}": RBRACE,
    "[": LSQBRACE,
    "]": RSQBRACE,
    "(": LPAREN,
    ")": RPAREN,
    "+": PLUS,
    "-": MINUS,
    "*": MUL,
    "/": DIV,
    "=": EQ,
    ":": COLON,
    ",": COMMA
}

DIGITS = string.digits
DIGITS_DOT = DIGITS + "."

ASCII_LETTERS = string.ascii_letters
ASCII_LETTERS_UNDERSCORE = ASCII_LETTERS + "_"
ASCII_LETTERS_UNDERSCORE_DIGITS = ASCII_LETTERS_UNDERSCORE + DIGITS

KEYWORDS = ("let", "ret", "dict", "from", "import", "as")


class Lexer:
    def __init__(self, input_str, file_name, keywords=KEYWORDS, simple_cases=None):
        if simple_cases is None:
            simple_cases = SIMPLE_CASES
        self.simple_cases = simple_cases
        self.keywords = keywords
        self.file_name = file_name
        self.input_str = input_str
        self.tokens = []
        self.current_char = None
        self.index = Position(file_name)
        self.position_error_start = None
        self.position_error_end = None

    def move_next(self):
        self.index.move_next(self.current_char)
        if self.index.index < len(self.input_str):
            self.current_char = self.input_str[self.index.index]
        else:
            self.current_char = None

    def tokenize(self):
        self.move_next()
        while self.current_char is not None:
            if self.current_char in self.simple_cases:
                self.tokens.append(Token(self.simple_cases[self.current_char]))
                self.move_next()
            elif self.current_char in DIGITS:
                token, error = self.build_number()
                if token:
                    self.tokens.append(token)
                else:
                    return None, error
            elif self.current_char in ASCII_LETTERS_UNDERSCORE:
                token, error = self.build_ident()
                if token:
                    self.tokens.append(token)
                else:
                    return None, error
            elif self.current_char == "\"":
                token, error = self.build_string()
                if token:
                    self.tokens.append(token)
                else:
                    return None, error
            else:
                self.move_next()
        self.tokens.append(Token(EOF))
        return self.tokens, None

    def build_number(self):
        nod = 0
        res = self.current_char
        while self.current_char is not None and self.current_char in DIGITS_DOT:
            self.move_next()
            if self.current_char == ".":
                nod += 1
                if nod > 1:
                    self.position_error_start = self.index.copy()
                    self.position_error_end = self.position_error_start
                    return None, InvalidCharacterError(self.file_name, self.position_error_start,
                                                       self.position_error_end, "'.' is not expected.")
                res += "."
            if self.current_char is not None and self.current_char in DIGITS:
                res += self.current_char
        if nod == 0:
            return Token(INT, res), None
        return Token(FLOAT, res), None

    def build_ident(self):
        res = ""

        while self.current_char is not None and self.current_char in ASCII_LETTERS_UNDERSCORE_DIGITS:
            res += self.current_char
            self.move_next()

        if res in self.keywords:
            return Token(KW, res), None
        return Token(IDENT, res), None

    def build_string(self):
        res = ""
        self.move_next()
        while self.current_char is not None and self.current_char != "\"":
            res += self.current_char
            self.move_next()

        if self.current_char == "\"":
            self.move_next()
            return Token(STRING, res), None

        self.position_error_start = self.index.copy()
        self.position_error_end = self.position_error_start

        return None, InvalidCharacterError(self.file_name, self.position_error_start, self.position_error_end,
                                           f"\" is expected")
