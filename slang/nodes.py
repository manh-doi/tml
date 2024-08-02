from tml.common.node import Node


class IntNode(Node):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"[INT: {self.token}]"


class FloatNode(Node):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"[FLOAT: {self.token}]"


class TermNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"[TERM: {self.left} {self.operator} {self.right}]"


class SumNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"[SUM: {self.left} {self.operator} {self.right}]"
