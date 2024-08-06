class Position:
    def __init__(self, file_name, content=None):
        self.index = -1
        self.file_name = file_name
        self.col = 0
        self.line = 1
        self.content = content

    def move_next(self, character):
        self.index += 1
        if character == "\n":
            self.col = 1
            self.line += 1
        else:
            self.col += 1

    def copy(self):
        res = Position(self.file_name)
        res.index = self.index
        res.col = self.col
        res.line = self.line
        res.content = self.content
        return res

    def __str__(self):
        return f"{self.line}:{self.col}"

    def __eq__(self, other):
        if isinstance(other, Position):
            return other.col == self.col and other.line == self.line and other.file_name == self.file_name
        return False
