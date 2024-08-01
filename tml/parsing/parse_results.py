class ParseResult:
    def __init__(self, res):
        self.res = res

    def is_success(self):
        pass

    def is_matched(self):
        pass

    def __repr__(self):
        return f"[{self.__class__.__name__}: {self.res}]"


class ParseSuccess(ParseResult):
    def __init__(self, res):
        super().__init__(res)

    def is_success(self):
        return True

    def is_matched(self):
        return True


class ParseFailure(ParseResult):
    def __init__(self, res):
        super().__init__(res)

    def is_success(self):
        return False

    def is_matched(self):
        return False


class ParseNotMatch(ParseResult):
    def __init__(self, res):
        super().__init__(res)

    def is_success(self):
        return True

    def is_matched(self):
        return False
