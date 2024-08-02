class Parser:
    def __init__(self, tokens, start_builder):
        self.tokens = tokens
        self.current_index = -1
        self.current_token = None
        self.start_builder = start_builder

    def move_next(self):
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = None

    def parse(self):
        if not self.start_builder.is_llk():
            print("WARNING: This language is not a LL(k=1) language.")
        self.move_next()
        return self.start_builder(self)


def parse(tokens, start_builder_class):
    parser = Parser(tokens, start_builder_class())
    return parser.parse()
