import os

from tml.errors.error import error_detail


class ParserSyntaxError:
    def __init__(self, token, message):
        self.token = token
        self.message = message

    def __str__(self):
        detail = error_detail(self.token.start_position.file_name, self.token.start_position, self.token.end_position)

        return "\n".join([f"{self.__class__.__name__}: {self.message}",
                          f"File: {os.path.abspath(self.token.start_position.file_name)} at {self.token.start_position.line}:{self.token.start_position.col}\n",
                          detail])