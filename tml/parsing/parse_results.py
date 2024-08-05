class ParseResult:
    def __init__(self, res, errors=None):
        self.res = res
        self.errors = errors

    def is_success(self):
        pass

    def is_matched(self):
        pass

    def __repr__(self):
        return f"[{self.__class__.__name__}: {self.res}]"

    def bind(self, parse_result):
        pass


class ParseSuccess(ParseResult):
    def __init__(self, res, errors=None):
        super().__init__(res, errors)

    def is_success(self):
        return True

    def is_matched(self):
        return True

    def bind(self, parse_result):
        return parse_result


class ParseFailure(ParseResult):
    def __init__(self, error):
        super().__init__(None)
        self.errors = isinstance(error, list) and error or [error]

    def is_success(self):
        return False

    def is_matched(self):
        return False

    def __repr__(self):
        return f"[{self.__class__.__name__}: {self.errors}]"

    def bind(self, parse_result):
        match parse_result:
            case ParseSuccess():
                res = self
            case ParseFailure():
                res = ParseFailure(self.errors + parse_result.errors)
            case ParseNotMatch():
                res = self
            case _:
                res = self
        return res


class ParseNotMatch(ParseResult):
    def __init__(self, res, error):
        super().__init__(res)
        if error:
            self.errors = isinstance(error, list) and error or [error]

    def is_success(self):
        return True

    def is_matched(self):
        return False

    def __repr__(self):
        return f"[{self.__class__.__name__}: {self.errors}]"

    def bind(self, parse_result):
        match parse_result:
            case ParseSuccess():
                res = parse_result
            case ParseFailure():
                res = ParseFailure(self.errors + parse_result.errors)
            case ParseNotMatch():
                res = ParseNotMatch(parse_result.res, self.errors + parse_result.errors)
            case _:
                res = self
        return res
