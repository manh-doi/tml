from tml.errors.error import error_detail
import os


class LexicalError:
    def __init__(self, file_name, start, end, message, content=None):
        self.file_name = file_name
        self.start = start
        self.end = end
        self.message = message
        self.content = content

    def __str__(self):
        detail = error_detail(self.file_name, self.start, self.end, self.content)
        abs_file = self.file_name == "<stdin>" and "<stdin>" or f"File: {os.path.abspath(self.file_name)}"

        return "\n".join([f"{self.__class__.__name__}: {self.message}",
                          f"{abs_file} at {self.start.line}:{self.start.col}\n",
                          detail])


class InvalidCharacterError(LexicalError):
    def __init__(self, file_name, start, end, message, content=None):
        super().__init__(file_name, start, end, message, content)
