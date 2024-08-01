class LexicalError:
    def __init__(self, file_name, start, end, message):
        self.file_name = file_name
        self.start = start
        self.end = end
        self.message = message

    def __str__(self):
        head = f"{self.__class__.__name__} at {self.file_name}:{self.start}: {self.message}"
        start_line = max(0, self.start.line - 1)
        end_line = self.end.line + 1
        with open(self.file_name, "r") as f:
            lines = f.readlines()

        cursor = "~" * self.start.col + "^" * (self.end.col - self.start.col + 1)
        print_lines = "".join(lines[start_line:end_line] + [cursor])

        return f"{head}\n{print_lines}"


class InvalidCharacterError(LexicalError):
    def __init__(self, file_name, start, end, message):
        super().__init__(file_name, start, end, message)
