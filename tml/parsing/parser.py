class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = -1
        self.current_token = None

    def move_next(self):
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = None

    def parse(self):
        pass
